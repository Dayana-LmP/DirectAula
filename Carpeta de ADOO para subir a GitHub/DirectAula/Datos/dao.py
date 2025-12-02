#Archivo que contiene las clases DAO para manejar los datos
#Aquí están las bases de datos y las operaciones CRUD para cada entidad.
#Una clase DAO (Data Access Object) se encarga de interactuar con la base de datos para una entidad específica.
from datetime import date
import sqlite3
from model import Alumno, Asistencia, Calificacion, CategoriaEvaluacion, Grupo 
#
#La clase BASE DAO maneja la conexión a la base de datos y las operaciones comunes.
class BaseDAO:
    def __init__(self): #Inicializa la conexión a la base de datos SQLite
        self._db_file = 'directaula.db' #Archivo de base de datos SQLite
        self._con = None #Conexión a la base de datos, dice none porque aún no está conectada
        self.inicializar_tablas() 
        
        #Aquí se asegura que las tablas necesarias existan al iniciar el DAO
    def inicializar_tablas(self):
        #Asegura que todas las tablas necesarias existan.
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS grupos ( 
                grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ciclo_escolar TEXT NOT NULL
            );
        """) # Tabla de grupos, el if not exists evita errores si la tabla ya existe
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS alumnos (
                matricula TEXT PRIMARY KEY,
                nombre_completo TEXT NOT NULL,
                datos_contacto TEXT,
                email TEXT,
                grupo_id INTEGER,
                FOREIGN KEY (grupo_id) REFERENCES grupos(grupo_id)
            );
        """) # Tabla de alumnos, con clave primaria matricula y clave foránea grupo_id
        #La diferencia entre text y varchar es que text no tiene límite de longitud en SQLite
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS categorias_evaluacion (
                grupo_id INTEGER NOT NULL,
                nombre_categoria TEXT NOT NULL,
                peso_porcentual REAL NOT NULL,
                max_items INTEGER NOT NULL DEFAULT 1, 
                PRIMARY KEY (grupo_id, nombre_categoria),
                FOREIGN KEY (grupo_id) REFERENCES grupos(grupo_id) ON DELETE CASCADE
            );
        """)
        #El self.ejecutar_query se usa para ejecutar comandos SQL que crean tablas 
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS asistencia (
                matricula TEXT NOT NULL,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                PRIMARY KEY (matricula, fecha),
                FOREIGN KEY (matricula) REFERENCES alumnos(matricula) ON DELETE CASCADE
            );
        """)
        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS calificaciones (
                matricula TEXT NOT NULL,
                categoria TEXT NOT NULL,
                fecha TEXT NOT NULL,
                valor REAL NOT NULL,
                PRIMARY KEY (matricula, categoria, fecha),
                FOREIGN KEY (matricula) REFERENCES alumnos(matricula) ON DELETE CASCADE
            );
        """) #El text not null es para asegurar que esos campos siempre tengan un valor

        self.ejecutar_query("""
            CREATE TABLE IF NOT EXISTS profesores (
    profesor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL, -- El usuario debe ser único
    password TEXT NOT NULL,
    email TEXT
            );
        """)
        
        #Métodos para conectar y desconectar de la base de datos
        #Crea una nueva conexión cada vez que se necesita ejecutar una consulta.
    def _conectar(self):
        self._con = sqlite3.connect(self._db_file)
        self._con.execute("PRAGMA foreign_keys = ON;") #Clave foránea activada
        self.cursor = self._con.cursor() 
        return self._con

#Se cierra la conexión después de que se realizo la operación
    def _desconectar(self, conn=None):
        connection = conn or self._con
        if connection:
            connection.close()
            if conn is None:
                self._con = None

#Método para ejecutar consultas SQL
#Polimorfismo: Este método puede ser sobrescrito en subclases si se necesita un comportamiento diferente.
    def ejecutar_query(self, query, params=()):
        try:
            conn = self._conectar()
            self.cursor.execute(query, params)
            conn.commit()
            if query.strip().upper().startswith(("SELECT", "PRAGMA")):
                return self.cursor.fetchall()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}") 
            return False
        finally:
            self._desconectar(conn)
    
    #Método para ejecutar múltiples consultas SQL
    def ejecutar_queries_multiples(self, query: str, params_list: list[tuple]):
        try:
            conn = self._conectar()
            self.cursor.executemany(query, params_list) #Ejecuta múltiples queries con diferentes parámetros
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar múltiples queries: {e}")
            conn.rollback() #Revierte los cambios en caso de error
            return False
        finally:
            self._desconectar(conn) #Desconecta la base de datos
        

# 1. GRUPO DAO 
#Esta clase maneja las operaciones CRUD para la entidad Grupo.
#Hereda de BaseDAO para reutilizar la conexión y métodos comunes.
#CRUD: crear, leer, actualizar, eliminar
class GrupoDAO(BaseDAO):

    def crear_grupo(self, grupo: Grupo):
        query = "INSERT INTO grupos (nombre, ciclo_escolar) VALUES (?, ?)" #Inserta un nuevo grupo
        params = (grupo.get_nombre(), grupo.get_ciclo())
        return self.ejecutar_query(query, params)

    def obtener_grupos(self): #Obtiene todos los grupos
        query = "SELECT grupo_id, nombre, ciclo_escolar FROM grupos ORDER BY ciclo_escolar, nombre"
        return self.ejecutar_query(query)

    def buscar_grupo_por_nombre_ciclo(self, nombre, ciclo_escolar): #Busca un grupo por nombre y ciclo escolar
        query = "SELECT grupo_id FROM grupos WHERE nombre = ? AND ciclo_escolar = ?"
        resultado = self.ejecutar_query(query, (nombre, ciclo_escolar))
        return resultado[0][0] if resultado else None

    def actualizar_grupo(self, grupo: Grupo): #Actualiza los datos de un grupo existente
        query = "UPDATE grupos SET nombre = ?, ciclo_escolar = ? WHERE grupo_id = ?"
        params = (grupo.get_nombre(), grupo.get_ciclo(), grupo.get_id())
        return self.ejecutar_query(query, params)

    def eliminar_grupo(self, grupo_id): #Elimina un grupo por su ID
        query = "DELETE FROM grupos WHERE grupo_id = ?"
        return self.ejecutar_query(query, (grupo_id,))


# 2. ALUMNO DAO (CASO DE USO 2)
#Esta clase maneja las operaciones CRUD para la entidad Alumno.
#Hereda de BaseDAO para reutilizar la conexión y métodos comunes.
class AlumnoDAO(BaseDAO):
    
    def crear_alumno(self, alumno: Alumno, grupo_id): #Crea un nuevo alumno asociado a un grupo
        query = "INSERT INTO alumnos (matricula, nombre_completo, datos_contacto, email, grupo_id) VALUES (?, ?, ?, ?, ?)"
        params = (alumno.get_matricula(), alumno.get_nombre_completo(), alumno.get_datos_contacto(), alumno.get_email(), grupo_id)
        return self.ejecutar_query(query, params)

    def obtener_alumnos_por_grupo(self, grupo_id): #Obtiene todos los alumnos de un grupo específico
        query = "SELECT matricula, nombre_completo, datos_contacto, email FROM alumnos WHERE grupo_id = ? ORDER BY nombre_completo"
        return self.ejecutar_query(query, (grupo_id,))

    def actualizar_alumno(self, alumno: Alumno): #Actualiza los datos de un alumno existente
        query = "UPDATE alumnos SET nombre_completo = ?, datos_contacto = ?, email = ? WHERE matricula = ?"
        params = (alumno.get_nombre_completo(), alumno.get_datos_contacto(), alumno.get_email(), alumno.get_matricula())
        return self.ejecutar_query(query, params)

    def eliminar_alumno(self, matricula): #Elimina un alumno por su matrícula
        query = "DELETE FROM alumnos WHERE matricula = ?"
        return self.ejecutar_query(query, (matricula,))

# 3. ASISTENCIA DAO (CASO DE USO 4)
#Esta clase maneja las operaciones CRUD para la entidad Asistencia.
class AsistenciaDAO(BaseDAO):

    def registrar_asistencia(self, asistencia_obj: Asistencia): #Registra o actualiza la asistencia de un alumno en una fecha específica
        fecha = asistencia_obj.get_fecha() or date.today().isoformat()
        estado = asistencia_obj.get_estado() or "Presente"
        query = "REPLACE INTO asistencia (matricula, fecha, estado) VALUES (?, ?, ?)"
        params = (asistencia_obj.get_matricula(), fecha, estado) #Parámetros para la consulta
        return self.ejecutar_query(query, params)
        
    def obtener_asistencia_del_dia(self, fecha, grupo_id): #Obtiene la asistencia de todos los alumnos de un grupo en una fecha específica
        #Query que une alumnos con su asistencia del día y muestra 'Ausente' si no hay registro
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
        return self.ejecutar_query(query, (fecha, grupo_id))

    def obtener_porcentaje_asistencia_por_alumno(self, matricula: str) -> float: #Calcula el porcentaje de asistencia (Asistencia + Justificado) / Total de días registrados
       #La flecha indica que el método retorna un valor float
        """
        MÉTODO AGREGADO para CU6. 
        Calcula el porcentaje de asistencia (Asistencia + Justificado) / Total de días registrados.
        """
        query = """
        SELECT 
            CAST(SUM(CASE WHEN estado IN ('Asistencia', 'Justificado') THEN 1 ELSE 0 END) AS REAL) AS asistencias_contables,
            COUNT(fecha) AS total_dias_registrados
        FROM asistencia
        WHERE matricula = ?;
        """
        resultado = self.ejecutar_query(query, (matricula,))
        #Si hay resultados, calcula el porcentaje
        if resultado and resultado[0]:
            asistencias, total_dias = resultado[0]
            if total_dias > 0:
                porcentaje = (asistencias / total_dias) * 100
                return round(porcentaje, 2) #Redondea a 2 decimales
        #Si no hay registros, retorna 100%
        return 100.0

# 4. CATEGORIAEVALUACION DAO (Ponderación CU3)
#Esta clase maneja las operaciones CRUD para la entidad CategoriaEvaluacion.
class CategoriaEvaluacionDAO(BaseDAO):
#Método para crear ponderaciones iniciales si no existen
    def crear_ponderacion_inicial(self, grupo_id: int) -> bool:
        try:
            conn = self._conectar()
            query_check = "SELECT COUNT(*) FROM categorias_evaluacion WHERE grupo_id = ?"
            self.cursor.execute(query_check, (grupo_id,))
            count = self.cursor.fetchone()[0] #Cuenta cuántas categorías existen para ese grupo
             #Si no hay categorías, inserta las predeterminadas

#Predeterminadas
            if count == 0:
                default_categories = [
                    (grupo_id, 'Examen Final', 50.0, 1),
                    (grupo_id, 'Tareas', 30.0, 1),
                    (grupo_id, 'Participación', 20.0, 1),
                ]
                query_insert = """
                INSERT INTO categorias_evaluacion (grupo_id, nombre_categoria, peso_porcentual, max_items) 
                VALUES (?, ?, ?, ?)
                """
                self.cursor.executemany(query_insert, default_categories) #Inserta múltiples categorías a la vez
                conn.commit() #Confirma los cambios
            return True
        except sqlite3.Error as e: #Maneja errores de la base de datos
            print(f"Error al crear ponderaciones iniciales: {e}")
            conn.rollback() #Revierte los cambios en caso de error, lo que significa que no se guardan los cambios realizados antes del error
            return False
        finally:
            self._desconectar(conn)
            
            #Método para obtener categorías de evaluación por grupo
    def obtener_categorias_por_grupo(self, grupo_id):
        query = """
        SELECT grupo_id, nombre_categoria, peso_porcentual, max_items
        FROM categorias_evaluacion 
        WHERE grupo_id = ?
        ORDER BY nombre_categoria
        """
        resultados = self.ejecutar_query(query, (grupo_id,))
        categorias = [
            CategoriaEvaluacion(r[0], r[1], r[2], r[3]) for r in resultados #La r[] es cada fila del resultado
        ]
        return categorias

#Método para guardar ponderaciones (categorías) para un grupo
    def guardar_ponderaciones(self, categorias: list[CategoriaEvaluacion], grupo_id: int):
        try:
            conn = self._conectar()
            
            #1. Eliminar las categorías existentes para ese grupo, se eliminan primero para evitar duplicados
            self.cursor.execute("DELETE FROM categorias_evaluacion WHERE grupo_id = ?", (grupo_id,))
            
            #2. Insertar las nuevas categorías
            if categorias:
                query = """
                INSERT INTO categorias_evaluacion (grupo_id, nombre_categoria, peso_porcentual, max_items) 
                VALUES (?, ?, ?, ?)
                """
                #Convertir lista de objetos a lista de tuplas
                params_list = []
                for c in categorias:
                    #Asumimos que CategoriaEvaluacion tiene los métodos get_x() correctos.
                    params_list.append((
                        grupo_id, 
                        c.get_nombre_categoria(), 
                        c.get_peso_porcentual(), 
                        c.get_max_items()
                    ))
                    
                self.cursor.executemany(query, params_list) #Inserta múltiples categorías a la vez
            
            conn.commit() #Confirma los cambios
            return True
        except sqlite3.Error as e:
            print(f"Error al guardar ponderaciones: {e}")
            conn.rollback()
            return False
        finally:
            self._desconectar(conn)   

# 5. CALIFICACION DAO (CASO DE USO 5)
#Clase que maneja las operaciones CRUD para la entidad Calificacion.
class CalificacionDAO(BaseDAO):
#Método para registrar o actualizar una calificación
    def registrar_calificacion(self, calificacion: Calificacion):
        #Calificacion tiene un método to_tuple() que retorna (matricula, categoria, fecha, valor)
        query = """
        REPLACE INTO calificaciones (matricula, categoria, fecha, valor) 
        VALUES (?, ?, ?, ?)
        """
        params = (calificacion.get_matricula(), calificacion.get_categoria(), calificacion.get_fecha() or date.today().isoformat(), calificacion.get_valor())
        return self.ejecutar_query(query, params)
#Método para obtener calificaciones por categoría en un grupo
    def obtener_calificaciones_por_categoria(self, grupo_id, categoria):
        query = """
        SELECT 
            A.matricula,
            A.nombre_completo,
            ROUND(AVG(T1.valor), 2) AS promedio_categoria 
        FROM alumnos A
        LEFT JOIN calificaciones T1 
        ON A.matricula = T1.matricula AND T1.categoria = ?
        WHERE A.grupo_id = ?
        GROUP BY A.matricula, A.nombre_completo --  Esto asegura una sola fila por alumno.
        ORDER BY A.nombre_completo;
        """
        # Ya no retornará múltiples filas, sino un promedio por alumno.
        return self.ejecutar_query(query, (categoria, grupo_id))

    #Método para obtener todas las calificaciones de un alumno por categoría para calcular promedios
    def obtener_calificaciones_por_alumno_y_categoria(self, matricula: str):
        query = """
        SELECT categoria, valor, fecha
        FROM calificaciones 
        WHERE matricula = ?
        ORDER BY categoria, fecha DESC;
        """
        return self.ejecutar_query(query, (matricula,))

# 6. PROFESOR DAO (Autenticación)
#Clase que maneja las operaciones CRUD para la entidad Profesor.
class ProfesorDAO(BaseDAO):
#Método para crear un nuevo profesor
    def crear_profesor(self, nombre, usuario, password, email=""):
        query = "INSERT INTO profesores (nombre_completo, usuario, password, email) VALUES (?, ?, ?, ?)"
        params = (nombre, usuario, password, email)
        #ejecutar_query simpre retorna True o False para operaciones de inserción/actualización
        return self.ejecutar_query(query, params)
  #Método para buscar un profesor por su nombre de usuario  
    def buscar_profesor_por_usuario(self, usuario):
        #Busca un profesor por su nombre de usuario.
        query = "SELECT profesor_id, nombre_completo, password, email FROM profesores WHERE usuario = ?"
        resultado = self.ejecutar_query(query, (usuario,))
        #ejecutar_query retorna una lista de tuplas (fetchall),
        return resultado[0] if resultado else None