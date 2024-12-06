from database.consultas_pacientes import Comunicacion
from metodos.metodos_pacientes import MetodosPacientes
from functools import partial
class PageDelete:
    def __init__(self, ui, statusBar, page_db):
        super().__init__()
        self.ui = ui
        self.db = Comunicacion()
        self.page_db = page_db
        self.ui.bt_volver_del.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.metodos_pacientes = MetodosPacientes(self.ui, statusBar)
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_del)

        # Conexiones a los botones
        self.ui.bt_volver_del.clicked.connect(self.volver)
        self.ui.bt_buscar_del.clicked.connect(partial(self.metodos_pacientes.buscar_por_nombre, self.ui.tabla_del, self.ui.line_dni_del))
        self.ui.bt_eliminar_del.clicked.connect(self.metodos_pacientes.eliminar_paciente)

        self.ui.tabla_del.cellClicked.connect(self.metodos_pacientes.cargar_producto_seleccionado)

    def volver(self):
        self.page_db.metodos_pacientes.mostrarPacientes(self.ui.tabla_db)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_db)