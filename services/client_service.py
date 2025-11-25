from dao import ClienteDAO
from models import Cliente
import re

class ClientService:
    def __init__(self):
        self.cliente_dao = ClienteDAO()

    def _validar_nombre(self, nombre: str):
        if nombre is None or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        nombre = nombre.strip()
        # Permitir letras (mayúsc/minúsc), acentos y espacio
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise ValueError("El nombre sólo puede contener letras y espacios (sin números).")
        return nombre
    def _validar_apellido(self, apellido: str):
        if apellido is None or not apellido.strip():
            raise ValueError("El apellido no puede estar vacío.")
        apellido = apellido.strip()
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', apellido):
            raise ValueError("El apellido sólo puede contener letras y espacios (sin números).")
        return apellido
    
    def _validar_dni(self, dni_str: str):
        if dni_str is None or not str(dni_str).strip():
            raise ValueError("El DNI no puede estar vacío.")
        dni_s = str(dni_str).strip()
        # Debe ser solo dígitos (no puntos, signos, letras)
        if not dni_s.isdigit():
            raise ValueError("El DNI debe contener sólo dígitos (sin puntos ni signos).")
        # longitud mínima y máxima
        if not (7 <= len(dni_s) <= 8):
            raise ValueError("El DNI debe tener entre 7 y 8 dígitos.")
        dni = int(dni_s)
        if dni <= 0:
            raise ValueError("El DNI debe ser un número entero positivo.")
        return dni


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

