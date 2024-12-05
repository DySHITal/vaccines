import sqlite3

class Comunicacion():
    def __init__(self):
        self.con = sqlite3.connect('control_vacunas.db')
    
    def agregar_paciente(self, nombre, apellido, telefono, correo):
        cursor = self.con.cursor()
        query = '''INSERT INTO pacientes (nombre, apellido, telefono, correo) VALUES ('{}', '{}', '{}', '{}')'''.format(nombre, apellido, telefono, correo)
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def mostrar_pacientes(self):
        cursor = self.con.cursor()
        query = 'SELECT * FROM pacientes'
        cursor.execute(query)
        pacientes = cursor.fetchall()
        cursor.close()
        return pacientes
    
    def busca_paciente(self, nombre=None, apellido=None):
        try:
            cursor = self.con.cursor()
            if nombre and apellido:
                query = "SELECT * FROM pacientes WHERE nombre = ? AND apellido = ?"
                cursor.execute(query, (nombre, apellido))
            elif nombre:
                query = "SELECT * FROM pacientes WHERE nombre = ?"
                cursor.execute(query, (nombre,))
            elif apellido:
                query = "SELECT * FROM pacientes WHERE apellido = ?"
                cursor.execute(query, (apellido,))
            else:
                return None

            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except sqlite3.OperationalError as e:
            print(f"Error en la consulta SQL: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None



    
    def elimina_paciente(self, nombre, apellido):
        cursor = self.con.cursor()
        try:
            query = 'DELETE FROM pacientes WHERE nombre = ? and apellido = ?'
            cursor.execute(query, (nombre, apellido))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar el producto: {e}")
            raise e
        finally:
            cursor.close()


    def actualiza_paciente(self, Id, nombre, apellido, telefono, correo):
        cursor = self.con.cursor()
        query = '''UPDATE pacientes SET nombre = '{}', apellido = '{}', correo = '{}', telefono = '{}' WHERE ID = '{}' '''.format(nombre, apellido, telefono, correo, Id)
        cursor.execute(query)
        a = cursor.rowcount
        self.con.commit()
        cursor.close()
        return a
    
    def consultar_paciente(self, nombre, apellido):
        cursor = self.con.cursor()
        query = f"SELECT * FROM pacientes WHERE nombre = '{nombre}' AND apellido = '{apellido}'"
        result = cursor.execute(query).fetchall()
        cursor.close()
        return result 