class PageVacunas:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.ui.bt_volver_vacuna.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))