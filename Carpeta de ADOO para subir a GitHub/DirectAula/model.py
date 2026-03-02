#Archivo encargado de definir las clases de modelo de datos, como Alumno, Grupo, Asistencia, Calificación, etc.
from datetime import date #Para manejar fechas en calificaciones y asistencias
#Clase alumno para representar a un estudiante dentro de un grupo
class Alumno: 
  #Método constructor para inicializar un objeto Alumno  
    def __init__(self, matricula, nombre_completo, datos_contacto, email):
        self._matricula = matricula
        self._nombre_completo = nombre_completo
        self._datos_contacto = datos_contacto
        self._email = email 
        self._grupo_id = None #Referencia al grupo al que pertenece

# Getters
    def get_matricula(self):
        return self._matricula

    def get_nombre_completo(self): 
        return self._nombre_completo 

    def get_datos_contacto(self):
        return self._datos_contacto
        
    def get_email(self):
        return self._email
 #Setters
    def set_nombre_completo(self, nombre_completo):
        self._nombre_completo = nombre_completo
        
    def set_datos_contacto(self, contacto):
        self._datos_contacto = contacto

    def set_email(self, email):
        self._email = email

    # Método para validación interna de datos. Como mínimo, debe tener matrícula y nombre.
    def es_valido(self):
        return bool(self._matricula) and bool(self._nombre_completo)
#Clase Asistencia para representar el estado de asistencia de un alumno en una fecha específica
class Asistencia:
 #Método constructor para inicializar un objeto Asistencia
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

#Clase Grupo para representar un grupo o curso académico
class Grupo:
    #Usaremos el id como clave primaria interna, y el nombre/ciclo para mostrar en la UI
    def __init__(self, grupo_id, nombre, ciclo_escolar):
        self._grupo_id = grupo_id #Usado internamente para referencias
        self._nombre = nombre
        self._ciclo_escolar = ciclo_escolar

    def get_id(self):
        return self._grupo_id

    def get_nombre(self):
        return self._nombre
    
    def get_ciclo(self):
        return self._ciclo_escolar
#Clase CategoriaEvaluacion para representar una categoría de evaluación dentro de un grupo
class CategoriaEvaluacion:
    #Método constructor para inicializar un objeto CategoriaEvaluacion
    def __init__(self, grupo_id, nombre_categoria, peso_porcentual, max_items=1):
        self._grupo_id = grupo_id
        self._nombre_categoria = nombre_categoria
        self._peso_porcentual = peso_porcentual  # Ej: 30.0 (30%)
        self._max_items = max_items  # BR.9 (No visible pero importante si lo implementas)

    # Getters(para el DAO)
    def get_grupo_id(self):
        return self._grupo_id

    def get_nombre_categoria(self):
        return self._nombre_categoria

    def get_peso_porcentual(self):
        return self._peso_porcentual

    def get_max_items(self):
        return self._max_items

    # Setters (para modificaciones en la UI)
    def set_peso_porcentual(self, peso):
        self._peso_porcentual = peso

#Clase Calificacion para representar una calificación individual de un alumno en una categoría en una fecha
class Calificacion:
    #Método constructor para inicializar un objeto Calificacion
    def __init__(self, matricula, categoria, valor, fecha=None):
        self._matricula = matricula
        self._categoria = categoria
        self._valor = valor
        #Si no se proporciona fecha, usa la de hoy (ISO 8601: YYYY-MM-DD)
        self._fecha = fecha if fecha is not None else date.today().isoformat()

    #Getters
    def get_matricula(self):
        return self._matricula

    def get_categoria(self):
        return self._categoria

    def get_valor(self):
        return self._valor

    def get_fecha(self):
        return self._fecha

    #Métodos para tuplas de BD que sirven para inserciones y actualizaciones
    def to_tuple(self):
        return (self._matricula, self._categoria, self._fecha, self._valor)