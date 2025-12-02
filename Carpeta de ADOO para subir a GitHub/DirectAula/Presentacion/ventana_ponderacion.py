#Archivo para la ventana de ponderación de categorías.
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QTableWidgetItem, QHeaderView, QLineEdit
)
from PyQt5.QtCore import Qt
from Logica.gestor_alumnos import GestorCalificaciones 

#Clase para la ventana de ponderación de categorías.
class VentanaPonderacion(QWidget):
   #Método constructor.
   #Atributos privados: grupo_id, nombre_grupo, gestor
    def __init__(self, grupo_id, nombre_grupo, parent=None):
        super().__init__(parent)
        self._grupo_id = grupo_id
        self._nombre_grupo = nombre_grupo
        self.gestor = GestorCalificaciones(grupo_id)
        self.setWindowTitle(f"Ponderación - {nombre_grupo}")
        self.resize(800, 450)
        self._inicializar_ui()
        self._cargar_datos()

#Método para inicializar la interfaz de usuario.
    def _inicializar_ui(self):
        main_layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel(f"Definir Categorías y Ponderación: {self._nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        main_layout.addWidget(lbl_titulo)
        
        # Tabla para categorías dinámicas
        self.tabla_ponderacion = QTableWidget()
        self.tabla_ponderacion.setColumnCount(3)
        self.tabla_ponderacion.setHorizontalHeaderLabels([
            "Categoría", 
            "Valor (%)", 
            "Número tareas/participaciones"
        ])
        #Ajustar ancho de las columnas
        self.tabla_ponderacion.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_ponderacion.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tabla_ponderacion.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        #Conexión para actualizar la suma visualmente al cambiar cualquier celda de peso
        self.tabla_ponderacion.cellChanged.connect(self._actualizar_suma) 
        main_layout.addWidget(self.tabla_ponderacion)
        
        #Indicador visual de la suma actual (FE.1)
        self.lbl_suma = QLabel("Suma Actual: 0.0%")
        self.lbl_suma.setObjectName("subtitulo")
        main_layout.addWidget(self.lbl_suma)

        #Botones de acción
        btn_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("Añadir Categoría")
        btn_agregar.clicked.connect(self._agregar_fila)
        btn_layout.addWidget(btn_agregar)
        
        btn_eliminar = QPushButton("Eliminar Categoría Seleccionada")
        btn_eliminar.setObjectName("btn_eliminar")
        btn_eliminar.clicked.connect(self._eliminar_fila)
        btn_layout.addWidget(btn_eliminar)
        
        btn_guardar = QPushButton("Guardar Estructura")
        btn_guardar.setObjectName("btn_agregar")
        btn_guardar.clicked.connect(self._guardar_ponderacion)
        btn_layout.addWidget(btn_guardar)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

#Método para cargar los datos existentes en la tabla.
    def _cargar_datos(self):
        #1. Obtener las categorías desde el gestor
        categorias = self.gestor.obtener_categorias_evaluacion()
        self.tabla_ponderacion.setRowCount(len(categorias))
        
        self.tabla_ponderacion.blockSignals(True)
        for fila_indice, cat in enumerate(categorias):
            #Columna 0: Nombre
            self.tabla_ponderacion.setItem(fila_indice, 0, QTableWidgetItem(cat.get_nombre_categoria()))
            #Columna 1: Peso
            self.tabla_ponderacion.setItem(fila_indice, 1, QTableWidgetItem(str(cat.get_peso_porcentual())))
            #Columna 2: Max Items
            self.tabla_ponderacion.setItem(fila_indice, 2, QTableWidgetItem(str(cat.get_max_items())))
            
        self.tabla_ponderacion.blockSignals(False)
        self._actualizar_suma()
#Método para añadir una nueva fila.
    def _agregar_fila(self):
       
        row_count = self.tabla_ponderacion.rowCount()
        self.tabla_ponderacion.insertRow(row_count)
        self.tabla_ponderacion.setItem(row_count, 1, QTableWidgetItem("0.0"))
        self.tabla_ponderacion.setItem(row_count, 2, QTableWidgetItem("1"))

#Método para eliminar la fila seleccionada.
    def _eliminar_fila(self):
        #Obtener la fila seleccionada
        fila_seleccionada = self.tabla_ponderacion.currentRow()
        if fila_seleccionada >= 0:
            self.tabla_ponderacion.removeRow(fila_seleccionada)
            self._actualizar_suma()

#Método para actualizar la suma de los pesos.
    def _actualizar_suma(self):
       #Calcular la suma de los pesos ingresados
        suma = 0.0
        try:
            for i in range(self.tabla_ponderacion.rowCount()):
                item = self.tabla_ponderacion.item(i, 1)
                if item and item.text():
                    suma += float(item.text())
            #Actualizar la etiqueta visual
            self.lbl_suma.setText(f"Suma Actual: {suma:.1f}%")
            if round(suma) != 100:
                self.lbl_suma.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.lbl_suma.setStyleSheet("color: green; font-weight: bold;")
        except ValueError:
            self.lbl_suma.setText("Suma Actual: Inválida (Valores no numéricos en Peso)")
            self.lbl_suma.setStyleSheet("color: red; font-weight: bold;")

#Método para obtener los datos de la tabla.
    def _obtener_datos_tabla(self):
        datos = []
        for i in range(self.tabla_ponderacion.rowCount()):
            nombre_item = self.tabla_ponderacion.item(i, 0)
            peso_item = self.tabla_ponderacion.item(i, 1)
            max_item = self.tabla_ponderacion.item(i, 2) #Número de tareas/participaciones
            
            #Validar que no haya campos vacíos
            if not (nombre_item and peso_item and max_item and nombre_item.text().strip()):
                QMessageBox.critical(self, "Error de Datos", f"La fila {i+1} tiene campos vacíos o la Categoría no tiene nombre.")
                return None
            
            try:
                nombre = nombre_item.text().strip()
                peso = float(peso_item.text())
                max_items = int(max_item.text())
                datos.append((nombre, peso, max_items))
            except ValueError:
                QMessageBox.critical(self, "Error de Datos", f"Asegúrese de que los números de la fila {i+1} son números válidos.")
                return None
        return datos

#Método para guardar la ponderación definida.
    def _guardar_ponderacion(self):
        
        datos_a_guardar = self._obtener_datos_tabla()
        if datos_a_guardar is None:
            return

        # FE.2: Modificación con promedios ya calculados
        alerta = QMessageBox.question(self, "Recálculo de Promedios (FE.2)",
            "Guardar esta nueva estructura ELIMINARÁ la anterior y forzará el recálculo de todos los promedios. ¿Desea continuar?",
            QMessageBox.Yes | QMessageBox.Cancel
        )
        
        if alerta == QMessageBox.Cancel:
            return
            
        #6. Guardar en la base de datos mediante el gestor logico
        resultado = self.gestor.guardar_categorias_evaluacion(datos_a_guardar)
        
        if "Error" in resultado:
            QMessageBox.critical(self, "Error al Guardar", resultado)
        else:
            QMessageBox.information(self, "Éxito", resultado)
            self.close()