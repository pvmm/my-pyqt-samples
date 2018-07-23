# -*- coding: utf-8 -*-
import sys, os

from PyQt5 import QtQuick
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from logger import StdoutLogger as Logger

Logger.debug("OK")

if __name__ == "__main__":
    os.environ['QT_QUICK_CONTROLS_STYLE']='Universal'

    # Create an instance of the application
    app = QGuiApplication(sys.argv)

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
