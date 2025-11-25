from dao import ReservaDAO

class ReportingService:
    def __init__(self):
        self.reserva_dao = ReservaDAO()

    def get_canchas_mas_utilizadas(self):
        """
        Obtiene un ranking de las canchas más utilizadas.
        Retorna dos listas: una con los nombres de las canchas y otra con los totales.
        """
        data = self.reserva_dao.reporte_canchas_mas_utilizadas()
        
        nombres = [row['nombre'] for row in data]
        totales = [row['total_reservas'] for row in data]
        
        return nombres, totales

    def get_utilizacion_mensual(self):
        """
        Obtiene la utilización de canchas por mes.
        Retorna una lista de tuplas (mes, total_reservas).
        """
        data = self.reserva_dao.reporte_utilizacion_mensual()
        
        # Asegurarse de que los meses esten ordenados
        # (La consulta SQL ya lo hace, pero una doble verificación no hace daño)
        sorted_data = sorted(data, key=lambda x: x['mes'])
        
        meses = [row['mes'] for row in sorted_data]
        totales = [row['total_reservas'] for row in sorted_data]
        
        return meses, totales
    
    def get_canchas_mas_utilizadas_con_ingresos(self):
        data = self.reserva_dao.reporte_canchas_mas_utilizadas_con_ingresos()
        return data


    def get_reservas_por_hora(self):
        data = self.reserva_dao.reporte_reservas_por_horario()
        horas = [row["hora"] for row in data]
        totales = [row["total"] for row in data]
        return horas, totales

