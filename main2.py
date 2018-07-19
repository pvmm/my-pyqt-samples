import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    # Create an instance of the application
    app = QGuiApplication(sys.argv)

    # Create QML engine
    engine = QQmlApplicationEngine()

    # Load the qml file into the engine
    engine.load("main.qml")
 
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
