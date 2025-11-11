from dao import ClienteDAO
from models import Cliente

class ClientService:
    def __init__(self):
        self.cliente_dao = ClienteDAO()

    def obtener_todos_los_clientes(self):
        return self.cliente_dao.obtener_todos()

    def agregar_cliente(self, nombre, apellido, dni):
        # validaciones
        if not nombre or not apellido or not dni:
            raise ValueError("Nombre apellido y DNI son obligatorios")
        
        # mas validaciones aca
        
        nuevo_cliente = Cliente(id_cliente=None, nombre=nombre, apellido=apellido, dni=dni)
        self.cliente_dao.crear(nuevo_cliente)

    def actualizar_cliente(self, id_cliente, nombre, apellido, dni):
        if not id_cliente or not nombre or not apellido or not dni:
            raise ValueError("Todos los campos son obligatorios para actualizar")
            
        cliente_a_actualizar = Cliente(id_cliente=id_cliente, nombre=nombre, apellido=apellido, dni=dni)
        self.cliente_dao.actualizar(cliente_a_actualizar)

    def eliminar_cliente(self, id_cliente):
        if not id_cliente:
            raise ValueError("Se necesita el ID del cliente para eliminarlo")
        self.cliente_dao.eliminar(id_cliente)
