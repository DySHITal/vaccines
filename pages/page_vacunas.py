from PySide6.QtGui import QColor, QBrush
from database.consultas_vacunas import Comms
from PySide6.QtWidgets import QTableWidgetItem, QDateEdit, QMessageBox
from PySide6.QtCore import QDate

class PageVacunas:
    def __init__(self, ui, statusBar):
        super().__init__()
        self.ui = ui
        self.statusBar = statusBar
        self.paciente_id = None
        self.comms = Comms()

        self.ui.bt_volver_vacuna.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.ui.bt_refrescar_vacuna.clicked.connect(self.refrescar_vacuna)
        self.ui.tabla_vacunas.cellDoubleClicked.connect(self.on_cellDoubleClicked)

    def cargar_vacunas(self, paciente_id):
        self.paciente_id = paciente_id
        self.ui.tabla_vacunas.clearContents() 
        vacunas_aplicadas = self.comms.obtener_vacunas_aplicadas(paciente_id)
        
        if vacunas_aplicadas:
            for nombre_vacuna, fecha_aplicacion, fecha_recordatorio in vacunas_aplicadas:
                column_index = self.buscar_columna_vacuna(nombre_vacuna)
                if column_index is not None:
                    row = self.buscar_fila_vacia(column_index)
                    
                    # Celda de vacuna aplicada
                    item_aplicacion = QTableWidgetItem(fecha_aplicacion)
                    item_aplicacion.setBackground(QBrush(QColor(0, 255, 0)))  # Verde
                    item_aplicacion.setForeground(QBrush(QColor(0, 0, 0)))   # Texto negro
                    self.ui.tabla_vacunas.setItem(row, column_index, item_aplicacion)
                    
                    # Celda de recordatorio
                    siguiente_fila = self.buscar_fila_vacia(column_index, row + 1)
                    item_recordatorio = QTableWidgetItem(fecha_recordatorio)
                    self.ui.tabla_vacunas.setItem(siguiente_fila, column_index, item_recordatorio)

                    fecha_recordatorio_qdate = QDate.fromString(fecha_recordatorio, 'yyyy-MM-dd')
                    fecha_actual = QDate.currentDate()
                    
                    if fecha_recordatorio_qdate < fecha_actual:
                        item_recordatorio.setBackground(QBrush(QColor(255, 0, 0)))  # Rojo (vencido)
                    elif fecha_recordatorio_qdate == fecha_actual:
                        item_recordatorio.setBackground(QBrush(QColor(255, 255, 0)))  # Amarillo (hoy)
                        QMessageBox.information(
                            self.ui, 'Recordatorio',
                            f'Es el día para aplicar la vacuna: {nombre_vacuna}.',
                            QMessageBox.Ok
                        )
                    else:
                        item_recordatorio.setBackground(QBrush(QColor(255, 255, 0)))  # Amarillo
                        item_recordatorio.setForeground(QBrush(QColor(0, 0, 0)))    # Texto negro


    def buscar_fila_vacia(self, column_index, start_row=0):
        row_count = self.ui.tabla_vacunas.rowCount()
        for row in range(start_row, row_count):
            if not self.ui.tabla_vacunas.item(row, column_index):
                return row
        return row_count

    def buscar_columna_vacuna(self, nombre_vacuna):
        column_count = self.ui.tabla_vacunas.columnCount()
        for col in range(column_count):
            if self.ui.tabla_vacunas.horizontalHeaderItem(col).text() == nombre_vacuna:
                return col
        return None
    
    def refrescar_vacuna(self):
        self.cargar_vacunas(self.paciente_id)
    
    def on_cellDoubleClicked(self, row, column): 
        # Crear el editor de fecha
        date_edit = QDateEdit(self.ui.tabla_vacunas)
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        self.ui.tabla_vacunas.setCellWidget(row, column, date_edit)
        
        # Validar el contenido de la celda
        item = self.ui.tabla_vacunas.item(row, column)
        
        # Si la celda ya tiene una vacuna aplicada
        if item and item.background().color() == QColor(0, 255, 0):
            QMessageBox.warning(self.ui, 'Vacuna ya colocada', 'Esta vacuna ya fue colocada, no se puede editar.', QMessageBox.OK)
            self.ui.tabla_vacunas.setCellWidget(row, column, None)  # Quitar el editor de fecha
            return

        # Si la celda corresponde a un recordatorio
        if item and item.background().color() == QColor(255, 255, 0):
            respuesta = QMessageBox.question(self.ui, 'Confirmar Aplicación', '¿Ya se colocó esta vacuna?', QMessageBox.Yes, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                item.setBackground(QBrush(QColor(0, 255, 0)))
                item.setText(QDate.currentDate().toString('yyyy-MM-dd'))
                self.ui.tabla_vacunas.setCellWidget(row, column, None)
                QMessageBox.information(self.ui, 'Vacuna Aplicada', 'La vacuna ha sido marcada como colocada.', QMessageBox.Ok)
                self.recordatorio_vacunas(row, column, QDate.currentDate(), self.paciente_id)
            return

        # Si la celda es de un recordatorio vencido
        if item and item.background().color() == QColor(255, 0, 0):
            respuesta = QMessageBox.question(self.ui, 'Confirmar Aplicación', '¿Ya se colocó esta vacuna?', QMessageBox.Yes, QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                item.setBackground(QBrush(QColor(0, 255, 0)))
                item.setText(QDate.currentDate().toString('yyyy-MM-dd'))
                self.ui.tabla_vacunas.setCellWidget(row, column, None)
                QMessageBox.information(self.ui, 'Vacuna Aplicada', 'La vacuna ha sido marcada como colocada.', QMessageBox.Ok)
                self.recordatorio_vacunas(row, column, QDate.currentDate(), self.paciente_id)
            return

        # Si la celda está vacía (nueva entrada)
        if not item or not item.text():
            # Conectar el editor de fecha para una nueva entrada
            date_edit.dateChanged.connect(lambda date: self.recordatorio_vacunas(row, column, date, self.paciente_id))
            return

    def recordatorio_vacunas(self, row, column, date, paciente_id):
        nombre_vacuna = self.ui.tabla_vacunas.horizontalHeaderItem(column).text().upper()
        vacuna_id = self.comms.obtener_vacuna_id(nombre_vacuna)
        if vacuna_id and paciente_id:
            fecha_aplicacion = date.toString('yyyy-MM-dd')
            self.ui.tabla_vacunas.setItem(row, column, QTableWidgetItem(fecha_aplicacion))
            QMessageBox.information(self.ui, 'Fecha Recordatorio', 'Por favor, selecciones una fecha recordatorio para esta vacuna.', QMessageBox.Ok)
            if not self.ui.tabla_vacunas.item(row+1, column):
                date_recordatorio = QDateEdit(self.ui.tabla_vacunas)
                date_recordatorio.setCalendarPopup(True)
                date_recordatorio.setDate(QDate.currentDate())
                self.ui.tabla_vacunas.setCellWidget(row+1, column, date_recordatorio)
                date_recordatorio.dateChanged.connect(lambda date: self.actualizar_vacuna(row, column, fecha_aplicacion, date, paciente_id, vacuna_id))
        else:
            self.statusBar.showMessage("No se pudo agregar la vacuna. Datos incompletos.")

    def actualizar_vacuna(self, row, column, fecha_aplicacion, fecha_recordatorio, paciente_id, vacuna_id):
        fecha_recordatorio_str = fecha_recordatorio.toString('yyyy-MM-dd')
        self.ui.tabla_vacunas.setCellWidget(row, column, None)
        self.comms.agregar_vacuna(paciente_id, vacuna_id, fecha_aplicacion, fecha_recordatorio_str)
        self.statusBar.showMessage("Vacuna actualizada correctamente.", 5000)

        # Asegurarse de que la celda para el recordatorio tiene un QTableWidgetItem
        siguiente_row = row + 1
        item_recordatorio = self.ui.tabla_vacunas.item(siguiente_row, column)
        if not item_recordatorio:
            item_recordatorio = QTableWidgetItem()
            self.ui.tabla_vacunas.setItem(siguiente_row, column, item_recordatorio)

        item_recordatorio.setText(fecha_recordatorio_str)

        # Cambiar el color de fondo según la fecha
        fecha_recordatorio_qdate = QDate.fromString(fecha_recordatorio_str, 'yyyy-MM-dd')
        fecha_actual = QDate.currentDate()
        if fecha_recordatorio_qdate < fecha_actual:
            item_recordatorio.setBackground(QBrush(QColor(255, 0, 0)))  # Rojo para fechas pasadas
        elif fecha_recordatorio_qdate == fecha_actual:
            item_recordatorio.setBackground(QBrush(QColor(255, 255, 0)))  # Amarillo para la fecha actual
            QMessageBox.information(self.ui, 'Recordatorio', f'Es el día para aplicar la vacuna: {self.ui.tabla_vacunas.horizontalHeaderItem(column).text()}.', QMessageBox.Ok)

