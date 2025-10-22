
import os
from src.database.database_manager import DatabaseManager
from src.database.cliente_dao import ClienteDAO
from src.database.cancha_dao import CanchaDAO
from src.database.estado_cancha_dao import EstadoCanchaDAO
from src.database.models import Cliente, Cancha, EstadoCancha

# --- Configuración Inicial ---
project_root = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(project_root, 'data', 'canchas.db')

def inicializar_db(db_manager):
    db_manager.create_tables()

def poblar_datos_iniciales(db_manager):
    """Puebla la base de datos con datos iniciales como los estados de cancha."""
    print("\n--- Poblando Datos Iniciales ---")
    conn = db_manager.get_connection()
    estado_dao = EstadoCanchaDAO(conn)
    
    estado_dao.add(EstadoCancha(None, 'Disponible', 'La cancha está libre para ser reservada.'))
    estado_dao.add(EstadoCancha(None, 'Ocupada', 'La cancha está actualmente en uso.'))
    estado_dao.add(EstadoCancha(None, 'Mantenimiento', 'La cancha no está disponible por mantenimiento.'))
    
    print("Estados de cancha creados.")

def probar_dao_clientes(cliente_dao):
    # ... (código de prueba de clientes sin cambios, solo se pasa el dao)
    print("\n--- Probando Patrón DAO para Clientes ---")
    cliente_juan = Cliente(None, "Juan Perez", "30123456")
    id_juan = cliente_dao.add(cliente_juan)
    # ... (resto del código de prueba)

def probar_dao_canchas(db_manager):
    """Función de prueba para demostrar el uso del DAO para Canchas."""
    print("\n--- Probando Patrón DAO para Canchas ---")
    conn = db_manager.get_connection()
    cancha_dao = CanchaDAO(conn)
    estado_dao = EstadoCanchaDAO(conn)

    # 1. Obtener los estados para usarlos en las canchas
    estado_disponible = estado_dao.get_by_name('Disponible')
    estado_mantenimiento = estado_dao.get_by_name('Mantenimiento')

    # 2. Agregar nuevas canchas
    print("\nAgregando nuevas canchas...")
    cancha_futbol5 = Cancha(None, estado_disponible.id_estado, "Fútbol 5 A", "Fútbol", 1000.0)
    id_cancha1 = cancha_dao.add(cancha_futbol5)
    
    cancha_tenis = Cancha(None, estado_disponible.id_estado, "Tenis Rápida", "Tenis", 1500.0)
    id_cancha2 = cancha_dao.add(cancha_tenis)

    # 3. Consultar todas las canchas
    print("\nListando todas las canchas...")
    todas_las_canchas = cancha_dao.get_all()
    for cancha in todas_las_canchas:
        print(f"  ID: {cancha.id_cancha}, Nombre: {cancha.nombre}, Deporte: {cancha.tipo_deporte}, Precio: ${cancha.tarifa_hora}")

    # 4. Actualizar una cancha (ponerla en mantenimiento)
    print(f"\nActualizando cancha '{cancha_futbol5.nombre}' a estado Mantenimiento...")
    cancha_a_actualizar = cancha_dao.get_by_id(id_cancha1)
    if cancha_a_actualizar:
        cancha_a_actualizar.id_estado = estado_mantenimiento.id_estado
        cancha_a_actualizar.tarifa_hora = 1100.0 # Aumento de precio
        cancha_dao.update(cancha_a_actualizar)
    
    cancha_actualizada = cancha_dao.get_by_id(id_cancha1)
    print(f"  Datos actualizados -> ID Estado: {cancha_actualizada.id_estado}, Precio: ${cancha_actualizada.tarifa_hora}")

    # 5. Eliminar una cancha
    print(f"\nEliminando cancha '{cancha_tenis.nombre}'...")
    cancha_dao.delete(id_cancha2)

    # 6. Consultar todas las canchas de nuevo
    print("\nListando canchas restantes...")
    canchas_restantes = cancha_dao.get_all()
    for cancha in canchas_restantes:
        print(f"  ID: {cancha.id_cancha}, Nombre: {cancha.nombre}")

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db_manager = DatabaseManager(db_path)

    try:
        inicializar_db(db_manager)
        poblar_datos_iniciales(db_manager)
        
        # Inyectamos la conexión a los DAOs a través del manager
        conn = db_manager.get_connection()
        cliente_dao = ClienteDAO(conn)

        # Ejecutamos las pruebas
        probar_dao_clientes(cliente_dao) # Pasamos el DAO ya creado
        probar_dao_canchas(db_manager) # Pasamos el manager para que la función cree sus DAOs

    except Exception as e:
        print(f"Ocurrió un error en la ejecución principal: {e}")
    finally:
        db_manager.close_connection()
        print("\nConexión a la base de datos cerrada.")

    print("\n--- Fin de las pruebas de DAO ---")
    print("Próximos pasos: Crear los DAO para las entidades restantes (Reserva, Horario, etc.).")
