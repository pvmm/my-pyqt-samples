# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty


class Singleton(QObject):
    __instance = None

    def __init__(self, parent = None):
        super().__init__(parent)

    @classmethod
    def getInstance(cls, *args):
        if cls.__instance == None:
            cls.__instance = cls()
        return cls.__instance

    @pyqtProperty('QString')
    def x(self):
        return "x"

    @pyqtSlot()
    def xpto(self):
        print("xpto called.")

