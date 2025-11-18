
# model.py
class Alumno:
    """Representa a un estudiante. Implementa Encapsulamiento."""
    
    # 💡 CAMBIO: Añadir email al constructor
    def __init__(self, matricula, nombre_completo, datos_contacto="", email=""):
        self._matricula = matricula
        self._nombre_completo = nombre_completo
        self._datos_contacto = datos_contacto
        self._email = email # Nuevo campo
        
    # Getters
    def get_matricula(self):
        return self._matricula

    def get_nombre(self):
        return self._nombre_completo

    def get_datos_contacto(self):
        return self._datos_contacto

    # 💡 CAMBIO: Getter para Email
    def get_email(self):
        return self._email
        
    # Setters
    def set_nombre(self, nombre):
        self._nombre_completo = nombre
        
    def set_datos_contacto(self, contacto):
        self._datos_contacto = contacto

    def set_email(self, email):
        self._email = email

    # Método para validación interna (BR.4)
    def es_valido(self):
        return bool(self._matricula) and bool(self._nombre_completo)
    
class Asistencia:
    """Representa el registro de asistencia para un alumno en una fecha dada."""
    def __init__(self, matricula, fecha, estado="Presente"):
        self._matricula = matricula
        self._fecha = fecha
        self._estado = estado
        
    def get_matricula(self):
        return self._matricula

    def get_fecha(self):
        return self._fecha

    def get_estado(self):
        return self._estado
    
    def set_estado(self, estado):
        self._estado = estado