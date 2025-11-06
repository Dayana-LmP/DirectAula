# test_app.py - Prueba simplificada
import sys
import os

print("🔍 Verificando dependencias...")

try:
    from PyQt5.QtWidgets import QApplication
    print("✅ PyQt5 está instalado correctamente")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("💡 Ejecuta: pip install PyQt5")
    sys.exit(1)

try:
    from data_access.database import Database
    from presentation.main_window import main
    print("✅ Todos los imports funcionan")
    print("🚀 Iniciando aplicación...")
    main()
except Exception as e:
    print(f"❌ Error al iniciar: {e}")
    input("Presiona Enter para salir...")