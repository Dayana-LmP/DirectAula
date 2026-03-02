#Archivo para gestionar la autenticación de profesores
from Datos.dao import ProfesorDAO
#Clase para gestionar la autenticación de profesores
class GestorAutenticacion:
    def __init__(self):
        self._profesor_dao = ProfesorDAO()
#Método para autenticar a un profesor
    def autenticar_profesor(self, usuario, password):
        profesor = self._profesor_dao.buscar_profesor_por_usuario(usuario)
    #Verificar si el profesor existe    
        if not profesor:
            return {
                "autenticado": False,
                "mensaje": "Usuario no encontrado"
            }
            
        #profesor[2] es la contraseña almacenada
        if profesor[2] != password: 
            return {
                "autenticado": False,
                "mensaje": "Contraseña incorrecta"
            }
            #Autenticación exitosa
        return {
            "autenticado": True,
            "mensaje": f"Bienvenido, {profesor[1]}",
            "profesor_id": profesor[0],
            "nombre": profesor[1]
        }
    #Método para registrar a un nuevo profesor
    def registrar_profesor(self, nombre, usuario, password, email=""):
        
        #1. Verificar si el usuario ya existe
        if self._profesor_dao.buscar_profesor_por_usuario(usuario):
            return {
                "exito": False,
                "mensaje": "El nombre de usuario ya está en uso. Por favor, elija otro."
            }
        
        #2. Registrar el profesor
        try:
            self._profesor_dao.crear_profesor(nombre, usuario, password, email)
            return {
                "exito": True,
                "mensaje": "¡Registro exitoso! Ya puedes iniciar sesión."
            }
        except Exception as e:
            #Manejo de errores de base de datos
            return {
                "exito": False,
                "mensaje": f"Error al guardar en la base de datos: {str(e)}"
            }