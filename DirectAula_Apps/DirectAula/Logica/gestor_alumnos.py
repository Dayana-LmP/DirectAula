# bll.py

from Datos.dao import AlumnoDAO, AsistenciaDAO
from model import Alumno, Asistencia, Asistencia 
from datetime import date, datetime

class GestorAlumnos:
    """Gestiona el flujo y aplica las reglas de negocio."""

    def __init__(self, grupo_actual_id):
        self._alumno_dao = AlumnoDAO() 
        self._grupo_actual_id = grupo_actual_id

    def _existe_matricula_en_grupo(self, matricula):
        """Verifica si la matrícula existe en el grupo (FE.2)."""
        alumnos_grupo = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        return any(a[0] == matricula for a in alumnos_grupo)

    def agregar_nuevo_alumno(self, matricula, nombre, contacto, email): # 💡 CAMBIO: Añadir email
        """Implementa la lógica del FA.1: Agregar nuevo alumno."""
        
        if not matricula or not nombre:
            return "Error: Matrícula y Nombre son obligatorios (BR.4 - FE.1)."
        
        if self._existe_matricula_en_grupo(matricula):
            return f"Error: La matrícula {matricula} ya existe en este grupo (FE.2)."

        # 💡 CAMBIO: Crear objeto Alumno con email
        nuevo_alumno = Alumno(matricula, nombre, contacto, email) 

        if self._alumno_dao.crear_alumno(nuevo_alumno, self._grupo_actual_id):
            return "Éxito: Alumno registrado correctamente."
        else:
            return "Error: No se pudo guardar en la base de datos."

    def obtener_lista_alumnos(self):
        """Retorna la lista de alumnos del grupo (R)."""
        return self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
    
    def actualizar_datos_alumno(self, matricula, nombre, contacto, email): # 💡 CAMBIO: Añadir email
        """Implementa la lógica del FA.2: Modificar datos de un alumno."""
        
        if not matricula or not nombre:
            return "Error: Nombre es obligatorio para la actualización (BR.4 - FE.1)."
        
        # 💡 CAMBIO: Crear objeto Alumno con email
        alumno_a_actualizar = Alumno(matricula, nombre, contacto, email)
        
        if self._alumno_dao.actualizar_alumno(alumno_a_actualizar):
            return "Éxito: Datos del alumno actualizados correctamente."
        else:
            return "Error: No se pudo actualizar el alumno."

    # 💡 NUEVA FUNCIONALIDAD: Eliminar Alumno
    def eliminar_alumno(self, matricula):
        """Implementa la lógica para eliminar un alumno (BR.6)."""
        # NOTA: Aquí iría la validación BR.2 (Un grupo no puede ser eliminado si tiene alumnos...),
        # pero para el UC-2, solo validamos que exista y procedemos.

        if self._alumno_dao.eliminar_alumno(matricula):
            return "Éxito: Alumno eliminado permanentemente (BR.6)."
        else:
            return "Error: No se pudo eliminar el alumno."
    pass

class GestorAsistencia:
    """Gestiona el flujo de registro de asistencia."""

    def __init__(self, grupo_actual_id):
        self._asistencia_dao = AsistenciaDAO()
        self._alumno_dao = AlumnoDAO() 
        self._grupo_actual_id = grupo_actual_id

    def registrar_asistencia_masiva(self, fecha=date.today().strftime("%Y-%m-%d")):
        """Implementa la lógica de 'poner asistencia a todos'."""
        alumnos_data = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        matriculas = [a[0] for a in alumnos_data] 
        registros_exitosos = 0
        
        for matricula in matriculas:
            asistencia = Asistencia(matricula, fecha, "Presente") 
            if self._asistencia_dao.registrar_asistencia(asistencia):
                registros_exitosos += 1
                
        if len(matriculas) == 0:
            return "Advertencia: No hay alumnos en este grupo."
        elif registros_exitosos > 0:
            return "Éxito: Asistencia masiva registrada como 'Presente'."
        else:
            return "Error: No se pudo registrar la asistencia."

    def actualizar_estado_asistencia(self, matricula, fecha, nuevo_estado):
        """Actualiza el estado de un solo alumno (para cambiar a Ausente/Retardo)."""
        # BR.11: Estado debe ser uno de los posibles valores
        if nuevo_estado not in ["Presente", "Ausente", "Retardo", "Justificado"]:
            return "Error: Estado de asistencia inválido."
        
        asistencia = Asistencia(matricula, fecha, nuevo_estado)
        if self._asistencia_dao.registrar_asistencia(asistencia):
            return "Éxito: Estado de asistencia actualizado."
        else:
            return "Error: No se pudo actualizar el estado en la base de datos."

    def obtener_asistencia_para_ui(self, fecha=date.today().strftime("%Y-%m-%d")):
        """Retorna la lista de asistencia del día para la UI (R)."""
        return self._asistencia_dao.obtener_asistencia_del_dia(fecha, self._grupo_actual_id)