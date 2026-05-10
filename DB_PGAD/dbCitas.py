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
from datetime import datetime, time

class DBCitas:
    """Clase para manejar operaciones de base de datos de citas"""

    @staticmethod
    def insertar_cita(datos):
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos", None)

        try:
            cursor = conexion.cursor()

            # Verificar disponibilidad
            cursor.execute(
                """SELECT id_cita FROM citas 
                   WHERE id_doctor = %s AND fecha = %s AND hora = %s 
                   AND estado != 'Cancelada'""",
                (datos['id_doctor'], datos['fecha'], datos['hora'])
            )

            if cursor.fetchone():
                cursor.close()
                return (False, "El doctor ya tiene una cita agendada en ese horario", None)

            # Insertar cita con RETURNING (PostgreSQL)
            query = """
                INSERT INTO citas 
                (id_paciente, id_doctor, fecha, hora, estado)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_cita
            """

            valores = (
                datos['id_paciente'],
                datos['id_doctor'],
                datos['fecha'],
                datos['hora'],
                datos.get('estado', 'Programada')
            )

            cursor.execute(query, valores)
            id_cita = cursor.fetchone()[0]
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
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")

        try:
            cursor = conexion.cursor()

            query = """
                SELECT c.id_cita, p.nombre AS paciente, d.nombre AS doctor,
                       c.fecha, c.hora, c.estado, c.fecha_registro
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN doctores d ON c.id_doctor = d.id_doctor
                ORDER BY c.fecha DESC, c.hora DESC
            """

            cursor.execute(query)
            citas = cursor.fetchall()
            cursor.close()

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
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar a la base de datos")

        try:
            cursor = conexion.cursor()

            query = """
                SELECT c.id_cita, c.id_paciente, p.nombre AS paciente,
                       c.id_doctor, d.nombre AS doctor, d.especialidad,
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
                return (True, {
                    'id_cita': cita[0],
                    'id_paciente': cita[1],
                    'paciente': cita[2],
                    'id_doctor': cita[3],
                    'doctor': cita[4],
                    'especialidad': cita[5],
                    'fecha': cita[6],
                    'hora': cita[7],
                    'estado': cita[8]
                })
            else:
                return (False, "Cita no encontrada")

        except Exception as e:
            return (False, f"Error al obtener cita: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def actualizar_cita(id_cita, datos):
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            # Verificar cambios de fecha/hora/doctor
            if 'fecha' in datos or 'hora' in datos or 'id_doctor' in datos:

                cursor.execute(
                    "SELECT id_doctor, fecha, hora FROM citas WHERE id_cita = %s",
                    (id_cita,)
                )
                actual = cursor.fetchone()

                if actual:
                    nuevo_doctor = datos.get('id_doctor', actual[0])
                    nueva_fecha = datos.get('fecha', actual[1])
                    nueva_hora = datos.get('hora', actual[2])

                    cursor.execute(
                        """SELECT id_cita FROM citas
                           WHERE id_doctor = %s AND fecha = %s AND hora = %s
                           AND estado != 'Cancelada' AND id_cita <> %s""",
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
                return (True, "Cita actualizada")

            cursor.close()
            return (False, "Cita no encontrada")

        except Exception as e:
            conexion.rollback()
            return (False, f"Error al actualizar cita: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def cancelar_cita(id_cita):
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            cursor.execute(
                "UPDATE citas SET estado = 'Cancelada' WHERE id_cita = %s",
                (id_cita,)
            )
            conexion.commit()

            if cursor.rowcount > 0:
                cursor.close()
                return (True, "Cita cancelada")

            cursor.close()
            return (False, "Cita no encontrada")

        except Exception as e:
            conexion.rollback()
            return (False, f"Error al cancelar cita: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def obtener_pacientes_activos():
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_paciente, nombre
                FROM pacientes
                WHERE activo = TRUE
                ORDER BY nombre
            """)

            datos = cursor.fetchall()
            cursor.close()

            return (True, [(d[0], d[1]) for d in datos])

        except Exception as e:
            return (False, f"Error al obtener pacientes: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def obtener_doctores_activos():
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_doctor, nombre, especialidad
                FROM doctores
                WHERE activo = TRUE
                ORDER BY nombre
            """)

            datos = cursor.fetchall()
            cursor.close()

            return (True, [(d[0], d[1], d[2]) for d in datos])

        except Exception as e:
            return (False, f"Error al obtener doctores: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def verificar_disponibilidad(id_doctor, fecha, hora):
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_cita FROM citas
                WHERE id_doctor = %s AND fecha = %s AND hora = %s
                AND estado != 'Cancelada'
            """, (id_doctor, fecha, hora))

            if cursor.fetchone():
                return (False, "El doctor ya tiene una cita en ese horario")

            return (True, "Horario disponible")

        except Exception as e:
            return (False, f"Error al verificar: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def obtener_citas_doctor_hoy(id_doctor):
        from datetime import date

        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            hoy = date.today()

            cursor.execute("""
                SELECT c.id_cita, p.id_paciente, p.nombre,
                       c.fecha, c.hora, c.estado,
                       p.telefono, p.edad, p.sexo
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                WHERE c.id_doctor = %s
                AND c.fecha = %s
                AND c.estado != 'Cancelada'
                ORDER BY c.hora ASC
            """, (id_doctor, hoy))

            citas = cursor.fetchall()
            cursor.close()

            citas_list = []
            for c in citas:
                citas_list.append({
                    'id_cita': c[0],
                    'id_paciente': c[1],
                    'paciente': c[2],
                    'fecha': c[3],
                    'hora': c[4],
                    'estado': c[5],
                    'telefono': c[6],
                    'edad': c[7],
                    'sexo': c[8]
                })

            return (True, citas_list)

        except Exception as e:
            return (False, f"Error: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def obtener_info_completa_cita(id_cita):
        conexion = obtener_conexion()
        if not conexion:
            return (False, "No se pudo conectar")

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT c.id_cita, c.fecha, c.hora, c.estado,
                       p.id_paciente, p.nombre, p.direccion, p.telefono,
                       p.fecha_nacimiento, p.sexo, p.edad, p.estatura,
                       d.id_doctor, d.nombre, d.especialidad
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN doctores d ON c.id_doctor = d.id_doctor
                WHERE c.id_cita = %s
            """, (id_cita,))

            r = cursor.fetchone()
            cursor.close()

            if r:
                return (True, {
                    'id_cita': r[0],
                    'fecha': r[1],
                    'hora': r[2],
                    'estado': r[3],
                    'paciente': {
                        'id': r[4],
                        'nombre': r[5],
                        'direccion': r[6],
                        'telefono': r[7],
                        'fecha_nacimiento': r[8],
                        'sexo': r[9],
                        'edad': r[10],
                        'estatura': r[11]
                    },
                    'doctor': {
                        'id': r[12],
                        'nombre': r[13],
                        'especialidad': r[14]
                    }
                })

            return (False, "Cita no encontrada")

        except Exception as e:
            return (False, f"Error: {str(e)}")

        finally:
            liberar_conexion(conexion)

    @staticmethod
    def obtener_id_doctor_por_nombre(nombre_doctor):
        conexion = obtener_conexion()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_doctor FROM doctores
                WHERE nombre = %s AND activo = TRUE
            """, (nombre_doctor,))

            r = cursor.fetchone()
            cursor.close()

            return r[0] if r else None

        except Exception as e:
            print("Error:", e)
            return None

        finally:
            liberar_conexion(conexion)
    
    @staticmethod
    def actualizar_estado_cita(id_cita, nuevo_estado):
        """
        Se agrego esta funcion con el fin de mejorar la funcionalidad del GUI
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
