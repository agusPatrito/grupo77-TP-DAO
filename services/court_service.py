from dao import CanchaDAO
from models import Cancha

class CourtService:
    def __init__(self):
        self.cancha_dao = CanchaDAO()

    def obtener_todas_las_canchas(self):
        return self.cancha_dao.obtener_todos_con_estado()

    def obtener_cancha_por_id(self, id_cancha):
        return self.cancha_dao.obtener_por_id(id_cancha)

    def agregar_cancha(self, nombre, tiene_luz, tarifa_hora):
        if not nombre or not tarifa_hora:
            raise ValueError("Nombre y tarifa son obligatorios")
        
        nueva_cancha = Cancha(id_cancha=None, nombre=nombre, tiene_luz=bool(tiene_luz), 
                              tarifa_hora=float(tarifa_hora))
        self.cancha_dao.crear(nueva_cancha)

    def actualizar_cancha(self, id_cancha, nombre, tiene_luz, tarifa_hora):
        if not all([id_cancha, nombre, tarifa_hora]):
            raise ValueError("ID nombre y tarifa son obligatorios para actualizar")
        
        # obtenemos la cancha actual para asegurarnos que el id_cancha existe
        cancha_actual = self.cancha_dao.obtener_por_id(int(id_cancha))
        if not cancha_actual:
            raise ValueError("La cancha no existe")

        cancha_a_actualizar = Cancha(id_cancha=id_cancha, nombre=nombre, tiene_luz=bool(tiene_luz), 
                                     tarifa_hora=float(tarifa_hora))
        self.cancha_dao.actualizar(cancha_a_actualizar)

    def eliminar_cancha(self, id_cancha):
        if not id_cancha:
            raise ValueError("Se necesita el ID de la cancha para eliminarla")
        self.cancha_dao.eliminar(id_cancha)
