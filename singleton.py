# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
import os
import prep_files
from logger import StdoutLogger as Logger


class Singleton(QObject):
    urlChanged = pyqtSignal()
    __instance = None
    _path = os.path.expanduser('~') if 'RELEASE' in os.environ else os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exemplo')
    _colunas_disponiveis = ['CEP', 'Endereço', 'RA', 'AAA', 'BBB'] # TODO: ler essa lista do arquivo csv.
    _colunas_escolhidas = []
    _url = 'http://geocodeapi.codeplan.df.gov.br'


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


    @pyqtSlot(str, name='abreArquivo')
    def abre_arquivo(self, arquivo):
        print('abre_arquivo() called: ' + arquivo)
        if arquivo != '' and os.path.exists(arquivo):
            dados_arquivo_original, colunas_arquivo_original = prep_files.lista_colunas(arquivo, delimitador)
            Logger.debug(dados_arquivo_original)
            Logger.debug(colunas_arquivo_original)
        else:
            Logger.error('"%s": file not found' % arquivo)

