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
from datetime import datetime, time

class DBCitas:
    """Clase para manejar operaciones de base de datos de citas"""
    
    @staticmethod
    def insertar_cita(datos):
        """
        Inserta una nueva cita en la base de datos
        
        Args:
            datos (dict): Diccionario con los datos de la cita
            
        Returns:
            tuple: (éxito: bool, mensaje: str, id_cita: int o None)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos", None)
        
        try:
            cursor = conexion.cursor()
            
            # Verificar que el doctor esté disponible en esa fecha/hora
            cursor.execute(
                """SELECT id_cita FROM citas 
                   WHERE id_doctor = %s AND fecha = %s AND hora = %s 
                   AND estado != 'Cancelada'""",
                (datos['id_doctor'], datos['fecha'], datos['hora'])
            )
            
            if cursor.fetchone():
                cursor.close()
                return (False, "El doctor ya tiene una cita agendada en ese horario", None)
            
            # Insertar cita
            query = """
                INSERT INTO citas 
                (id_paciente, id_doctor, fecha, hora, estado)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            valores = (
                datos['id_paciente'],
                datos['id_doctor'],
                datos['fecha'],
                datos['hora'],
                datos.get('estado', 'Programada')
            )
            
            cursor.execute(query, valores)
            id_cita = cursor.lastrowid
            conexion.commit()
            cursor.close()
            
            return (True, "Cita registrada exitosamente", id_cita)
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al insertar cita: {str(e)}", None)
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_todas_citas():
        """
        Obtiene todas las citas de la base de datos
        
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT c.id_cita, p.nombre as paciente, d.nombre as doctor,
                       c.fecha, c.hora, c.estado, c.fecha_registro
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN doctores d ON c.id_doctor = d.id_doctor
                ORDER BY c.fecha DESC, c.hora DESC
            """
            
            cursor.execute(query)
            citas = cursor.fetchall()
            cursor.close()
            
            # Convertir a lista de diccionarios
            citas_list = []
            for cita in citas:
                citas_list.append({
                    'id_cita': cita[0],
                    'paciente': cita[1],
                    'doctor': cita[2],
                    'fecha': cita[3],
                    'hora': cita[4],
                    'estado': cita[5],
                    'fecha_registro': cita[6]
                })
            
            return (True, citas_list)
            
        except Exception as e:
            return (False, f"Error al obtener citas: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_cita_por_id(id_cita):
        """
        Obtiene una cita específica por su ID
        
        Args:
            id_cita (int): ID de la cita
            
        Returns:
            tuple: (éxito: bool, datos: dict o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT c.id_cita, c.id_paciente, p.nombre as paciente,
                       c.id_doctor, d.nombre as doctor, d.especialidad,
                       c.fecha, c.hora, c.estado
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN doctores d ON c.id_doctor = d.id_doctor
                WHERE c.id_cita = %s
            """
            
            cursor.execute(query, (id_cita,))
            cita = cursor.fetchone()
            cursor.close()
            
            if cita:
                cita_dict = {
                    'id_cita': cita[0],
                    'id_paciente': cita[1],
                    'paciente': cita[2],
                    'id_doctor': cita[3],
                    'doctor': cita[4],
                    'especialidad': cita[5],
                    'fecha': cita[6],
                    'hora': cita[7],
                    'estado': cita[8]
                }
                return (True, cita_dict)
            else:
                return (False, "Cita no encontrada")
            
        except Exception as e:
            return (False, f"Error al obtener cita: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_cita(id_cita, datos):
        """
        Actualiza los datos de una cita
        
        Args:
            id_cita (int): ID de la cita
            datos (dict): Diccionario con los datos a actualizar
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            # Verificar disponibilidad si se cambia fecha/hora/doctor
            if 'fecha' in datos or 'hora' in datos or 'id_doctor' in datos:
                # Obtener datos actuales
                cursor.execute(
                    "SELECT id_doctor, fecha, hora FROM citas WHERE id_cita = %s",
                    (id_cita,)
                )
                actual = cursor.fetchone()
                
                if actual:
                    nuevo_doctor = datos.get('id_doctor', actual[0])
                    nueva_fecha = datos.get('fecha', actual[1])
                    nueva_hora = datos.get('hora', actual[2])
                    
                    # Verificar conflictos (excluyendo la cita actual)
                    cursor.execute(
                        """SELECT id_cita FROM citas 
                           WHERE id_doctor = %s AND fecha = %s AND hora = %s 
                           AND estado != 'Cancelada' AND id_cita != %s""",
                        (nuevo_doctor, nueva_fecha, nueva_hora, id_cita)
                    )
                    
                    if cursor.fetchone():
                        cursor.close()
                        return (False, "El doctor ya tiene una cita en ese horario")
            
            query = """
                UPDATE citas
                SET id_paciente = %s, id_doctor = %s, fecha = %s,
                    hora = %s, estado = %s
                WHERE id_cita = %s
            """
            
            valores = (
                datos['id_paciente'],
                datos['id_doctor'],
                datos['fecha'],
                datos['hora'],
                datos['estado'],
                id_cita
            )
            
            cursor.execute(query, valores)
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Cita actualizada exitosamente")
            else:
                cursor.close()
                return (False, "Cita no encontrada")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al actualizar cita: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def cancelar_cita(id_cita):
        """
        Cancela una cita (cambia estado a 'Cancelada')
        
        Args:
            id_cita (int): ID de la cita
            
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = "UPDATE citas SET estado = 'Cancelada' WHERE id_cita = %s"
            cursor.execute(query, (id_cita,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Cita cancelada exitosamente")
            else:
                cursor.close()
                return (False, "Cita no encontrada")
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return (False, f"Error al cancelar cita: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_pacientes_activos():
        """Obtiene lista de pacientes activos para combobox"""
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            query = """
                SELECT id_paciente, nombre 
                FROM pacientes 
                WHERE activo = TRUE
                ORDER BY nombre
            """
            cursor.execute(query)
            pacientes = cursor.fetchall()
            cursor.close()
            
            return (True, [(p[0], p[1]) for p in pacientes])
            
        except Exception as e:
            return (False, f"Error al obtener pacientes: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_doctores_activos():
        """Obtiene lista de doctores activos con especialidad"""
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            query = """
                SELECT id_doctor, nombre, especialidad 
                FROM doctores 
                WHERE activo = TRUE
                ORDER BY nombre
            """
            cursor.execute(query)
            doctores = cursor.fetchall()
            cursor.close()
            
            return (True, [(d[0], d[1], d[2]) for d in doctores])
            
        except Exception as e:
            return (False, f"Error al obtener doctores: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def verificar_disponibilidad(id_doctor, fecha, hora):
        """
        Verifica si un doctor está disponible en fecha/hora específica
        
        Returns:
            tuple: (disponible: bool, mensaje: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT id_cita FROM citas 
                WHERE id_doctor = %s AND fecha = %s AND hora = %s 
                AND estado != 'Cancelada'
            """
            
            cursor.execute(query, (id_doctor, fecha, hora))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                return (False, "El doctor ya tiene una cita en ese horario")
            else:
                return (True, "Horario disponible")
            
        except Exception as e:
            return (False, f"Error al verificar disponibilidad: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_citas_doctor_hoy(id_doctor):
        """
        Obtiene las citas del doctor para el día actual
        
        Args:
            id_doctor (int): ID del doctor
            
        Returns:
            tuple: (éxito: bool, datos: list o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            from datetime import date
            cursor = conexion.cursor()
            
            query = """
                SELECT c.id_cita, p.id_paciente, p.nombre as paciente, 
                       c.fecha, c.hora, c.estado,
                       p.telefono, p.edad, p.sexo
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                WHERE c.id_doctor = %s 
                AND c.fecha = %s
                AND c.estado != 'Cancelada'
                ORDER BY c.hora ASC
            """
            
            hoy = date.today()
            cursor.execute(query, (id_doctor, hoy))
            citas = cursor.fetchall()
            cursor.close()
            
            # Convertir a lista de diccionarios
            citas_list = []
            for cita in citas:
                citas_list.append({
                    'id_cita': cita[0],
                    'id_paciente': cita[1],
                    'paciente': cita[2],
                    'fecha': cita[3],
                    'hora': cita[4],
                    'estado': cita[5],
                    'telefono': cita[6],
                    'edad': cita[7],
                    'sexo': cita[8]
                })
            
            return (True, citas_list)
            
        except Exception as e:
            return (False, f"Error al obtener citas del doctor: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_info_completa_cita(id_cita):
        """
        Obtiene información completa de la cita incluyendo datos del paciente y doctor
        
        Args:
            id_cita (int): ID de la cita
            
        Returns:
            tuple: (éxito: bool, datos: dict o mensaje_error: str)
        """
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")
        
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT c.id_cita, c.fecha, c.hora, c.estado,
                    p.id_paciente, p.nombre as paciente, p.direccion, 
                    p.telefono, p.fecha_nacimiento, p.sexo, p.edad, p.estatura,
                    d.id_doctor, d.nombre as doctor, d.especialidad
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN doctores d ON c.id_doctor = d.id_doctor
                WHERE c.id_cita = %s
            """
            
            cursor.execute(query, (id_cita,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                info = {
                    'id_cita': resultado[0],
                    'fecha': resultado[1],
                    'hora': resultado[2],
                    'estado': resultado[3],
                    'paciente': {
                        'id': resultado[4],
                        'nombre': resultado[5],
                        'direccion': resultado[6],
                        'telefono': resultado[7],
                        'fecha_nacimiento': resultado[8],
                        'sexo': resultado[9],
                        'edad': resultado[10],
                        'estatura': resultado[11]
                    },
                    'doctor': {
                        'id': resultado[12],
                        'nombre': resultado[13],
                        'especialidad': resultado[14]
                    }
                }
                return (True, info)
            else:
                return (False, "Cita no encontrada")
            
        except Exception as e:
            return (False, f"Error al obtener información de la cita: {str(e)}")
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def obtener_id_doctor_por_nombre(nombre_doctor):
        """
        Obtiene el ID del doctor por su nombre
        
        Args:
            nombre_doctor (str): Nombre del doctor
            
        Returns:
            int o None: ID del doctor o None si no se encuentra
        """
        conexion = obtener_conexion()
        if not conexion:
            return None
        
        try:
            cursor = conexion.cursor()
            query = "SELECT id_doctor FROM doctores WHERE nombre = %s AND activo = TRUE"
            cursor.execute(query, (nombre_doctor,))
            resultado = cursor.fetchone()
            cursor.close()
            
            return resultado[0] if resultado else None
            
        except Exception as e:
            print(f"Error al obtener ID del doctor: {e}")
            return None
        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_estado_cita(id_cita, nuevo_estado):
        """
        Se agrego esta funcion despues de la revision presencial, con el fin de mejorar la funcionalidad del GUI
        """
        conexion = obtener_conexion()
        if not conexion:
            return None
        
        try:
            cursor = conexion.cursor()
            
            query = """
                UPDATE citas 
                SET estado = %s 
                WHERE id_cita = %s
            """
            
            cursor.execute(query, (nuevo_estado, id_cita))
            conexion.commit()
            
            cursor.close()
            conexion.close()
            
            return True
            
        except Exception as e:
            print(f"Error al actualizar estado de cita: {e}")
            if conexion:
                conexion.close()
            return False