import sqlite3
from PySide6 import QtWidgets
from database.consultas_pacientes import Comunicacion
class MetodosPacientes:
    def __init__(self, ui, statusBar):
        super().__init__()
        self.ui = ui
        self.statusBar = statusBar
        self.db = Comunicacion()

    def mostrarPacientes(self, tabla):
        datos = self.db.mostrar_pacientes()
        i = len(datos)
        tabla.setRowCount(i)
        tablerow = 0
        for row in datos:
            for col in range(1, 5):
                tabla.setItem(tablerow, col - 1, QtWidgets.QTableWidgetItem(row[col]))
            tablerow += 1

    def buscar_por_nombre(self, tabla, line_nombre, line_apellido):
        nombre = line_nombre.text().strip().upper()
        apellido = line_apellido.text().strip().upper()

        self.paciente = self.db.busca_paciente(nombre, apellido)

        if not self.paciente:
            tabla.setRowCount(0)
            return

        if not all(isinstance(row, (tuple, list)) and len(row) > 4 for row in self.paciente):
            self.statusBar.showMessage('Formato de datos incorrecto', 5000)
            return

        tabla.setRowCount(len(self.paciente))

        for tablerow, row in enumerate(self.paciente):
            for col in range(1, 5):
                tabla.setItem(tablerow, col - 1, QtWidgets.QTableWidgetItem(str(row[col])))

    def buscar_por_nombre_modificar(self):
        nombre = self.ui.line_nombre_buscar_mod.text().strip().upper()
        apellido = self.ui.line_apellido_buscar_mod.text().strip().upper()

        if not nombre or not apellido:
            self.statusBar.showMessage('El nombre y el modelo son obligatorios', 5000)
            return

        self.paciente = self.db.busca_paciente(nombre, apellido)
        
        if self.paciente: 
            self.Id = self.paciente[0][0]
            self.ui.line_nombre_mod.setText(self.paciente[0][1])
            self.ui.line_apellido_mod.setText(self.paciente[0][2])
            self.ui.line_cel_mod.setText(str(self.paciente[0][4]))
            self.ui.line_correo_mod.setText(str(self.paciente[0][3]))
            self.statusBar.showMessage('Producto encontrado')
        else:
            self.statusBar.showMessage('Producto no encontrado')


    def agregar_paciente(self):
        nombre = self.ui.line_nombre_add.text().strip().upper()
        apellido = self.ui.line_apellido_add.text().strip().upper()
        telefono = self.ui.line_cel_add.text().strip()
        correo = self.ui.line_correo_add.text().strip()

        if not (nombre and apellido):
            self.statusBar.showMessage('Nombre y apellido son obligatorio', 5000)
            return

        try:
            paciente_existente = self.db.consultar_paciente(nombre, apellido)
            if paciente_existente:
                self.statusBar.showMessage('Producto ya existe', 5000)
            else:
                self.db.agregar_paciente(nombre, apellido, telefono, correo)
                self.statusBar.showMessage('Producto Registrado', 5000)

                self.ui.line_nombre_add.clear()
                self.ui.line_apellido_add.clear()
                self.ui.line_cel_add.clear()
                self.ui.line_correo_add.clear()

        except sqlite3.OperationalError as e:
            self.statusBar.showMessage('Error en la base de datos', 5000)
            self.statusBar.showMessage(f"Error SQLite: {e}", 5000)
        except Exception as e:
            self.statusBar.showMessage('Error inesperado', 5000)
            self.statusBar.showMessage(f"Error inesperado: {e}", 5000)

    def eliminar_paciente(self):
        nombre = self.ui.line_nombre_del.text().upper()
        apellido = self.ui.line_apellido_del.text().upper()
        if nombre.strip() and apellido.strip():
            try:
                self.db.elimina_paciente(nombre, apellido)
                self.statusBar.showMessage('Paciente Eliminado', 5000)
                self.ui.line_nombre_del.clear()
                self.ui.line_apellido_del.clear()
                self.mostrarPacientes(self.ui.tabla_del)
            except Exception as e:
                self.statusBar.showMessage(f"Error al eliminar: {str(e)}", 5000)
        else:
            self.statusBar.showMessage('Por favor, ingrese un nombre válido para eliminar.', 5000)

    def cargar_producto_seleccionado(self, row):
        nombre = self.ui.tabla_del.item(row, 0).text()
        apellido = self.ui.tabla_del.item(row, 1).text()
        self.ui.line_nombre_del.setText(nombre)
        self.ui.line_apellido_del.setText(apellido)

    def modificar_paciente(self):
        if self.paciente != '':
            nombre = self.ui.line_nombre_act.text().upper()
            apellido = self.ui.line_apellido_act.text().upper()
            telefono = self.ui.line_cant_act.text().upper()
            correo = self.ui.line_correo_act.text().upper()
            act = self.db.actualiza_paciente(self.Id, nombre, apellido, telefono, correo)
            if act == 1:
                self.statusBar.showMessage('paciente Actualizado', 5000)
                self.ui.line_nombre_mod.clear()
                self.ui.line_apellido_mod.clear()
                self.ui.line_cant_mod.clear()
                self.ui.line_correo_mod.clear()
                self.ui.line_desc_mod.clear()
                self.ui.line_nombre_mod.setText('')
                self.ui.line_apellido_mod.setText('')
            elif act == 0:
                self.statusBar.showMessage('Error', 5000)
            else:
                self.statusBar.showMessage('paciente no encontrado', 5000)