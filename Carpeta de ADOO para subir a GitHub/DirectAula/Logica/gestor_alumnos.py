#Archivo para la lógica de negocio relacionada con la gestión de alumnos, grupos, asistencia y calificaciones.
from Datos.dao import AlumnoDAO, AsistenciaDAO, GrupoDAO, CategoriaEvaluacionDAO, CalificacionDAO
from model import Alumno, Asistencia, Grupo, CategoriaEvaluacion, Calificacion
from datetime import date  #Para manejo de fechas

# 1. GESTOR GRUPOS 
#Clase para gestionar la lógica de negocio relacionada con los grupos. Qué reglas de negocio aplicar en cada caso de uso.
class GestorGrupos:
#Métodos para gestionar grupos, aplicando las reglas de negocio correspondientes.
    def __init__(self):
        self._grupo_dao = GrupoDAO()
        self._alumno_dao = AlumnoDAO() #Necesario para BR.2
#Método que retornan listas de grupos
    def obtener_lista_grupos(self):
        return self._grupo_dao.obtener_grupos()

#Método para agregar un nuevo grupo, validando reglas de negocio
    def agregar_nuevo_grupo(self, nombre, ciclo_escolar):
        nombre = nombre.strip() #Eliminar espacios en blanco al inicio y final
        ciclo_escolar = ciclo_escolar.strip() #Eliminar espacios en blanco al inicio y final
# Validaciones básicas
        if not nombre or not ciclo_escolar:
            return "Error: Nombre y Ciclo Escolar son obligatorios."

        #BR.1: El nombre del grupo debe ser único para ese Ciclo Escolar.
        if self._grupo_dao.buscar_grupo_por_nombre_ciclo(nombre, ciclo_escolar):
            return "Error: Ya existe un grupo con ese nombre en este Ciclo Escolar."
#Crear el nuevo grupo
        nuevo_grupo = Grupo(None, nombre, ciclo_escolar)
        if self._grupo_dao.crear_grupo(nuevo_grupo):
            return "Éxito: Grupo registrado correctamente."
        else:
            return "Error: No se pudo guardar el grupo en la base de datos."
#Método para actualizar datos de un grupo.
    def actualizar_datos_grupo(self, grupo_id, nombre, ciclo_escolar):
        nombre = nombre.strip()
        ciclo_escolar = ciclo_escolar.strip()

        #BR.1 (Revisar si otro grupo ya tiene esa combinación nombre/ciclo)
        id_existente = self._grupo_dao.buscar_grupo_por_nombre_ciclo(nombre, ciclo_escolar)
        if id_existente and id_existente != grupo_id:
            return "Error: Otro grupo ya usa ese nombre y ciclo escolar."
#Actualizar el grupo
        grupo_a_actualizar = Grupo(grupo_id, nombre, ciclo_escolar)
        if self._grupo_dao.actualizar_grupo(grupo_a_actualizar):
            return "Éxito: Grupo actualizado correctamente."
        else:
            return "Error: No se pudo actualizar el grupo."
#Método para eliminar un grupo.
    def eliminar_grupo(self, grupo_id):
        #BR.2: Un grupo no puede ser eliminado si tiene alumnos registrados
        if self._alumno_dao.obtener_alumnos_por_grupo(grupo_id):
            return "Error: No se puede eliminar el grupo porque tiene alumnos registrados."
        
        if self._grupo_dao.eliminar_grupo(grupo_id):
            return "Éxito: Grupo eliminado."
        else:
            return "Error: No se pudo eliminar el grupo."

#2. GESTOR ALUMNOS
#Clase para gestionar la lógica de negocio relacionada con los alumnos.
#Polimorfismo: Esta clase puede ser extendida para diferentes tipos de alumnos si es necesario.
class GestorAlumnos:
#Método para inicializar el gestor con el grupo actual
    def __init__(self, grupo_actual_id):
        self._alumno_dao = AlumnoDAO() 
        self._grupo_actual_id = grupo_actual_id
#Método privado para verificar si una matrícula ya existe en el grupo
#Es privado porque es una función auxiliar interna.
    def _existe_matricula_en_grupo(self, matricula):
        alumnos_grupo = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        return any(a[0] == matricula for a in alumnos_grupo)
#Método para agregar un nuevo alumno, aplicando las reglas de negocio
    def agregar_nuevo_alumno(self, matricula, nombre, contacto, email):
        #Si no se proporcionan matrícula o nombre, retorna error  
        if not matricula or not nombre:
            return "Error: Matrícula y Nombre son obligatorios."
        
        if self._existe_matricula_en_grupo(matricula):
            return f"Error: La matrícula {matricula} ya existe en este grupo."
#Crear el nuevo alumno
        nuevo_alumno = Alumno(matricula, nombre, contacto, email) 

        if self._alumno_dao.crear_alumno(nuevo_alumno, self._grupo_actual_id):
            return "Éxito: Alumno registrado correctamente."
        else:
            return "Error: No se pudo guardar en la base de datos."
#Método para obtener la lista de alumnos del grupo actual
    def obtener_lista_alumnos(self):
        return self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
#Método para actualizar datos de un alumno 
    def actualizar_datos_alumno(self, matricula, nombre, contacto, email):

        if not matricula or not nombre:
            return "Error: Nombre es obligatorio para la actualización."
        
        alumno_a_actualizar = Alumno(matricula, nombre, contacto, email)
        
        if self._alumno_dao.actualizar_alumno(alumno_a_actualizar):
            return "Éxito: Datos del alumno actualizados correctamente."
        else:
            return "Error: No se pudo actualizar el alumno."
#Método para eliminar un alumno
    def eliminar_alumno(self, matricula):
        if self._alumno_dao.eliminar_alumno(matricula):
            return "Éxito: Alumno eliminado."
        else:
            return "Error: No se pudo eliminar el alumno."

# 3. GESTOR ASISTENCIA 
#Clase para gestionar la lógica de negocio relacionada con la asistencia de los alumnos.
#Polimorfismo: Esta clase puede ser extendida para diferentes tipos de asistencia si es necesario.
class GestorAsistencia:
#Método para inicializar el gestor con el grupo actual
    def __init__(self, grupo_actual_id):
        self._asistencia_dao = AsistenciaDAO()
        self._alumno_dao = AlumnoDAO() 
        self._grupo_actual_id = grupo_actual_id
#Método para registrar asistencia masiva (poner asistencia a todos)
    def registrar_asistencia_masiva(self, fecha=date.today().strftime("%Y-%m-%d")):
        alumnos_data = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        matriculas = [a[0] for a in alumnos_data] 
        registros_exitosos = 0
#Registrar asistencia para cada alumno
        for matricula in matriculas:
#Crear el objeto Asistencia con estado "Asistencia"
            asistencia = Asistencia(matricula, fecha, "Asistencia") 
            if self._asistencia_dao.registrar_asistencia(asistencia):
                registros_exitosos += 1
       #Retornar mensaje según resultados         
        if len(matriculas) == 0:
            return "Advertencia: No hay alumnos en este grupo."
        elif registros_exitosos > 0:
            return "Éxito: Asistencia masiva registrada."
        else:
            return "Error: No se pudo registrar la asistencia."
#Método para actualizar el estado de asistencia de un alumno
    def actualizar_estado_asistencia(self, matricula, fecha, nuevo_estado):
        if nuevo_estado not in ["Asistencia", "Ausente", "Retardo", "Justificado"]:
            return "Error: Estado de asistencia inválido."
    #Crear el objeto Asistencia con el nuevo estado    
        asistencia = Asistencia(matricula, fecha, nuevo_estado)
        if self._asistencia_dao.registrar_asistencia(asistencia):
            return "Éxito: Estado de asistencia actualizado."
        else:
            return "Error: No se pudo actualizar el estado en la base de datos."
#Método para obtener la lista de asistencia del día para la UI
    def obtener_asistencia_para_ui(self, fecha=date.today().strftime("%Y-%m-%d")):
        return self._asistencia_dao.obtener_asistencia_del_dia(fecha, self._grupo_actual_id)

# 4. GESTOR CALIFICACIONES (CASO DE USO 3, 5 y 6)
#Clase para gestionar la lógica de negocio relacionada con las calificaciones y evaluaciones.
class GestorCalificaciones:
    #Método para inicializar el gestor con el grupo actual
    def __init__(self, grupo_id):
        self._grupo_actual_id = grupo_id
        self._categoria_dao = CategoriaEvaluacionDAO() 
        self._calificacion_dao = CalificacionDAO()
        #CU6: Promedio Final y Riesgo 
        self._alumno_dao = AlumnoDAO()
        self._asistencia_dao = AsistenciaDAO()
        #Aseguramos la ponderación inicial 
        self._categoria_dao.crear_ponderacion_inicial(grupo_id)
    
    #Métodos para gestionar categorías de evaluación
    def obtener_categorias_evaluacion(self):
        return self._categoria_dao.obtener_categorias_por_grupo(self._grupo_actual_id)

    #Método para guardar las categorías de evaluación con sus ponderaciones    
    def guardar_categorias_evaluacion(self, categorias_data: list[tuple]):
        #Validar la suma de pesos 100%
        try:
            total_peso = sum([float(peso) for _, peso, _ in categorias_data])
        except (TypeError, ValueError):
            return "Error: Los pesos porcentuales deben ser numéricos."
            
        if round(total_peso) != 100:
            return f"Error: La suma de las ponderaciones debe ser 100%, la suma actual es {total_peso:.1f}%."
        
        #Crear objetos del modelo CategoriaEvaluacion
        lista_modelos = []
        for nombre, peso, max_items in categorias_data:
            lista_modelos.append(
                CategoriaEvaluacion(self._grupo_actual_id, nombre, float(peso), int(max_items))
            )
        
        #Guardar en la base de datos 
        try:
            #Llamada al método guardando el orden (lista_modelos, grupo_id)
            if self._categoria_dao.guardar_ponderaciones(lista_modelos, self._grupo_actual_id):
                #6. Guarda la estructura y recalcula todos los promedios 
                self._recalcular_promedios()
                return "Éxito: Estructura de evaluación guardada y promedios recalculados exitosamente."
            else:
                return "Error: El DAO retornó un fallo al guardar la estructura de evaluación."
        except Exception as e:
            return f"Error crítico al intentar guardar ponderaciones: {e}"
#Método para recalcular promedios de todos los alumnos
    def _recalcular_promedios(self):
        alumnos_data = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        categorias = self.obtener_categorias_evaluacion()
#Recorre cada alumno para recalcular su promedio
        for matricula, _, _, _ in alumnos_data: 
            #Recalcula el promedio de cada alumno.
            self._calcular_promedio_alumno_ponderado(matricula, categorias) 
            
        print(f"Recalculo de promedios finalizado para grupo {self._grupo_actual_id}.")
        return True
#Método para calcular el promedio ponderado de un alumno
    def _calcular_promedio_alumno_ponderado(self, matricula, ponderaciones):
        #Obtener todas las calificaciones del alumno (categoría, valor, fecha)
        calificaciones_alumno = self._calificacion_dao.obtener_calificaciones_por_alumno_y_categoria(matricula)
        
        #Reestructurar calificaciones por categoría para un acceso más fácil
        notas_por_categoria = {}
        for categoria, valor, _ in calificaciones_alumno:
            if categoria not in notas_por_categoria:
                notas_por_categoria[categoria] = []
            notas_por_categoria[categoria].append(valor)
#Calcular el promedio ponderado 
        suma_ponderada = 0.0
        peso_total_valido = 0.0
        #Recorrer cada categoría y aplicar las reglas de negocio
        for categoria in ponderaciones:
            nombre_cat = categoria.get_nombre_categoria()
            peso_cat = categoria.get_peso_porcentual()
            max_items = categoria.get_max_items()
            
            notas_categoria = notas_por_categoria.get(nombre_cat)
            
            if notas_categoria:
                #Ordenar notas de mayor a menor y seleccionar las mejores según max_items
                notas_categoria.sort(reverse=True)
                notas_seleccionadas = notas_categoria[:max_items]
                
                #Calcular promedio de la categoría
                promedio_categoria = sum(notas_seleccionadas) / len(notas_seleccionadas)
                
                suma_ponderada += promedio_categoria * (peso_cat / 100.0)
                peso_total_valido += peso_cat #Suma el peso solo si hay al menos una nota registrada en la categoría
                
        if peso_total_valido == 0:
            return 0.0
        
        #Retornar el promedio ponderado final
        return suma_ponderada / (peso_total_valido / 100.0)

#Método para calcular promedios finales y estado de riesgo de todos los alumnos      
    def calcular_promedios_y_estado_final(self):
        alumnos = self._alumno_dao.obtener_alumnos_por_grupo(self._grupo_actual_id)
        ponderaciones = self._categoria_dao.obtener_categorias_por_grupo(self._grupo_actual_id)
        
        resultados_finales = []
        
        for matricula, nombre, _, _ in alumnos:
            #1. Calcular promedio ponderado (BR.14)
            promedio = self._calcular_promedio_alumno_ponderado(matricula, ponderaciones) 
            
            #2. Obtener porcentaje de asistencia
            porcentaje_asistencia = self._asistencia_dao.obtener_porcentaje_asistencia_por_alumno(matricula)
            
            #3. Determinar estado de riesgo (BR.12) y redondear (BR.17)
            #Redondeo a 2 decimales
            promedio_redondeado = round(promedio, 2)
            porcentaje_asistencia_redondeado = round(porcentaje_asistencia, 2)
            
            estado_riesgo = "Normal"
            
            #BR.12: Riesgo Académico < 7.0
            if promedio_redondeado < 7.0:
                estado_riesgo = "Riesgo Académico"
            
            #BR.12: Riesgo Asistencia < 80.0
            if porcentaje_asistencia_redondeado < 80.0:
                if estado_riesgo == "Riesgo Académico":
                    estado_riesgo = "Riesgo Académico y Asistencia"
                else:
                    estado_riesgo = "Riesgo Asistencia"
            #Agregar resultado a la lista final  
            resultados_finales.append((
                matricula, 
                nombre, 
                promedio_redondeado, 
                porcentaje_asistencia_redondeado, 
                estado_riesgo
            ))
            
        return resultados_finales
  
  #Método para obtener alumnos con calificaciones en una categoría específica  
    def obtener_alumnos_con_calificaciones(self, categoria):
        #Retorna: [(matricula, nombre, valor), ...]
        return self._calificacion_dao.obtener_calificaciones_por_categoria(self._grupo_actual_id, categoria)
#Método para registrar una calificación para un alumno
    def registrar_calificacion(self, matricula, categoria, valor):
        #Validación de rangos 
        try:
            valor_num = float(valor)
        except (TypeError, ValueError):
            return "Error: La calificación debe ser un valor numérico."
        
        if not (0.0 <= valor_num <= 10.0):
            return "Error: La calificación debe estar entre 0 y 10."

        #Construir el modelo de calificación
        nueva_calificacion = Calificacion(matricula, categoria, valor_num)
        try:
            saved = self._calificacion_dao.registrar_calificacion(nueva_calificacion)
        except Exception as e:
            print(f"Error al registrar calificación: {e}")
            saved = False

        if saved:
            #Recalcular promedios para actualizar estado de riesgo 
            try:
                self._recalcular_promedios()
            except Exception as e:
                #Alerta pero no bloquea el guardado
                print(f"Advertencia: Fallo en el recálculo de promedios post-guardado: {e}")
                pass
            return "Éxito: Calificación registrada."
        else:
            return "Error: No se pudo registrar la calificación."