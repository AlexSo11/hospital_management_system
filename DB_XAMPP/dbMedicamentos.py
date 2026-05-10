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
from dbConfigXAMPP import obtener_conexion, liberar_conexion
from datetime import datetime

class DBMedicamentos:
    """Clase para manejar operaciones de base de datos de medicamentos"""
    
    @staticmethod
    def insertar_medicamento(datos):
        """
        Inserta un nuevo medicamento en la base de datos
        
        Args:
            datos (dict): Diccionario con los datos del medicamento
            
        Returns:
            tuple: (éxito: bool, mensaje: str, id_medicamento: int o None)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos", None)
        
        try:
            cursor = conexion.cursor()
            
            # Verificar si el medicamento ya existe
            cursor.execute(
                "SELECT id_medicamento FROM medicamentos WHERE nombre = %s AND activo = TRUE",
                (datos['nombre'],)
            )
            
            if cursor.fetchone():
                cursor.close()
                return (False, "Ya existe un medicamento con ese nombre", None)
            
            # Insertar medicamento
            query = """
                INSERT INTO medicamentos 
                (nombre, via_administracion, presentacion, fecha_caducidad)
                VALUES (%s, %s, %s, %s)
            """
            
            valores = (
                datos['nombre'],
                datos['via_administracion'],
                datos['presentacion'],
                datos['fecha_caducidad']
            )
            
            cursor.execute(query, valores)
            id_medicamento = cursor.lastrowid
            conexion.commit()
            cursor.close()
            
            return (True, "Medicamento insertado exitosamente", id_medicamento)
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al insertar medicamento: {str(e)}", None)
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_todos_medicamentos():
        """
        Obtiene todos los medicamentos activos de la base de datos
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_medicamento, nombre, via_administracion, 
                       presentacion, fecha_caducidad, fecha_registro
                FROM medicamentos
                WHERE activo = TRUE
                ORDER BY nombre
            """
            
            cursor.execute(query)
            medicamentos = cursor.fetchall()
            cursor.close()
            
            # Convertir a lista de diccionarios
            medicamentos_list = []
            for med in medicamentos:
                medicamentos_list.append({
                    'id_medicamento': med[0],
                    'nombre': med[1],
                    'via_administracion': med[2],
                    'presentacion': med[3],
                    'fecha_caducidad': med[4],
                    'fecha_registro': med[5]
                })
            
            return (True, medicamentos_list)
            
        except Exception as e:
            return (False, f"Error al obtener medicamentos: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_medicamento_por_id(id_medicamento):
        """
        Obtiene un medicamento específico por su ID
        
        Args:
            id_medicamento (int): ID del medicamento
            
        Returns:
            tuple: (éxito: bool, datos: dict o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_medicamento, nombre, via_administracion, 
                       presentacion, fecha_caducidad
                FROM medicamentos
                WHERE id_medicamento = %s AND activo = TRUE
            """
            
            cursor.execute(query, (id_medicamento,))
            med = cursor.fetchone()
            cursor.close()
            
            if med:
                medicamento = {
                    'id_medicamento': med[0],
                    'nombre': med[1],
                    'via_administracion': med[2],
                    'presentacion': med[3],
                    'fecha_caducidad': med[4]
                }
                return (True, medicamento)
            else:
                return (False, "Medicamento no encontrado")
            
        except Exception as e:
            return (False, f"Error al obtener medicamento: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_medicamento(id_medicamento, datos):
        """
        Actualiza los datos de un medicamento
        
        Args:
            id_medicamento (int): ID del medicamento
            datos (dict): Diccionario con los datos a actualizar
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                UPDATE medicamentos
                SET nombre = %s, via_administracion = %s, presentacion = %s,
                    fecha_caducidad = %s
                WHERE id_medicamento = %s AND activo = TRUE
            """
            
            valores = (
                datos['nombre'],
                datos['via_administracion'],
                datos['presentacion'],
                datos['fecha_caducidad'],
                id_medicamento
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Medicamento actualizado exitosamente")
            else:
                cursor.close()
                return (False, "Medicamento no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al actualizar medicamento: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def eliminar_medicamento(id_medicamento):
        """
        Realiza un borrado lógico del medicamento (activo = FALSE)
        
        Args:
            id_medicamento (int): ID del medicamento
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = "UPDATE medicamentos SET activo = FALSE WHERE id_medicamento = %s"
            cursor.execute(query, (id_medicamento,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Medicamento eliminado exitosamente")
            else:
                cursor.close()
                return (False, "Medicamento no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al eliminar medicamento: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_medicamentos_proximos_vencer(dias=30):
        """
        Obtiene medicamentos que vencen en los próximos X días
        
        Args:
            dias (int): Número de días para el filtro
            
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_medicamento, nombre, via_administracion, 
                       presentacion, fecha_caducidad,
                       DATEDIFF(fecha_caducidad, CURDATE()) as dias_restantes
                FROM medicamentos
                WHERE activo = TRUE 
                AND fecha_caducidad >= CURDATE()
                AND fecha_caducidad <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                ORDER BY fecha_caducidad
            """
            
            cursor.execute(query, (dias,))
            medicamentos = cursor.fetchall()
            cursor.close()
            
            medicamentos_list = []
            for med in medicamentos:
                medicamentos_list.append({
                    'id_medicamento': med[0],
                    'nombre': med[1],
                    'via_administracion': med[2],
                    'presentacion': med[3],
                    'fecha_caducidad': med[4],
                    'dias_restantes': med[5]
                })
            
            return (True, medicamentos_list)
            
        except Exception as e:
            return (False, f"Error al obtener medicamentos por vencer: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_medicamentos_vencidos():
        """
        Obtiene medicamentos que ya vencieron
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_medicamento, nombre, via_administracion, 
                       presentacion, fecha_caducidad,
                       DATEDIFF(CURDATE(), fecha_caducidad) as dias_vencido
                FROM medicamentos
                WHERE activo = TRUE 
                AND fecha_caducidad < CURDATE()
                ORDER BY fecha_caducidad DESC
            """
            
            cursor.execute(query)
            medicamentos = cursor.fetchall()
            cursor.close()
            
            medicamentos_list = []
            for med in medicamentos:
                medicamentos_list.append({
                    'id_medicamento': med[0],
                    'nombre': med[1],
                    'via_administracion': med[2],
                    'presentacion': med[3],
                    'fecha_caducidad': med[4],
                    'dias_vencido': med[5]
                })
            
            return (True, medicamentos_list)
            
        except Exception as e:
            return (False, f"Error al obtener medicamentos vencidos: {str(e)}")
        finally:
            liberar_conexion(conexion)