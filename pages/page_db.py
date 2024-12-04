from PySide6 import QtWidgets

class Page_DB:
    def __init__(self, ui, mainwindow):
        super().__init__
        self.mainwindow = mainwindow
        self.ui = ui
        # Botones
        self.ui.bt_add_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_user))
        self.ui.bt_mod_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_mod_user))
        self.ui.bt_del_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_del_user))
        self.ui.bt_salir_user.clicked.connect(lambda: self.mainwindow.close())
