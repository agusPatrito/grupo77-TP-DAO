from dao import ReservaDAO, CanchaDAO, ClienteDAO, HorariosDAO, EstadosReservaDAO, HorariosXCanchasDAO
from models import Reserva, HorariosXCanchas, Cliente
from services.court_service import CourtService
import datetime

class ReservationService:
    def __init__(self):
        self.reserva_dao = ReservaDAO()
        self.cancha_dao = CanchaDAO()
        self.cliente_dao = ClienteDAO()
        self.horarios_dao = HorariosDAO() # Nuevo DAO
        self.estados_reserva_dao = EstadosReservaDAO() # Nuevo DAO
        self.horarios_x_canchas_dao = HorariosXCanchasDAO() # Nuevo DAO
        self.servicio_cancha = CourtService()

        # cargamos IDs de estados de reserva al inicio
        self.id_estado_confirmada = self.estados_reserva_dao.obtener_por_nombre('Confirmada').id_estado_reserva
        self.id_estado_cancelada = self.estados_reserva_dao.obtener_por_nombre('Cancelada').id_estado_reserva
        self.id_estado_pendiente = self.estados_reserva_dao.obtener_por_nombre('Pendiente').id_estado_reserva


    def obtener_detalles_reservas(self):
        return self.reserva_dao.obtener_todos_detalles()

    def obtener_todos_los_clientes(self):
        return self.cliente_dao.obtener_todos()
    
    def obtener_todas_las_canchas(self):
        return self.cancha_dao.obtener_todos()

    def obtener_horarios_disponibles_para_cancha(self, id_cancha, fecha_str): # Eliminado dia_semana
        # este metodo ahora devuelve los horarios de la tabla Horarios que estan libres
        horarios_base = self.horarios_dao.obtener_todos()
        horarios_libres = []

        for horario in horarios_base:
            # verificamos si el slot de 1 hora esta ocupado en HorariosXCanchas
            # solo consideramos ocupados los slots de reservas confirmadas
            if not self.horarios_x_canchas_dao.verificar_ocupacion(id_cancha, horario.id_horario, fecha_str, self.id_estado_confirmada):
                horarios_libres.append(horario)
        return horarios_libres

   # reservation_service.py (parte de class ReservationService)

    def agregar_reserva(self, id_cliente, id_cancha, fecha, hora_inicio, duracion, monto):
        if not all([id_cliente, id_cancha, fecha, hora_inicio, duracion, monto]):
            raise ValueError("Todos los campos son obligatorios")

        duracion_float = float(duracion)
        hora_actual_dt = datetime.datetime.strptime(hora_inicio, '%H:%M').time()

        # verifico existencia de horarios base y calculo ids de los slots que corresponderian
        slots_a_ocupar_ids = []
        for _ in range(int(duracion_float)):
            horario_obj = self.horarios_dao.obtener_por_hora_inicio(hora_actual_dt.strftime('%H:%M'))
            if not horario_obj:
                raise ValueError(f"Horario base {hora_actual_dt.strftime('%H:%M')} no encontrado")
            slots_a_ocupar_ids.append(horario_obj.id_horario)
            hora_actual_dt = (datetime.datetime.combine(datetime.date.min, hora_actual_dt) + datetime.timedelta(hours=1)).time()

        cancha = self.servicio_cancha.obtener_cancha_por_id(id_cancha)
        if not cancha:
            raise ValueError("Cancha no encontrada")
        hora_inicio_int = int(hora_inicio.split(':')[0])
        hora_fin = hora_inicio_int + duracion_float
        if not cancha.tiene_luz and hora_fin > 18:
            raise ValueError(f"Una reserva de {duracion} hs desde las {hora_inicio} en una cancha sin luz excede el horario permitido (18:00)")

        # CREAR la reserva con estado PENDIENTE (no confirmada) -> no ocupamos slots ahora
        nueva_reserva = Reserva(id_reserva=None, id_cliente=id_cliente, id_cancha=id_cancha,
                                id_estado_reserva=self.id_estado_pendiente, # ahora Pendiente
                                fecha=fecha, hora_inicio=hora_inicio, duracion_horas=duracion_float,
                                monto_total=float(monto))

        id_reserva_creada = self.reserva_dao.crear(nueva_reserva)

        # opcional: retornar el id y/o la lista de slots esperados (para mostrar en UI)
        return id_reserva_creada
    
    def confirmar_pago(self, id_reserva):
        reserva = self.reserva_dao.obtener_reserva_por_id(id_reserva)
        if not reserva:
            raise ValueError("La reserva no existe.")

        if reserva.id_estado_reserva != self.id_estado_pendiente:
            raise ValueError("Solo se pueden confirmar reservas en estado Pendiente.")

        # Recalculo los slots a partir de la reserva (hora_inicio y duracion)
        hora_actual_dt = datetime.datetime.strptime(reserva.hora_inicio, '%H:%M').time()
        slots_a_ocupar_ids = []
        for _ in range(int(reserva.duracion_horas)):
            horario_obj = self.horarios_dao.obtener_por_hora_inicio(hora_actual_dt.strftime('%H:%M'))
            if not horario_obj:
                raise ValueError(f"Horario base {hora_actual_dt.strftime('%H:%M')} no encontrado")
            # Chequeo ocupación por reservas CONFIRMADAS
            if self.horarios_x_canchas_dao.verificar_ocupacion(reserva.id_cancha, horario_obj.id_horario, reserva.fecha, self.id_estado_confirmada):
                raise ValueError(f"El slot {hora_actual_dt.strftime('%H:%M')} ya fue ocupado por otra reserva confirmada. No se pudo confirmar.")
            slots_a_ocupar_ids.append(horario_obj.id_horario)
            hora_actual_dt = (datetime.datetime.combine(datetime.date.min, hora_actual_dt) + datetime.timedelta(hours=1)).time()

        # Aquí podemos simular el pago (ej: llamada a pasarela). Lo simulamos con un print/log.
        print("Simulando pago online... (aqui iría la llamada real)")

        # Usamos el metodo atomic del DAO para actualizar estado y crear horarios_x_canchas
        self.reserva_dao.confirmar_reserva_con_slots(id_reserva, self.id_estado_confirmada, reserva.id_cancha, reserva.fecha, slots_a_ocupar_ids)

        return True




    def cancelar_reserva(self, id_reserva):
        reserva_existente = self.reserva_dao.obtener_reserva_por_id(id_reserva)
        if not reserva_existente:
            raise ValueError("Reserva no encontrada")
        
        # actualizamos el estado de la reserva a Cancelada
        reserva_existente.id_estado_reserva = self.id_estado_cancelada
        self.reserva_dao.actualizar(reserva_existente)

        # no liberamos los slots de HorariosXCanchas, solo cambiamos el estado de la reserva
        # esto permite mantener un historial de que esos slots fueron parte de una reserva cancelada

    def eliminar_reserva(self, id_reserva):
        if not id_reserva:
            raise ValueError("Se necesita el ID de la reserva para eliminarla")
        
        # antes de eliminar la reserva, liberamos los slots que ocupaba
        self.horarios_x_canchas_dao.eliminar_por_reserva(id_reserva)
        
        self.reserva_dao.eliminar(id_reserva)

    def eliminar_reservas_canceladas(self):
        # obtenemos el id del estado 'Cancelada'
        id_cancelada = self.estados_reserva_dao.obtener_por_nombre('Cancelada').id_estado_reserva
        
        # el DAO de Reserva ya maneja la liberacion de slots para las reservas canceladas
        self.reserva_dao.eliminar_reservas_por_estado(id_cancelada)

    def agregar_cliente(self, nombre, apellido):
        """
        Crea un cliente nuevo con DNI temporal y devuelve su id_cliente.
        """
        # DNI temporal único, solo para cumplir el NOT NULL + UNIQUE
        dni_temp = f"tmp-{datetime.datetime.now().timestamp()}"

        nuevo_cliente = Cliente(
            id_cliente=None,
            nombre=nombre,
            apellido=apellido,
            dni=dni_temp
        )

        nuevo_id = self.cliente_dao.crear(nuevo_cliente)
        return nuevo_id
    
    def eliminar_reservas_finalizadas(self):
        hoy_str = datetime.date.today().strftime('%Y-%m-%d')
        self.reserva_dao.eliminar_reservas_finalizadas(hoy_str, self.id_estado_confirmada)