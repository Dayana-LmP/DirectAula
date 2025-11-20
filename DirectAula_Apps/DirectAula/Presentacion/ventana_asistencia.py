# presentacion/ventana_asistencia.py (Código Corregido)

import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QPushButton, QMessageBox, QTableWidgetItem, QHeaderView, QDateEdit, QComboBox,
    # 💡 CORRECTO: Se importa la clase QLabel
    QLabel , QDateEdit, QCalendarWidget, QGroupBox, QGridLayout 
)
from PyQt5.QtCore import QDate, Qt
# 💡 IMPORTACIÓN MODULAR CORREGIDA: Asumimos que GestorAsistencia está en logica/bll.py

from Logica.gestor_alumnos import GestorAsistencia 
from datetime import date

class VentanaAsistencia(QWidget):
    # ¡AHORA RECIBE EL ID DEL GRUPO!
    def __init__(self, grupo_id, nombre_grupo): 
        super().__init__()
        self._grupo_id = grupo_id # Usar el ID real
        self.setWindowTitle(f"DirectAula - Asistencia para: {nombre_grupo}")
        self.resize(800, 600)
        # El gestor ahora solo necesita el grupo_id al ser instanciado
        self.gestor = GestorAsistencia(self._grupo_id) 
        self._inicializar_ui(nombre_grupo)
        # self._cargar_datos() # Se llamará desde el selector de fecha

    def _inicializar_ui(self, nombre_grupo):
        main_layout = QVBoxLayout()
        
        lbl_titulo = QLabel(f"Registro de Asistencia: {nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        main_layout.addWidget(lbl_titulo)
        
        # ----------------------------------------------------
        # 💡 NUEVA SECCIÓN: SELECTOR DE FECHA (Calendario)
        # ----------------------------------------------------
        control_fecha_box = QGroupBox("Control de Asistencia")
        control_layout = QGridLayout(control_fecha_box)

        # 1. Selector de Fecha (QDateEdit)
        lbl_fecha = QLabel("Seleccionar Fecha:")
        self.fecha_asistencia = QDateEdit()
        self.fecha_asistencia.setCalendarPopup(True) # Muestra el calendario al hacer clic
        self.fecha_asistencia.setDate(QDate.currentDate()) # Fecha de hoy por defecto
        # 💡 Conexión: Cuando la fecha cambia, recargar los datos
        self.fecha_asistencia.dateChanged.connect(self._cargar_datos) 
        
        control_layout.addWidget(lbl_fecha, 0, 0)
        control_layout.addWidget(self.fecha_asistencia, 0, 1)

        # 2. Botón de Registro Masivo
        self.btn_masivo = QPushButton("✅ Poner 'Presente' a Todos")
        self.btn_masivo.setObjectName("btn_agregar")
        self.btn_masivo.clicked.connect(self._registrar_asistencia_masiva)
        
        control_layout.addWidget(self.btn_masivo, 1, 0, 1, 2) # Ocupa 2 columnas
        main_layout.addWidget(control_fecha_box)
        
        # ----------------------------------------------------
        # ... (Resto del código de la tabla de asistencia) ...
        # ----------------------------------------------------
        self.tabla_asistencia = QTableWidget()
        self.tabla_asistencia.setColumnCount(3)
        self.tabla_asistencia.setHorizontalHeaderLabels(["Matrícula", "Nombre Completo", "Estado"])
        self.tabla_asistencia.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.tabla_asistencia)

        self.setLayout(main_layout)
        self._cargar_datos() # Carga los datos al iniciar con la fecha de hoy
        
    def _cargar_datos(self):
        """Muestra los datos de asistencia del grupo para la fecha seleccionada."""
        # 💡 Obtiene la fecha del QDateEdit
        fecha = self.fecha_asistencia.date().toString("yyyy-MM-dd") 
        
        datos = self.gestor.obtener_asistencia_para_ui(fecha)
        # ... (el resto del método _cargar_datos sigue igual) ...
        # (Asegúrate que el resto del método que construye la tabla esté correcto)
        
    def _registrar_asistencia_masiva(self):
        """Llama al BLL para marcar a todos como Presente."""
        # 💡 Obtiene la fecha del QDateEdit
        fecha = self.fecha_asistencia.date().toString("yyyy-MM-dd")
        
        confirmacion = QMessageBox.question(self, "Confirmar Registro",
            f"¿Desea marcar a TODOS los alumnos como 'Presente' para la fecha {fecha}?",
            QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            resultado_mensaje = self.gestor.registrar_asistencia_masiva(fecha)
            # ... (el resto del método sigue igual) ...

    def _actualizar_asistencia_individual(self, matricula, fecha, nuevo_estado):
        """Guarda el estado de un alumno individualmente (Activado por el ComboBox)."""
        resultado_mensaje = self.gestor.actualizar_estado_asistencia(matricula, fecha, nuevo_estado)
        
        if "Error" in resultado_mensaje:
             QMessageBox.critical(self, "Error de Guardado", resultado_mensaje)