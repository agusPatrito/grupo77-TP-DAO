
from abc import ABC, abstractmethod

class BaseDAO(ABC):
    """
    Clase Base Abstracta para los Data Access Objects (DAO).
    Define la interfaz común que todos los DAOs de entidades deben implementar.
    """
    def __init__(self, conn):
        """Recibe una conexión a la base de datos."""
        self.conn = conn

    @abstractmethod
    def add(self, model_instance):
        """Agrega una nueva instancia del modelo a la base de datos."""
        pass

    @abstractmethod
    def get_by_id(self, id_instance):
        """Obtiene una instancia del modelo por su ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Obtiene todas las instancias de un modelo."""
        pass

    @abstractmethod
    def update(self, model_instance):
        """Actualiza una instancia del modelo en la base de datos."""
        pass

    @abstractmethod
    def delete(self, id_instance):
        """Elimina una instancia del modelo por su ID."""
        pass
