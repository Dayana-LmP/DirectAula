# data_access/database.py
import sqlite3

class Database:
    def __init__(self, db_path="directaula.db"):
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de grupos (PRE-2 del UC-2)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grupos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                ciclo_escolar TEXT NOT NULL
            )
        ''')
        
        # Tabla de alumnos (core del UC-2)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                grupo_id INTEGER,
                estado TEXT DEFAULT 'Activo',
                FOREIGN KEY (grupo_id) REFERENCES grupos (id),
                UNIQUE(matricula, grupo_id)
            )
        ''')
        
        # Insertar un grupo de prueba si no existe
        cursor.execute('''
            INSERT OR IGNORE INTO grupos (id, nombre, ciclo_escolar) 
            VALUES (1, 'Grupo de Prueba', '2025-A')
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)