# presentacion/ventana_asistencia.py (Código Corregido)

import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QPushButton, QMessageBox, QTableWidgetItem, QHeaderView, QDateEdit, QComboBox,
    # 💡 CORRECTO: Se importa la clase QLabel
    QLabel 
)
from PyQt5.QtCore import QDate, Qt
# 💡 IMPORTACIÓN MODULAR CORREGIDA: Asumimos que GestorAsistencia está en logica/bll.py
from Logica.gestor_alumnos import GestorAsistencia 
from datetime import date

class VentanaAsistencia(QWidget):
    """Interfaz gráfica de PyQt5 para el CU-4: Registrar Asistencia."""

    def __init__(self, grupo_id=1):
        super().__init__()
        self.setWindowTitle("DirectAula - Registro de Asistencia (CU-4)")
        self.resize(700, 500)
        self.gestor = GestorAsistencia(grupo_id)
        self.grupo_id = grupo_id
        self._inicializar_ui()
        self._cargar_datos()

    def _inicializar_ui(self):
        main_layout = QVBoxLayout()
        
        # 💡 TÍTULO PRINCIPAL: Usamos QLabel correctamente
        self.lbl_titulo_principal = QLabel("DirectAula - Registro de Asistencia")
        self.lbl_titulo_principal.setObjectName("titulo_principal") 
        main_layout.addWidget(self.lbl_titulo_principal)

        # 💡 Controles Superiores: Fecha y Botones
        top_bar_layout = QHBoxLayout()
        
        # Selector de Fecha (BR.10)
        self.fecha_asistencia = QDateEdit(QDate.currentDate())
        self.fecha_asistencia.setCalendarPopup(True)
        self.fecha_asistencia.setDisplayFormat("yyyy-MM-dd")
        self.fecha_asistencia.dateChanged.connect(self._cargar_datos)
        top_bar_layout.addWidget(self.fecha_asistencia)
        
        # Botón Asistencia Masiva
        self.btn_asistencia_masiva = QPushButton("✅ Asistencia a Todos")
        self.btn_asistencia_masiva.setObjectName("btn_agregar")
        self.btn_asistencia_masiva.clicked.connect(self._registrar_asistencia_masiva)
        top_bar_layout.addWidget(self.btn_asistencia_masiva)
        
        main_layout.addLayout(top_bar_layout)
        
        # 💡 Tabla de Alumnos y Estado
        # Usamos QLabel correctamente
        self.lbl_subtitulo_lista = QLabel("Lista de alumnos y estado de asistencia") 
        self.lbl_subtitulo_lista.setProperty("class", "subtitulo")
        main_layout.addWidget(self.lbl_subtitulo_lista)
        
        self.tabla_asistencia = QTableWidget() 
        self.tabla_asistencia.setColumnCount(3)
        self.tabla_asistencia.setHorizontalHeaderLabels(["Matrícula", "Nombre Completo", "Estado"])
        self.tabla_asistencia.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        main_layout.addWidget(self.tabla_asistencia)

        self.setLayout(main_layout)

    def _cargar_datos(self):
        """Muestra los datos de asistencia del día seleccionado."""
        fecha = self.fecha_asistencia.date().toString("yyyy-MM-dd")
        datos = self.gestor.obtener_asistencia_para_ui(fecha)
        
        self.tabla_asistencia.setRowCount(0) 
        
        # ... (La lógica de la tabla con ComboBox permanece igual y es correcta) ...
        for fila_indice, alumno_data in enumerate(datos):
            # alumno_data: [matricula, nombre, estado]
            self.tabla_asistencia.insertRow(fila_indice)
            
            # Columna 0: Matrícula (Solo lectura)
            item_matricula = QTableWidgetItem(str(alumno_data[0]))
            item_matricula.setFlags(item_matricula.flags() & ~Qt.ItemIsEditable) 
            self.tabla_asistencia.setItem(fila_indice, 0, item_matricula)
            
            # Columna 1: Nombre (Solo lectura)
            item_nombre = QTableWidgetItem(str(alumno_data[1]))
            item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
            self.tabla_asistencia.setItem(fila_indice, 1, item_nombre)
            
            # Columna 2: Estado (ComboBox editable)
            estado_combo = QComboBox()
            # Estado de asistencia, según el glosario: "Presente, ausente, retardo, justificado"
            estados = ["Presente", "Ausente", "Retardo", "Justificado"] 
            estado_combo.addItems(estados)
            estado_combo.setCurrentText(alumno_data[2])
            
            # Conexión: Al cambiar el estado, se llama a la función de guardado individual
            estado_combo.currentIndexChanged.connect(
                lambda index, m=alumno_data[0], d=fecha, combo=estado_combo: self._actualizar_asistencia_individual(m, d, combo.currentText())
            )
            self.tabla_asistencia.setCellWidget(fila_indice, 2, estado_combo)

    def _registrar_asistencia_masiva(self):
        """Llama al BLL para marcar a todos como Presente."""
        fecha = self.fecha_asistencia.date().toString("yyyy-MM-dd")
        
        confirmacion = QMessageBox.question(self, "Confirmar Registro",
            f"¿Desea marcar a TODOS los alumnos como 'Presente' para la fecha {fecha}?",
            QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            resultado_mensaje = self.gestor.registrar_asistencia_masiva(fecha)
            
            if "Error" in resultado_mensaje:
                QMessageBox.critical(self, "Error", resultado_mensaje)
            else:
                QMessageBox.information(self, "Operación Exitosa", resultado_mensaje)
                self._cargar_datos() 

    def _actualizar_asistencia_individual(self, matricula, fecha, nuevo_estado):
        """Guarda el estado de un alumno individualmente (Activado por el ComboBox)."""
        resultado_mensaje = self.gestor.actualizar_estado_asistencia(matricula, fecha, nuevo_estado)
        
        if "Error" in resultado_mensaje:
             QMessageBox.critical(self, "Error de Guardado", resultado_mensaje)