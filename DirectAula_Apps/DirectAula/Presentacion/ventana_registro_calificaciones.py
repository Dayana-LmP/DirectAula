# presentacion/ventana_registro_calificaciones.py (NUEVO ARCHIVO)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QComboBox, 
    QLabel, QPushButton, QMessageBox, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from Logica.gestor_alumnos import GestorCalificaciones

class VentanaRegistroCalificaciones(QWidget):
    """Ventana para el Caso de Uso 5: Registrar Calificaciones."""
    
    # Categorías simplificadas. En un entorno real se obtendrían de la BLL/Ponderación.
    CATEGORIAS = ["Examen", "Participacion", "Tarea_1", "Tarea_2", "Tarea_3"] 

    def __init__(self, grupo_id, nombre_grupo, parent=None):
        super().__init__(parent)
        self._grupo_id = grupo_id
        self._nombre_grupo = nombre_grupo
        self.gestor = GestorCalificaciones(grupo_id)
        self.setWindowTitle(f"Registro de Calificaciones - {nombre_grupo}")
        self.resize(800, 600)
        self._inicializar_ui()
        
    def _inicializar_ui(self):
        main_layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel(f"Registrar Calificaciones: {self._nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        main_layout.addWidget(lbl_titulo)

        # 1. Selector de Categoría
        selector_layout = QVBoxLayout()
        lbl_categoria = QLabel("Seleccionar Categoría:")
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(self.CATEGORIAS)
        self.combo_categoria.setCurrentText(self.CATEGORIAS[0])
        self.combo_categoria.currentIndexChanged.connect(self._cargar_datos) 
        
        selector_layout.addWidget(lbl_categoria)
        selector_layout.addWidget(self.combo_categoria)
        main_layout.addLayout(selector_layout)

        # 2. Tabla de Calificaciones
        self.tabla_calificaciones = QTableWidget()
        self.tabla_calificaciones.setColumnCount(3)
        self.tabla_calificaciones.setHorizontalHeaderLabels(["Matrícula", "Nombre Completo", "Calificación (0-10)"])
        self.tabla_calificaciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Conexión principal: Al editar una celda, guardar automáticamente (FA.1)
        self.tabla_calificaciones.cellChanged.connect(self._guardar_calificacion_celda) 
        main_layout.addWidget(self.tabla_calificaciones)
        
        # 4. Botón Guardar (Sirve como confirmación de fin de registro)
        self.btn_guardar = QPushButton("Guardar y Recalcular Promedios")
        self.btn_guardar.setObjectName("btn_agregar")
        self.btn_guardar.clicked.connect(self._guardar_todo_manual) 
        main_layout.addWidget(self.btn_guardar)

        self.setLayout(main_layout)
        self._cargar_datos() # Carga inicial

    def _cargar_datos(self):
        """Muestra la lista de estudiantes con notas existentes para la categoría seleccionada."""
        categoria_seleccionada = self.combo_categoria.currentText()
        # Retorna: [(matricula, nombre, valor), ...]
        datos = self.gestor.obtener_alumnos_con_calificaciones(categoria_seleccionada)
        
        self.tabla_calificaciones.setRowCount(len(datos))
        
        self.tabla_calificaciones.blockSignals(True) # Bloquear para evitar guardado al cargar
        
        for fila_indice, alumno_data in enumerate(datos):
            matricula, nombre, valor_db = alumno_data
            
            # Columna 0 y 1: Datos del alumno (Solo Lectura)
            item_matricula = QTableWidgetItem(matricula)
            item_matricula.setFlags(item_matricula.flags() & ~Qt.ItemIsEditable) 
            self.tabla_calificaciones.setItem(fila_indice, 0, item_matricula)
            
            item_nombre = QTableWidgetItem(nombre)
            item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable) 
            self.tabla_calificaciones.setItem(fila_indice, 1, item_nombre)
            
            # Columna 2: Calificación (Editable)
            valor_str = str(valor_db) if valor_db is not None else ""
            self.tabla_calificaciones.setItem(fila_indice, 2, QTableWidgetItem(valor_str))
            
        self.tabla_calificaciones.blockSignals(False) 

    def _guardar_calificacion_celda(self, row, column):
        """Guarda la calificación en la BLL y recalcula el promedio al cambiar una celda."""
        if column != 2:
            return

        matricula = self.tabla_calificaciones.item(row, 0).text()
        categoria = self.combo_categoria.currentText()
        
        try:
            self.tabla_calificaciones.blockSignals(True) # Evitar recursión
            
            nuevo_valor_str = self.tabla_calificaciones.item(row, 2).text().strip()
            
            if not nuevo_valor_str:
                # Si está vacío, no se guarda y no se trata como 0 (BR.18)
                self.tabla_calificaciones.blockSignals(False)
                return

            # Llama al gestor, que valida el rango 0-10 (FE.1)
            resultado_mensaje = self.gestor.registrar_calificacion(matricula, categoria, nuevo_valor_str)
            
            if "Error" in resultado_mensaje:
                QMessageBox.critical(self, "Error de Validación (FE.1)", resultado_mensaje)
            else:
                # 7. El Sistema muestra un mensaje de confirmación.
                print(resultado_mensaje) # Confirmación en consola para no interrumpir
                
        except Exception as e:
            QMessageBox.critical(self, "Error de Entrada", f"Error inesperado: {e}")
            
        finally:
            self.tabla_calificaciones.blockSignals(False)

    def _guardar_todo_manual(self):
        """Función para el botón 'Guardar'. Llama a la BLL para asegurar el recálculo."""
        self.gestor._recalcular_promedios() # Forzar recálculo
        QMessageBox.information(self, "Éxito", "Todos los promedios han sido actualizados y el registro es automático por celda.")