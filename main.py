from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication
from mainwindow import MainWindow
import sys

QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()