
import sqlite3
from .base_dao import BaseDAO
from .models import Torneo

class TorneoDAO(BaseDAO):
    """DAO para la entidad Torneo."""

    def add(self, torneo):
        """Agrega un nuevo torneo a la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO torneos (nombre, fecha_inicio, fecha_fin) VALUES (?, ?, ?)",
                (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al agregar torneo: {e}")
            self.conn.rollback()
            return None

    def get_by_id(self, id_torneo):
        """Obtiene un torneo por su ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM torneos WHERE id_torneo = ?", (id_torneo,))
        row = cursor.fetchone()
        if row:
            return self._row_to_model(row)
        return None

    def get_all(self):
        """Obtiene una lista de todos los torneos."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM torneos ORDER BY fecha_inicio")
        rows = cursor.fetchall()
        return [self._row_to_model(row) for row in rows]

    def update(self, torneo):
        """Actualiza los datos de un torneo existente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE torneos SET nombre = ?, fecha_inicio = ?, fecha_fin = ? WHERE id_torneo = ?",
                (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin, torneo.id_torneo)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar torneo: {e}")
            self.conn.rollback()
            return False

    def delete(self, id_torneo):
        """Elimina un torneo por su ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM torneos WHERE id_torneo = ?", (id_torneo,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print(f"Error: No se puede eliminar el torneo porque tiene canchas asociadas en detalles_torneo_cancha.")
            self.conn.rollback()
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar torneo: {e}")
            self.conn.rollback()
            return False

    def _row_to_model(self, row):
        """Convierte una fila de la base de datos a un objeto Torneo."""
        return Torneo(
            id_torneo=row['id_torneo'],
            nombre=row['nombre'],
            fecha_inicio=row['fecha_inicio'],
            fecha_fin=row['fecha_fin']
        )
