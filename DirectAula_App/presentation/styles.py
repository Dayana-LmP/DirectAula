# presentation/styles.py

def get_styles():
    return """
    /* Paleta de colores DirectAula */
    QMainWindow {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QWidget {
        background-color: #f8f9fa;
    }
    
    /* BARRA SUPERIOR */
    QLabel#titulo {
        color: #2c3e50;
        font-size: 24px;
        font-weight: bold;
        padding: 15px;
        background-color: #ffffff;
        border-bottom: 3px solid #3498db;
    }
    
    /* BARRA DE BÚSQUEDA Y BOTONES */
    QLineEdit {
        padding: 10px;
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        font-size: 14px;
        background-color: white;
    }
    
    QLineEdit:focus {
        border-color: #3498db;
        background-color: #ecf0f1;
    }
    
    QPushButton {
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        color: white;
        margin: 5px;
    }
    
    QPushButton:hover {
        opacity: 0.9;
    }
    
    /* BOTONES DE COLORES */
    QPushButton#btn_agregar {
        background-color: #27ae60;  /* VERDE */
    }
    
    QPushButton#btn_editar {
        background-color: #f39c12;  /* NARANJA */
    }
    
    QPushButton#btn_eliminar {
        background-color: #e74c3c;  /* ROJO */
    }
    
    QPushButton#btn_buscar {
        background-color: #3498db;  /* AZUL */
    }
    
    QPushButton#btn_exportar {
        background-color: #9b59b6;  /* MORADO */
    }
    
    /* TABLA DE ALUMNOS */
    QTableWidget {
        background-color: white;
        border: 1px solid #bdc3c7;
        border-radius: 8px;
        gridline-color: #ecf0f1;
        font-size: 14px;
    }
    
    QTableWidget::item {
        padding: 12px;
        border-bottom: 1px solid #ecf0f1;
    }
    
    QTableWidget::item:selected {
        background-color: #3498db;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #2c3e50;
        color: white;
        padding: 12px;
        border: none;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* FORMULARIOS */
    QDialog {
        background-color: #f8f9fa;
    }
    
    QFormLayout QLabel {
        color: #2c3e50;
        font-weight: bold;
        font-size: 14px;
    }
    
    /* BARRA DE ESTADO */
    QStatusBar {
        background-color: #34495e;
        color: white;
        padding: 5px;
    }
    
    /* GROUP BOXES */
    QGroupBox {
        font-weight: bold;
        font-size: 16px;
        color: #2c3e50;
        border: 2px solid #bdc3c7;
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
    """