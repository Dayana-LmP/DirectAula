
from datetime import date
import sqlite3
# Asegúrate que las tres entidades del modelo estén importadas
from model import Alumno, Asistencia, Calificacion, CategoriaEvaluacion, Grupo

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

        # Creación de la tabla PONDERACIONES (CU3)
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS categorias_evaluacion (
                grupo_id INTEGER NOT NULL,
                nombre_categoria TEXT NOT NULL,
                peso_porcentual REAL NOT NULL,
                max_items INTEGER NOT NULL DEFAULT 1, -- Total de Tareas a considerar para categorías múltiples
                PRIMARY KEY (grupo_id, nombre_categoria),
                FOREIGN KEY (grupo_id) REFERENCES grupos(grupo_id) ON DELETE CASCADE
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

        # Creación de la tabla CALIFICACIONES (CU5)
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS calificaciones (
                matricula TEXT NOT NULL,
                categoria TEXT NOT NULL,
                fecha TEXT NOT NULL,
                valor REAL NOT NULL,
                PRIMARY KEY (matricula, categoria, fecha),
                FOREIGN KEY (matricula) REFERENCES alumnos(matricula) ON DELETE CASCADE
            );
        """)
        
    def _conectar(self):
        self._con = sqlite3.connect(self._db_file)
        self._con.execute("PRAGMA foreign_keys = ON;") # Permite la integridad referencial
        self.cursor = self._con.cursor()
        return self._con

    def _desconectar(self, conn=None):
        connection = conn or self._con
        if connection:
            connection.close()
            if conn is None:
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
    def ejecutar_queries_multiples(self, query: str, params_list: list[tuple]):
        """Ejecuta una sola query varias veces con diferentes parámetros en una transacción."""
        try:
            self._conectar()
            self.cursor.executemany(query, params_list)
            self._con.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar múltiples queries: {e}")
            self._con.rollback()
            return False
        finally:
            self._desconectar()

# ====================================================
# 1. GRUPO DAO (CASO DE USO 1) 
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

    def registrar_asistencia(self, matricula, fecha=None, estado="Presente"):
        # Permite llamadas con solo la matrícula; usa la fecha de hoy si no se proporciona.
        # También acepta un objeto Asistencia y extrae sus atributos para no pasar
        # el objeto entero como parámetro a sqlite3 (causa: "type 'Asistencia' is not supported").
        if isinstance(matricula, Asistencia):
            asistencia_obj = matricula
            matricula = asistencia_obj.get_matricula()
            fecha = asistencia_obj.get_fecha() or date.today().isoformat()
            estado = asistencia_obj.get_estado() or "Presente"
        else:
            if fecha is None:
                fecha = date.today().isoformat()
        query = "REPLACE INTO asistencia (matricula, fecha, estado) VALUES (?, ?, ?)"
        params = (matricula, fecha, estado)
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

# ====================================================
# 4. CATEGORIAEVALUACION DAO (Ponderación flexible - CU3)
# ====================================================
class CategoriaEvaluacionDAO(BaseDAO):
    """Maneja las categorías de evaluación flexibles por Grupo."""
    
    # BR.3 (Ponderación inicial por defecto) ahora se maneja insertando múltiples registros
    def crear_ponderacion_inicial(self, grupo_id):
        # La ponderación inicial por defecto (si se desea mantener una base)
        categorias_base = [
            (grupo_id, "Asistencia", 10.0, 1),
            (grupo_id, "Examen Final", 40.0, 1),
            (grupo_id, "Participación", 10.0, 5), # Total 5 participaciones
            (grupo_id, "Tareas", 40.0, 10)      # Total 10 tareas
        ]
        query = "INSERT OR IGNORE INTO categorias_evaluacion (grupo_id, nombre_categoria, peso_porcentual, max_items) VALUES (?, ?, ?, ?)"
        
        for cat in categorias_base:
            self.ejecutar_query(query, cat)
        return True

    def obtener_categorias(self, grupo_id):
        query = "SELECT nombre_categoria, peso_porcentual, max_items FROM categorias_evaluacion WHERE grupo_id = ?"
        resultados = self.ejecutar_query(query, (grupo_id,))
        
        if not resultados:
            # Si no hay categorías, crear las iniciales y reintentar
            self.crear_ponderacion_inicial(grupo_id)
            return self.obtener_categorias(grupo_id)
            
        # Retornamos objetos del modelo
        lista_categorias = [
            CategoriaEvaluacion(grupo_id, nombre, peso, items) 
            for nombre, peso, items in resultados
        ]
        return lista_categorias 

    def guardar_categorias(self, categorias: list[CategoriaEvaluacion], grupo_id):
        # 1. Eliminar las categorías existentes para ese grupo
        self.ejecutar_query("DELETE FROM categorias_evaluacion WHERE grupo_id = ?", (grupo_id,))
        
        # 2. Insertar las nuevas categorías
        query = "INSERT INTO categorias_evaluacion (grupo_id, nombre_categoria, peso_porcentual, max_items) VALUES (?, ?, ?, ?)"
        
        params_list = [
            (cat.get_grupo_id(), cat.get_nombre_categoria(), cat.get_peso_porcentual(), cat.get_max_items())
            for cat in categorias
        ]
        return self.ejecutar_queries_multiples(query, params_list)

# ====================================================
# 5. CALIFICACION DAO (CASO DE USO 5)
# ====================================================
class CalificacionDAO(BaseDAO):
    """Maneja las operaciones CRUD para las Calificaciones de Alumnos."""

    def registrar_calificacion(self, calificacion: Calificacion):
        # Usamos REPLACE INTO para insertar o actualizar (FA.1: Modificar calificación existente)
        query = "REPLACE INTO calificaciones (matricula, categoria, fecha, valor) VALUES (?, ?, ?, ?)"
        params = (
            calificacion.get_matricula(), 
            calificacion.get_categoria(), 
            calificacion.get_fecha() or date.today().isoformat(), 
            calificacion.get_valor()
        )
        return self.ejecutar_query(query, params)
    
    def obtener_calificaciones_por_grupo_categoria(self, grupo_id, categoria):
        query = """
            SELECT 
                A.matricula, 
                A.nombre_completo, 
                C.valor
            FROM alumnos A
            LEFT JOIN calificaciones C 
            ON A.matricula = C.matricula AND C.categoria = ?
            WHERE A.grupo_id = ?
            ORDER BY A.nombre_completo;
        """
        return self.ejecutar_query(query, (categoria, grupo_id))
    
    def obtener_todas_calificaciones_por_grupo(self, grupo_id):
        query = """
            SELECT A.matricula, C.categoria, C.valor
            FROM alumnos A
            JOIN calificaciones C 
            ON A.matricula = C.matricula
            WHERE A.grupo_id = ?
        """
        return self.ejecutar_query(query, (grupo_id,))