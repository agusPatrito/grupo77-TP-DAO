from dao import ReservaDAO, CanchaDAO, ClienteDAO, HorariosDAO, EstadosReservaDAO, HorariosXCanchasDAO
from models import Reserva, HorariosXCanchas
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

    def agregar_reserva(self, id_cliente, id_cancha, fecha, hora_inicio, duracion, monto):
        if not all([id_cliente, id_cancha, fecha, hora_inicio, duracion, monto]):
            raise ValueError("Todos los campos son obligatorios")

        duracion_float = float(duracion)
        hora_inicio_int = int(hora_inicio.split(':')[0])

        # validacion: verificar si los slots estan disponibles usando HorariosXCanchasDAO
        # identificamos todos los slots de 1 hora que abarca la reserva
        slots_a_ocupar_ids = []
        hora_actual_dt = datetime.datetime.strptime(hora_inicio, '%H:%M').time()
        for _ in range(int(duracion_float)):
            horario_obj = self.horarios_dao.obtener_por_hora_inicio(hora_actual_dt.strftime('%H:%M'))
            if not horario_obj:
                raise ValueError(f"Horario base {hora_actual_dt.strftime('%H:%M')} no encontrado")
            
            # verificamos ocupacion solo para reservas confirmadas
            if self.horarios_x_canchas_dao.verificar_ocupacion(id_cancha, horario_obj.id_horario, fecha, self.id_estado_confirmada):
                raise ValueError(f"El slot {hora_actual_dt.strftime('%H:%M')} ya esta ocupado por una reserva confirmada")
            
            slots_a_ocupar_ids.append(horario_obj.id_horario)
            hora_actual_dt = (datetime.datetime.combine(datetime.date.min, hora_actual_dt) + datetime.timedelta(hours=1)).time()


        # obtener detalles de la cancha para verificar la luz
        cancha = self.servicio_cancha.obtener_cancha_por_id(id_cancha)
        if not cancha:
            raise ValueError("Cancha no encontrada")

        # validacion: verificar luz para reservas nocturnas
        hora_fin = hora_inicio_int + duracion_float
        if not cancha.tiene_luz and hora_fin > 18:
            raise ValueError(f"Una reserva de {duracion} hs desde las {hora_inicio} en una cancha sin luz excede el horario permitido (18:00)")

        # creamos la reserva con estado Confirmada
        nueva_reserva = Reserva(id_reserva=None, id_cliente=id_cliente, id_cancha=id_cancha,
                                id_estado_reserva=self.id_estado_confirmada, # Usamos el ID de Confirmada
                                fecha=fecha, hora_inicio=hora_inicio, duracion_horas=duracion_float,
                                monto_total=float(monto))
        
        id_reserva_creada = self.reserva_dao.crear(nueva_reserva)

        # ocupamos los slots correspondientes en horarios_x_canchas
        for id_horario_slot in slots_a_ocupar_ids:
            hxc = HorariosXCanchas(id_horarios_x_canchas=None, id_cancha=id_cancha, 
                                   id_horario=id_horario_slot, id_reserva=id_reserva_creada, fecha=fecha)
            self.horarios_x_canchas_dao.crear(hxc)


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
