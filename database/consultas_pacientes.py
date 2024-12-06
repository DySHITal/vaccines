import sqlite3

class Comunicacion():
    def __init__(self):
        self.con = sqlite3.connect('control_vacunas.db')

    def get_paciente_id(self, nombre, apellido):
        cursor = self.con.cursor()
        query = "SELECT id FROM pacientes WHERE nombre = ? AND apellido = ?"
        cursor.execute(query, (nombre, apellido))
        paciente_id = cursor.fetchone()
        cursor.close()
        return paciente_id[0] if paciente_id else None
    
    def agregar_paciente(self, nombre, apellido, telefono, correo, dni):
        cursor = self.con.cursor()
        query = '''INSERT INTO pacientes (nombre, apellido, telefono, correo, dni) VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(nombre, apellido, telefono, correo, dni)
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
    
    def busca_paciente(self, nombre=None, apellido=None, dni=None):
        try:
            cursor = self.con.cursor()
            if nombre and apellido and dni:
                query = "SELECT * FROM pacientes WHERE nombre = ? AND apellido = ? AND dni = ?"
                cursor.execute(query, (nombre, apellido, dni))
            elif nombre:
                query = "SELECT * FROM pacientes WHERE nombre = ?"
                cursor.execute(query, (nombre,))
            elif apellido:
                query = "SELECT * FROM pacientes WHERE apellido = ?"
                cursor.execute(query, (apellido,))
            elif dni:
                query = "SELECT * FROM pacientes WHERE dni = ?"
                cursor.execute(query, (dni,))
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



    
    def elimina_paciente(self, dni):
        cursor = self.con.cursor()
        try:
            query = 'DELETE FROM pacientes WHERE dni = ?'
            cursor.execute(query, (dni,))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar el paciente: {e}")
            raise e
        finally:
            cursor.close()


    def actualiza_paciente(self, Id, nombre, apellido, telefono, correo, dni):
        cursor = self.con.cursor()
        query = '''UPDATE pacientes SET nombre = '{}', apellido = '{}', correo = '{}', telefono = '{}', dni = '{}' WHERE ID = '{}' '''.format(nombre, apellido, telefono, correo, dni, Id)
        cursor.execute(query)
        a = cursor.rowcount
        self.con.commit()
        cursor.close()
        return a
    
    def consultar_paciente(self, dni):
        cursor = self.con.cursor()
        query = f"SELECT * FROM pacientes WHERE nombre = '{dni}'"
        result = cursor.execute(query).fetchall()
        cursor.close()
        return result 