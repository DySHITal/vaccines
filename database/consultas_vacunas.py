import sqlite3

class Comms():
    def __init__(self):
        self.con = sqlite3.connect('control_vacunas.db')
    
    def agregar_vacuna(self, paciente_id, vacuna_id, fecha_aplicacion):
        cursor = self.con.cursor()
        query = '''INSERT INTO pacientesvacunas (paciente_id, vacuna_id, fecha_aplicacion) VALUES ('{}', '{}', '{}')'''.format(paciente_id, vacuna_id, fecha_aplicacion)
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

    def obtener_vacuna_id(self, nombre_vacuna):
        cursor = self.con.cursor()
        query = "SELECT id FROM Vacunas WHERE nombre = ?"
        cursor.execute(query, (nombre_vacuna,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0] if resultado else None
