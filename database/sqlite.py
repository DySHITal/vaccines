import sqlite3

class Database:
    def __init__(self):
        db_name = "control_vacunas.db"
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

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

        vacunas_iniciales = [
            "BCG", "HEPATITIS B", "NEUMOCOCO CONJUGADA", "QUINTUPLE O PENTAVALENTE", "IPV", 
            "ROTAVIRUS", "MENINGOCOCO ACYW", "ANTIGRIPAL", "HEPATITIS A", "TRIPLE VIRAL", 
            "VARICELA", "TRIPLE BACTERIANA CELULAR", "TRIPLE BACTERIANA ACELULAR", 
            "VIRUS PAPILOMA HUMANO", "DOBLE BACTERIANA", "VIRUS SINCICIAL RESPIRATORIO", 
            "FIEBRE AMARILLA", "FIEBRE HEMORRAGICA ARGENTINA"
        ]


        cursor.execute("SELECT COUNT(*) FROM Vacunas")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO Vacunas (nombre) VALUES (?)", [(v,) for v in vacunas_iniciales])
            print("Datos iniciales insertados en la tabla Vacunas.")

        conn.commit()
        conn.close()
