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

class DBPacientes:
    """Clase para manejar operaciones de base de datos de pacientes"""
    
    @staticmethod
    def verificar_telefono_existente(telefono):
        """Verifica si ya existe un paciente con el mismo teléfono"""
        conexion = obtener_conexion()
        if not conexion:
            return False
        
        cursor = None
        try:
            cursor = conexion.cursor(buffered=True)
            
            query = "SELECT id_paciente FROM pacientes WHERE telefono = %s AND activo = TRUE"
            cursor.execute(query, (telefono,))
            resultado = cursor.fetchone()
            
            return resultado is not None  
            
        except Exception as e:
            print(f"Error al verificar teléfono: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            liberar_conexion(conexion)
    
    @staticmethod
    def insertar_paciente(datos):
        """
        Inserta un nuevo paciente en la base de datos
        
        Args:
            datos (dict): Diccionario con los datos del paciente
            
        Returns:
            tuple: (éxito: bool, mensaje: str, id_paciente: int o None)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos", None)
        
        try:
            cursor = conexion.cursor()
            
            # Insertar paciente
            query = """
                INSERT INTO pacientes 
                (nombre, direccion, telefono, fecha_nacimiento, sexo, 
                 edad, estatura)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            valores = (
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['fecha_nacimiento'],
                datos['sexo'],
                datos['edad'],
                datos['estatura']
            )
            
            cursor.execute(query, valores)
            id_paciente = cursor.lastrowid
            conexion.commit()
            cursor.close()
            
            return (True, "Paciente insertado exitosamente", id_paciente)
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al insertar paciente: {str(e)}", None)
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_todos_pacientes():
        """
        Obtiene todos los pacientes activos de la base de datos
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_paciente, nombre, direccion, telefono, 
                       fecha_nacimiento, sexo, edad, estatura,
                       fecha_registro
                FROM pacientes
                WHERE activo = TRUE
                ORDER BY nombre
            """
            
            cursor.execute(query)
            pacientes = cursor.fetchall()
            cursor.close()
            
            # Convertir a lista de diccionarios
            pacientes_list = []
            for pac in pacientes:
                pacientes_list.append({
                    'id_paciente': pac[0],
                    'nombre': pac[1],
                    'direccion': pac[2],
                    'telefono': pac[3],
                    'fecha_nacimiento': pac[4],
                    'sexo': pac[5],
                    'edad': pac[6],
                    'estatura': pac[7],
                    'fecha_registro': pac[8]
                })
            
            return (True, pacientes_list)
            
        except Exception as e:
            return (False, f"Error al obtener pacientes: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_paciente_por_id(id_paciente):
        """
        Obtiene un paciente específico por su ID
        
        Args:
            id_paciente (int): ID del paciente
            
        Returns:
            tuple: (éxito: bool, datos: dict o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_paciente, nombre, direccion, telefono, 
                       fecha_nacimiento, sexo, edad, estatura
                FROM pacientes
                WHERE id_paciente = %s AND activo = TRUE
            """
            
            cursor.execute(query, (id_paciente,))
            pac = cursor.fetchone()
            cursor.close()
            
            if pac:
                paciente = {
                    'id_paciente': pac[0],
                    'nombre': pac[1],
                    'direccion': pac[2],
                    'telefono': pac[3],
                    'fecha_nacimiento': pac[4],
                    'sexo': pac[5],
                    'edad': pac[6],
                    'estatura': pac[7]
                }
                return (True, paciente)
            else:
                return (False, "Paciente no encontrado")
            
        except Exception as e:
            return (False, f"Error al obtener paciente: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_paciente(id_paciente, datos):
        """
        Actualiza los datos de un paciente
        
        Args:
            id_paciente (int): ID del paciente
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
                UPDATE pacientes
                SET nombre = %s, direccion = %s, telefono = %s,
                    fecha_nacimiento = %s, sexo = %s, edad = %s,
                    estatura = %s
                WHERE id_paciente = %s AND activo = TRUE
            """
            
            valores = (
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['fecha_nacimiento'],
                datos['sexo'],
                datos['edad'],
                datos['estatura'],
                id_paciente
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            cursor.close()
            
            if cursor.rowcount > 0:
                return (True, "Paciente actualizado exitosamente")
            else:
                return (False, "Paciente no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al actualizar paciente: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def eliminar_paciente(id_paciente):
        """
        Realiza un borrado lógico del paciente (activo = FALSE)
        
        Args:
            id_paciente (int): ID del paciente
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = "UPDATE pacientes SET activo = FALSE WHERE id_paciente = %s"
            cursor.execute(query, (id_paciente,))
            conexion.commit()
            cursor.close()
            
            if cursor.rowcount > 0:
                return (True, "Paciente eliminado exitosamente")
            else:
                return (False, "Paciente no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al eliminar paciente: {str(e)}")
        finally:
            liberar_conexion(conexion)