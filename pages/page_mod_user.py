from metodos.metodos_pacientes import MetodosPacientes

class PageModify:
    def __init__(self, ui, statusBar):
        super().__init__()
        self.ui = ui
        self.statusBar = statusBar 
        self.metodos_pacientes = MetodosPacientes(self.ui, statusBar)

        # Botones
        self.ui.bt_volver_mod.clicked.connect(self.volver)
        self.ui.bt_buscar_mod.clicked.connect(self.metodos_pacientes.buscar_por_nombre_modificar)
        self.ui.bt_modificar_mod.clicked.connect(self.metodos_pacientes.modificar_paciente)

    def volver(self):
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_db)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_db)