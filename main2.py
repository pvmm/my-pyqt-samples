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


# Carrega PyQt5
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty
from PyQt5 import QtQuick
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType

Logger.debug("Bibliotecas do PyQt5 carregadas.")


if __name__ == "__main__":
    os.environ['QT_QUICK_CONTROLS_STYLE']='Universal'

    # Define função de captura de erro para capturar erros com QML.
    import traceback

    def excepthook(exctype, value, tb):
        print('** Error Information **')
        print('Type:', exctype)
        print('Message:', value)
        traceback.print_tb(tb)
        exit()
    sys.excepthook = excepthook
    Logger.debug("Captura de erros ativada.")


    # Create an instance of the application
    app = QGuiApplication(sys.argv)

    # Register singleton python object
    from singleton import Singleton
    qmlRegisterSingletonType(Singleton, "PySingletonModule", 1, 0, "PySingleton", Singleton.getInstance)

    # Create QML engine
    engine = QQmlApplicationEngine()

    # Load the qml file into the engine
    engine.load("main2.qml")

    win = engine.rootObjects().pop()
    Logger.debug("win = %s: %i, %s, %s." % (str(win), win.width(), win.title(), win.objectName()))
    swipeView = win.findChild(QtQuick.QQuickItem, "view")
    row = win.findChild(QtQuick.QQuickItem, "row")
    #Logger.debug("children = %s." % win.children())
    Logger.debug("swipeView = %s" % swipeView)
    Logger.debug("row = %s" % row)
	
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())

