#app.py, aqui se inicia la aplicación y se muestra la ventana de login
import sys #Para manejo de rutas y sistema
import os #Para manejo de rutas
# Importaciones PyQt5 necesarias:
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QStyleFactory, QDialog, QMessageBox, QFileDialog
)
#Esta línea es necesaria para alinear el título al centro
from PyQt5.QtCore import Qt
# Importaciones de nuestros otros archivos:
from Presentacion.ventana_grupos import VentanaGrupos 
from Presentacion.ventana_calificaciones_menu import VentanaCalificacionesMenu
from Presentacion.ventana_alumnos import VentanaAlumnos 
from Presentacion.ventana_asistencia import VentanaAsistencia
from Presentacion.seleccion_grupo import SeleccionGrupo
from Logica.gestor_exportacion import GestorExportaciones
from Presentacion.seleccion_grupo import SeleccionGrupo

#1. IMPORTAR LA VENTANA DE LOGIN
from Presentacion.ventana_login import VentanaLogin 
#Clase de la ventana principal del menú
class VentanaMenuPrincipal(QMainWindow):
#Método constructor de la ventana principal
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DirectAula - Sistema de Gestión")
        self.resize(450, 300) #Tamaño inicial de la ventana
        
        central_widget = QWidget() #Crear un widget central
        self.setCentralWidget(central_widget)
        #Crear un layout vertical para los botones
        layout = QVBoxLayout(central_widget)
        
        #Título principal
        lbl_titulo = QLabel("DirectAula - Menú Principal")
        lbl_titulo.setObjectName("titulo_principal")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        #1. Botón CU1: Administrar Grupos 
        btn_grupos = QPushButton("Administrar Grupos")
        btn_grupos.clicked.connect(self.abrir_ventana_grupos)
        btn_grupos.setObjectName("btn_exportar") #Color azul
        layout.addWidget(btn_grupos)

        #2. Botón CU2: Administrar Alumnos
        btn_alumnos = QPushButton("Administrar Alumnos")
        btn_alumnos.clicked.connect(self.abrir_ventana_alumnos)
        btn_alumnos.setObjectName("btn_exportar") #Viene de style.css
        layout.addWidget(btn_alumnos)

        #3. Botón CU4: Registrar Asistencia
        btn_asistencia = QPushButton("Registrar Asistencia")
        btn_asistencia.clicked.connect(self.abrir_ventana_asistencia)
        btn_asistencia.setObjectName("btn_exportar") 
        layout.addWidget(btn_asistencia)

        #4. Botón CU3/CU5: Calificaciones
        btn_calificaciones = QPushButton("Registar Calificaciones")
        btn_calificaciones.clicked.connect(self.abrir_ventana_calificaciones)
        btn_calificaciones.setObjectName("btn_exportar") 
        layout.addWidget(btn_calificaciones)

        #5. Botón exportar
        btn_exportar = QPushButton("Exportar Datos")
        btn_exportar.setObjectName("btn_exportar")
        btn_exportar.clicked.connect(self.exportar_datos_excel)
        layout.addWidget(btn_exportar)
#Métodos para abrir las diferentes ventanas
    def abrir_ventana_grupos(self):
        #Ventana de Grupos (CU1)
        self.ventana_grupos = VentanaGrupos() 
        self.ventana_grupos.show()
    
    def abrir_ventana_alumnos(self):
        #Ventana de Alumnos (CU2)
        dialogo = SeleccionGrupo("Administrar Alumnos", self)
        if dialogo.exec_() == QDialog.Accepted:
            grupo_id = dialogo.get_grupo_id()
            nombre_grupo = dialogo.combo_grupos.currentText()
            self.ventana_alumnos = VentanaAlumnos(grupo_id=grupo_id, nombre_grupo=nombre_grupo) 
            self.ventana_alumnos.show()
        
    def abrir_ventana_asistencia(self):
        #Ventana de Asistencia (CU4)
        dialogo = SeleccionGrupo("Registrar Asistencia", self)
        if dialogo.exec_() == QDialog.Accepted:
            grupo_id = dialogo.get_grupo_id()
            nombre_grupo = dialogo.combo_grupos.currentText()
            self.ventana_asistencia = VentanaAsistencia(grupo_id=grupo_id, nombre_grupo=nombre_grupo) 
            self.ventana_asistencia.show()
    
    def abrir_ventana_calificaciones(self):
        #Ventana de Calificaciones (CU3/CU5)
        dialogo = SeleccionGrupo("Gestión de Calificaciones", self)
        if dialogo.exec_() == QDialog.Accepted:
            grupo_id = dialogo.get_grupo_id()
            nombre_grupo = dialogo.combo_grupos.currentText()
            self.ventana_calificaciones = VentanaCalificacionesMenu(grupo_id=grupo_id, nombre_grupo=nombre_grupo)
            self.ventana_calificaciones.show()
    
    def exportar_datos_excel(self):
        #Exportar datos de un grupo completo a Excel
        dialogo = SeleccionGrupo("Exportar Datos a Excel", self)
        if dialogo.exec_() == QDialog.Accepted: #Si se presionó Aceptar
            grupo_id = dialogo.get_grupo_id()
            nombre_grupo = dialogo.combo_grupos.currentText()
            #Abrir un diálogo para seleccionar el directorio donde guardar el archivo
            directorio = QFileDialog.getExistingDirectory(
                self, 
                "Seleccionar carpeta para guardar el archivo Excel",
                "",
                QFileDialog.ShowDirsOnly
            )
            
            if not directorio:
                return
            
            QMessageBox.information(self, "Exportando", 
                                   "Exportando todos los datos a Excel.")
            
            gestor_export = GestorExportaciones() #Crear el gestor de exportaciones
            exito, mensaje, ruta_archivo = gestor_export.exportar_grupo_completo(
                grupo_id, 
                nombre_grupo,
                directorio
            )
            
            if exito: #Si la exportación fue exitosa
                QMessageBox.information(self, "Exportación Exitosa", 
                                      f"{mensaje}\n\nArchivo guardado en:\n{ruta_archivo}")
            else:
                QMessageBox.critical(self, "Error en Exportación", mensaje)

#Punto de entrada de la aplicación
if __name__ == '__main__': #Si se ejecuta este archivo directamente
    #Crear la aplicación PyQt5
    QApplication.setStyle(QStyleFactory.create('Fusion')) 
    app = QApplication(sys.argv)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_css = os.path.join(directorio_actual, 'style.css')
    
    try:
        with open(ruta_css, 'r', encoding='utf-8-sig') as f: #Abrir el archivo CSS con manejo de caracteres especiales
            app.setStyleSheet(f.read())
        print(f"Éxito: style.css cargado desde: {ruta_css}")
    except FileNotFoundError:
        print(f"Advertencia: El archivo style.css no fue encontrado en la ruta: {ruta_css}")
    except UnicodeDecodeError as e:
        print(f"Error de encoding: {e}. Intenta guardar style.css en UTF-8 sin BOM.")
        
    ventana_login = VentanaLogin()
    ventana_login.show()
    sys.exit(app.exec_())