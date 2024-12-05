from metodos.metodos_pacientes import MetodosPacientes

class PageModify:
    def __init__(self, ui, statusBar):
        super().__init__()
        self.ui = ui
        self.statusBar = statusBar 
        self.metodos_pacientes = MetodosPacientes(self.ui, statusBar)
        self.ui.bt_volver_mod.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.ui.bt_buscar_mod.clicked.connect(self.metodos_pacientes.buscar_por_nombre_modificar)