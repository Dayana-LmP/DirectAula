# DirectAula/app.py (Actualizado)

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStyleFactory, QDialog
)
from PyQt5.QtCore import Qt
# Importaciones Modulares:
from Presentacion.ventana_grupos import VentanaGrupos # <-- NUEVA IMPORTACIÓN CU1
from Presentacion.ventana_alumnos import VentanaAlumnos 
from Presentacion.ventana_asistencia import VentanaAsistencia
from Presentacion.seleccion_grupo import SeleccionGrupo

class VentanaMenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DirectAula - Sistema de Gestión")
        self.resize(400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        lbl_titulo = QLabel("DirectAula - Menú Principal")
        lbl_titulo.setObjectName("titulo_principal")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        # 1. Botón CU1: Administrar Grupos (NUEVO)
        btn_grupos = QPushButton("Administrar Grupos")
        btn_grupos.clicked.connect(self.abrir_ventana_grupos)
        btn_grupos.setObjectName("btn_exportar") # Color azul
        layout.addWidget(btn_grupos)

        # 2. Botón CU2: Administrar Alumnos
        btn_alumnos = QPushButton("Administrar Alumnos")
        btn_alumnos.clicked.connect(self.abrir_ventana_alumnos)
        btn_alumnos.setObjectName("btn_exportar") 
        layout.addWidget(btn_alumnos)

        # 3. Botón CU4: Registrar Asistencia
        btn_asistencia = QPushButton("Registrar Asistencia")
        btn_asistencia.clicked.connect(self.abrir_ventana_asistencia)
        btn_asistencia.setObjectName("btn_agregar") 
        layout.addWidget(btn_asistencia)
        
        # 4. Botón para otros CUs (Mockup)
        btn_otros = QPushButton("Otras Funcionalidades (Pendiente)")
        layout.addWidget(btn_otros)

    def abrir_ventana_grupos(self):
        """Lanza la ventana del Caso de Uso 1."""
        self.ventana_grupos = VentanaGrupos() 
        self.ventana_grupos.show()

    def abrir_ventana_alumnos(self):
        """Lanza el diálogo de selección y luego la ventana de Alumnos (CU2)."""
        dialogo = SeleccionGrupo("Administrar Alumnos", self)
        if dialogo.exec_() == QDialog.Accepted:
            grupo_id = dialogo.get_grupo_id()
            nombre_grupo = dialogo.combo_grupos.currentText()
            # 💡 Pasamos el ID del grupo y su nombre a la ventana de alumnos
            self.ventana_alumnos = VentanaAlumnos(grupo_id=grupo_id, nombre_grupo=nombre_grupo) 
            self.ventana_alumnos.show()
        
    def abrir_ventana_asistencia(self):
        """Lanza el diálogo de selección y luego la ventana de Asistencia (CU4)."""
        dialogo = SeleccionGrupo("Registrar Asistencia", self)
        if dialogo.exec_() == QDialog.Accepted:
            grupo_id = dialogo.get_grupo_id()
            nombre_grupo = dialogo.combo_grupos.currentText()
            # 💡 Pasamos el ID del grupo y su nombre a la ventana de asistencia
            self.ventana_asistencia = VentanaAsistencia(grupo_id=grupo_id, nombre_grupo=nombre_grupo) 
            self.ventana_asistencia.show()


if __name__ == '__main__':
    QApplication.setStyle(QStyleFactory.create('Fusion')) 
    app = QApplication(sys.argv)
    
    # 💡 CÓDIGO CORREGIDO PARA ENCONTRAR style.css SIEMPRE:
    # 1. Obtiene la ruta del archivo actual (app.py)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # 2. Construye la ruta completa al archivo CSS
    ruta_css = os.path.join(directorio_actual, 'style.css')
    
    try:
        with open(ruta_css, 'r') as f: 
            app.setStyleSheet(f.read())
        print(f"Éxito: style.css cargado desde: {ruta_css}")
    except FileNotFoundError:
        print(f"Advertencia: El archivo style.css no fue encontrado en la ruta: {ruta_css}")
        
    ventana_principal = VentanaMenuPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())