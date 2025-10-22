
import sqlite3
from .base_dao import BaseDAO
from .models import HorarioDisponible

class HorarioDisponibleDAO(BaseDAO):
    """DAO para la entidad HorarioDisponible."""

    def add(self, horario):
        """Agrega un nuevo horario disponible a la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO horarios_disponibles (id_cancha, dia_semana, hora_inicio, hora_fin) VALUES (?, ?, ?, ?)",
                (horario.id_cancha, horario.dia_semana, horario.hora_inicio, horario.hora_fin)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al agregar horario: {e}")
            self.conn.rollback()
            return None
        except sqlite3.Error as e:
            print(f"Error al agregar horario disponible: {e}")
            self.conn.rollback()
            return None

    def get_by_id(self, id_horario):
        """Obtiene un horario disponible por su ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM horarios_disponibles WHERE id_horario = ?", (id_horario,))
        row = cursor.fetchone()
        if row:
            return HorarioDisponible(
                id_horario=row['id_horario'],
                id_cancha=row['id_cancha'],
                dia_semana=row['dia_semana'],
                hora_inicio=row['hora_inicio'],
                hora_fin=row['hora_fin']
            )
        return None

    def get_all(self):
        """Obtiene una lista de todos los horarios disponibles."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM horarios_disponibles ORDER BY dia_semana, hora_inicio")
        rows = cursor.fetchall()
        return [
            HorarioDisponible(
                id_horario=row['id_horario'],
                id_cancha=row['id_cancha'],
                dia_semana=row['dia_semana'],
                hora_inicio=row['hora_inicio'],
                hora_fin=row['hora_fin']
            ) for row in rows
        ]

    def get_horarios_by_cancha(self, id_cancha):
        """Obtiene todos los horarios disponibles para una cancha específica."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM horarios_disponibles WHERE id_cancha = ? ORDER BY dia_semana, hora_inicio", (id_cancha,))
        rows = cursor.fetchall()
        return [
            HorarioDisponible(
                id_horario=row['id_horario'],
                id_cancha=row['id_cancha'],
                dia_semana=row['dia_semana'],
                hora_inicio=row['hora_inicio'],
                hora_fin=row['hora_fin']
            ) for row in rows
        ]

    def update(self, horario):
        """Actualiza los datos de un horario disponible existente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE horarios_disponibles SET id_cancha = ?, dia_semana = ?, hora_inicio = ?, hora_fin = ? WHERE id_horario = ?",
                (horario.id_cancha, horario.dia_semana, horario.hora_inicio, horario.hora_fin, horario.id_horario)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al actualizar horario: {e}")
            self.conn.rollback()
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar horario disponible: {e}")
            self.conn.rollback()
            return False

    def delete(self, id_horario):
        """Elimina un horario disponible por su ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM horarios_disponibles WHERE id_horario = ?", (id_horario,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print(f"Error: No se puede eliminar el horario con ID {id_horario} porque tiene reservas asociadas.")
            self.conn.rollback()
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar horario disponible: {e}")
            self.conn.rollback()
            return False
