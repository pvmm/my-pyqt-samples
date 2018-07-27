# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
import os, re
import prep_files, prep_geocode
from logger import StdoutLogger as Logger


class Singleton(QObject):
    urlChanged = pyqtSignal(str)
    valores_filtrados_changed = pyqtSignal(list, name='valoresFiltradosChanged', arguments=['valores'])
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


    @pyqtProperty(str, notify=urlChanged)
    def url(self):
        return self._url


    @url.setter
    def url(self, url):
        if self._url != url:
            self._url = url
            self.urlChanged.emit()


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


    @pyqtSlot(str, name='registrosPorArquivo')
    def registros_por_arquivo(self, qtd_registros):        
        tam = len(self._dados_arquivo_original)
        self._registros_por_arquivo = tam if (qtd_registros == 'Todos') else int(re.sub('[^0-9]', '', qtd_registros))
    

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
            valores_unicos.insert(0, '<Selecione>')
            self._valores_filtrados.extend(valores_unicos if len(valores_unicos) <= 100 else [muitos_valores])
            Logger.debug('%d valores encontrados para a coluna "%s".' % (len(valores_unicos), coluna))
            self.valores_filtrados_changed.emit(self._valores_filtrados)
        else:
            Logger.warning('"%s": coluna não encontrada entre as colunas escolhidas.' % coluna)


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
            if len(self._dados_arquivo_original)==0:
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


    def process_button_click(self):
        http_code = prep_geocode.testa_conexao(self._url)
        if http_code == 200:
            self.show_popup('Aguarde o fim do processamento...')
            mythread = threading.Thread(target=self.inicia_processamento)
            mythread.start()
        else:
            self.show_popup('Verifique a URL do serviço de geocodificação.')

    def inicia_processamento(self):
        # colunas = self.recupera_labels()
        colunas = colunas_selecionadas[:]
        dados_preparados = prep_files.prepara_dados(self._dados_arquivo_original, colunas)
        dados_padronizados = prep_files.padroniza_dados(dados_preparados)

        prep_files.gera_arquivo(self._dados_arquivo_original, 'original', self._arquivo, self._colunas_disponiveis)

        labels_arquivo_geocode = ['KEY', 'COLUNA_PESQ', 'DADO_COMPL_PESQ', 'DADO_PESQ', 'LOCAL_ENCONTRADO', 'SIMILARIDADE', 'LAT', 'LONG']

        fatias = list( prep_geocode.fatia_lista(dados_padronizados, self._registros_por_arquivo) )
        val = 0
        for v in fatias:
            val += 1

            dct_pesquisa = {'prioridade': colunas, 'dados': v, 'geocode_service': self._url}
            # lista_final = prep_geocode.gera_lista_final(dct_pesquisa)
            lista_final = self.gera_lista_final(dct_pesquisa)

            prep_files.gera_arquivo(lista_final, 'geocode' + str(val), arquivo, labels_arquivo_geocode)

        self.lista_arquivos_gerados()

        ## Fecha pop up de progresso
        # self.pop_up.dismiss()


    def gera_lista_final(self, dct_pesquisa):
        '''
        Recebe dicionário com dados do arquivo csv (lista de dicionários com a chave e com as colunas a serem geocodificadas) e lista de colunas na ordem que deve ser feita a geocodificação.
        Monta a lista final que será gravada em novo arquivo csv aplicando a função _consulta_geocode para cada registro.
        '''
        try:
            dados = dct_pesquisa['dados']
            colunas = dct_pesquisa['prioridade']
            geocode_service = dct_pesquisa['geocode_service']

            dados_finais = []
            total = len(dados)
            ct = 1

            for d in dados:

                lb_key = 'KEY'
                key = d[lb_key]

                dct = {lb_key: key}

                for c in colunas:
                    if c in list(d.keys()):
                        result_set = prep_geocode._consulta_geocode(d[c], c, geocode_service)
                        dct.update(result_set)
                        if dct['SIMILARIDADE']!=0.0:
                            break

                dados_finais.append(dct)

                ## Atualiza contador do pop up de progresso
                # self.pop_up.update_pop_up_text(str(ct) + ' de ' + str(total))

                Logger.debug('main: {0} de {1}'.format(ct, total))
                ct += 1

            return dados_finais
        except Exception as e:
            Logger.error('main: Erro ao gerar lista final: %s' % e)
            raise e

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

                ## Atualiza a textarea da última tela com os arquivos gerados
                # App.get_running_app().root.screens[index_screen].ids.text_input_diretorio.text = text_label
            else:
                text_label = 'Houve um problema ao acessar o diretório de saída. Verifique se novos arquivos foram gerados no diretório do arquivo csv original.'
                ## Atualiza a textarea da última tela com os arquivos gerados
                # App.get_running_app().root.screens[index_screen].ids.text_input_diretorio.text = text_label
        except Exception as e:
            Logger.error('main: error %s' % e)
            raise e
            text_label = 'Verifique se novos arquivos foram gerados no diretório do arquivo csv original.'
            ## Atualiza a textarea da última tela com os arquivos gerados
            # App.get_running_app().root.screens[index_screen].ids.text_input_diretorio.text = text_label
