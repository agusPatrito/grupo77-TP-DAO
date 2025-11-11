class Cliente:
    def __init__(self, id_cliente, nombre, apellido, dni):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

class Cancha:
    def __init__(self, id_cancha, nombre, tiene_luz, tarifa_hora):
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.tiene_luz = tiene_luz
        self.tarifa_hora = tarifa_hora

class Horarios: # Nueva clase
    def __init__(self, id_horario, hora_inicio, hora_fin):
        self.id_horario = id_horario
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

class EstadosReserva: # Nueva clase
    def __init__(self, id_estado_reserva, nombre_estado, descripcion):
        self.id_estado_reserva = id_estado_reserva
        self.nombre_estado = nombre_estado
        self.descripcion = descripcion

class Reserva:
    def __init__(self, id_reserva, id_cliente, id_cancha, id_estado_reserva, fecha, hora_inicio, duracion_horas, monto_total):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_cancha = id_cancha
        self.id_estado_reserva = id_estado_reserva # Ahora es FK
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.duracion_horas = duracion_horas
        self.monto_total = monto_total

class HorariosXCanchas: # Nueva clase
    def __init__(self, id_horarios_x_canchas, id_cancha, id_horario, id_reserva, fecha):
        self.id_horarios_x_canchas = id_horarios_x_canchas
        self.id_cancha = id_cancha
        self.id_horario = id_horario
        self.id_reserva = id_reserva
        self.fecha = fecha

class Torneo:
    def __init__(self, id_torneo, nombre, fecha_inicio, fecha_fin):
        self.id_torneo = id_torneo
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

class DetalleTorneoReserva: # Renombrada de DetalleTorneoCancha
    def __init__(self, id_torneo, id_reserva):
        self.id_torneo = id_torneo
        self.id_reserva = id_reserva
