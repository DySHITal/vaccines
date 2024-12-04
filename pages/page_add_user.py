from database.consultas import Comunicacion
from database.consultas import Comunicacion

class Page_add_user:
    def __init__(self, ui, page_db):
        super().__init__()
        self.ui = ui
        self.db = Comunicacion()
        self.page_db = page_db
        
        # Conexiones de los botones
        self.ui.bt_volver_add.clicked.connect(self.volver)
        self.ui.bt_guardar_add.clicked.connect(self.guardar_paciente)

    def guardar_paciente(self):
        nombre = self.ui.line_nombre_add.text().strip().upper()
        apellido = self.ui.line_apellido_add.text().strip().upper()
        telefono = self.ui.line_cel_add.text().strip()
        correo = self.ui.line_correo_add.text().strip()

        if not (nombre and apellido):
            print("El nombre y apellido son obligatorios.")
            return

        try:
            self.db.agregar_paciente(nombre, apellido, telefono, correo)
            print("Paciente registrado exitosamente.")
            
            # Limpiar campos
            self.ui.line_nombre_add.clear()
            self.ui.line_apellido_add.clear()
            self.ui.line_cel_add.clear()
            self.ui.line_correo_add.clear()
        except Exception as e:
            print(f"Error al agregar el paciente: {e}")

    def volver(self):
        self.page_db.metodos_pacientes.mostrarPacientes()
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_db)