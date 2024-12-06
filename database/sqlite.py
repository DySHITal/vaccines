import sqlite3

class Database:
    def __init__(self):
        # Conexión a la base de datos (se creará si no existe)
        db_name = "control_vacunas.db"
        conn = sqlite3.connect(db_name)

        # Crear un cursor para ejecutar comandos SQL
        cursor = conn.cursor()

        # Crear tablas
        cursor.execute("""CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            dni TEXT UNIQUE NOT NULL
        )
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS Vacunas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS PacientesVacunas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            vacuna_id INTEGER NOT NULL,
            fecha_aplicacion DATE NOT NULL,
            fecha_proxima DATE NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes (id) ON DELETE CASCADE,
            FOREIGN KEY (vacuna_id) REFERENCES Vacunas (id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        conn.close()
