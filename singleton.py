# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
import os
import prep_files, prep_geocode
from logger import StdoutLogger as Logger


class Singleton(QObject):
    urlChanged = pyqtSignal(str)
    valoresFiltradosChanged = pyqtSignal(list)

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


    @pyqtSlot(str, name='filtraColuna')
    def filtra_coluna(self, coluna):
        Logger.debug('coluna = "%s"' % coluna)
        Logger.debug('coluna = "%s"' % ','.join(self._colunas_escolhidas))
        self._valores_filtrados = []
        self._coluna_filtrada = coluna

        if coluna in self._colunas_escolhidas:
            conj_valores = set()

            for dado in self._dados_arquivo_original:
                conj_valores.add(dado[coluna])
                if len(conj_valores) >= 100:
                    break

            valores_unicos = list(conj_valores)
            muitos_valores = '%d valores possíveis.' % len(valores_unicos)
            valores_unicos.insert(0, '<Selecione>')
            self._valores_filtrados.extend(valores_unicos if len(valores_unicos) <= 100 else [muitos_valores])

        self.valoresFiltradosChanged.emit(self._valores_filtrados)


    @pyqtProperty(list, notify=valoresFiltradosChanged)
    def valores_filtrados(self):
        return self._valores_filtrados

