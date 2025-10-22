
import sqlite3
from .base_dao import BaseDAO
from .models import Reserva

class ReservaDAO(BaseDAO):
    """DAO para la entidad Reserva."""

    def add(self, reserva):
        """Agrega una nueva reserva a la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO reservas (id_cliente, id_cancha, fecha, hora_inicio, duracion_horas, estado, monto_total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (reserva.id_cliente, reserva.id_cancha, reserva.fecha, reserva.hora_inicio, reserva.duracion_horas, reserva.estado, reserva.monto_total)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al agregar reserva: {e}")
            self.conn.rollback()
            return None
        except sqlite3.Error as e:
            print(f"Error al agregar reserva: {e}")
            self.conn.rollback()
            return None

    def get_by_id(self, id_reserva):
        """Obtiene una reserva por su ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = ?", (id_reserva,))
        row = cursor.fetchone()
        if row:
            return self._row_to_model(row)
        return None

    def get_all(self):
        """Obtiene una lista de todas las reservas."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reservas ORDER BY fecha, hora_inicio")
        rows = cursor.fetchall()
        return [self._row_to_model(row) for row in rows]

    def get_reservas_by_cancha_and_fecha(self, id_cancha, fecha):
        """Obtiene todas las reservas para una cancha y fecha específicas."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id_cancha = ? AND fecha = ? AND estado = 'Confirmada' ORDER BY hora_inicio", (id_cancha, fecha))
        rows = cursor.fetchall()
        return [self._row_to_model(row) for row in rows]

    def update(self, reserva):
        """Actualiza los datos de una reserva existente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE reservas SET id_cliente = ?, id_cancha = ?, fecha = ?, hora_inicio = ?, duracion_horas = ?, estado = ?, monto_total = ? WHERE id_reserva = ?",
                (reserva.id_cliente, reserva.id_cancha, reserva.fecha, reserva.hora_inicio, reserva.duracion_horas, reserva.estado, reserva.monto_total, reserva.id_reserva)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al actualizar reserva: {e}")
            self.conn.rollback()
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar reserva: {e}")
            self.conn.rollback()
            return False

    def delete(self, id_reserva):
        """Elimina una reserva por su ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar reserva: {e}")
            self.conn.rollback()
            return False

    def _row_to_model(self, row):
        """Convierte una fila de la base de datos a un objeto Reserva."""
        return Reserva(
            id_reserva=row['id_reserva'],
            id_cliente=row['id_cliente'],
            id_cancha=row['id_cancha'],
            fecha=row['fecha'],
            hora_inicio=row['hora_inicio'],
            duracion_horas=row['duracion_horas'],
            estado=row['estado'],
            monto_total=row['monto_total']
        )
