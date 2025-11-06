# models/entities.py
class Grupo:
    def __init__(self, id=None, nombre="", ciclo_escolar=""):
        self.id = id
        self.nombre = nombre
        self.ciclo_escolar = ciclo_escolar

class Alumno:
    def __init__(self, id=None, matricula="", nombre_completo="", 
                 email="", telefono="", grupo_id=None, estado="Activo"):
        self.id = id
        self.matricula = matricula
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono
        self.grupo_id = grupo_id
        self.estado = estado
    
    def es_valido(self):
        """Valida BR.4 - Campos obligatorios"""
        return bool(self.matricula and self.nombre_completo)