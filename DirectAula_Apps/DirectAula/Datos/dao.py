# datos/dao.py (CONTENIDO COMPLETO Y CORREGIDO)

import sqlite3
# Asegúrate que las tres entidades del modelo estén importadas
from model import Alumno, Asistencia, Grupo 

# ====================================================
# BASE DAO (Manejo de Conexión y Creación de Tablas)
# ====================================================
class BaseDAO:
    def __init__(self):
        self._db_file = 'directaula.db'
        self._con = None
        self.inicializar_tablas() # Llama a la función para crear o verificar tablas
        
    def inicializar_tablas(self):
        """Asegura que todas las tablas necesarias existan (Grupos, Alumnos, Asistencia)."""
        # Creación de la tabla GRUPOS (CU1)
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS grupos (
                grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ciclo_escolar TEXT NOT NULL
            );
        """)
        # Creación de la tabla ALUMNOS (CU2)
        # 💡 La columna 'email' debe estar aquí para evitar errores.
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS alumnos (
                matricula TEXT PRIMARY KEY,
                nombre_completo TEXT NOT NULL,
                datos_contacto TEXT,
                email TEXT,
                grupo_id INTEGER,
                FOREIGN KEY (grupo_id) REFERENCES grupos(grupo_id)
            );
        """)
        # Creación de la tabla ASISTENCIA (CU4)
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS asistencia (
                matricula TEXT NOT NULL,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                PRIMARY KEY (matricula, fecha),
                FOREIGN KEY (matricula) REFERENCES alumnos(matricula)
            );
        """)
        
    def _conectar(self):
        self._con = sqlite3.connect(self._db_file)
        self._con.execute("PRAGMA foreign_keys = ON;") # Permite la integridad referencial
        self.cursor = self._con.cursor()

    def _desconectar(self):
        if self._con:
            self._con.close()
            self._con = None

    def ejecutar_query(self, query, params=()):
        try:
            self._conectar()
            self.cursor.execute(query, params)
            self._con.commit()
            if query.strip().upper().startswith(("SELECT", "PRAGMA")):
                return self.cursor.fetchall()
            return True
        except sqlite3.Error as e:
            # 💡 Esto es útil para el debugging de errores SQL.
            print(f"Error al ejecutar consulta: {e}") 
            return False
        finally:
            self._desconectar()

# ====================================================
# 1. GRUPO DAO (CASO DE USO 1) ⬅️ ESTA ERA LA CLASE QUE FALTABA
# ====================================================
class GrupoDAO(BaseDAO):
    """Maneja las operaciones CRUD para la entidad Grupo."""

    def crear_grupo(self, grupo: Grupo):
        query = "INSERT INTO grupos (nombre, ciclo_escolar) VALUES (?, ?)"
        params = (grupo.get_nombre(), grupo.get_ciclo())
        return self.ejecutar_query(query, params)

    def obtener_grupos(self):
        query = "SELECT grupo_id, nombre, ciclo_escolar FROM grupos ORDER BY ciclo_escolar, nombre"
        return self.ejecutar_query(query)

    def buscar_grupo_por_nombre_ciclo(self, nombre, ciclo_escolar):
        query = "SELECT grupo_id FROM grupos WHERE nombre = ? AND ciclo_escolar = ?"
        resultado = self.ejecutar_query(query, (nombre, ciclo_escolar))
        return resultado[0][0] if resultado else None

    def actualizar_grupo(self, grupo: Grupo):
        query = "UPDATE grupos SET nombre = ?, ciclo_escolar = ? WHERE grupo_id = ?"
        params = (grupo.get_nombre(), grupo.get_ciclo(), grupo.get_id())
        return self.ejecutar_query(query, params)

    def eliminar_grupo(self, grupo_id):
        query = "DELETE FROM grupos WHERE grupo_id = ?"
        return self.ejecutar_query(query, (grupo_id,))


# ====================================================
# 2. ALUMNO DAO (CASO DE USO 2)
# ====================================================
class AlumnoDAO(BaseDAO):
    """Maneja las operaciones CRUD para la entidad Alumno."""

    def crear_alumno(self, alumno: Alumno, grupo_id):
        query = "INSERT INTO alumnos (matricula, nombre_completo, datos_contacto, email, grupo_id) VALUES (?, ?, ?, ?, ?)"
        params = (alumno.get_matricula(), alumno.get_nombre_completo(), alumno.get_datos_contacto(), alumno.get_email(), grupo_id)
        return self.ejecutar_query(query, params)

    def obtener_alumnos_por_grupo(self, grupo_id):
        query = "SELECT matricula, nombre_completo, datos_contacto, email FROM alumnos WHERE grupo_id = ? ORDER BY nombre_completo"
        return self.ejecutar_query(query, (grupo_id,))

    def actualizar_alumno(self, alumno: Alumno):
        query = "UPDATE alumnos SET nombre_completo = ?, datos_contacto = ?, email = ? WHERE matricula = ?"
        params = (alumno.get_nombre_completo(), alumno.get_datos_contacto(), alumno.get_email(), alumno.get_matricula())
        return self.ejecutar_query(query, params)

    def eliminar_alumno(self, matricula):
        query = "DELETE FROM alumnos WHERE matricula = ?"
        return self.ejecutar_query(query, (matricula,))


# ====================================================
# 3. ASISTENCIA DAO (CASO DE USO 4)
# ====================================================
class AsistenciaDAO(BaseDAO):
    """Maneja las operaciones CRUD para el registro de Asistencia."""

    def registrar_asistencia(self, asistencia: Asistencia):
        query = "REPLACE INTO asistencia (matricula, fecha, estado) VALUES (?, ?, ?)"
        params = (asistencia.get_matricula(), asistencia.get_fecha(), asistencia.get_estado())
        return self.ejecutar_query(query, params)
    
    def obtener_asistencia_del_dia(self, fecha, grupo_id):
        """
        Retorna la lista de todos los alumnos de un grupo junto con su estado de
        asistencia para una fecha dada.
        """
        # 💡 CONSULTA CORREGIDA: Usa LEFT JOIN para incluir a todos los alumnos.
        # COALESCE convierte NULL (si no hay registro de asistencia) en 'Ausente'.
        query = """
            SELECT 
                A.matricula, 
                A.nombre_completo, 
                COALESCE(S.estado, 'Ausente') 
            FROM alumnos A
            LEFT JOIN asistencia S 
            ON A.matricula = S.matricula AND S.fecha = ?
            WHERE A.grupo_id = ?
            ORDER BY A.nombre_completo;
        """
        try:
            self._conectar()
            # 💡 PARÁMETROS: (fecha, grupo_id)
            self.cursor.execute(query, (fecha, grupo_id)) 
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener asistencia: {e}")
            # Si hay un error SQL, devuelve una lista vacía para evitar un crash.
            return []
        finally:
            self._desconectar()