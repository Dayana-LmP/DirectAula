# presentacion/ventana_ponderacion.py (NUEVO ARCHIVO)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from Logica.gestor_alumnos import GestorCalificaciones 

class VentanaPonderacion(QWidget):
    """Ventana para el Caso de Uso 3: Administrar Ponderación."""

    def __init__(self, grupo_id, nombre_grupo, parent=None):
        super().__init__(parent)
        self._grupo_id = grupo_id
        self._nombre_grupo = nombre_grupo
        self.gestor = GestorCalificaciones(grupo_id)
        self.setWindowTitle(f"Ponderación - {nombre_grupo}")
        self.resize(450, 400)
        self._inicializar_ui()
        self._cargar_datos()

    def _inicializar_ui(self):
        main_layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel(f"Ponderación de Calificaciones: {self._nombre_grupo}")
        lbl_titulo.setObjectName("titulo_principal")
        main_layout.addWidget(lbl_titulo)
        
        # Formulario de pesos
        form_layout = QFormLayout()
        
        self.peso_asistencia = QLineEdit()
        self.peso_examen = QLineEdit()
        self.peso_participacion = QLineEdit()
        self.peso_tareas = QLineEdit()
        self.total_tareas = QLineEdit() # Total de Tareas a Considerar
        
        # Conexión para actualizar la suma al escribir
        self.peso_asistencia.textChanged.connect(self._actualizar_suma)
        self.peso_examen.textChanged.connect(self._actualizar_suma)
        self.peso_participacion.textChanged.connect(self._actualizar_suma)
        self.peso_tareas.textChanged.connect(self._actualizar_suma)
        
        form_layout.addRow("Asistencia (%)", self.peso_asistencia)
        form_layout.addRow("Examen (%)", self.peso_examen)
        form_layout.addRow("Participación (%)", self.peso_participacion)
        form_layout.addRow("Tareas (%)", self.peso_tareas)
        form_layout.addRow("Total de Tareas a Considerar", self.total_tareas)
        
        main_layout.addLayout(form_layout)
        
        # Indicador visual de la suma actual (FE.1)
        self.lbl_suma = QLabel("Suma Actual: 0.0%")
        self.lbl_suma.setObjectName("subtitulo")
        main_layout.addWidget(self.lbl_suma)

        # Botones
        btn_layout = QHBoxLayout()
        
        btn_restaurar = QPushButton("Restaurar Predeterminado (FA.1)")
        btn_restaurar.clicked.connect(self._restaurar_predeterminado)
        btn_layout.addWidget(btn_restaurar)
        
        btn_guardar = QPushButton("Guardar Ponderación")
        btn_guardar.setObjectName("btn_agregar")
        btn_guardar.clicked.connect(self._guardar_ponderacion)
        btn_layout.addWidget(btn_guardar)
        
        main_layout.addLayout(btn_layout)

    def _cargar_datos(self):
        # Retorna: (asist, examen, part, tareas, total_tareas)
        asist, examen, part, tareas, total_tareas = self.gestor.obtener_ponderacion_actual()
        
        self.peso_asistencia.setText(str(asist))
        self.peso_examen.setText(str(examen))
        self.peso_participacion.setText(str(part))
        self.peso_tareas.setText(str(tareas))
        self.total_tareas.setText(str(total_tareas))
        
        self._actualizar_suma()

    def _actualizar_suma(self):
        # 4. El Sistema muestra un indicador visual de la suma actual de todas las ponderaciones.
        try:
            p_asist = float(self.peso_asistencia.text() or 0)
            p_examen = float(self.peso_examen.text() or 0)
            p_part = float(self.peso_participacion.text() or 0)
            p_tareas = float(self.peso_tareas.text() or 0)
            suma = p_asist + p_examen + p_part + p_tareas
            self.lbl_suma.setText(f"Suma Actual: {suma:.1f}%")
            if suma != 100:
                self.lbl_suma.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.lbl_suma.setStyleSheet("color: green; font-weight: bold;")
        except ValueError:
            self.lbl_suma.setText("Suma Actual: Inválida (Valores no numéricos)")
            self.lbl_suma.setStyleSheet("color: red; font-weight: bold;")

    def _restaurar_predeterminado(self):
        # 4.2. El Sistema carga los valores originales definidos por defecto.
        self.peso_asistencia.setText("10.0")
        self.peso_examen.setText("40.0")
        self.peso_participacion.setText("10.0")
        self.peso_tareas.setText("40.0")
        self.total_tareas.setText("10")
        self._actualizar_suma()
        QMessageBox.information(self, "Restaurado", "Valores predeterminados cargados.")

    def _guardar_ponderacion(self):
        try:
            asist = float(self.peso_asistencia.text())
            examen = float(self.peso_examen.text())
            part = float(self.peso_participacion.text())
            tareas = float(self.peso_tareas.text())
            total = int(self.total_tareas.text())
            
            # FE.1: La validación del 100% se realiza en el BLL, pero si falló
            # el indicador visual ya lo mostró.
            
            # FE.2: Modificación con promedios ya calculados
            alerta_promedios = QMessageBox.question(self, "Recálculo de Promedios (FE.2)",
                "Al modificar la ponderación, todos los promedios finales de este grupo serán recalculados. ¿Desea continuar?",
                QMessageBox.Yes | QMessageBox.Cancel
            )
            
            if alerta_promedios == QMessageBox.Cancel:
                return # 5.2.b. Si el Docente cancela, termina el caso de uso.
                
            # 6. El Sistema guarda y recalcula
            resultado = self.gestor.guardar_ponderacion(asist, examen, part, tareas, total)
            
            if "Error" in resultado:
                QMessageBox.critical(self, "Error de Ponderación", resultado)
            else:
                QMessageBox.information(self, "Éxito (7)", resultado)
                self.close() 
                
        except ValueError:
            QMessageBox.critical(self, "Error de Datos", "Asegúrese de que todos los pesos son números (ej. 10.0) y el total de tareas es un número entero.")