"""
Equipo 6

LISTA DE INTEGRANTES (ordenados alfabéticamente por apellidos)
Rizzoli Domínguez Carlos Daniel
Rodriguez Macias Juan Diego
Solís Quiñones Héctor Alejandro
Solís Regín Juan Pablo
Vazquez Delgado Kevin
Verduzco Rosales Luis Enrique

Materia: Bases de Datos
Clave: IL356          Sección: D02
NRC: 204855                 2025 B

NOMBRE DEL PROFESOR:  Mariscal Lugo Luis Felipe


Script de depuración para detectar problemas
"""

import sys
import traceback

print("=" * 60)
print("INICIANDO DEPURACIÓN DE LA APLICACIÓN")
print("=" * 60)

# Paso 1: Verificar imports
print("\n1. Verificando imports...")
try:
    import tkinter as tk
    print("   ✓ tkinter OK")
except Exception as e:
    print(f"   ✗ Error con tkinter: {e}")
    sys.exit(1)

try:
    from tkinter import ttk, messagebox
    print("   ✓ ttk y messagebox OK")
except Exception as e:
    print(f"   ✗ Error con ttk/messagebox: {e}")
    sys.exit(1)

try:
    import mysql.connector
    print("   ✓ mysql.connector OK")
except Exception as e:
    print(f"   ✗ Error con mysql.connector: {e}")
    print("   Instala: pip install mysql-connector-python")
    sys.exit(1)

try:
    from tkcalendar import DateEntry
    print("   ✓ tkcalendar OK")
except Exception as e:
    print(f"   ✗ Error con tkcalendar: {e}")
    print("   Instala: pip install tkcalendar")
    sys.exit(1)

# Paso 2: Verificar configuración de base de datos
print("\n2. Verificando configuración de base de datos...")
try:
    from dbConfigXAMPP import DatabaseConfig
    print("   ✓ dbConfigXAMPP importado correctamente")
    print(f"   Host: {DatabaseConfig.DB_CONFIG['host']}")
    print(f"   Database: {DatabaseConfig.DB_CONFIG['database']}")
    print(f"   User: {DatabaseConfig.DB_CONFIG['user']}")
    print(f"   Port: {DatabaseConfig.DB_CONFIG['port']}")
except Exception as e:
    print(f"   ✗ Error al importar dbConfigXAMPP: {e}")
    traceback.print_exc()
    sys.exit(1)

# Paso 3: Probar conexión a la base de datos
print("\n3. Probando conexión a MySQL...")
try:
    if DatabaseConfig.inicializar_pool():
        print("   ✓ Conexión exitosa!")
        
        # Probar obtener una conexión
        from dbConfigXAMPP import obtener_conexion, liberar_conexion
        conn = obtener_conexion()
        if conn:
            print("   ✓ Pool funcionando correctamente")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"   ✓ Base de datos activa: {db_name}")
            cursor.close()
            liberar_conexion(conn)
        else:
            print("   ✗ No se pudo obtener conexión del pool")
            sys.exit(1)
    else:
        print("   ✗ No se pudo inicializar el pool")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Error en conexión: {e}")
    traceback.print_exc()
    sys.exit(1)

# Paso 4: Verificar que existan las tablas
print("\n4. Verificando tablas en la base de datos...")
try:
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    tablas_requeridas = ['administrador', 'empleados', 'doctores']
    cursor.execute("SHOW TABLES")
    tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]
    
    print(f"   Tablas encontradas: {len(tablas_existentes)}")
    
    falta_algo = False
    for tabla in tablas_requeridas:
        if tabla in tablas_existentes:
            print(f"   ✓ {tabla}")
        else:
            print(f"   ✗ {tabla} - NO EXISTE")
            falta_algo = True
    
    if falta_algo:
        print("\n   FALTAN TABLAS!")
        print("   Ejecuta el script DBhospitalXAMPP.sql en phpMyAdmin")
        cursor.close()
        liberar_conexion(conn)
        sys.exit(1)
    
    cursor.close()
    liberar_conexion(conn)
    
except Exception as e:
    print(f"   ✗ Error verificando tablas: {e}")
    traceback.print_exc()
    sys.exit(1)

# Paso 5: Verificar datos de administrador
print("\n5. Verificando datos de administrador...")
try:
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM administrador")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"   ✓ Se encontraron {count} administrador(es)")
        cursor.execute("SELECT usuario FROM administrador LIMIT 1")
        usuario = cursor.fetchone()[0]
        print(f"   ✓ Usuario de prueba: {usuario}")
    else:
        print("   ✗ NO hay administradores en la base de datos")
        print("   La aplicación no podrá hacer login")
        print("   Ejecuta: INSERT INTO administrador (usuario, contrasena, nombre)")
        print("            VALUES ('admin', 'admin123', 'Admin');")
    
    cursor.close()
    liberar_conexion(conn)
    
except Exception as e:
    print(f"   ✗ Error verificando administrador: {e}")
    traceback.print_exc()

# Paso 6: Intentar importar los módulos principales
print("\n6. Verificando módulos de la aplicación...")
modulos = [
    ('login', 'LoginWindow'),
    ('menuAdmin', 'MenuAdministrador'),
    ('DB.dbEmpleados', 'DBEmpleado'),
    ('DB.dbDoctores', 'DBDoctor'),
    ('UI.empleados', 'UIEmpleados'),
    ('UI.doctores', 'UIDoctores')
]

errores_import = []
for modulo, clase in modulos:
    try:
        exec(f"from {modulo} import {clase}")
        print(f"   ✓ {modulo}.{clase}")
    except Exception as e:
        print(f"   ✗ {modulo}.{clase} - ERROR: {e}")
        errores_import.append((modulo, clase, e))

if errores_import:
    print("\n ERRORES DE IMPORTACIÓN:")
    for modulo, clase, error in errores_import:
        print(f"\n   Módulo: {modulo}")
        print(f"   Clase: {clase}")
        print(f"   Error: {error}")

# Paso 7: Intentar ejecutar la aplicación
print("\n7. Intentando ejecutar la aplicación...")
if not errores_import:
    print("   Todos los imports están OK")
    print("   Ejecutando: python app.py")
    print("\n" + "=" * 60)
    print("SI VES ESTE MENSAJE, LA APLICACIÓN DEBERÍA FUNCIONAR")
    print("=" * 60)
    
    # Intentar ejecutar
    try:
        print("\nIniciando aplicación...")
        import app
        app_instance = app.App()
        print("✓ Ventana de login debería aparecer")
        app_instance.run()
    except Exception as e:
        print(f"\n✗ Error al ejecutar app.py: {e}")
        traceback.print_exc()
else:
    print("\n✗ NO se puede ejecutar la aplicación debido a errores de importación")
    print("   Revisa la estructura de carpetas:")
    print("\n   proyecto/")
    print("   ├── app.py")
    print("   ├── dbConfigXAMPP.py")
    print("   ├── login.py")
    print("   ├── menuAdmin.py")
    print("   ├── DB/")
    print("   │   ├── __init__.py")
    print("   │   ├── dbEmpleados.py")
    print("   │   └── dbDoctores.py")
    print("   └── UI/")
    print("       ├── __init__.py")
    print("       ├── empleados.py")
    print("       └── doctores.py")
    print("\n   IMPORTANTE: Las carpetas DB/ y UI/ deben tener __init__.py vacío")