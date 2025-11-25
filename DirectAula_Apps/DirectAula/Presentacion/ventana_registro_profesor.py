# Presentacion/ventana_registro_profesor.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Logica.gestor_autenticacion import GestorAutenticacion

class VentanaRegistroProfesor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gestor = GestorAutenticacion()
        self.setWindowTitle("DirectAula - Registrar Docente")
        self.setFixedSize(450, 600)
        self._inicializar_ui()
    
    def _inicializar_ui(self):
        # Mismo fondo que Login
        self.setStyleSheet("""
            VentanaRegistroProfesor {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #FF6B35, 
                    stop:0.5 #FF8E53, 
                    stop:1 #F7931E);
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Frame principal
        main_frame = QFrame()
        main_frame.setFixedSize(380, 520)
        main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setAlignment(Qt.AlignTop)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        lbl_titulo = QLabel("Registro de Docente")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        lbl_titulo.setStyleSheet("color: #FF6B35;")
        frame_layout.addWidget(lbl_titulo)
        frame_layout.addSpacing(20)
        
        # --- Formulario de Registro ---
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Estilos de etiquetas y campos (simplificados para no repetir tanto)
        input_style = """
            QLineEdit {padding: 8px 12px; border: 2px solid #e2e8f0; border-radius: 8px; background-color: white; font-size: 14px; color: #2d3748;}
            QLineEdit:focus {border-color: #FF6B35;}
        """
        label_style = "color: #2d3748; font-weight: bold; font-size: 12px; margin-bottom: 2px;"
        
        # 1. Nombre Completo
        lbl_nombre = QLabel("Nombre Completo:")
        lbl_nombre.setStyleSheet(label_style)
        self.campo_nombre = QLineEdit()
        self.campo_nombre.setPlaceholderText("Ej. Juan Pérez")
        self.campo_nombre.setFixedHeight(40)
        self.campo_nombre.setStyleSheet(input_style)
        form_layout.addWidget(lbl_nombre)
        form_layout.addWidget(self.campo_nombre)
        
        # 2. Usuario
        lbl_usuario = QLabel("Usuario Único:")
        lbl_usuario.setStyleSheet(label_style)
        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Ej. jperez")
        self.campo_usuario.setFixedHeight(40)
        self.campo_usuario.setStyleSheet(input_style)
        form_layout.addWidget(lbl_usuario)
        form_layout.addWidget(self.campo_usuario)
        
        # 3. Contraseña
        lbl_password = QLabel("Contraseña:")
        lbl_password.setStyleSheet(label_style)
        self.campo_password = QLineEdit()
        self.campo_password.setPlaceholderText("Mínimo 6 caracteres")
        self.campo_password.setEchoMode(QLineEdit.Password)
        self.campo_password.setFixedHeight(40)
        self.campo_password.setStyleSheet(input_style)
        form_layout.addWidget(lbl_password)
        form_layout.addWidget(self.campo_password)
        
        # 4. Email (Opcional)
        lbl_email = QLabel("Email (Opcional):")
        lbl_email.setStyleSheet(label_style)
        self.campo_email = QLineEdit()
        self.campo_email.setPlaceholderText("Ej. correo@dominio.com")
        self.campo_email.setFixedHeight(40)
        self.campo_email.setStyleSheet(input_style)
        form_layout.addWidget(lbl_email)
        form_layout.addWidget(self.campo_email)

        frame_layout.addLayout(form_layout)
        frame_layout.addSpacing(25)
        
        # Botón de Registro (Color azul diferente para diferenciar)
        btn_registro = QPushButton("Registrarme")
        btn_registro.setFixedHeight(45)
        btn_registro.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4299E1, stop:1 #63B3ED);
                color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover {background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3182CE, stop:1 #4299E1);}
        """)
        btn_registro.clicked.connect(self._registrar_profesor)
        frame_layout.addWidget(btn_registro)
        
        # Botón para volver al login
        btn_volver = QPushButton("Volver a Iniciar Sesión")
        btn_volver.setStyleSheet("border: none; color: #4299E1; font-size: 12px;")
        btn_volver.clicked.connect(self.close)
        frame_layout.addWidget(btn_volver)

        main_layout.addWidget(main_frame)
        
        # Conectar eventos
        self.campo_email.returnPressed.connect(btn_registro.click)

    def _registrar_profesor(self):
        nombre = self.campo_nombre.text().strip()
        usuario = self.campo_usuario.text().strip()
        password = self.campo_password.text().strip()
        email = self.campo_email.text().strip()
        
        if not nombre or not usuario or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete Nombre, Usuario y Contraseña.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Contraseña Insegura", "La contraseña debe tener al menos 6 caracteres.")
            self.campo_password.setFocus()
            return

        self.setEnabled(False)
        
        try:
            resultado = self.gestor.registrar_profesor(nombre, usuario, password, email)
            
            if resultado["exito"]:
                QMessageBox.information(self, "Registro Exitoso", resultado["mensaje"])
                # Devuelve el estado "Aceptado" para que la ventana de login sepa que fue exitoso
                self.accept() 
            else:
                QMessageBox.critical(self, "Error de Registro", resultado["mensaje"])
                self.campo_usuario.selectAll()
                self.campo_usuario.setFocus()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {str(e)}")
            
        finally:
            self.setEnabled(True)