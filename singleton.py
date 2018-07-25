# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty


class Singleton(QObject):
    urlChanged = pyqtSignal()
    __instance = None
    _colunas_disponiveis = ['CEP', 'Endereço', 'RA', 'AAA', 'BBB']
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
        print("adiciona '%s'" % coluna)
        self._colunas_escolhidas.append(coluna)


    @pyqtSlot(str, name='removeColuna')
    def remove_coluna(self, coluna):
        print("removendo '%s'" % coluna)
        self._colunas_escolhidas.remove(coluna)

