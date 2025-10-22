
import sqlite3
from .models import EstadoCancha

class EstadoCanchaDAO:
    """DAO para la entidad EstadoCancha."""
    def __init__(self, conn):
        self.conn = conn

    def add(self, estado_cancha):
        """Agrega un nuevo estado de cancha."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO estados_cancha (nombre, descripcion) VALUES (?, ?)",
                (estado_cancha.nombre, estado_cancha.descripcion)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Esto previene duplicados si se intenta insertar el mismo estado dos veces
            self.conn.rollback()
            return self.get_by_name(estado_cancha.nombre).id_estado
        except sqlite3.Error as e:
            print(f"Error al agregar estado de cancha: {e}")
            self.conn.rollback()
            return None

    def get_by_name(self, nombre):
        """Obtiene un estado de cancha por su nombre."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM estados_cancha WHERE nombre = ?", (nombre,))
        row = cursor.fetchone()
        if row:
            return EstadoCancha(
                id_estado=row['id_estado'],
                nombre=row['nombre'],
                descripcion=row['descripcion']
            )
        return None

    def get_all(self):
        """Obtiene todos los estados de cancha."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM estados_cancha")
        rows = cursor.fetchall()
        return [
            EstadoCancha(
                id_estado=row['id_estado'],
                nombre=row['nombre'],
                descripcion=row['descripcion']
            ) for row in rows
        ]
