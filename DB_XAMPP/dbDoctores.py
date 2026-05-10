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

# SI VAN A USAR POSTGRES (O YA LO TIENEN LISTO) CAMBIEN EL NOMBRE DEL ARCHIVO A LLAMAR
from dbConfigXAMPP import obtener_conexion, liberar_conexion
#from dbConfig import obtener_conexion, liberar_conexion

class DBDoctor:
    """Clase para manejar operaciones de base de datos de doctores"""
    
    @staticmethod
    def insertar_doctor(datos):
        """
        Inserta un nuevo doctor en la base de datos
        
        Args:
            datos (dict): Diccionario con los datos del doctor
            
        Returns:
            tuple: (éxito: bool, mensaje: str, id_doctor: int o None)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos", None)
        
        try:
            cursor = conexion.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT id_doctor FROM doctores WHERE usuario = %s",
                (datos['usuario'],)
            )
            
            if cursor.fetchone():
                cursor.close()
                return (False, "El usuario ya existe en el sistema", None)
            
            # Insertar doctor - SIN RETURNING (eso es de PostgreSQL)
            query = """
                INSERT INTO doctores 
                (nombre, direccion, telefono, fecha_nacimiento, sexo, 
                 especialidad, contrasena, usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            valores = (
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['fecha_nacimiento'],
                datos['sexo'],
                datos['especialidad'],
                datos['contrasena'],
                datos['usuario']
            )
            
            cursor.execute(query, valores)
            # En MySQL usamos lastrowid en lugar de RETURNING
            id_doctor = cursor.lastrowid
            conexion.commit()
            cursor.close()
            
            return (True, "Doctor insertado exitosamente", id_doctor)
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al insertar doctor: {str(e)}", None)
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_todos_doctores():
        """
        Obtiene todos los doctores activos de la base de datos
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_doctor, nombre, direccion, telefono, 
                       fecha_nacimiento, sexo, especialidad, usuario,
                       fecha_registro
                FROM doctores
                WHERE activo = TRUE
                ORDER BY nombre
            """
            
            cursor.execute(query)
            doctores = cursor.fetchall()
            cursor.close()
            
            # Convertir a lista de diccionarios
            doctores_list = []
            for doc in doctores:
                doctores_list.append({
                    'id_doctor': doc[0],
                    'nombre': doc[1],
                    'direccion': doc[2],
                    'telefono': doc[3],
                    'fecha_nacimiento': doc[4],
                    'sexo': doc[5],
                    'especialidad': doc[6],
                    'usuario': doc[7],
                    'fecha_registro': doc[8]
                })
            
            return (True, doctores_list)
            
        except Exception as e:
            return (False, f"Error al obtener doctores: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_doctor_por_id(id_doctor):
        """
        Obtiene un doctor específico por su ID
        
        Args:
            id_doctor (int): ID del doctor
            
        Returns:
            tuple: (éxito: bool, datos: dict o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_doctor, nombre, direccion, telefono, 
                       fecha_nacimiento, sexo, especialidad, usuario
                FROM doctores
                WHERE id_doctor = %s AND activo = TRUE
            """
            
            cursor.execute(query, (id_doctor,))
            doc = cursor.fetchone()
            cursor.close()
            
            if doc:
                doctor = {
                    'id_doctor': doc[0],
                    'nombre': doc[1],
                    'direccion': doc[2],
                    'telefono': doc[3],
                    'fecha_nacimiento': doc[4],
                    'sexo': doc[5],
                    'especialidad': doc[6],
                    'usuario': doc[7]
                }
                return (True, doctor)
            else:
                return (False, "Doctor no encontrado")
            
        except Exception as e:
            return (False, f"Error al obtener doctor: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_doctor(id_doctor, datos):
        """
        Actualiza los datos de un doctor
        
        Args:
            id_doctor (int): ID del doctor
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
                UPDATE doctores
                SET nombre = %s, direccion = %s, telefono = %s,
                    fecha_nacimiento = %s, sexo = %s, especialidad = %s
                WHERE id_doctor = %s AND activo = TRUE
            """
            
            valores = (
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['fecha_nacimiento'],
                datos['sexo'],
                datos['especialidad'],
                id_doctor
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Doctor actualizado exitosamente")
            else:
                cursor.close()
                return (False, "Doctor no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al actualizar doctor: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def eliminar_doctor(id_doctor):
        """
        Realiza un borrado lógico del doctor (activo = FALSE)
        
        Args:
            id_doctor (int): ID del doctor
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = "UPDATE doctores SET activo = FALSE WHERE id_doctor = %s"
            cursor.execute(query, (id_doctor,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Doctor eliminado exitosamente")
            else:
                cursor.close()
                return (False, "Doctor no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al eliminar doctor: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_especialidades():
        """
        Obtiene lista de especialidades únicas
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT DISTINCT especialidad 
                FROM doctores 
                WHERE activo = TRUE
                ORDER BY especialidad
            """
            
            cursor.execute(query)
            especialidades = [row[0] for row in cursor.fetchall()]
            cursor.close()
            
            return (True, especialidades)
            
        except Exception as e:
            return (False, f"Error al obtener especialidades: {str(e)}")
        finally:
            liberar_conexion(conexion)