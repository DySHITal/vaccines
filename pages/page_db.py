from metodos.metodos_pacientes import MetodosPacientes
from functools import partial
from PySide6.QtWidgets import QApplication
from pages.page_vacunas import PageVacunas
from database.consultas_pacientes import Comunicacion

class Page_DB:
    def __init__(self, ui, mainwindow, statusBar):
        super().__init__()
        self.mainwindow = mainwindow
        self.ui = ui
        self.db = Comunicacion()
        self.page_vacunas = PageVacunas(self.ui, statusBar)
        self.metodos_pacientes = MetodosPacientes(self.ui, statusBar)
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_db)
        
        # Botones
        self.ui.bt_add_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_user))
        self.ui.bt_mod_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_mod_user))
        self.ui.bt_del_user.clicked.connect(self.actualizar_tabla_del)
        self.ui.bt_salir_user.clicked.connect(lambda: QApplication.instance().quit())
        self.ui.bt_refrescar_db.clicked.connect(lambda: self.metodos_pacientes.mostrarPacientes(self.ui.tabla_db))
        self.ui.bt_buscar_db.clicked.connect(partial(self.metodos_pacientes.buscar_por_nombre, self.ui.tabla_db, self.ui.line_nombre_db, self.ui.line_apellido_db, self.ui.line_dni_db))

        self.ui.tabla_db.cellDoubleClicked.connect(self.mostrar_vacunas)

    def actualizar_tabla_del(self):
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_del)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_del_user)        

    def mostrar_vacunas(self, row):
        nombre = self.ui.tabla_db.item(row, 0).text()
        apellido = self.ui.tabla_db.item(row, 1).text()
        paciente_id = self.db.get_paciente_id(nombre, apellido)
        if paciente_id:
            self.page_vacunas.cargar_vacunas(paciente_id)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_vacunas)
        else:
            self.statusBar.showMessage("No se pudo obtener el ID del paciente.")