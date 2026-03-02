#Archivo para la ventana de calificación final y estado de riesgo.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from Logica.gestor_alumnos import GestorCalificaciones 
from Logica.gestor_exportacion import GestorExportaciones
#Clase para la ventana de calificación final y estado de riesgo.
class VentanaCalificacionFinal(QDialog):
 #Método constructor.
    def __init__(self, grupo_id, nombre_grupo, parent=None):
        super().__init__(parent)
        self._grupo_id = grupo_id
        self._nombre_grupo = nombre_grupo
        
        self.setWindowTitle(f"Calificación final - {nombre_grupo} ")
        self.setGeometry(100, 100, 800, 400) 
        
        self._setup_ui()
        self._cargar_resultados() 
#Método para configurar la interfaz de usuario.
    def _setup_ui(self):
        layout_principal = QVBoxLayout(self)

        #Etiqueta de título que muestra el grupo actual
        lbl_titulo = QLabel(f"Resultados finales del grupo: {self._nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        #2. Tabla de Resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(5)
        self.tabla_resultados.setHorizontalHeaderLabels([
            "Matrícula", "Nombre Completo", "Promedio Final", "Asistencia (%)", "Estado de Riesgo"
        ])
        
        #Configuración para que las columnas se ajusten automáticamente
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla_resultados.horizontalHeader().setStretchLastSection(True)
        
        layout_principal.addWidget(self.tabla_resultados)
        
        btn_reporte = QPushButton("Generar Reporte Excel")
        btn_reporte.setObjectName("btn_exportar")
        btn_reporte.clicked.connect(self._generar_reporte_excel)
        layout_principal.addWidget(btn_reporte)

#Método para cargar los resultados finales en la tabla.
    def _cargar_resultados(self):
       
        try:
            #Usamos el grupo_id que ya recibimos en el constructor
            gestor_calif = GestorCalificaciones(self._grupo_id)
            
            #Llamada al método central de la lógica (CU6)
            resultados = gestor_calif.calcular_promedios_y_estado_final()
            
            self.tabla_resultados.setRowCount(len(resultados))
            #Llenar la tabla con los datos obtenidos
            for row, data in enumerate(resultados):
                matricula, nombre, promedio, asistencia, riesgo = data
                
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem(matricula))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(nombre))
                
                #Promedio final, redondeo a 2 decimales
                item_promedio = QTableWidgetItem(f"{promedio:.2f}")
                item_promedio.setTextAlignment(Qt.AlignCenter)
                self.tabla_resultados.setItem(row, 2, item_promedio)
                
                #Asistencia % 
                item_asistencia = QTableWidgetItem(f"{asistencia:.2f}%")
                item_asistencia.setTextAlignment(Qt.AlignCenter)
                self.tabla_resultados.setItem(row, 3, item_asistencia)
                
                #Estado de riesgo 
                item_riesgo = QTableWidgetItem(riesgo)
                item_riesgo.setTextAlignment(Qt.AlignCenter)
                
                #Resaltado visual para el estado de riesgo
                if "Riesgo" in riesgo:
                    #Color rojo
                    item_riesgo.setForeground(Qt.red)
                elif riesgo == "Normal":
                    # Color verde para estado Normal
                    item_riesgo.setForeground(Qt.darkGreen) 
                    
                self.tabla_resultados.setItem(row, 4, item_riesgo)
            #Ajustar el tamaño de las filas
        except Exception as e:
            QMessageBox.critical(self, "Error de Carga", f"Ocurrió un error al cargar los datos: {str(e)}")
    #Método para generar reporte Excel
    def _generar_reporte_excel(self):
      
        directorio = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta para guardar el reporte",
            "",
            QFileDialog.ShowDirsOnly
        )
        if not directorio:
            return
        QMessageBox.information(self,"Generando reporte",
                                "Generando reporte, puede tomar unos segundos.")
        gestor_export = GestorExportaciones()
        exito, mensaje, ruta_archivo = gestor_export.exportar_grupo_completo(
            self._grupo_id,
            self._nombre_grupo,
            directorio
        )
        if exito:
            QMessageBox.information(self, "Reporte generado",
                                    f"{mensaje}\n\nReporte guardado en:\n{ruta_archivo}")
        else:
            QMessageBox.critical(self, "Error ", mensaje)