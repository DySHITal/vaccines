from PySide6.QtGui import QColor, QBrush
from database.consultas_vacunas import Comms
from PySide6.QtWidgets import QTableWidgetItem, QDateEdit
from PySide6.QtCore import QDate

class PageVacunas:
    def __init__(self, ui, statusBar):
        super().__init__()
        self.ui = ui
        self.statusBar = statusBar
        self.paciente_id = None
        self.comms = Comms()

        self.ui.bt_volver_vacuna.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.ui.tabla_vacunas.cellDoubleClicked.connect(self.on_cellDoubleClicked)
    def cargar_vacunas(self, paciente_id):
        self.paciente_id = paciente_id
        self.ui.tabla_vacunas.clearContents() 
        vacunas_aplicadas = self.comms.obtener_vacunas_aplicadas(paciente_id)
        
        if vacunas_aplicadas:
            for row, (nombre_vacuna, fecha_aplicacion) in enumerate(vacunas_aplicadas):
                column_index = self.buscar_columna_vacuna(nombre_vacuna)
                print(f'Column index: {column_index}')
                if column_index is not None:
                    item = QTableWidgetItem(fecha_aplicacion)
                    item.setBackground(QBrush(QColor(0, 255, 0)))
                    self.ui.tabla_vacunas.setItem(row, column_index, item)

    def buscar_columna_vacuna(self, nombre_vacuna):
        column_count = self.ui.tabla_vacunas.columnCount()
        for col in range(column_count):
            if self.ui.tabla_vacunas.horizontalHeaderItem(col).text() == nombre_vacuna:
                return col
        return None
    
    def on_cellDoubleClicked(self, row, column): 
        date_edit = QDateEdit(self.ui.tabla_vacunas)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        self.ui.tabla_vacunas.setCellWidget(row, column, date_edit)
        paciente_id_capturado = self.paciente_id
        date_edit.dateChanged.connect(lambda date: self.actualizar_vacuna(row, column, date, paciente_id_capturado))

    def actualizar_vacuna(self, row, column, date, paciente_id):
        nombre_vacuna = self.ui.tabla_vacunas.horizontalHeaderItem(column).text().upper()
        vacuna_id = self.comms.obtener_vacuna_id(nombre_vacuna)

        if vacuna_id and paciente_id:
            fecha_aplicacion = date.toString("yyyy-MM-dd")
            self.ui.tabla_vacunas.setItem(row, column, QTableWidgetItem(fecha_aplicacion))
            self.ui.tabla_vacunas.setCellWidget(row, column, None)
            self.comms.agregar_vacuna(paciente_id, vacuna_id, fecha_aplicacion)
        else:
            self.statusBar.showMessage("No se pudo actualizar la vacuna. Datos incompletos.")