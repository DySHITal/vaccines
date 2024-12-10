import sqlite3

class Comms():
    def __init__(self):
        self.con = sqlite3.connect('control_vacunas.db')
    
    def agregar_vacuna(self, paciente_id, vacuna_id, fecha_aplicacion, fecha_recordatorio):
        cursor = self.con.cursor()
        query = '''SELECT COUNT(*) from pacientesvacunas WHERE paciente_id = ? AND vacuna_id = ?'''
        cursor.execute(query, (paciente_id, vacuna_id))
        existe = cursor.fetchone()[0]
        if existe:
            update_query = '''UPDATE pacientesvacunas SET fecha_aplicacion = ?, fecha_proxima = ? WHERE paciente_id = ? AND vacuna_id = ?'''
            cursor.execute(update_query, (fecha_aplicacion, fecha_recordatorio, paciente_id, vacuna_id))
        else:
            insert_query = '''INSERT INTO pacientesvacunas (paciente_id, vacuna_id, fecha_aplicacion, fecha_proxima) VALUES (?, ?, ?, ?)'''
            cursor.execute(insert_query, (paciente_id, vacuna_id, fecha_aplicacion, fecha_recordatorio))
        self.con.commit()
        cursor.close()

    def obtener_vacunas_aplicadas(self, paciente_id):
        cursor = self.con.cursor()
        query = '''SELECT v.nombre, pv.fecha_aplicacion, pv.fecha_proxima
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
