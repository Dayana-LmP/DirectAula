# presentacion/ventana_calificaciones_menu.py (NUEVO ARCHIVO)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from Presentacion.ventana_ponderacion import VentanaPonderacion 
from Presentacion.ventana_registro_calificaciones import VentanaRegistroCalificaciones # Aún no existe

class VentanaCalificacionesMenu(QWidget):
    def __init__(self, grupo_id, nombre_grupo, parent=None):
        super().__init__(parent)
        self._grupo_id = grupo_id
        self._nombre_grupo = nombre_grupo
        self.setWindowTitle(f"Calificaciones - {nombre_grupo}")
        self.resize(500, 300)
        self._inicializar_ui()
        
    def _inicializar_ui(self):
        layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel(f"Gestión de Calificaciones: {self._nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        # CU3: Administrar Ponderación
        btn_ponderacion = QPushButton("1. ⚖️ Administrar Ponderación (CU3)")
        btn_ponderacion.setObjectName("btn_editar")
        btn_ponderacion.clicked.connect(self.abrir_ponderacion)
        layout.addWidget(btn_ponderacion)

        # CU5: Registrar Calificaciones
        btn_registro = QPushButton("2. 📝 Registrar Calificaciones (CU5)")
        btn_registro.setObjectName("btn_agregar")
        btn_registro.clicked.connect(self.abrir_registro)
        layout.addWidget(btn_registro)
        
    def abrir_ponderacion(self):
        self.ventana_ponderacion = VentanaPonderacion(self._grupo_id, self._nombre_grupo)
        self.ventana_ponderacion.show()

    def abrir_registro(self):
        self.ventana_registro = VentanaRegistroCalificaciones(self._grupo_id, self._nombre_grupo)
        self.ventana_registro.show()