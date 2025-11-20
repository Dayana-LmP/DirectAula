# logica/bll.py (Contiene toda la Lógica de Negocio)

from Datos.dao import AlumnoDAO, AsistenciaDAO, GrupoDAO # 💡 CORREGIDO: Importación con minúscula y añadida GrupoDAO
from model import Alumno, Asistencia, Grupo
from datetime import date # Solo necesitamos 'date'

# ====================================================
# 1. GESTOR GRUPOS (CU-1)
# ====================================================

class GestorGrupos:
    """Gestiona el flujo y aplica las reglas de negocio para Grupos."""

    def __init__(self):
        self._grupo_dao = GrupoDAO()
        self._alumno_dao = AlumnoDAO() # Necesario para BR.2

    def obtener_lista_grupos(self):
        """Retorna la lista de grupos (R)."""
        return self._grupo_dao.obtener_grupos()

    def agregar_nuevo_grupo(self, nombre, ciclo_escolar):
        """Implementa la lógica de Crear Grupo, valida BR.1 y AC-1."""
        nombre = nombre.strip()
        ciclo_escolar = ciclo_escolar.strip()

        if not nombre or not ciclo_escolar:
            return "Error: Nombre y Ciclo Escolar son obligatorios (AC-1)."

        # BR.1: El nombre del grupo debe ser único para ese Ciclo Escolar.
        if self._grupo_dao.buscar_grupo_por_nombre_ciclo(nombre, ciclo_escolar):
            return "Error: Ya existe un grupo con ese nombre en este Ciclo Escolar (BR.1)."

        nuevo_grupo = Grupo(None, nombre, ciclo_escolar)
        if self._grupo_dao.crear_grupo(nuevo_grupo):
            return "Éxito: Grupo registrado correctamente."
        else:
            return "Error: No se pudo guardar el grupo en la base de datos."

    def actualizar_datos_grupo(self, grupo_id, nombre, ciclo_escolar):
        """Implementa la lógica de Editar Grupo, valida BR.1."""
        nombre = nombre.strip()
        ciclo_escolar = ciclo_escolar.strip()

        # BR.1 (Revisar si otro grupo ya tiene esa combinación nombre/ciclo)
        id_existente = self._grupo_dao.buscar_grupo_por_nombre_ciclo(nombre, ciclo_escolar)
        if id_existente and id_existente != grupo_id:
            return "Error: Otro grupo ya usa ese nombre y ciclo escolar (BR.1)."

        grupo_a_actualizar = Grupo(grupo_id, nombre, ciclo_escolar)
        if self._grupo_dao.actualizar_grupo(grupo_a_actualizar):
            return "Éxito: Grupo actualizado correctamente."
        else:
            return "Error: No se pudo actualizar el grupo."

    def eliminar_grupo(self, grupo_id):
        """Implementa la lógica para eliminar un grupo, valida BR.2."""
        # BR.2: Un grupo no puede ser eliminado si tiene alumnos registrados
        if self._alumno_dao.obtener_alumnos_por_grupo(grupo_id):
            return "Error: No se puede eliminar el grupo porque tiene alumnos registrados (BR.2)."
        
        if self._grupo_dao.eliminar_grupo(grupo_id):
            return "Éxito: Grupo eliminado."
        else:
            return "Error: No se pudo eliminar el grupo."

# ====================================================
# 2. GESTOR ALUMNOS (CU-2)
# ====================================================
class GestorAlumnos:
    """Gestiona el flujo y aplica las reglas de negocio para Alumnos."""

    def __init__(self, grupo_actual_id):
        self._alumno_dao = AlumnoDAO() 
        self._grupo_actual_id = grupo_actual_id

    def _existe_matricula_en_grupo(self, matricula):
        """Verifica si la matrícula existe en el grupo (FE.2)."""
        alumnos_grupo = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        # Esto es eficiente, ya que la validación se hace en la base de datos (dao.py)
        # Aquí solo filtramos si la matrícula existe en el resultado.
        return any(a[0] == matricula for a in alumnos_grupo)

    def agregar_nuevo_alumno(self, matricula, nombre, contacto, email):
        """Implementa la lógica del FA.1: Agregar nuevo alumno."""
        
        if not matricula or not nombre:
            return "Error: Matrícula y Nombre son obligatorios (BR.4 - FE.1)."
        
        if self._existe_matricula_en_grupo(matricula):
            return f"Error: La matrícula {matricula} ya existe en este grupo (FE.2)."

        nuevo_alumno = Alumno(matricula, nombre, contacto, email) 

        if self._alumno_dao.crear_alumno(nuevo_alumno, self._grupo_actual_id):
            return "Éxito: Alumno registrado correctamente."
        else:
            return "Error: No se pudo guardar en la base de datos."

    def obtener_lista_alumnos(self):
        """Retorna la lista de alumnos del grupo (R)."""
        return self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
    
    def actualizar_datos_alumno(self, matricula, nombre, contacto, email):
        """Implementa la lógica del FA.2: Modificar datos de un alumno."""
        
        if not matricula or not nombre:
            return "Error: Nombre es obligatorio para la actualización (BR.4 - FE.1)."
        
        alumno_a_actualizar = Alumno(matricula, nombre, contacto, email)
        
        if self._alumno_dao.actualizar_alumno(alumno_a_actualizar):
            return "Éxito: Datos del alumno actualizados correctamente."
        else:
            return "Error: No se pudo actualizar el alumno."

    def eliminar_alumno(self, matricula):
        """Implementa la lógica para eliminar un alumno (BR.6)."""
        # BR.6 implica la eliminación, asumiendo que las referencias a asistencia/calificaciones
        # también se eliminarán o se manejarán con integridad referencial.
        if self._alumno_dao.eliminar_alumno(matricula):
            return "Éxito: Alumno eliminado permanentemente (BR.6)."
        else:
            return "Error: No se pudo eliminar el alumno."

# ====================================================
# 3. GESTOR ASISTENCIA (CU-4)
# ====================================================
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
            # BR.11: La asistencia se registra como Presente por defecto
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