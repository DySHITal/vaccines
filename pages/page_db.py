from metodos.metodos_pacientes import MetodosPacientes
from functools import partial

class Page_DB:
    def __init__(self, ui, mainwindow, statusBar):
        super().__init__()
        self.mainwindow = mainwindow
        self.ui = ui
        self.metodos_pacientes = MetodosPacientes(self.ui, statusBar)
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_db)
        
        # Botones
        self.ui.bt_add_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_user))
        self.ui.bt_mod_user.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_mod_user))
        self.ui.bt_del_user.clicked.connect(self.actualizar_tabla_del)
        self.ui.bt_salir_user.clicked.connect(lambda: self.mainwindow.close())

        # Conectar buscar a buscar_por_nombre
        self.ui.bt_buscar_db.clicked.connect(partial(self.metodos_pacientes.buscar_por_nombre, self.ui.tabla_db, self.ui.line_nombre_db, self.ui.line_apellido_db))
        self.ui.tabla_db.cellDoubleClicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_vacunas))

    def actualizar_tabla_del(self):
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_del)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_del_user)

