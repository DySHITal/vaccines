import sqlite3
from PySide6 import QtWidgets
from database.consultas import Comunicacion
class MetodosPacientes:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.db = Comunicacion()

    def mostrarPacientes(self):
            datos = self.db.mostrar_pacientes()
            i = len(datos)
            self.ui.tabla_db.setRowCount(i)
            tablerow = 0
            for row in datos:
                self.Id = row[0]
                self.ui.tabla_db.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
                self.ui.tabla_db.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
                self.ui.tabla_db.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
                self.ui.tabla_db.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
                tablerow += 1

    def buscar_por_nombre(self):
        nombre = self.ui.line_nombre_db.text().strip().upper()
        apellido = self.ui.line_apellido_db.text().strip().upper()

        paciente = self.db.busca_paciente(nombre, apellido)

        if not paciente:
            self.ui.tabla_db.setRowCount(0)
            return

        if not all(isinstance(row, (tuple, list)) and len(row) > 4 for row in paciente):
            self.ui.signal_db.setText('Formato de datos incorrecto')
            return

        self.ui.tabla_db.setRowCount(len(paciente))

        for tablerow, row in enumerate(paciente):
            for col in range(1, 5):
                self.ui.tabla_db.setItem(tablerow, col - 1, QtWidgets.QTableWidgetItem(str(row[col])))

    def agregar_paciente(self):
        nombre = self.ui.line_nombre_add.text().strip().upper()
        apellido = self.ui.line_apellido_add.text().strip().upper()
        telefono = self.ui.line_cel_add.text().strip()
        correo = self.ui.line_correo_add.text().strip()

        if not (nombre and apellido):
            print('Nombre y apellido son obligatorio')
            return

        try:
            paciente_existente = self.db.consultar_paciente(nombre, apellido)
            if paciente_existente:
                print('Producto ya existe')
            else:
                self.db.agregar_paciente(nombre, apellido, telefono, correo)
                print('Producto Registrado')

                self.ui.line_nombre_add.clear()
                self.ui.line_apellido_add.clear()
                self.ui.line_cel_add.clear()
                self.ui.line_correo_add.clear()

        except sqlite3.OperationalError as e:
            print('Error en la base de datos')
            print(f"Error SQLite: {e}")
        except Exception as e:
            print('Error inesperado')
            print(f"Error inesperado: {e}")