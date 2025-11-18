# app.py (En la carpeta DirectAula)

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStyleFactory
)
from PyQt5.QtCore import Qt
from Presentacion.ventana_alumnos import VentanaAlumnos # <-- Importación Modular
from Presentacion.ventana_asistencia import VentanaAsistencia # <-- Importación Modular

class VentanaMenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DirectAula - Sistema de Gestión")
        self.resize(400, 300)
        
        # Contenedor central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 💡 Título
        lbl_titulo = QLabel("DirectAula - Menú Principal")
        lbl_titulo.setObjectName("titulo_principal")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        # 1. Botón CU2: Administrar Alumnos
        btn_alumnos = QPushButton("📋 CU2: Administrar Alumnos")
        btn_alumnos.clicked.connect(self.abrir_ventana_alumnos)
        btn_alumnos.setObjectName("btn_exportar") # Color azul
        layout.addWidget(btn_alumnos)

        # 2. Botón CU4: Registrar Asistencia
        btn_asistencia = QPushButton("✅ CU4: Registrar Asistencia")
        btn_asistencia.clicked.connect(self.abrir_ventana_asistencia)
        btn_asistencia.setObjectName("btn_agregar") # Color verde
        layout.addWidget(btn_asistencia)
        
        # 3. Botón para otros CUs (Mockup)
        btn_otros = QPushButton("Otras Funcionalidades (Pendiente)")
        layout.addWidget(btn_otros)

    def abrir_ventana_alumnos(self):
        """Lanza la ventana del Caso de Uso 2."""
        # Nota: Asumimos grupo_id=1 por ahora.
        self.ventana_alumnos = VentanaAlumnos(grupo_id=1) 
        self.ventana_alumnos.show()
        
    def abrir_ventana_asistencia(self):
        """Lanza la ventana del Caso de Uso 4."""
        self.ventana_asistencia = VentanaAsistencia(grupo_id=1) 
        self.ventana_asistencia.show()


if __name__ == '__main__':
    QApplication.setStyle(QStyleFactory.create('Fusion')) 
    app = QApplication(sys.argv)
    
    # Aplicar el CSS desde la raíz (DirectAula/)
    try:
        with open('style.css', 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Advertencia: El archivo style.css no fue encontrado.")

    ventana_principal = VentanaMenuPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())