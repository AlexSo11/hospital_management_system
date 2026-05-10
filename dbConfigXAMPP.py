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
"""
import mysql.connector
from mysql.connector import pooling
from tkinter import messagebox

class DatabaseConfig:    
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'nucleo_diagnostico',
        'user': 'root',         
        'password': '',         
        'port': 3306
    }
    
    connection_pool = None
    
    @classmethod
    def inicializar_pool(cls):
        """Inicializa el pool de conexiones"""
        try:
            cls.connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=10,
                **cls.DB_CONFIG
            )
            print("✓ Pool de conexiones MySQL creado exitosamente")
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", 
                f"No se pudo conectar a la base de datos MySQL:\n{str(err)}")
            return False
    
    @classmethod
    def obtener_conexion(cls):
        """Obtiene una conexión del pool"""
        if cls.connection_pool is None:
            cls.inicializar_pool()
        
        try:
            return cls.connection_pool.get_connection()
        except mysql.connector.Error as err:
            print(f"Error al obtener conexión: {err}")
            return None
    
    @classmethod
    def liberar_conexion(cls, conexion):
        """Libera una conexión de vuelta al pool (cerrar = liberar en MySQL)"""
        if conexion:
            conexion.close()
    
    @classmethod
    def cerrar_pool(cls):
        """Cierra todas las conexiones del pool (opcional)"""
        if cls.connection_pool:
            cls.connection_pool = None
            print("✓ Pool de conexiones MySQL cerrado")


def obtener_conexion():
    """Función helper para obtener una conexión"""
    return DatabaseConfig.obtener_conexion()


def liberar_conexion(conexion):
    """Función helper para liberar una conexión"""
    DatabaseConfig.liberar_conexion(conexion)
