import sqlite3
import datetime

def obtener_conexion_bd():
    # establece una conexion con la base de datos sqlite
    conn = sqlite3.connect('canchas.db')
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    # crea las tablas de la base de datos si no existen
    conn = obtener_conexion_bd()
    cursor = conn.cursor()
    
    # eliminamos tablas para empezar de cero en cada ejecucion (solo para desarrollo)
    cursor.execute("DROP TABLE IF EXISTS detalle_torneo_reserva;")
    cursor.execute("DROP TABLE IF EXISTS torneos;")
    cursor.execute("DROP TABLE IF EXISTS horarios_x_canchas;") # Nueva tabla
    cursor.execute("DROP TABLE IF EXISTS reservas;")
    cursor.execute("DROP TABLE IF EXISTS horarios;") # Nueva tabla
    cursor.execute("DROP TABLE IF EXISTS estados_reserva;") # Nueva tabla
    cursor.execute("DROP TABLE IF EXISTS canchas;")
    cursor.execute("DROP TABLE IF EXISTS clientes;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canchas (
            id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            tiene_luz INTEGER NOT NULL, -- 1 para si, 0 para no
            tarifa_hora REAL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS horarios (
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            hora_inicio TEXT NOT NULL UNIQUE, -- ej '08:00'
            hora_fin TEXT NOT NULL UNIQUE, -- ej '09:00'
            UNIQUE (hora_inicio, hora_fin)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estados_reserva (
            id_estado_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_estado TEXT NOT NULL UNIQUE, -- ej 'Confirmada', 'Cancelada', 'Pendiente'
            descripcion TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_cancha INTEGER NOT NULL,
            id_estado_reserva INTEGER NOT NULL,
            fecha TEXT NOT NULL, -- formato YYYY-MM-DD
            hora_inicio TEXT NOT NULL, -- formato HH:MM (hora de inicio de la reserva general)
            duracion_horas REAL NOT NULL,
            monto_total REAL NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
            FOREIGN KEY (id_cancha) REFERENCES canchas (id_cancha),
            FOREIGN KEY (id_estado_reserva) REFERENCES estados_reserva (id_estado_reserva)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS horarios_x_canchas (
            id_horarios_x_canchas INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cancha INTEGER NOT NULL,
            id_horario INTEGER NOT NULL, -- el slot de 1 hora
            id_reserva INTEGER NOT NULL, -- la reserva que ocupa este slot
            fecha TEXT NOT NULL, -- formato YYYY-MM-DD
            FOREIGN KEY (id_cancha) REFERENCES canchas (id_cancha),
            FOREIGN KEY (id_horario) REFERENCES horarios (id_horario),
            FOREIGN KEY (id_reserva) REFERENCES reservas (id_reserva),
            UNIQUE (id_cancha, id_horario, fecha)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS torneos (
            id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_inicio TEXT,
            fecha_fin TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_torneo_reserva (
            id_torneo INTEGER NOT NULL,
            id_reserva INTEGER NOT NULL,
            PRIMARY KEY (id_torneo, id_reserva),
            FOREIGN KEY (id_torneo) REFERENCES torneos (id_torneo),
            FOREIGN KEY (id_reserva) REFERENCES reservas (id_reserva)
        );
    """)
    
    conn.commit()
    conn.close()

def poblar_datos_iniciales():
    # llena la base de datos con datos de prueba
    conn = obtener_conexion_bd()
    cursor = conn.cursor()
    
    # clientes de prueba
    clientes = [
        ('Juan', 'Perez', '12345678'), ('Maria', 'Gomez', '87654321'),
        ('Carlos', 'Lopez', '11223344'), ('Ana', 'Martinez', '44332211'),
        ('Pedro', 'Rodriguez', '55667788'), ('Laura', 'Fernandez', '99001122')
    ]
    cursor.executemany("INSERT INTO clientes (nombre, apellido, dni) VALUES (?, ?, ?)", clientes)

    # canchas de prueba con nombres de futbolistas
    canchas = [
        ('Cancha Lionel Messi', 1, 1800.0), # con luz
        ('Cancha Cristiano Ronaldo', 1, 1700.0), # con luz
        ('Cancha Diego Maradona', 0, 1500.0), # sin luz
        ('Cancha Pelé', 1, 1900.0), # con luz
        ('Cancha Neymar Jr.', 0, 1400.0), # sin luz
        ('Cancha Kylian Mbappé', 1, 1750.0) # con luz
    ]
    cursor.executemany("INSERT INTO canchas (nombre, tiene_luz, tarifa_hora) VALUES (?, ?, ?)", canchas)

    # horarios de 1 hora (08:00 a 22:00)
    for hora in range(8, 22):
        hora_inicio_str = f"{hora:02d}:00"
        hora_fin_str = f"{(hora + 1):02d}:00"
        cursor.execute("INSERT INTO horarios (hora_inicio, hora_fin) VALUES (?, ?)", (hora_inicio_str, hora_fin_str))

    # estados de reserva
    estados_reserva = [
        ('Confirmada', 'La reserva esta confirmada'),
        ('Cancelada', 'La reserva fue cancelada'),
        ('Pendiente', 'La reserva esta pendiente de confirmacion')
    ]
    cursor.executemany("INSERT INTO estados_reserva (nombre_estado, descripcion) VALUES (?, ?)", estados_reserva)

    conn.commit()
    conn.close()
    print("Base de datos poblada con datos iniciales.")

if __name__ == '__main__':
    crear_tablas()
    poblar_datos_iniciales()
    print("Configuración de la base de datos completa.")
