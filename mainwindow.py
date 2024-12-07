import sys
from PySide6.QtWidgets import QMainWindow, QStatusBar
from PySide6.QtCore import QFile
from PySide6 import QtUiTools
from pages.page_db import Page_DB
from pages.page_add_user import Page_add_user
from pages.page_mod_user import PageModify
from pages.page_del_user import PageDelete
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
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)


        # Paginas
        self.page_db = Page_DB(self, self.ui, self.statusBar)
        self.page_addUser = Page_add_user(self.ui, self.page_db.metodos_pacientes, self.statusBar)
        self.page_modUser = PageModify(self.ui, self.statusBar)
        self.page_delUser = PageDelete(self.ui, self.statusBar, self.page_db)
