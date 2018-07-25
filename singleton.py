# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty


class Singleton(QObject):
    url_changed = pyqtSignal()
    __instance = None
    _url = 'http://geocodeapi.codeplan.df.gov.br'
    _colunas_disponiveis = ['CEP', 'Endereço', 'RA', 'AAA', 'BBB']
    _colunas_escolhidas = []

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


    @pyqtProperty('QString', notify=url_changed)
    def url(self):
        return self._url


    @pyqtProperty(list)
    def colunas_disponiveis(self):
        return self._colunas_disponiveis


    @pyqtProperty(list)
    def colunas(self):
        return self._colunas_escolhidas


    @url.setter
    def setUrl(self, url):
        self._url = url
        self.url_changed.emit()


    @pyqtSlot(str, name='adicionaColuna')
    def adiciona_coluna(self, coluna):
        print("adiciona '%s'" % coluna)
        self._colunas_escolhidas.append(coluna)


    @pyqtSlot(str, name='removeColuna')
    def remove_coluna(self, coluna):
        print("removendo '%s'" % coluna)
        self._colunas_escolhidas.remove(coluna)

