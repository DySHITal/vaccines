from PySide6.QtGui import QColor, QBrush
from database.consultas_vacunas import Comms
from PySide6.QtWidgets import QTableWidgetItem

class PageVacunas:
    def __init__(self, ui, statusBar):
        super().__init__()
        self.ui = ui
        self.statusBar = statusBar
        self.paciente_id = None
        self.comms = Comms()

        self.ui.bt_volver_vacuna.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.ui.tabla_vacunas.cellDoubleClicked.connect(self.double_click)

    def double_click(self, row, column):
        print(f'Click en fila: {row} y columna: {column}')

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