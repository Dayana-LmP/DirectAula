#Archivo para la ventana de menú de calificaciones.
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from Presentacion.ventana_ponderacion import VentanaPonderacion 
from Presentacion.ventana_registro_calificaciones import VentanaRegistroCalificaciones 
from Presentacion.ventana_calificacion_final import VentanaCalificacionFinal

#Clase para la ventana de menú de calificaciones.
class VentanaCalificacionesMenu(QWidget):
    #Método constructor.
    def __init__(self, grupo_id, nombre_grupo, parent=None):
        super().__init__(parent)
        self._grupo_id = grupo_id
        self._nombre_grupo = nombre_grupo
        self.setWindowTitle(f"Calificaciones - {nombre_grupo}")
        self.resize(500, 300)
        self._inicializar_ui()
        #Método para inicializar la interfaz de usuario.
    def _inicializar_ui(self):
        layout = QVBoxLayout(self)
        #Título principal
        lbl_titulo = QLabel(f"Gestión de Calificaciones: {self._nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        #CU3: Administrar Ponderación
        btn_ponderacion = QPushButton("1. Administrar Ponderación")
        btn_ponderacion.setObjectName("btn_agregar")
        btn_ponderacion.clicked.connect(self.abrir_ponderacion)
        layout.addWidget(btn_ponderacion)

        #CU5: Registrar Calificaciones
        btn_registro = QPushButton("2. Registrar Calificaciones")
        btn_registro.setObjectName("btn_agregar")
        btn_registro.clicked.connect(self.abrir_registro)
        layout.addWidget(btn_registro)

        #Ver Calificación Final Ponderada y Estado de Riesgo
        btn_final = QPushButton("3. Calificación Final y Estado de Riesgo")
        btn_final.setObjectName("btn_agregar")
        btn_final.clicked.connect(self.abrir_calificacion_final)
        layout.addWidget(btn_final)
        
        #Establecer el diseño principal
    def abrir_ponderacion(self):
        self.ventana_ponderacion = VentanaPonderacion(self._grupo_id, self._nombre_grupo) #Abrir ventana de ponderación
        self.ventana_ponderacion.show()
#Método para abrir la ventana de registro de calificaciones.
    def abrir_registro(self):
        self.ventana_registro = VentanaRegistroCalificaciones(self._grupo_id, self._nombre_grupo)
        self.ventana_registro.show()
    #Método para abrir la ventana de calificación final y estado de riesgo.
    def abrir_calificacion_final(self):
        self.ventana_final = VentanaCalificacionFinal(self._grupo_id, self._nombre_grupo, self)
        self.ventana_final.exec_()