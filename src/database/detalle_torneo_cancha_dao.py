
import sqlite3
from .models import DetalleTorneoCancha

class DetalleTorneoCanchaDAO:
    """DAO para la tabla de asociación DetalleTorneoCancha."""
    def __init__(self, conn):
        self.conn = conn

    def add(self, detalle):
        """Asocia una cancha a un torneo en una fecha y hora específicas."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO detalles_torneo_cancha (id_torneo, id_cancha, fecha_uso, hora_uso) VALUES (?, ?, ?, ?)",
                (detalle.id_torneo, detalle.id_cancha, detalle.fecha_uso, detalle.hora_uso)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al agregar detalle de torneo: {e}")
            self.conn.rollback()
        except sqlite3.Error as e:
            print(f"Error al agregar detalle de torneo: {e}")
            self.conn.rollback()

    def get_by_torneo(self, id_torneo):
        """Obtiene todos los detalles de canchas para un torneo específico."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM detalles_torneo_cancha WHERE id_torneo = ?", (id_torneo,))
        rows = cursor.fetchall()
        return [self._row_to_model(row) for row in rows]

    def delete(self, id_torneo, id_cancha, fecha_uso, hora_uso):
        """Elimina una asociación específica entre un torneo y una cancha."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM detalles_torneo_cancha WHERE id_torneo = ? AND id_cancha = ? AND fecha_uso = ? AND hora_uso = ?",
                (id_torneo, id_cancha, fecha_uso, hora_uso)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar detalle de torneo: {e}")
            self.conn.rollback()
            return False

    def _row_to_model(self, row):
        """Convierte una fila de la base de datos a un objeto DetalleTorneoCancha."""
        return DetalleTorneoCancha(
            id_torneo=row['id_torneo'],
            id_cancha=row['id_cancha'],
            fecha_uso=row['fecha_uso'],
            hora_uso=row['hora_uso']
        )
