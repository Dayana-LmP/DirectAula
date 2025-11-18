# dal.py

import sqlite3
#import os #-Necesario para eliminar la BD si se quiere reiniciar 

# Asegúrate de que esta importación esté presente
from model import Alumno, Asistencia 

class BaseDAO:
    """Clase base para Data Access Objects. Implementa Herencia y maneja la conexión."""
    def __init__(self, db_name="directaula.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def _conectar(self):
        """Establece la conexión con la base de datos local (SQLite)."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            raise 

    def _desconectar(self):
        """Cierra la conexión."""
        if self.conn:
            self.conn.close()

    def ejecutar_query(self, query, params=()):
        """Ejecuta una consulta y maneja la conexión."""
        try:
            self._conectar()
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            # Aquí se atrapan errores de integridad (e.g., matrícula duplicada)
            print(f"Error al ejecutar consulta: {e}")
            return False
        finally:
            self._desconectar()


class AlumnoDAO(BaseDAO):
    """Maneja las operaciones CRUD para la entidad Alumno. Implementa Encapsulamiento."""

    def __init__(self):
        super().__init__() 
        
        # 💡 CAMBIO CRUCIAL: Añadir la columna 'email'
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS alumnos (
                matricula TEXT PRIMARY KEY,
                nombre_completo TEXT NOT NULL,
                datos_contacto TEXT,
                email TEXT,                     -- NUEVO CAMPO EMAIL
                grupo_id INTEGER NOT NULL
            );
        """)

    def crear_alumno(self, alumno: Alumno, grupo_id):
        """Implementación CREATE (C). Inserta un nuevo alumno."""
        # 💡 CAMBIO CRUCIAL: Añadir 'email' a la query y los parámetros
        query = "INSERT INTO alumnos (matricula, nombre_completo, datos_contacto, email, grupo_id) VALUES (?, ?, ?, ?, ?)"
        params = (
            alumno.get_matricula(), 
            alumno.get_nombre(), 
            alumno.get_datos_contacto(), 
            alumno.get_email(), # Nuevo dato
            grupo_id
        )
        return self.ejecutar_query(query, params)

    def obtener_alumnos_por_grupo(self, grupo_id):
        """Implementación READ (R). Recupera todos los alumnos de un grupo."""
        try:
            self._conectar()
            # SELECT * ahora retorna la columna email
            self.cursor.execute("SELECT * FROM alumnos WHERE grupo_id = ?", (grupo_id,))
            return self.cursor.fetchall()
        except Exception:
            return []
        finally:
            self._desconectar()
    
    def actualizar_alumno(self, alumno: Alumno):
        """Implementación UPDATE (U). Actualiza los datos de un alumno existente."""
        query = """
            UPDATE alumnos SET 
                nombre_completo = ?, 
                datos_contacto = ?, 
                email = ?                       -- ACTUALIZAR EMAIL
            WHERE matricula = ?
        """
        # 💡 CAMBIO CRUCIAL: Orden de parámetros (nombre, contacto, email, matricula)
        params = (
            alumno.get_nombre(), 
            alumno.get_datos_contacto(), 
            alumno.get_email(), # Nuevo dato
            alumno.get_matricula()
        )
        return self.ejecutar_query(query, params)
    
    def eliminar_alumno(self, matricula):
        """Implementación DELETE (D). Elimina un alumno por su matrícula (BR.6)."""
        query = "DELETE FROM alumnos WHERE matricula = ?"
        return self.ejecutar_query(query, (matricula,))
    pass

class AsistenciaDAO(BaseDAO):
    """Maneja las operaciones CRUD para el registro de Asistencia (CU4)."""

    def __init__(self):
        super().__init__()
        # Crear la tabla de asistencia
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS asistencia (
                matricula TEXT NOT NULL,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                PRIMARY KEY (matricula, fecha),
                FOREIGN KEY (matricula) REFERENCES alumnos(matricula)
            );
        """)

    def registrar_asistencia(self, asistencia: Asistencia):
        """Registra o actualiza el estado de asistencia para un alumno en una fecha (Upsert)."""
        query = "REPLACE INTO asistencia (matricula, fecha, estado) VALUES (?, ?, ?)"
        params = (asistencia.get_matricula(), asistencia.get_fecha(), asistencia.get_estado())
        return self.ejecutar_query(query, params)
    
    def obtener_asistencia_del_dia(self, fecha, grupo_id):
        """Obtiene el estado de asistencia de todos los alumnos de un grupo para una fecha."""
        # Query que junta Alumnos y Asistencia para mostrar el estado
        query = """
            SELECT 
                A.matricula, A.nombre_completo, COALESCE(S.estado, 'Ausente') 
            FROM alumnos A
            LEFT JOIN asistencia S 
            ON A.matricula = S.matricula AND S.fecha = ?
            WHERE A.grupo_id = ?
            ORDER BY A.nombre_completo;
        """
        try:
            self._conectar()
            self.cursor.execute(query, (fecha, grupo_id))
            return self.cursor.fetchall()
        except Exception:
            return []
        finally:
            self._desconectar()