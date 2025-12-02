#Archivo para gestionar las calificaciones y ponderaciones
from Datos.dao import AsistenciaDAO, CategoriaEvaluacionDAO, CalificacionDAO, AlumnoDAO 
from model import Calificacion, CategoriaEvaluacion 
from datetime import date

#Clase para gestionar las calificaciones y ponderaciones
class GestorCalificaciones:
#Método constructor
    def __init__(self, grupo_id :int):
        self._grupo_actual_id = grupo_id
        self._calificacion_dao = CalificacionDAO() 
        self._ponderacion_dao = CategoriaEvaluacionDAO() 
        self._alumno_dao = AlumnoDAO() #Necesario para obtener alumnos y sus matrículas
        self._asistencia_dao = AsistenciaDAO()
        self._ponderacion_dao.crear_ponderacion_inicial(grupo_id) #Asegura ponderación inicial

#LÓGICA CU3: ADMINISTRAR PONDERACIONES DE EVALUACIÓN
#Método para obtener categorías
    def obtener_categorias(self):
        return self._ponderacion_dao.obtener_categorias_por_grupo(self._grupo_actual_id)
#Método para guardar ponderaciones
    def guardar_ponderaciones(self, categorias: list[CategoriaEvaluacion]):
        #BR.5: Debe haber al menos una categoría
        if not categorias:
            return "Error: Debe definir al menos una categoría de evaluación."

        #BR.4: La suma de los pesos debe ser 100.0 
        suma_pesos = sum(c.get_peso_porcentual() for c in categorias)
        if abs(suma_pesos - 100.0) > 0.01: #La tolerancia de 0.01 para evitar errores de punto flotante
            return f"Error: La suma de los pesos porcentuales debe ser 100%. Suma actual: {suma_pesos:.2f}% ."
        for categoria in categorias:
            pass 

        if self._ponderacion_dao.guardar_ponderaciones(self._grupo_actual_id, categorias):
            return "Éxito: Ponderaciones guardadas correctamente."
        else:
            return "Error: No se pudieron guardar las ponderaciones en la base de datos."

#LÓGICA CU5: REGISTRAR CALIFICACIONES
#Método para obtener calificaciones por categoría
    def obtener_calificaciones_por_categoria(self, categoria_nombre):
        return self._calificacion_dao.obtener_calificaciones_por_categoria(
            self._grupo_actual_id, categoria_nombre
        )
#Método para registrar calificación
    def registrar_calificacion(self, matricula, categoria, valor, fecha=None):
        try:
            valor = float(valor)
        except ValueError:
            return "Error: La calificación debe ser un valor numérico."

        #BR.13: Todas las calificaciones deben ser numéricas y estar dentro de la escala (0-10)
        if not (0.0 <= valor <= 10.0):
            return "Error: La calificación debe estar entre 0.0 y 10.0 "

        #Usar la fecha de hoy si no se proporciona
        fecha_registro = fecha if fecha is not None else date.today().isoformat()

        nueva_calificacion = Calificacion(matricula, categoria, valor, fecha_registro)

        if self._calificacion_dao.registrar_calificacion(nueva_calificacion): #Así se registra en la BD
            return "Éxito: Calificación registrada."
        else:
            return "Error: No se pudo registrar la calificación."
        
    # LÓGICA BR.14/BR.15: CÁLCULO DE PROMEDIOS
    #Método para calcular el promedio final de un alumno
    def calcular_promedio_final(self, matricula):
        categorias = self.obtener_categorias()
        if not categorias: #Si no hay categorías definidas
            return 0.0 
        #1. Obtener todas las calificaciones del alumno para cada categoría
        promedio_ponderado = 0.0 #Valor inicial
        peso_total_valido = 0.0 #Para manejar casos donde no hay calificaciones
        for categoria in categorias:
            nota_categoria = 0.0 #Valor por defecto si no hay calificaciones
            promedio_ponderado += (nota_categoria * categoria.get_peso_porcentual()) #Ponderar
            peso_total_valido += categoria.get_peso_porcentual() #Acumular peso válido
        return promedio_ponderado / 100.0 

    #Función que junta todo para el reporte/vista final
    
    def obtener_resumen_calificaciones_grupo(self):
        
        alumnos = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        categorias = self.obtener_categorias()
        #Datos a retornar
        datos_grupo = []
        for alumno in alumnos:
            matricula = alumno.get_matricula()
            nombre = alumno.get_nombre_completo()
            
            registro = {
                'matricula': matricula,
                'nombre_completo': nombre,
                #Promedio final
                'promedio_final': self.calcular_promedio_final(matricula) 
            }
            
            # Agregar la nota individual por cada categoría
            for categoria in categorias:
                pass 
                
            datos_grupo.append(registro)
            
        return datos_grupo, categorias