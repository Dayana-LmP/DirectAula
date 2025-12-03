# DirectAula - Sistema de Gestión Escolar para Docentes


## Resumen del Proyecto

**DirectAula** es una aplicación de escritorio diseñada para facilitar la gestión académica y administrativa de grupos escolares. Permite a los docentes registrar asistencias, administrar calificaciones por ponderación y monitorear el estado de riesgo de sus alumnos (académico y de asistencia) en tiempo real.

Este repositorio contiene el código fuente final del proyecto.

## Funcionalidades Principales

El sistema está organizado en módulos que permiten una gestión integral de la clase:

### Módulo de Autenticación
* **Inicio de Sesión:** Acceso seguro para usuarios registrados.
* **Crear Cuenta:** Registro de nuevos docentes.

### Módulo de Alumnos y Grupos
* **Administrar Grupos:** Creación y gestión de grupos por ciclo escolar.
* **Administrar Alumnos:** Alta, baja y edición de la información de contacto y matriculación de los estudiantes.

### Módulo de Asistencia
* **Registrar Asistencia (UC-4):** Toma de asistencia rápida y visual para el control diario.

### Módulo de Calificaciones
* **Administrar Ponderación:** Definición del peso porcentual de cada categoría de evaluación (tareas, exámenes, proyectos, etc.).
* **Registrar Calificaciones:** Ingreso de notas por alumno, categoría y fecha.
* **Calificación Final y Estado de Riesgo:**
    * Cálculo automático de la calificación final ponderada.
    * **Alertas de Riesgo Académico:** Alumno con calificación final menor a **7**.
    * **Alertas de Riesgo de Asistencia:** Alumno con porcentaje de asistencia menor al **80%**.

### Módulo de Reportes
* **Exportar Datos:** Funcionalidad para generar y exportar reportes de calificaciones y asistencia en formatos estándar (ej. CSV, Excel).

## Tecnologías Utilizadas

* **Lenguaje:** Python
* **Base de Datos:** SQLite (Manejada a través de `dao.py`)
* **Framework (UI/GUI):** [Asumir el framework de tu aplicación, ej: Tkinter, PyQt, Kivy, etc. Si no lo sabes, dejarlo genérico o omitirlo.]
* **Empaquetado:** PyInstaller

## Estructura del Repositorio

La versión final del código se encuentra en la siguiente estructura de carpetas:

* `Carpeta de ADOO para subir a GitHub`: Contiene el código fuente (`main.py`, `dao.py`, etc.).
    * `style.css`: Archivo de estilos de la interfaz de usuario.
    * `directaula.db`: Archivo de base de datos SQLite.
* `.gitignore`: Reglas para ignorar archivos generados (como las carpetas `build/` y `dist/`).

## Instalación y Ejecución

### 1. Requisitos

Asegúrate de tener instalado Python 3.x.

### 2. Clonar el Repositorio

Clonar la rama `final` que contiene el código completo:

```bash
git clone -b final [https://github.com/Dayana-LmP/DirectAula.git](https://github.com/Dayana-LmP/DirectAula.git)
cd DirectAula/DirectAula_Apps_final_finalisimo