import sys
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QFile
from PySide6 import QtUiTools
from pages.page_db import Page_DB
from database.sqlite import Database

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        ui_file = QFile("setup.ui")
        if not ui_file.open(QFile.ReadOnly):
            print(f"Error al cargar el archivo de interfaz: {ui_file.errorString()}")
            sys.exit(1)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Vaccine Reminder")
        self.showMaximized()

        self.db = Database()

        self.page_db = Page_DB(self.ui, self)