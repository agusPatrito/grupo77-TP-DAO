from database import obtener_conexion_bd
from models import (Cliente, Cancha, Horarios, EstadosReserva, 
                    Reserva, HorariosXCanchas, Torneo, DetalleTorneoReserva)
import datetime # para manejar fechas y horas

# aca van las operaciones con la base de datos

class ClienteDAO:
    def crear(self, cliente: Cliente):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, apellido, dni) VALUES (?, ?, ?)",
            (cliente.nombre, cliente.apellido, cliente.dni)
        )
        nuevo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return nuevo_id

    def obtener_todos(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes_data = cursor.fetchall()
        conn.close()
        return [Cliente(**data) for data in clientes_data]

    def obtener_por_id(self, id_cliente):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
        cliente_data = cursor.fetchone()
        conn.close()
        return Cliente(**cliente_data) if cliente_data else None

    def actualizar(self, cliente: Cliente):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET nombre = ?, apellido = ?, dni = ? WHERE id_cliente = ?",
                       (cliente.nombre, cliente.apellido, cliente.dni, cliente.id_cliente))
        conn.commit()
        conn.close()

    def eliminar(self, id_cliente):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        conn.close()

class CanchaDAO:
    def crear(self, cancha: Cancha):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO canchas (nombre, tiene_luz, tarifa_hora) VALUES (?, ?, ?)",
                       (cancha.nombre, cancha.tiene_luz, cancha.tarifa_hora))
        conn.commit()
        conn.close()

    def obtener_todos(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM canchas")
        canchas_data = cursor.fetchall()
        conn.close()
        return [Cancha(**data) for data in canchas_data]

    def obtener_por_id(self, id_cancha):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM canchas WHERE id_cancha = ?", (id_cancha,))
        cancha_data = cursor.fetchone()
        conn.close()
        return Cancha(**cancha_data) if cancha_data else None

    # este metodo obtiene las canchas sin el estado porque ya no existe esa tabla
    def obtener_todos_con_estado(self): 
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_cancha, c.nombre, c.tiene_luz, c.tarifa_hora
            FROM canchas c
        """)
        return cursor.fetchall()

    def actualizar(self, cancha: Cancha):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("UPDATE canchas SET nombre = ?, tiene_luz = ?, tarifa_hora = ? WHERE id_cancha = ?",
                       (cancha.nombre, cancha.tiene_luz, cancha.tarifa_hora, cancha.id_cancha))
        conn.commit()
        conn.close()

    def eliminar(self, id_cancha):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM canchas WHERE id_cancha = ?", (id_cancha,))
        conn.commit()
        conn.close()

class HorariosDAO: # Nueva clase
    def obtener_todos(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM horarios ORDER BY hora_inicio")
        horarios_data = cursor.fetchall()
        conn.close()
        return [Horarios(**data) for data in horarios_data]

    def obtener_por_hora_inicio(self, hora_inicio):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM horarios WHERE hora_inicio = ?", (hora_inicio,))
        horario_data = cursor.fetchone()
        conn.close()
        return Horarios(**horario_data) if horario_data else None

class EstadosReservaDAO: # Nueva clase
    def obtener_todos(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estados_reserva")
        estados_data = cursor.fetchall()
        conn.close()
        return [EstadosReserva(**data) for data in estados_data]

    def obtener_por_nombre(self, nombre_estado):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estados_reserva WHERE nombre_estado = ?", (nombre_estado,))
        estado_data = cursor.fetchone()
        conn.close()
        return EstadosReserva(**estado_data) if estado_data else None
    
def confirmar_pago(self, id_reserva):
    # Obtener la reserva
    reserva = self.obtener_reserva_por_id(id_reserva)
    if not reserva:
        raise ValueError("La reserva no existe.")

    # Obtener estados
    estado_confirmada = self.obtener_id_estado_por_nombre("Confirmada")
    estado_pendiente = self.obtener_id_estado_por_nombre("Pendiente")

    # Validar que la reserva esté pendiente
    if reserva.id_estado_reserva != estado_pendiente:
        raise ValueError("Solo se pueden pagar reservas en estado Pendiente.")

    # Simulación del pago
    print("Procesando pago simulado...")

    # Actualizar estado a Confirmada
    conn = obtener_conexion_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reserva
        SET id_estado_reserva = ?
        WHERE id_reserva = ?
    """, (estado_confirmada, id_reserva))
    conn.commit()
    conn.close()

    return True



class HorariosXCanchasDAO: # Nueva clase
    def crear(self, hxc: HorariosXCanchas):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO horarios_x_canchas (id_cancha, id_horario, id_reserva, fecha)
            VALUES (?, ?, ?, ?)
        """, (hxc.id_cancha, hxc.id_horario, hxc.id_reserva, hxc.fecha))
        conn.commit()
        conn.close()

    def eliminar_por_reserva(self, id_reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM horarios_x_canchas WHERE id_reserva = ?", (id_reserva,))
        conn.commit()
        conn.close()

    def verificar_ocupacion(self, id_cancha, id_horario, fecha, id_estado_confirmada):
        # verifica si un slot esta ocupado por una reserva CONFIRMADA
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hxc.id_horarios_x_canchas FROM horarios_x_canchas hxc
            JOIN reservas r ON hxc.id_reserva = r.id_reserva
            WHERE hxc.id_cancha = ? AND hxc.id_horario = ? AND hxc.fecha = ? AND r.id_estado_reserva = ?
        """, (id_cancha, id_horario, fecha, id_estado_confirmada))
        result = cursor.fetchone()
        conn.close()
        return result is not None # True si esta ocupado por una reserva confirmada, False si esta libre o cancelada

class ReservaDAO:
    def crear(self, reserva: Reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (id_cliente, id_cancha, id_estado_reserva, fecha, hora_inicio, duracion_horas, monto_total)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (reserva.id_cliente, reserva.id_cancha, reserva.id_estado_reserva, reserva.fecha, reserva.hora_inicio, reserva.duracion_horas, reserva.monto_total))
        reserva_id = cursor.lastrowid # obtenemos el ID de la reserva recien creada
        conn.commit()
        conn.close()
        return reserva_id

    def obtener_todos_detalles(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                r.id_reserva,
                cl.nombre || ' ' || cl.apellido as cliente_nombre,
                ca.nombre as cancha_nombre,
                r.fecha,
                r.hora_inicio,
                r.duracion_horas,
                es.nombre_estado as estado_reserva_nombre,
                r.monto_total
            FROM reservas r
            JOIN clientes cl ON r.id_cliente = cl.id_cliente
            JOIN canchas ca ON r.id_cancha = ca.id_cancha
            JOIN estados_reserva es ON r.id_estado_reserva = es.id_estado_reserva
        """)
        return cursor.fetchall()

    def obtener_reserva_por_id(self, id_reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
        reserva_data = cursor.fetchone()
        conn.close()
        return Reserva(**reserva_data) if reserva_data else None

    def actualizar(self, reserva: Reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservas 
            SET id_cliente = ?, id_cancha = ?, id_estado_reserva = ?, fecha = ?, hora_inicio = ?, duracion_horas = ?, monto_total = ?
            WHERE id_reserva = ?
        """, (reserva.id_cliente, reserva.id_cancha, reserva.id_estado_reserva, reserva.fecha, reserva.hora_inicio, reserva.duracion_horas, reserva.monto_total, reserva.id_reserva))
        conn.commit()
        conn.close()

    def eliminar(self, id_reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva,))
        conn.commit()
        conn.close()

    def eliminar_reservas_por_estado(self, id_estado_reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        # primero obtenemos los id_reserva de las reservas con ese estado
        cursor.execute("SELECT id_reserva FROM reservas WHERE id_estado_reserva = ?", (id_estado_reserva,))
        ids_reservas_a_eliminar = [row['id_reserva'] for row in cursor.fetchall()]

        if ids_reservas_a_eliminar:
            # eliminamos los slots asociados a estas reservas
            for res_id in ids_reservas_a_eliminar:
                HorariosXCanchasDAO().eliminar_por_reserva(res_id) # Usamos el DAO de HorariosXCanchas
            # ahora si eliminamos las reservas
            cursor.execute("DELETE FROM reservas WHERE id_estado_reserva = ?", (id_estado_reserva,))
        
        conn.commit()
        conn.close()

    def reporte_canchas_mas_utilizadas(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nombre, COUNT(r.id_reserva) as total_reservas
            FROM reservas r
            JOIN canchas c ON r.id_cancha = c.id_cancha
            WHERE r.id_estado_reserva = (SELECT id_estado_reserva FROM estados_reserva WHERE nombre_estado = 'Confirmada')
            GROUP BY c.nombre
            ORDER BY total_reservas DESC
        """)
        return cursor.fetchall()
    
    def obtener_reservas_por_rango(self, fecha_desde, fecha_hasta):
        """
        Devuelve reservas entre dos fechas, con info de cliente, cancha y estado.
        """
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id_reserva,
                   cl.nombre || ' ' || cl.apellido AS cliente,
                   ca.nombre                        AS cancha,
                   r.fecha,
                   r.hora_inicio,
                   r.duracion_horas,
                   es.nombre_estado                 AS estado
            FROM reservas r
            JOIN clientes cl        ON r.id_cliente = cl.id_cliente
            JOIN canchas ca         ON r.id_cancha  = ca.id_cancha
            JOIN estados_reserva es ON r.id_estado_reserva = es.id_estado_reserva
            WHERE r.fecha BETWEEN ? AND ?
            ORDER BY r.fecha, r.hora_inicio
        """, (fecha_desde, fecha_hasta))
        filas = cursor.fetchall()
        conn.close()
        return filas

    def reporte_utilizacion_mensual(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', fecha) as mes, COUNT(id_reserva) as total_reservas
            FROM reservas
            WHERE id_estado_reserva = (SELECT id_estado_reserva FROM estados_reserva WHERE nombre_estado = 'Confirmada')
            GROUP BY mes
            ORDER BY mes
        """)
        return cursor.fetchall()
    
    def confirmar_reserva_con_slots(self, id_reserva, id_estado_confirmada, id_cancha, fecha, lista_id_horarios):
        """
        Marca la reserva como confirmada y crea los registros en horarios_x_canchas
        en una misma transaccion/conn para evitar inconsistencias.
        lista_id_horarios: lista de id_horario que ocupan la reserva
        """
        conn = obtener_conexion_bd()
        try:
            cursor = conn.cursor()
            # Verifico que la reserva exista y este en estado Pendiente (se puede ajustar)
            cursor.execute("SELECT id_estado_reserva FROM reservas WHERE id_reserva = ?", (id_reserva,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("Reserva no encontrada.")
            # Actualizo estado
            cursor.execute("""
                UPDATE reservas
                SET id_estado_reserva = ?
                WHERE id_reserva = ?
            """, (id_estado_confirmada, id_reserva))

            # Inserto los slots en horarios_x_canchas
            for id_horario in lista_id_horarios:
                cursor.execute("""
                    INSERT INTO horarios_x_canchas (id_cancha, id_horario, id_reserva, fecha)
                    VALUES (?, ?, ?, ?)
                """, (id_cancha, id_horario, id_reserva, fecha))

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class TorneoDAO:
    def crear(self, torneo: Torneo):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO torneos (nombre, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?)
        """, (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin))
        torneo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return torneo_id

    def obtener_todos(self):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM torneos
            ORDER BY fecha_inicio DESC
        """)
        torneos_data = cursor.fetchall()
        conn.close()
        return [Torneo(**data) for data in torneos_data]

    def obtener_por_id(self, id_torneo):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM torneos WHERE id_torneo = ?", (id_torneo,))
        data = cursor.fetchone()
        conn.close()
        return Torneo(**data) if data else None

    def actualizar(self, torneo: Torneo):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE torneos
            SET nombre = ?, fecha_inicio = ?, fecha_fin = ?
            WHERE id_torneo = ?
        """, (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin, torneo.id_torneo))
        conn.commit()
        conn.close()

    def eliminar(self, id_torneo):
        # primero borro sus relaciones con reservas
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM detalle_torneo_reserva WHERE id_torneo = ?", (id_torneo,))
        cursor.execute("DELETE FROM torneos WHERE id_torneo = ?", (id_torneo,))
        conn.commit()
        conn.close()


class DetalleTorneoReservaDAO:
    def agregar_reserva_a_torneo(self, id_torneo, id_reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO detalle_torneo_reserva (id_torneo, id_reserva)
            VALUES (?, ?)
        """, (id_torneo, id_reserva))
        conn.commit()
        conn.close()

    def quitar_reserva_de_torneo(self, id_torneo, id_reserva):
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM detalle_torneo_reserva
            WHERE id_torneo = ? AND id_reserva = ?
        """, (id_torneo, id_reserva))
        conn.commit()
        conn.close()

    def obtener_reservas_de_torneo(self, id_torneo):
        """
        Devuelve las reservas asociadas a un torneo con info útil
        (cliente, cancha, fecha, hora, estado).
        """
        conn = obtener_conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id_reserva,
                   cl.nombre || ' ' || cl.apellido AS cliente,
                   ca.nombre                        AS cancha,
                   r.fecha,
                   r.hora_inicio,
                   r.duracion_horas,
                   es.nombre_estado                 AS estado
            FROM detalle_torneo_reserva dtr
            JOIN reservas r         ON dtr.id_reserva = r.id_reserva
            JOIN clientes cl        ON r.id_cliente   = cl.id_cliente
            JOIN canchas ca         ON r.id_cancha    = ca.id_cancha
            JOIN estados_reserva es ON r.id_estado_reserva = es.id_estado_reserva
            WHERE dtr.id_torneo = ?
            ORDER BY r.fecha, r.hora_inicio
        """, (id_torneo,))
        data = cursor.fetchall()
        conn.close()
        return data

