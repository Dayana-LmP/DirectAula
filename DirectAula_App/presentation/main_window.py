# presentation/main_window.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QTableWidget, QTableWidgetItem, QLineEdit, 
                             QPushButton, QMessageBox, QHeaderView, QLabel, 
                             QStatusBar, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from presentation.alumno_form import AlumnoForm
from presentation.styles import get_styles
from business.alumno_service import AlumnoService
from data_access.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.alumno_service = AlumnoService(self.db)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        self.setWindowTitle("DirectAula - Sistema de Gestión Estudiantil")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Título principal
        titulo = QLabel("DirectAula - Administración de Estudiantes")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(titulo)
        
        # Grupo: Búsqueda y Acciones
        grupo_busqueda = QGroupBox("Búsqueda y Acciones Rápidas")
        layout_busqueda = QHBoxLayout(grupo_busqueda)
        
        # Barra de búsqueda
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("🔍 Buscar por nombre o matrícula...")
        self.busqueda_input.textChanged.connect(self.buscar_alumnos)
        layout_busqueda.addWidget(self.busqueda_input)
        
        # Botones de acción
        self.btn_agregar = QPushButton("➕ Agregar Alumno")
        self.btn_agregar.setObjectName("btn_agregar")
        self.btn_agregar.clicked.connect(self.mostrar_formulario_agregar)
        layout_busqueda.addWidget(self.btn_agregar)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.setObjectName("btn_editar")
        self.btn_editar.clicked.connect(self.editar_alumno)
        layout_busqueda.addWidget(self.btn_editar)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setObjectName("btn_eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_alumno)
        layout_busqueda.addWidget(self.btn_eliminar)
        
        self.btn_exportar = QPushButton("📊 Exportar")
        self.btn_exportar.setObjectName("btn_exportar")
        self.btn_exportar.clicked.connect(self.exportar_datos)
        layout_busqueda.addWidget(self.btn_exportar)
        
        layout.addWidget(grupo_busqueda)
        
        # Grupo: Lista de Alumnos
        grupo_tabla = QGroupBox("Lista de Alumnos")
        layout_tabla = QVBoxLayout(grupo_tabla)
        
        # Tabla de alumnos
        self.tabla_alumnos = QTableWidget()
        self.tabla_alumnos.setColumnCount(5)
        self.tabla_alumnos.setHorizontalHeaderLabels([
            "ID", "Matrícula", "Nombre Completo", "Email", "Teléfono"
        ])
        
        # Configurar tabla
        header = self.tabla_alumnos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Matrícula
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Nombre
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Email
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Teléfono
        
        # Ocultar columna ID
        self.tabla_alumnos.setColumnHidden(0, True)
        
        layout_tabla.addWidget(self.tabla_alumnos)
        layout.addWidget(grupo_tabla)
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ Sistema listo - Grupo: Prueba 2025-A")
        
        # Cargar datos iniciales
        self.grupo_actual_id = 1
        self.cargar_alumnos()
    
    def apply_styles(self):
        """Aplicar estilos CSS a la ventana"""
        self.setStyleSheet(get_styles())
    
    def cargar_alumnos(self, criterio=""):
        try:
            alumnos = self.alumno_service.buscar_alumnos(self.grupo_actual_id, criterio)
            self.tabla_alumnos.setRowCount(len(alumnos))
            
            for row, alumno in enumerate(alumnos):
                self.tabla_alumnos.setItem(row, 0, QTableWidgetItem(str(alumno.id)))
                self.tabla_alumnos.setItem(row, 1, QTableWidgetItem(alumno.matricula))
                self.tabla_alumnos.setItem(row, 2, QTableWidgetItem(alumno.nombre_completo))
                self.tabla_alumnos.setItem(row, 3, QTableWidgetItem(alumno.email or "Sin email"))
                self.tabla_alumnos.setItem(row, 4, QTableWidgetItem(alumno.telefono or "Sin teléfono"))
                
            # Actualizar barra de estado
            self.status_bar.showMessage(f"✅ {len(alumnos)} alumnos encontrados")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar alumnos: {str(e)}")
            self.status_bar.showMessage("❌ Error al cargar alumnos")
    
    def buscar_alumnos(self):
        criterio = self.busqueda_input.text()
        self.cargar_alumnos(criterio)
    
    def mostrar_formulario_agregar(self):
        """Abrir formulario para agregar alumno"""
        formulario = AlumnoForm(self, self.alumno_service, self.grupo_actual_id)
        formulario.setStyleSheet(get_styles())  # Aplicar mismos estilos
        if formulario.exec_():
            self.cargar_alumnos()  # Refrescar tabla
    
    def editar_alumno(self):
        """Editar alumno seleccionado"""
        fila_seleccionada = self.tabla_alumnos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Selección requerida", "Por favor selecciona un alumno para editar")
            return
        
        # Obtener ID del alumno seleccionado
        alumno_id = int(self.tabla_alumnos.item(fila_seleccionada, 0).text())
        QMessageBox.information(self, "Editar", f"Editando alumno ID: {alumno_id}")
        # Aquí implementarás la edición
    
    def eliminar_alumno(self):
        """Eliminar alumno seleccionado"""
        fila_seleccionada = self.tabla_alumnos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Selección requerida", "Por favor selecciona un alumno para eliminar")
            return
        
        # Obtener datos del alumno
        alumno_id = int(self.tabla_alumnos.item(fila_seleccionada, 0).text())
        nombre = self.tabla_alumnos.item(fila_seleccionada, 2).text()
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar al alumno: {nombre}?\n\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            try:
                # Aquí implementarás la eliminación
                # self.alumno_service.eliminar_alumno(alumno_id)
                QMessageBox.information(self, "Eliminado", f"Alumno {nombre} eliminado (simulación)")
                self.cargar_alumnos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar: {str(e)}")
    
    def exportar_datos(self):
        """Exportar datos a Excel (simulación)"""
        QMessageBox.information(self, "Exportar", "Función de exportación en desarrollo...")

def main():
    app = QApplication(sys.argv)
    
    # Establecer estilo general de la aplicación
    app.setStyle('Fusion')  # Estilo moderno
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()