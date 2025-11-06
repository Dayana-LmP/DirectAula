# data_access/alumno_repository.py
from models.entities import Alumno
import sqlite3

class AlumnoRepository:
    def __init__(self, db):
        self.db = db
    
    def crear(self, alumno):
        """Implementa FA.1 - Agregar nuevo alumno"""
        if not alumno.es_valido():
            raise ValueError("BR.4 - Matrícula y Nombre son obligatorios")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # BR.4 - Verificar matrícula única en el grupo
            cursor.execute(
                "SELECT id FROM alumnos WHERE matricula = ? AND grupo_id = ?",
                (alumno.matricula, alumno.grupo_id)
            )
            if cursor.fetchone():
                raise ValueError("BR.4 - Matrícula ya existe en este grupo")
            
            cursor.execute('''
                INSERT INTO alumnos (matricula, nombre_completo, email, telefono, grupo_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (alumno.matricula, alumno.nombre_completo, 
                  alumno.email, alumno.telefono, alumno.grupo_id))
            
            alumno.id = cursor.lastrowid
            conn.commit()
            return alumno
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Error de base de datos: {str(e)}")
        finally:
            conn.close()
    
    def buscar_por_grupo(self, grupo_id, criterio=""):
        """Implementa Flujo Normal paso 4-5 - Búsqueda predictiva"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM alumnos WHERE grupo_id = ? AND estado = 'Activo'"
        params = [grupo_id]
        
        if criterio:
            query += " AND (nombre_completo LIKE ? OR matricula LIKE ?)"
            params.extend([f"%{criterio}%", f"%{criterio}%"])
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        
        # Convertir resultados a objetos Alumno
        alumnos = []
        for fila in resultados:
            alumno = Alumno(
                id=fila[0],
                matricula=fila[1],
                nombre_completo=fila[2],
                email=fila[3],
                telefono=fila[4],
                grupo_id=fila[5],
                estado=fila[6]
            )
            alumnos.append(alumno)
        
        return alumnos
    
    def actualizar(self, alumno):
        """Implementa FA.2 - Modificar datos de alumno"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE alumnos 
                SET matricula=?, nombre_completo=?, email=?, telefono=?
                WHERE id=?
            ''', (alumno.matricula, alumno.nombre_completo, 
                  alumno.email, alumno.telefono, alumno.id))
            
            conn.commit()
            return alumno
            
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Error al actualizar alumno: {str(e)}")
        finally:
            conn.close()
    
    def eliminar(self, alumno_id):
        """Implementa baja de alumno - BR.6 Eliminación permanente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM alumnos WHERE id=?', (alumno_id,))
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Error al eliminar alumno: {str(e)}")
        finally:
            conn.close()