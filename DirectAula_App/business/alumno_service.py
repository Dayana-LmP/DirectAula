# business/alumno_service.py
import re
from data_access.alumno_repository import AlumnoRepository
from models.entities import Alumno

class AlumnoService:
    def __init__(self, db):
        self.repository = AlumnoRepository(db)
    
    def agregar_alumno(self, datos_alumno):
        """Orquesta FA.1 - Agregar nuevo alumno con validaciones completas"""
        alumno = Alumno(**datos_alumno)
        
        # Validaciones adicionales
        self._validar_matricula(alumno.matricula)
        self._validar_nombre(alumno.nombre_completo)
        
        return self.repository.crear(alumno)
    
    def buscar_alumnos(self, grupo_id, criterio_busqueda=""):
        """Orquesta búsqueda con AC-2 - Resultados inmediatos"""
        return self.repository.buscar_por_grupo(grupo_id, criterio_busqueda)
    
    def validar_email(self, email):
        """Implementa regla implícita de formato email"""
        if not email:  # Email opcional
            return True
            
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validar_matricula(self, matricula):
        """BR.5 - Validar formato de matrícula"""
        if not matricula or len(matricula) < 3:
            raise ValueError("La matrícula debe tener al menos 3 caracteres")
        
        # Puedes agregar más reglas específicas de tu institución
        if not matricula.isalnum():
            raise ValueError("La matrícula solo puede contener letras y números")
    
    def _validar_nombre(self, nombre):
        """Validaciones básicas para el nombre"""
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        
        if len(nombre) > 100:
            raise ValueError("El nombre es demasiado largo")