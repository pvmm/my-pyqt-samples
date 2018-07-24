# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty


class Singleton(QObject):
    __instance = None
    url = ""
    colunas = []

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


    @pyqtProperty('QString')
    def url(self):
        return self.url


    @pyqtSlot(str)
    def setUrl(self, url):
        self.url = url


    @pyqtSlot(str, name = 'adicionaColuna')
    def adiciona_coluna(self, coluna):
        print("adiciona '%s'" % coluna)
        self.colunas.append(coluna)


    @pyqtSlot(str, name = 'removeColuna')
    def remove_coluna(self, coluna):
        print("removendo '%s'" % coluna)
        self.colunas.remove(coluna)

