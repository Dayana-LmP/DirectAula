# ventana_login.py (Modificado)

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QMessageBox, QFrame, QDialog 
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from Logica.gestor_autenticacion import GestorAutenticacion
# 💡 Importar la nueva ventana
from Presentacion.ventana_registro_profesor import VentanaRegistroProfesor 

class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.gestor = GestorAutenticacion()
        self.ventana_principal = None
        self._inicializar_ui()

    def _inicializar_ui(self):
        self.setWindowTitle("DirectAula - Iniciar Sesión")
        # 💡 Ajustamos la altura
        self.setFixedSize(450, 550) 
        
        # Fondo con degradado (Tu estilo CSS original)
        self.setStyleSheet("""
            VentanaLogin {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #FF6B35, 
                    stop:0.5 #FF8E53, 
                    stop:1 #F7931E);
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Frame principal - tamaño ajustado
        main_frame = QFrame()
        main_frame.setFixedSize(380, 480) 
        main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setAlignment(Qt.AlignTop)
        frame_layout.setSpacing(0)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        
        # Sección del logo y título
        logo_section = QVBoxLayout()
        logo_section.setSpacing(5)
        logo_section.setContentsMargins(0, 0, 0, 0)
        
        # Logo/Icono (Si tienes un archivo de logo, úsalo aquí)
        # 💡 Si tienes el logo, usa QPixmap y comenta el QLabel("🎓")
        lbl_icono = QLabel("🎓") 
        # try:
        #     lbl_icono.setPixmap(QPixmap("ruta/a/tu/logo.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #     lbl_icono.setText("") # Quitar el texto del emoji si se carga la imagen
        # except:
        #     pass # Si falla cargar el logo, se queda el emoji
            
        lbl_icono.setAlignment(Qt.AlignCenter)
        lbl_icono.setStyleSheet("font-size: 45px;")
        lbl_icono.setFixedHeight(60)
        logo_section.addWidget(lbl_icono)
        
        # Título y Subtítulo (Tu código original)
        # ...

        frame_layout.addLayout(logo_section)
        frame_layout.addSpacing(25)
        
        # Formulario de login (Tu código original)
        # ...
        
        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Ingrese su usuario")
        self.campo_usuario.setFixedHeight(40)
        # ... (Estilos) ...
        
        self.campo_password = QLineEdit()
        self.campo_password.setPlaceholderText("Ingrese su contraseña")
        self.campo_password.setEchoMode(QLineEdit.Password)
        self.campo_password.setFixedHeight(40)
        # ... (Estilos) ...
        
        frame_layout.addLayout(QVBoxLayout()) # Reconstruye el layout con tus QLineEdit
        
        # Botón de login (Tu código original)
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setFixedHeight(45)
        # ... (Estilos) ...
        btn_login.clicked.connect(self._autenticar_usuario)
        frame_layout.addWidget(btn_login)
        
        frame_layout.addSpacing(10)

        # 💡 Botón de registro
        btn_registro = QPushButton("¿Eres nuevo? Regístrate aquí")
        btn_registro.setStyleSheet("border: none; color: #4299E1; font-size: 12px; padding: 5px;")
        btn_registro.clicked.connect(self._abrir_registro)
        frame_layout.addWidget(btn_registro)
        
        frame_layout.addSpacing(10)
        
        # Texto informativo (demo) - Se mantiene
        lbl_info = QLabel("Usuario demo: admin | Contraseña: admin123")
        lbl_info.setAlignment(Qt.AlignCenter)
        lbl_info.setStyleSheet("""
            QLabel {
                color: #718096; font-size: 10px; font-style: italic;
                background-color: rgba(237, 242, 247, 0.8);
                padding: 6px 10px; border-radius: 5px;
            }
        """)
        lbl_info.setFixedHeight(30)
        frame_layout.addWidget(lbl_info)
        
        # Agregar frame principal al layout
        main_layout.addWidget(main_frame)
        
        # Conectar eventos
        self.campo_password.returnPressed.connect(btn_login.click)
        
        # 💡 Eliminar valores por defecto
        # self.campo_usuario.setText("admin") 
        # self.campo_password.setText("admin123") 
        self.campo_usuario.setFocus()
    
    # ... (método _autenticar_usuario, _abrir_ventana_principal sin cambios) ...

    def _abrir_registro(self):
        """Abre la ventana de registro de profesor."""
        ventana_registro = VentanaRegistroProfesor(self)
        # Ejecuta la ventana como modal. Si retorna Accepted (registro exitoso)...
        if ventana_registro.exec_() == QDialog.Accepted:
            # Rellena el campo de usuario con el que acaba de registrar
            self.campo_usuario.setText(ventana_registro.campo_usuario.text())
            self.campo_password.setFocus()