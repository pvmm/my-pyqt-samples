# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty


class Singleton(QObject):
    __instance = None


    def __init__(self, parent = None):
        super().__init__(parent)
        self.url = "http://geocodeapi.codeplan.df.gov.br"
        self.colunas = []


    @classmethod
    def getInstance(cls, *args):
        if cls.__instance == None:
            cls.__instance = cls()
        return cls.__instance


    @pyqtProperty('QString')
    def url(self):
        return self.url


    @pyqtSlot(str)
    def setUrl(self, url):
        self.url = url


    @pyqtSlot(str)
    def adicionar_coluna(coluna):
        self.colunas.append(coluna)


    @pyqtSlot(str)
    def remover_coluna(coluna):
        self.colunas.remove(coluna)

