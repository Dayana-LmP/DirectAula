#Archivos para la gestión de la ventana de asistencia.
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QPushButton, QMessageBox, QTableWidgetItem, QHeaderView, QDateEdit, 
    QComboBox, QLabel, QGroupBox, QGridLayout 
)
from PyQt5.QtCore import QDate, Qt
from Logica.gestor_alumnos import GestorAsistencia 
from datetime import date

class VentanaAsistencia(QWidget):
#Ventana para el Caso de Uso 4: Registrar Asistencia

    def __init__(self, grupo_id, nombre_grupo): 
        super().__init__()
        self._grupo_id = grupo_id 
        self._nombre_grupo = nombre_grupo 
        self.setWindowTitle(f"DirectAula - Asistencia {nombre_grupo}")
        self.resize(800, 400)
        self.gestor = GestorAsistencia(self._grupo_id) 
        self._inicializar_ui(nombre_grupo)

    def _inicializar_ui(self, nombre_grupo):

        main_layout = QVBoxLayout()
        lbl_titulo = QLabel(f"Registro de Asistencia: {nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        main_layout.addWidget(lbl_titulo)
    
        #SECCIÓN: CONTROL DE FECHA Y REGISTRO MASIVO

        control_fecha_box = QGroupBox("Control de Asistencia")
        control_layout = QGridLayout(control_fecha_box)

        #1. Selector de Fecha (QDateEdit)
        lbl_fecha = QLabel("Seleccionar Fecha:")
        self.fecha_asistencia = QDateEdit()
        self.fecha_asistencia.setCalendarPopup(True) #Muestra el calendario al hacer clic
        self.fecha_asistencia.setDate(QDate.currentDate()) #Fecha de hoy por defecto
        self.fecha_asistencia.dateChanged.connect(self._cargar_datos) 
        control_layout.addWidget(lbl_fecha, 0, 0)
        control_layout.addWidget(self.fecha_asistencia, 0, 1)

        #2. Botón de Registro Masivo
        self.btn_masivo = QPushButton("Poner Asistencia a todos")
        self.btn_masivo.setObjectName("btn_agregar")
        self.btn_masivo.clicked.connect(self._registrar_asistencia_masiva)
        
        control_layout.addWidget(self.btn_masivo, 1, 0, 1, 2) 
        main_layout.addWidget(control_fecha_box)
      
        #TABLA DE ASISTENCIA
  
        self.tabla_asistencia = QTableWidget()
        self.tabla_asistencia.setColumnCount(3)
        self.tabla_asistencia.setHorizontalHeaderLabels(["Matrícula", "Nombre Completo", "Estado"])
        self.tabla_asistencia.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.tabla_asistencia)
        self.setLayout(main_layout)
        self._cargar_datos() #Carga los datos al iniciar con la fecha de hoy
    #Método para cargar los datos de asistencia en la tabla. 
    def _cargar_datos(self):
      
        #1. Obtener la fecha seleccionada
        fecha = self.fecha_asistencia.date().toString("yyyy-MM-dd") 
        
        #2. Obtener los datos del gestor
        datos = self.gestor.obtener_asistencia_para_ui(fecha)
        
        #3. Configurar la tabla
        self.tabla_asistencia.setRowCount(len(datos))
        
        #4. Iterar y llenar la tabla 
        for fila_indice, alumno_data in enumerate(datos):
            
            #Columna 0: Matrícula (Solo Lectura, no se puede editar)
            item_matricula = QTableWidgetItem(alumno_data[0])
            item_matricula.setFlags(item_matricula.flags() & ~Qt.ItemIsEditable) #Desactivar edición
            self.tabla_asistencia.setItem(fila_indice, 0, item_matricula)
            
            #Columna 1: Nombre Completo (Solo Lectura)
            item_nombre = QTableWidgetItem(alumno_data[1])
            item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable) #Desactivar edición
            self.tabla_asistencia.setItem(fila_indice, 1, item_nombre)
            
            #Columna 2: Estado (QComboBox para interactividad)
            estado_combo = QComboBox()
            estados = ["Presente", "Ausente", "Retardo", "Justificado"]
            estado_combo.addItems(estados)
            
            #Seleccionar el estado actual (devuelto por el DAO: 'Presente', 'Ausente', etc.)
            estado_combo.setCurrentText(alumno_data[2])

            #lambda para capturar los valores específicos de esta fila (matrícula y fecha)
            estado_combo.currentIndexChanged.connect( #lambda es usado para pasar parámetros
                lambda index, m=alumno_data[0], d=fecha, combo=estado_combo: 
                    self._actualizar_asistencia_individual(m, d, combo.currentText())
            )
            
            self.tabla_asistencia.setCellWidget(fila_indice, 2, estado_combo)

#Método para registrar asistencia masiva.
    def _registrar_asistencia_masiva(self):
      
        fecha = self.fecha_asistencia.date().toString("yyyy-MM-dd")
        #Confirmación antes de proceder
        confirmacion = QMessageBox.question(self, "Confirmar Registro",
            f"¿Desea marcar a TODOS los alumnos con 'Asistencia' para la fecha {fecha}?",
            QMessageBox.Yes | QMessageBox.No)
#Si el usuario confirma, proceder con el registro masivo
        if confirmacion == QMessageBox.Yes:
            resultado_mensaje = self.gestor.registrar_asistencia_masiva(fecha)
            
            if "Error" in resultado_mensaje:
                QMessageBox.critical(self, "Error", resultado_mensaje)
            else:
                QMessageBox.information(self, "Operación Exitosa", resultado_mensaje)
                self._cargar_datos() 
#Método para actualizar la asistencia individual.
    def _actualizar_asistencia_individual(self, matricula, fecha, nuevo_estado):
        resultado_mensaje = self.gestor.actualizar_estado_asistencia(matricula, fecha, nuevo_estado)
        
        if "Error" in resultado_mensaje:
            QMessageBox.critical(self, "Error de Guardado", resultado_mensaje)