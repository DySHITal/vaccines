from database.consultas_pacientes import Comunicacion

class Page_add_user:
    def __init__(self, ui, metodos_pacientes, statusBar):
        super().__init__()
        self.ui = ui
        self.db = Comunicacion()
        self.metodos_pacientes = metodos_pacientes
        self.statusBar = statusBar
        
        # Conexiones de los botones
        self.ui.bt_volver_add.clicked.connect(self.volver)
        self.ui.bt_guardar_add.clicked.connect(self.guardar_paciente)

    def guardar_paciente(self):
        nombre = self.ui.line_nombre_add.text().strip().upper()
        apellido = self.ui.line_apellido_add.text().strip().upper()
        telefono = self.ui.line_cel_add.text().strip()
        correo = self.ui.line_correo_add.text().strip()

        if not (nombre and apellido):
            self.statusBar.showMessage("El nombre y apellido son obligatorios.", 5000)
            return

        try:
            self.db.agregar_paciente(nombre, apellido, telefono, correo)
            self.statusBar.showMessage("Paciente registrado exitosamente.", 5000)
            
            # Limpiar campos
            self.ui.line_nombre_add.clear()
            self.ui.line_apellido_add.clear()
            self.ui.line_cel_add.clear()
            self.ui.line_correo_add.clear()
        except Exception as e:
            self.statusBar.showMessage(f"Error al agregar el paciente: {e}", 5000)

    def volver(self):
        self.metodos_pacientes.mostrarPacientes(self.ui.tabla_db)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_db)