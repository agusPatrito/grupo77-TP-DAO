
import sqlite3
from .base_dao import BaseDAO
from .models import Cancha

class CanchaDAO(BaseDAO):
    """DAO para la entidad Cancha."""

    def add(self, cancha):
        """Agrega una nueva cancha a la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO canchas (id_estado, nombre, tipo_deporte, tarifa_hora) VALUES (?, ?, ?, ?)",
                (cancha.id_estado, cancha.nombre, cancha.tipo_deporte, cancha.tarifa_hora)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: canchas.nombre" in str(e):
                print(f"Error: Ya existe una cancha con el nombre '{cancha.nombre}'.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print(f"Error: El ID de estado '{cancha.id_estado}' no existe.")
            else:
                print(f"Error de integridad al agregar cancha: {e}")
            self.conn.rollback()
            return None
        except sqlite3.Error as e:
            print(f"Error al agregar cancha: {e}")
            self.conn.rollback()
            return None

    def get_by_id(self, id_cancha):
        """Obtiene una cancha por su ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM canchas WHERE id_cancha = ?", (id_cancha,))
        row = cursor.fetchone()
        if row:
            return Cancha(
                id_cancha=row['id_cancha'],
                id_estado=row['id_estado'],
                nombre=row['nombre'],
                tipo_deporte=row['tipo_deporte'],
                tarifa_hora=row['tarifa_hora']
            )
        return None

    def get_all(self):
        """Obtiene una lista de todas las canchas."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM canchas ORDER BY nombre")
        rows = cursor.fetchall()
        return [
            Cancha(
                id_cancha=row['id_cancha'],
                id_estado=row['id_estado'],
                nombre=row['nombre'],
                tipo_deporte=row['tipo_deporte'],
                tarifa_hora=row['tarifa_hora']
            ) for row in rows
        ]

    def update(self, cancha):
        """Actualiza los datos de una cancha existente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE canchas SET id_estado = ?, nombre = ?, tipo_deporte = ?, tarifa_hora = ? WHERE id_cancha = ?",
                (cancha.id_estado, cancha.nombre, cancha.tipo_deporte, cancha.tarifa_hora, cancha.id_cancha)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: canchas.nombre" in str(e):
                print(f"Error: Ya existe otra cancha con el nombre '{cancha.nombre}'.")
            elif "FOREIGN KEY constraint failed" in str(e):
                print(f"Error: El ID de estado '{cancha.id_estado}' no existe.")
            else:
                print(f"Error de integridad al actualizar cancha: {e}")
            self.conn.rollback()
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar cancha: {e}")
            self.conn.rollback()
            return False

    def delete(self, id_cancha):
        """Elimina una cancha por su ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM canchas WHERE id_cancha = ?", (id_cancha,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print(f"Error: No se puede eliminar la cancha con ID {id_cancha} porque tiene reservas o horarios asociados.")
            self.conn.rollback()
            return False
        except sqlite3.Error as e:
            print(f"Error al eliminar cancha: {e}")
            self.conn.rollback()
            return False
