from dao import TorneoDAO, DetalleTorneoReservaDAO, ReservaDAO
from models import Torneo
import datetime

class TournamentService:
    def __init__(self):
        self.torneo_dao = TorneoDAO()
        self.detalle_dao = DetalleTorneoReservaDAO()
        self.reserva_dao = ReservaDAO()

    # ---------- Torneos ----------
    def listar_torneos(self):
        return self.torneo_dao.obtener_todos()

    def crear_torneo(self, nombre, fecha_inicio_str, fecha_fin_str):
        if not nombre or not fecha_inicio_str or not fecha_fin_str:
            raise ValueError("Nombre y fechas son obligatorios")

        fi = self._parse_fecha(fecha_inicio_str)
        ff = self._parse_fecha(fecha_fin_str)

        if ff < fi:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio")

        torneo = Torneo(
            id_torneo=None,
            nombre=nombre.strip(),
            fecha_inicio=fi.strftime("%Y-%m-%d"),
            fecha_fin=ff.strftime("%Y-%m-%d")
        )
        return self.torneo_dao.crear(torneo)

    def actualizar_torneo(self, id_torneo, nombre, fecha_inicio_str, fecha_fin_str):
        if not id_torneo:
            raise ValueError("Falta el ID del torneo")

        fi = self._parse_fecha(fecha_inicio_str)
        ff = self._parse_fecha(fecha_fin_str)
        if ff < fi:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio")

        torneo = Torneo(
            id_torneo=id_torneo,
            nombre=nombre.strip(),
            fecha_inicio=fi.strftime("%Y-%m-%d"),
            fecha_fin=ff.strftime("%Y-%m-%d")
        )
        self.torneo_dao.actualizar(torneo)

    def eliminar_torneo(self, id_torneo):
        if not id_torneo:
            raise ValueError("Falta el ID del torneo")
        self.torneo_dao.eliminar(id_torneo)

    # ---------- Reservas en torneo ----------
    def listar_reservas_de_torneo(self, id_torneo):
        return self.detalle_dao.obtener_reservas_de_torneo(id_torneo)

    def agregar_reserva_a_torneo(self, id_torneo, id_reserva):
        torneo = self.torneo_dao.obtener_por_id(id_torneo)
        if not torneo:
            raise ValueError("Torneo no encontrado")

        reserva = self.reserva_dao.obtener_reserva_por_id(id_reserva)
        if not reserva:
            raise ValueError("Reserva no encontrada")

        # validación: que la fecha de la reserva esté dentro del rango del torneo
        fi = self._parse_fecha(torneo.fecha_inicio)
        ff = self._parse_fecha(torneo.fecha_fin)
        fr = self._parse_fecha(reserva.fecha)

        if fr < fi or fr > ff:
            raise ValueError("La reserva está fuera del rango de fechas del torneo")

        self.detalle_dao.agregar_reserva_a_torneo(id_torneo, id_reserva)

    def quitar_reserva_de_torneo(self, id_torneo, id_reserva):
        self.detalle_dao.quitar_reserva_de_torneo(id_torneo, id_reserva)

    # ---------- helpers ----------
    def _parse_fecha(self, fecha_str):
        # admite 'YYYY-MM-DD' directo
        return datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
    
    def reservas_disponibles_para_torneo(self, id_torneo):
        """
        Reservas dentro del rango de fechas del torneo
        y que todavía no estén asociadas a ese torneo.
        """
        torneo = self.torneo_dao.obtener_por_id(id_torneo)
        if not torneo:
            raise ValueError("Torneo no encontrado")

        # todas las reservas entre fecha_inicio y fecha_fin
        todas = self.reserva_dao.obtener_reservas_por_rango(
            torneo.fecha_inicio,
            torneo.fecha_fin
        )

        # ids ya asociadas al torneo
        ya_asociadas = {
            fila["id_reserva"] for fila in self.detalle_dao.obtener_reservas_de_torneo(id_torneo)
        }

        # filtramos las que ya están en el torneo
        disponibles = [r for r in todas if r["id_reserva"] not in ya_asociadas]
        return disponibles
