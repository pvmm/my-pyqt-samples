# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
import os, re, typing, threading
import prep_files, prep_geocode
from logger import StdoutLogger as Logger

from prep_geocode import OK, FAIL, INTERRUPTED, ThreadInterrompidaError


class ThreadCancelavel(threading.Thread):
    """Classe Thread com um método stop(). A thread precisa checar ela mesma regularmente pela condição de parada."""

    def __init__(self, *args, **kwargs):
        super(ThreadCancelavel, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()


    def stop(self):
        self._stop_event.set()


    def stopped(self):
        return self._stop_event.is_set()



class Singleton(QObject):
    url_changed = pyqtSignal(str, name='urlChanged', arguments=['url'])
    valores_filtrados_changed = pyqtSignal(list, name='valoresFiltradosChanged', arguments=['valores'])
    quantidade_registros_changed = pyqtSignal(int, name='quantidadeRegistrosChanged', arguments=['quantidade'])
    status_operacao_changed = pyqtSignal(int, int, str, name='statusOperacaoChanged', arguments=['status', 'httpCode', 'erro'])
    registro_processado = pyqtSignal(int, name='registroProcessado', arguments=['indice'])
    arquivos_gerados = pyqtSignal(str, name='arquivosGerados', arguments=['texto'])

    # msg_filtro_ignorado = pyqtSignal(str, name='msgFiltroIgnorado', arguments='msg')

    __instance = None
    _path = os.path.expanduser('~') if 'RELEASE' in os.environ else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exemplo')
    _colunas_disponiveis = []
    _colunas_escolhidas = []
    _url = 'http://geocodeapi.codeplan.df.gov.br'

    _arquivo = ''
    _delimitador = ''
    _dados_arquivo_original = []
    _registros_por_arquivo = 0

    # Página 3
    _coluna_filtrada = ''
    _valores_filtrados = []
    _filtro_ignorado = False

    # Página 5
    _thread_operacao = None
    thread_finished = pyqtSignal(name='threadFinished')


    def __init__(self, parent = None):
        if self.__class__.__instance != None:
            raise Exception("classe é singleton")
        else:
            self.__class__.__instance = self

        super().__init__(parent)


    @classmethod
    def getInstance(cls, *args):
        if cls.__instance == None:
            cls.__instance = cls()

        return cls.__instance


    @pyqtProperty(list, constant=True)
    def colunas_disponiveis(self):
        return self._colunas_disponiveis


    @pyqtProperty(list)
    def colunas(self):
        return self._colunas_escolhidas


    @pyqtProperty(str, constant=True)
    def path(self):
        return self._path


    @pyqtProperty(str, notify=url_changed)
    def url(self):
        return self._url


    @url.setter
    def url(self, url):
        if self._url != url:
            self._url = url
            self.url_changed.emit(url)


    @pyqtSlot(str, name='adicionaColuna')
    def adiciona_coluna(self, coluna):
        Logger.debug("adiciona '%s'" % coluna)
        self._colunas_escolhidas.append(coluna)


    @pyqtSlot(str, name='removeColuna')
    def remove_coluna(self, coluna):
        Logger.debug("removendo '%s'" % coluna)
        self._colunas_escolhidas.remove(coluna)


    @pyqtSlot(str, str, name='manipulaArquivo')
    def manipula_arquivo(self, arquivo, delimitador):
        path_arquivo = prep_files.formata_nome_arquivo(arquivo)
        if path_arquivo != '' and os.path.exists(path_arquivo):
            self._arquivo = path_arquivo
            self._delimitador = delimitador        
            self._dados_arquivo_original, self._colunas_disponiveis = prep_files.lista_colunas_e_dados(self._arquivo, self._delimitador)
        else:
            Logger.error('"%s": arquivo não encontrado' % arquivo)


    @pyqtSlot(str, name='defineQuantidadeRegistros')
    def define_quantidade_registros(self, qtd_registros: int):        
        tam = len(self._dados_arquivo_original)
        qtd_registros = int(qtd_registros)
        Logger.debug('Contador de %s elementos selecionado' % qtd_registros)
        self._registros_por_arquivo = tam if (qtd_registros == -1) else qtd_registros
    

    @pyqtSlot(str, name='filtraColuna')
    def filtra_coluna(self, coluna):
        Logger.debug('coluna = "%s"' % coluna)
        self._valores_filtrados = []
        self._coluna_filtrada = coluna

        if coluna in self._colunas_disponiveis:
            conj_valores = set()

            for dado in self._dados_arquivo_original:
                conj_valores.add(dado[coluna])
                if len(conj_valores) >= 100:
                    break

            valores_unicos = list(conj_valores)
            muitos_valores = '%d valores possíveis.' % len(valores_unicos)
            self._valores_filtrados.extend(valores_unicos if len(valores_unicos) <= 100 else [muitos_valores])
            Logger.debug('%d valores encontrados para a coluna "%s".' % (len(valores_unicos), coluna))
        else:
            self._valores_filtrados = []
            Logger.debug('0 valor encontrados para a coluna "%s".' % coluna)

        self.valores_filtrados_changed.emit(self._valores_filtrados)


    @pyqtProperty(list, notify=valores_filtrados_changed)
    def valores_filtrados(self):
        """Obtem valores filtrados após processamento da função filtra_coluna()."""
        return self._valores_filtrados

    
    @pyqtSlot(str, str, name='filtraDados')
    def filtra_dados(self, filtro_coluna, filtro_valor):
        # if (filtro_coluna != '<Selecione>' and filtro_valor != '<Selecione>'):
        if (filtro_coluna in self.colunas_disponiveis and filtro_valor != '<Selecione>'):
            # Logger.debug("%s, %s" % (filtro_coluna, filtro_valor))
            dados = self._dados_arquivo_original[:]
            for i in dados:
                if i[filtro_coluna] != filtro_valor:
                    self._dados_arquivo_original.remove(i)
            if len(self._dados_arquivo_original) == 0:
                # msg = 'Nenhum registro encontrado para o filtro especificado.\nO filtro será ignorado.'
                self._dados_arquivo_original = dados[:]
                # self.msg_filtro_ignorado.emit(msg)
                self._filtro_ignorado = True
            else:
                self._filtro_ignorado = False

        Logger.debug('Filtro: %i registro(s) para {%s: %s}' % (len(self._dados_arquivo_original), filtro_coluna, filtro_valor))


    @pyqtProperty(bool)
    def filtro_ignorado(self):
        return self._filtro_ignorado


    @pyqtProperty(int, notify=quantidade_registros_changed)
    def quantidade_registros(self):
        return len(self._dados_arquivo_original)


    @pyqtSlot(name='iniciaOperacao')
    def inicia_operacao(self):
        """Deve ser chamado de fora de thread."""
        Logger.debug('inicia_operacao() chamado.')
        self.status_operacao_changed.connect(self.operacao_terminada)
        self._thread_operacao = ThreadCancelavel(target=self._processa)
        self._thread_operacao.start()


    @pyqtSlot(name='cancelaOperacao')
    def cancela_operacao(self):
        """Deve ser chamado de fora de thread."""
        Logger.debug('cancela_operacao() chamado.')
        self._thread_operacao.stop()
        self._thread_operacao.join()


    def operacao_terminada(self, status, http_code, mensagem):
        """Faz limpeza de thread depois que ela termina."""
        Logger.debug('operacao_terminada: %i, %s, "%s"' % (status, http_code, mensagem))
        self._thread_operacao.join()


    def atualiza_progresso(self, valor):
        if self._thread_operacao.stopped():
            return False
        else:
            self.registro_processado.emit(valor)
            return True


    def _processa(self):
        status, http_code, message = prep_geocode.testa_conexao(self._url)
        Logger.debug('_processa: %i, %s, %s' % (status, http_code, message))

        if status == OK and http_code != 200:
            Logger.debug('status_operacao_changed: FAIL, %s, %s' % (http_code, message))
            self.status_operacao_changed.emit(FAIL, http_code, message)
            return
        elif status == FAIL:
            Logger.debug('status_operacao_changed: FAIL, 0, "%s"' % message)
            self.status_operacao_changed.emit(FAIL, 0, message)
            return

        colunas = self._colunas_escolhidas[:]
        dados_preparados = prep_files.prepara_dados(self._dados_arquivo_original, colunas)
        dados_padronizados = prep_files.padroniza_dados(dados_preparados)

        prep_files.gera_arquivo(self._dados_arquivo_original, 'original', self._arquivo, self._colunas_disponiveis)

        labels_arquivo_geocode = ['KEY', 'COLUNA_PESQ', 'DADO_COMPL_PESQ', 'DADO_PESQ', 'LOCAL_ENCONTRADO', 'SIMILARIDADE', 'LAT', 'LONG']

        fatias = list(prep_geocode.fatia_lista(dados_padronizados, self._registros_por_arquivo))
        val = 0

        try:
            for v in fatias:
                val += 1
                dct_pesquisa = {'prioridade': colunas, 'dados': v, 'geocode_service': self._url}
                lista_final = prep_geocode.gera_lista_final(dct_pesquisa, self.atualiza_progresso)
                prep_files.gera_arquivo(lista_final, 'geocode' + str(val), self._arquivo, labels_arquivo_geocode)
        except ThreadInterrompidaError:
            Logger.debug('** interrompido pelo usuário')
            self.status_operacao_changed.emit(INTERRUPTED, 0, '')
            return

        self.arquivos_gerados.emit(self.lista_arquivos_gerados())

        # Fecha pop up de progresso
        Logger.debug('status_operacao_changed: OK, 0, ""')
        self.status_operacao_changed.emit(OK, 0, '')


    def lista_arquivos_gerados(self):
        try:
            diretorio, arquivo_saida = prep_files._identifica_diretorio(self._arquivo)
            diretorio_saida = os.path.join(diretorio, 'files_%s' % arquivo_saida.replace('.csv', ''))

            if os.path.exists(diretorio_saida):
                lista_arquivos = os.listdir(diretorio_saida)
                lista_arquivos_ordenada = sorted(lista_arquivos)

                text_label = 'Arquivos gerados:\n\t' + diretorio_saida

                for i in lista_arquivos_ordenada:
                    text_label += ('\n\t\t' + i)

            else:
                text_label = 'Houve um problema ao acessar o diretório de saída. Verifique se novos arquivos foram gerados no diretório do arquivo csv original.'
        except Exception as e:
            Logger.error('%s' % e)
            raise e
            text_label = 'Verifique se novos arquivos foram gerados no diretório do arquivo csv original.'
        Logger.debug(text_label)
        return text_label
