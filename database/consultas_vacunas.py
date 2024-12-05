import sqlite3

class Comms():
    def __init__(self):
        self.con = sqlite3.connect('control_vacunas.db')
    
    def agregar_vacuna(self, nombre):
        cursor = self.con.cursor()
        query = '''INSERT INTO pacientes (nombre) VALUES ('{}')'''.format(nombre)
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def obtener_vacunas_aplicadas(self, paciente_id):
        cursor = self.con.cursor()
        query = '''SELECT v.nombre, pv.fecha_aplicacion
                FROM PacientesVacunas pv
                JOIN Vacunas v ON pv.vacuna_id = v.id
                WHERE pv.paciente_id = ?'''
        cursor.execute(query, (paciente_id,))
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

