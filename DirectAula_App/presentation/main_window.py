# presentation/main_window.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QTableWidget, QTableWidgetItem,
                             QLineEdit, QPushButton, QHBoxLayout, QMessageBox,
                             QHeaderView)

# Importar el formulario al inicio del archivo
from presentation.alumno_form import AlumnoForm
from business.alumno_service import AlumnoService
from data_access.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.alumno_service = AlumnoService(self.db)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("DirectAula - Administrar Alumnos")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Barra de búsqueda (AC-2 - Búsqueda predictiva)
        search_layout = QHBoxLayout()
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Buscar por nombre o matrícula...")
        self.busqueda_input.textChanged.connect(self.buscar_alumnos)
        
        btn_agregar = QPushButton("Agregar Alumno")
        btn_agregar.clicked.connect(self.mostrar_formulario_agregar)
        
        search_layout.addWidget(self.busqueda_input)
        search_layout.addWidget(btn_agregar)
        layout.addLayout(search_layout)
        
        # Tabla de alumnos
        self.tabla_alumnos = QTableWidget()
        self.tabla_alumnos.setColumnCount(4)
        self.tabla_alumnos.setHorizontalHeaderLabels([
            "Matrícula", "Nombre Completo", "Email", "Teléfono"
        ])
        
        # Ajustar columnas
        header = self.tabla_alumnos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Matrícula
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nombre (más espacio)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Email
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Teléfono
        
        layout.addWidget(self.tabla_alumnos)
        
        # Cargar datos iniciales (grupo temporal para pruebas)
        self.grupo_actual_id = 1  # Esto vendrá de la selección del grupo
        self.cargar_alumnos()
    
    def cargar_alumnos(self, criterio=""):
        try:
            alumnos = self.alumno_service.buscar_alumnos(self.grupo_actual_id, criterio)
            self.tabla_alumnos.setRowCount(len(alumnos))
            
            for row, alumno in enumerate(alumnos):
                self.tabla_alumnos.setItem(row, 0, QTableWidgetItem(alumno.matricula))
                self.tabla_alumnos.setItem(row, 1, QTableWidgetItem(alumno.nombre_completo))
                self.tabla_alumnos.setItem(row, 2, QTableWidgetItem(alumno.email or ""))
                self.tabla_alumnos.setItem(row, 3, QTableWidgetItem(alumno.telefono or ""))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar alumnos: {str(e)}")
    
    def buscar_alumnos(self):
        criterio = self.busqueda_input.text()
        self.cargar_alumnos(criterio)
    
    def mostrar_formulario_agregar(self):
        """Implementa FA.1 - Agregar nuevo alumno"""
        formulario = AlumnoForm(self, self.alumno_service, self.grupo_actual_id)
        if formulario.exec_():
            self.cargar_alumnos()  # Refrescar tabla después de agregar

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()