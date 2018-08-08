#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger import StdoutLogger as Logger

# Carregar ambiente virtual
import sys, os, platform

if platform.system() == 'Windows':
    virtualenv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'env/Scripts/activate_this.py')
else:
    virtualenv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'env/bin/activate_this.py')

if os.path.exists(virtualenv_file):
    with open(virtualenv_file) as file_:
        exec(file_.read(), dict(__file__ = virtualenv_file))
        Logger.debug("Virtualenv ativado.")


import click
@click.command(name = 'geocode-csv')
@click.option('--gui', is_flag=True, default=True, help = 'Executa geocode-csv em modo gráfico.')
@click.option('--csvfile', default='AMOSTRA.csv', help = 'Arquivo .CSV de entrada.')
@click.option('--dir', default='files_AMOSTRA', help = 'Diretório de saída.')
def main(gui, csvfile, dir):
    from singleton import Singleton

    if gui:
        os.environ['QT_QUICK_CONTROLS_STYLE']='Universal'

        # Define função de captura de erro para capturar erros com QML.
        if 'RELEASE' not in os.environ:
            import traceback

            def excepthook(exctype, value, tb):
                print('** Error Information **')
                print('Type: %s' % exctype)
                print('Message: %s' % value)
                traceback.print_tb(tb)
                exit()
            sys.excepthook = excepthook
            Logger.debug("Captura de erros ativada.")

        app = QGuiApplication(sys.argv)
        qmlRegisterSingletonType(Singleton, "PySingletonModule", 1, 0, "PySingleton", Singleton.getInstance)
        engine = QQmlApplicationEngine()
        engine.load("main.qml")
        rc = app.exec_()
        del engine
        del app
        exit()

    else:
        Logger.debug('iniciando em modo texto.')
        singleton.abre_arquivo(csvfile)


if __name__ == "__main__":
    # Carrega PyQt5
    from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty
    from PyQt5 import QtQuick
    from PyQt5.QtGui import QGuiApplication
    from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
    Logger.debug("Bibliotecas do PyQt5 carregadas.")

    main()

