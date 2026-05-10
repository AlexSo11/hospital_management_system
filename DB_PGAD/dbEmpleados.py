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
from dbConfig import obtener_conexion, liberar_conexion

class DBEmpleado:
    """Clase para manejar operaciones de base de datos de empleados - PostgreSQL"""
    
    @staticmethod
    def insertar_empleado(datos):
        """
        Inserta un nuevo empleado en la base de datos
        
        Args:
            datos (dict): Diccionario con los datos del empleado
            
        Returns:
            tuple: (éxito: bool, mensaje: str, id_empleado: int o None)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos", None)
        
        try:
            cursor = conexion.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT id_empleado FROM empleados WHERE usuario = %s",
                (datos['usuario'],)
            )
            
            if cursor.fetchone():
                cursor.close()
                return (False, "El usuario ya existe en el sistema", None)
            
            # Insertar empleado con RETURNING (PostgreSQL)
            query = """
                INSERT INTO empleados 
                (nombre, direccion, telefono, fecha_nacimiento, sexo, 
                 sueldo, turno, contrasena, usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_empleado
            """
            
            valores = (
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['fecha_nacimiento'],
                datos['sexo'],
                datos['sueldo'],
                datos['turno'],
                datos['contrasena'],
                datos['usuario']
            )
            
            cursor.execute(query, valores)
            id_empleado = cursor.fetchone()[0]
            conexion.commit()
            cursor.close()
            
            return (True, "Empleado insertado exitosamente", id_empleado)
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al insertar empleado: {str(e)}", None)
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_todos_empleados():
        """
        Obtiene todos los empleados activos de la base de datos
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_empleado, nombre, direccion, telefono, 
                       fecha_nacimiento, sexo, sueldo, turno, usuario,
                       fecha_registro
                FROM empleados
                WHERE activo = TRUE
                ORDER BY nombre
            """
            
            cursor.execute(query)
            empleados = cursor.fetchall()
            cursor.close()
            
            # Convertir a lista de diccionarios
            empleados_list = []
            for emp in empleados:
                empleados_list.append({
                    'id_empleado': emp[0],
                    'nombre': emp[1],
                    'direccion': emp[2],
                    'telefono': emp[3],
                    'fecha_nacimiento': emp[4],
                    'sexo': emp[5],
                    'sueldo': emp[6],
                    'turno': emp[7],
                    'usuario': emp[8],
                    'fecha_registro': emp[9]
                })
            
            return (True, empleados_list)
            
        except Exception as e:
            return (False, f"Error al obtener empleados: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_empleado_por_id(id_empleado):
        """
        Obtiene un empleado específico por su ID
        
        Args:
            id_empleado (int): ID del empleado
            
        Returns:
            tuple: (éxito: bool, datos: dict o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_empleado, nombre, direccion, telefono, 
                       fecha_nacimiento, sexo, sueldo, turno, usuario
                FROM empleados
                WHERE id_empleado = %s AND activo = TRUE
            """
            
            cursor.execute(query, (id_empleado,))
            emp = cursor.fetchone()
            cursor.close()
            
            if emp:
                empleado = {
                    'id_empleado': emp[0],
                    'nombre': emp[1],
                    'direccion': emp[2],
                    'telefono': emp[3],
                    'fecha_nacimiento': emp[4],
                    'sexo': emp[5],
                    'sueldo': emp[6],
                    'turno': emp[7],
                    'usuario': emp[8]
                }
                return (True, empleado)
            else:
                return (False, "Empleado no encontrado")
            
        except Exception as e:
            return (False, f"Error al obtener empleado: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_empleado(id_empleado, datos):
        """
        Actualiza los datos de un empleado
        
        Args:
            id_empleado (int): ID del empleado
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
                UPDATE empleados
                SET nombre = %s, direccion = %s, telefono = %s,
                    fecha_nacimiento = %s, sexo = %s, sueldo = %s,
                    turno = %s
                WHERE id_empleado = %s AND activo = TRUE
            """
            
            valores = (
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['fecha_nacimiento'],
                datos['sexo'],
                datos['sueldo'],
                datos['turno'],
                id_empleado
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Empleado actualizado exitosamente")
            else:
                cursor.close()
                return (False, "Empleado no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al actualizar empleado: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def eliminar_empleado(id_empleado):
        """
        Realiza un borrado lógico del empleado (activo = FALSE)
        
        Args:
            id_empleado (int): ID del empleado
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = "UPDATE empleados SET activo = FALSE WHERE id_empleado = %s"
            cursor.execute(query, (id_empleado,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Empleado eliminado exitosamente")
            else:
                cursor.close()
                return (False, "Empleado no encontrado")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al eliminar empleado: {str(e)}")
        finally:
            liberar_conexion(conexion)