
# Este archivo define las clases que representan las entidades de la base de datos.
# Sirven como una estructura de datos para manejar la información en la lógica de la aplicación.

class Cliente:
    def __init__(self, id_cliente, nombre, dni):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.dni = dni

class EstadoCancha:
    def __init__(self, id_estado, nombre, descripcion):
        self.id_estado = id_estado
        self.nombre = nombre
        self.descripcion = descripcion

class Cancha:
    def __init__(self, id_cancha, id_estado, nombre, tipo_deporte, tarifa_hora):
        self.id_cancha = id_cancha
        self.id_estado = id_estado
        self.nombre = nombre
        self.tipo_deporte = tipo_deporte
        self.tarifa_hora = tarifa_hora

class HorarioDisponible:
    def __init__(self, id_horario, id_cancha, dia_semana, hora_inicio, hora_fin):
        self.id_horario = id_horario
        self.id_cancha = id_cancha
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

class Reserva:
    def __init__(self, id_reserva, id_cliente, id_cancha, fecha, hora_inicio, duracion_horas, estado, monto_total):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_cancha = id_cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.duracion_horas = duracion_horas
        self.estado = estado
        self.monto_total = monto_total

class Torneo:
    def __init__(self, id_torneo, nombre, fecha_inicio, fecha_fin):
        self.id_torneo = id_torneo
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

class DetalleTorneoCancha:
    def __init__(self, id_torneo, id_cancha, fecha_uso, hora_uso):
        self.id_torneo = id_torneo
        self.id_cancha = id_cancha
        self.fecha_uso = fecha_uso
        self.hora_uso = hora_uso
