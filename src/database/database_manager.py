
import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._conn = None # Usamos _conn para indicar que no debe ser accedido directamente

    def get_connection(self):
        """Retorna la conexión a la base de datos. Si no está abierta, la abre."""
        if self._conn is None:
            try:
                self._conn = sqlite3.connect(self.db_path)
                self._conn.row_factory = sqlite3.Row
                self._conn.execute("PRAGMA foreign_keys = ON")
            except sqlite3.Error as e:
                print(f"Error connecting to database: {e}")
                raise
        return self._conn

    def close_connection(self):
        """Cierra la conexión a la base de datos si está abierta."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def create_tables(self):
        """Crea las tablas en la base de datos según el modelo PlantUML."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Tabla de Clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    dni TEXT NOT NULL UNIQUE
                )
            ''')

            # Tabla de Estados de Cancha
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estados_cancha (
                    id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL CHECK(nombre IN ('Disponible', 'Ocupada', 'Mantenimiento')),
                    descripcion TEXT
                )
            ''')

            # Tabla de Canchas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS canchas (
                    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_estado INTEGER NOT NULL,
                    nombre TEXT NOT NULL UNIQUE,
                    tipo_deporte TEXT,
                    tarifa_hora REAL NOT NULL,
                    FOREIGN KEY (id_estado) REFERENCES estados_cancha (id_estado)
                )
            ''')

            # Tabla de Horarios Disponibles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS horarios_disponibles (
                    id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cancha INTEGER NOT NULL,
                    dia_semana INTEGER NOT NULL, -- 1 para Lunes, 7 para Domingo
                    hora_inicio TEXT NOT NULL,
                    hora_fin TEXT NOT NULL,
                    FOREIGN KEY (id_cancha) REFERENCES canchas (id_cancha)
                )
            ''')

            # Tabla de Reservas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    id_cancha INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    hora_inicio TEXT NOT NULL,
                    duracion_horas REAL NOT NULL,
                    estado TEXT NOT NULL CHECK(estado IN ('Confirmada', 'Cancelada')),
                    monto_total REAL NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
                    FOREIGN KEY (id_cancha) REFERENCES canchas (id_cancha)
                )
            ''')

            # Tabla de Torneos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS torneos (
                    id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT NOT NULL
                )
            ''')

            # Tabla de Detalle Torneo-Cancha (Tabla de asociación)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalles_torneo_cancha (
                    id_torneo INTEGER NOT NULL,
                    id_cancha INTEGER NOT NULL,
                    fecha_uso TEXT NOT NULL,
                    hora_uso TEXT NOT NULL,
                    PRIMARY KEY (id_torneo, id_cancha, fecha_uso, hora_uso),
                    FOREIGN KEY (id_torneo) REFERENCES torneos (id_torneo),
                    FOREIGN KEY (id_cancha) REFERENCES canchas (id_cancha)
                )
            ''')

            conn.commit()
            print("Tablas actualizadas/creadas exitosamente según el diagrama PlantUML.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            conn.rollback()
            raise

    # Los métodos CRUD específicos de Cliente han sido movidos a ClienteDAO
