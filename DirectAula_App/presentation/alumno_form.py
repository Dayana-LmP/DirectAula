# presentation/alumno_form.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QMessageBox, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AlumnoForm(QDialog):
    def __init__(self, parent=None, alumno_service=None, grupo_id=None):
        super().__init__(parent)
        self.alumno_service = alumno_service
        self.grupo_id = grupo_id
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("➕ Agregar Nuevo Alumno")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Título del formulario
        titulo = QLabel("Registro de Nuevo Alumno")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(titulo)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Campos del formulario
        self.matricula_input = QLineEdit()
        self.matricula_input.setPlaceholderText("Ej: 20250001")
        self.matricula_input.setStyleSheet("padding: 8px; border-radius: 5px;")
        form_layout.addRow("📋 Matrícula*:", self.matricula_input)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo del alumno")
        self.nombre_input.setStyleSheet("padding: 8px; border-radius: 5px;")
        form_layout.addRow("👤 Nombre Completo*:", self.nombre_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ejemplo@correo.com")
        self.email_input.setStyleSheet("padding: 8px; border-radius: 5px;")
        form_layout.addRow("📧 Email:", self.email_input)
        
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("+52 123 456 7890")
        self.telefono_input.setStyleSheet("padding: 8px; border-radius: 5px;")
        form_layout.addRow("📞 Teléfono:", self.telefono_input)
        
        layout.addLayout(form_layout)
        
        # Nota sobre campos obligatorios
        nota = QLabel("* Campos obligatorios")
        nota.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 10px;")
        layout.addWidget(nota)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.btn_guardar = QPushButton("💾 Guardar Alumno")
        self.btn_guardar.setObjectName("btn_agregar")
        self.btn_guardar.clicked.connect(self.guardar_alumno)
        
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.setObjectName("btn_eliminar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        button_layout.addWidget(self.btn_guardar)
        button_layout.addWidget(self.btn_cancelar)
        
        layout.addLayout(button_layout)
    
    def guardar_alumno(self):
        """Implementa FA.1 - Agregar nuevo alumno con validaciones"""
        try:
            # Obtener datos del formulario
            matricula = self.matricula_input.text().strip()
            nombre_completo = self.nombre_input.text().strip()
            email = self.email_input.text().strip()
            telefono = self.telefono_input.text().strip()
            
            # Validaciones básicas (BR.4 - Campos obligatorios)
            if not matricula:
                QMessageBox.warning(self, "Validación", "❌ La matrícula es obligatoria")
                self.matricula_input.setFocus()
                return
            
            if not nombre_completo:
                QMessageBox.warning(self, "Validación", "❌ El nombre completo es obligatorio")
                self.nombre_input.setFocus()
                return
            
            # Validar formato de email si se proporciona
            if email and not self.alumno_service.validar_email(email):
                QMessageBox.warning(self, "Validación", "❌ El formato del email no es válido")
                self.email_input.setFocus()
                return
            
            # Preparar datos para el servicio
            datos_alumno = {
                'matricula': matricula,
                'nombre_completo': nombre_completo,
                'email': email if email else None,
                'telefono': telefono if telefono else None,
                'grupo_id': self.grupo_id
            }
            
            # Llamar al servicio para crear el alumno
            alumno_creado = self.alumno_service.agregar_alumno(datos_alumno)
            
            QMessageBox.information(self, "✅ Éxito", 
                                  f"Alumno {alumno_creado.nombre_completo} agregado correctamente")
            self.accept()  # Cerrar diálogo con éxito
            
        except ValueError as e:
            # Capturar errores de validación del servicio
            QMessageBox.critical(self, "❌ Error de Validación", str(e))
        except Exception as e:
            # Capturar otros errores
            QMessageBox.critical(self, "❌ Error", f"Error al guardar alumno: {str(e)}")