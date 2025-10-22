
import sqlite3
from .base_dao import BaseDAO
from .models import Cliente

class ClienteDAO(BaseDAO):
    """DAO para la entidad Cliente."""

    def add(self, cliente):
        """Agrega un nuevo cliente a la base de datos."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO clientes (nombre, dni) VALUES (?, ?)",
                (cliente.nombre, cliente.dni)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: El DNI '{cliente.dni}' ya existe.")
            self.conn.rollback()
            return None

    def get_by_id(self, id_cliente):
        """Obtiene un cliente por su ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
        row = cursor.fetchone()
        if row:
            return Cliente(id_cliente=row['id_cliente'], nombre=row['nombre'], dni=row['dni'])
        return None

    def get_by_dni(self, dni):
        """Obtiene un cliente por su DNI."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        if row:
            return Cliente(id_cliente=row['id_cliente'], nombre=row['nombre'], dni=row['dni'])
        return None

    def get_all(self):
        """Obtiene una lista de todos los clientes."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY nombre")
        rows = cursor.fetchall()
        return [Cliente(id_cliente=row['id_cliente'], nombre=row['nombre'], dni=row['dni']) for row in rows]

    def update(self, cliente):
        """Actualiza los datos de un cliente."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE clientes SET nombre = ?, dni = ? WHERE id_cliente = ?",
                (cliente.nombre, cliente.dni, cliente.id_cliente)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print(f"Error: El DNI '{cliente.dni}' ya está en uso.")
            self.conn.rollback()
            return False

    def delete(self, id_cliente):
        """Elimina un cliente por su ID."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print(f"Error: No se puede eliminar el cliente porque tiene reservas asociadas.")
            self.conn.rollback()
            return False
