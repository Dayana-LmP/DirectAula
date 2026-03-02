#Archivo para la gestión de la ventana de grupos.
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, 
    QPushButton, QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QLabel, QTableWidgetItem, QHeaderView
)
from Logica.gestor_alumnos import GestorGrupos 

#Clase para agregar o editar un grupo. 
class DialogoGrupo(QDialog):
   #Método constructor.
    def __init__(self, datos_grupo=None, parent=None): #Ningún dato al inicio.
        super().__init__(parent) #Llama al constructor padre. 
        self.datos_grupo = datos_grupo 
        self.setWindowTitle("Registrar Grupo" if not datos_grupo else "Editar Grupo") 
        layout = QFormLayout()
        self.campo_nombre = QLineEdit()
        self.campo_ciclo = QLineEdit() 
        #Si se proporcionan datos para editar, se llenan los campos.
        if datos_grupo:
            #datos_grupo = [id, nombre, ciclo]
            self.campo_nombre.setText(datos_grupo[1])
            self.campo_ciclo.setText(datos_grupo[2])

        layout.addRow(QLabel("Nombre del Grupo *"), self.campo_nombre)
        layout.addRow(QLabel("Ciclo Escolar *"), self.campo_ciclo)
#Botones Aceptar y Cancelar.
        self.botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)

        layout.addRow(self.botones)
        self.setLayout(layout)
#Método para obtener los datos ingresados.
    def get_data(self):
        grupo_id = self.datos_grupo[0] if self.datos_grupo else None
        
        return (
            grupo_id,
            self.campo_nombre.text().strip(),
            self.campo_ciclo.text().strip()
        )

#Clase principal de la ventana de grupos.
class VentanaGrupos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DirectAula - Administrar Grupos")
        self.resize(600, 400)
        self.gestor = GestorGrupos() 
        self._inicializar_ui()
        self._cargar_datos()
#Inicialización de la interfaz de usuario.
    def _inicializar_ui(self):
        main_layout = QVBoxLayout()
        
        #TÍTULO PRINCIPAL
        lbl_titulo = QLabel("DirectAula - Administración de Grupos")
        lbl_titulo.setObjectName("titulo_principal")
        main_layout.addWidget(lbl_titulo)
        
        #Botones
        top_bar_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("➕ Agregar Grupo")
        self.btn_agregar.setObjectName("btn_agregar")
        self.btn_agregar.clicked.connect(lambda: self._mostrar_formulario(None))
        
        self.btn_editar = QPushButton("✏️ Editar Grupo")
        self.btn_editar.setObjectName("btn_editar")
        self.btn_editar.clicked.connect(self._mostrar_formulario_editar)

        self.btn_eliminar = QPushButton("🗑️ Eliminar Grupo")
        self.btn_eliminar.setObjectName("btn_eliminar")
        self.btn_eliminar.clicked.connect(self._eliminar_grupo_seleccionado)
        #Añadir botones al layout superior
        top_bar_layout.addWidget(self.btn_agregar)
        top_bar_layout.addWidget(self.btn_editar)
        top_bar_layout.addWidget(self.btn_eliminar)
#Barra superior con botones
        main_layout.addLayout(top_bar_layout)

        #Tabla de grupos
        lbl_subtitulo = QLabel("Lista de Grupos Registrados")
        lbl_subtitulo.setProperty("class", "subtitulo")
        main_layout.addWidget(lbl_subtitulo)
        #Tabla de grupos
        self.tabla_grupos = QTableWidget() 
        self.tabla_grupos.setColumnCount(3) 
        self.tabla_grupos.setHorizontalHeaderLabels(["ID", "Nombre del Grupo", "Ciclo Escolar"])
        self.tabla_grupos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.tabla_grupos.setColumnHidden(0, True) #Ocultar la columna ID
        main_layout.addWidget(self.tabla_grupos)

        self.setLayout(main_layout)

#Carga de datos en la tabla
    def _cargar_datos(self):
        datos = self.gestor.obtener_lista_grupos() # [id, nombre, ciclo]
        
        self.tabla_grupos.setRowCount(0) 
        #Insertar filas con los datos obtenidos
        for fila_indice, grupo_data in enumerate(datos):
            self.tabla_grupos.insertRow(fila_indice)
            
            #Insertamos las 3 columnas (ID, Nombre, Ciclo Escolar)
            for columna, valor in enumerate(grupo_data):
                item = QTableWidgetItem(str(valor))
                self.tabla_grupos.setItem(fila_indice, columna, item)
    
    #Mostrar formulario para agregar o editar grupo
    def _mostrar_formulario(self, datos_grupo=None):
        dialogo = DialogoGrupo(datos_grupo, self)
        if dialogo.exec_() == QDialog.Accepted:
            
            grupo_id, nombre, ciclo = dialogo.get_data() 
            
            if grupo_id is None:
                #Lógica Agregar
                resultado_mensaje = self.gestor.agregar_nuevo_grupo(nombre, ciclo) 
            else:
                #Lógica Editar
                resultado_mensaje = self.gestor.actualizar_datos_grupo(grupo_id, nombre, ciclo) 
            
            if "Error" in resultado_mensaje:
                QMessageBox.critical(self, "Error", resultado_mensaje) 
            else:
                QMessageBox.information(self, "Operación Exitosa", resultado_mensaje)
                self._cargar_datos() 

    def _mostrar_formulario_editar(self):
        #Prepara los datos de la fila seleccionada
        fila_seleccionada = self.tabla_grupos.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un grupo para editar.")
            return
        #Obtenemos ID, Nombre y Ciclo
        datos_seleccionados = [
            int(self.tabla_grupos.item(fila_seleccionada, 0).text()), #ID (Oculto)
            self.tabla_grupos.item(fila_seleccionada, 1).text(),       #Nombre
            self.tabla_grupos.item(fila_seleccionada, 2).text()        #Ciclo
        ]
        
        self._mostrar_formulario(datos_seleccionados)
     #Método para eliminar el grupo seleccionado   
    def _eliminar_grupo_seleccionado(self):
        fila_seleccionada = self.tabla_grupos.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un grupo para eliminar.")
            return
        
        grupo_id = int(self.tabla_grupos.item(fila_seleccionada, 0).text())
        nombre_grupo = self.tabla_grupos.item(fila_seleccionada, 1).text()
        
        confirmacion = QMessageBox.question(self, "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar permanentemente el grupo '{nombre_grupo}'? (BR.2)",
            QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            resultado_mensaje = self.gestor.eliminar_grupo(grupo_id)
            
            if "Error" in resultado_mensaje:
                QMessageBox.critical(self, "Error de Eliminación", resultado_mensaje)
            else:
                QMessageBox.information(self, "Operación Exitosa", resultado_mensaje)
                self._cargar_datos()