import customtkinter as ctk
from gui.main_window import VentanaPrincipal
from  database import crear_tablas, poblar_datos_iniciales
import os

ARCHIVO_BD = 'canchas.db'

def inicializar_base_de_datos():
    # si la base de datos no existe la creamos y la llenamos con datos de prueba
    if not os.path.exists(ARCHIVO_BD):
        print(f"Base de datos '{ARCHIVO_BD}' no encontrada. Creando y poblando...")
        
        crear_tablas()
        print("Tablas de la base de datos creadas.")

        poblar_datos_iniciales()
        print("Base de datos poblada con datos iniciales.")
    else:
        print(f"Base de datos '{ARCHIVO_BD}' encontrada. No se requieren acciones.")

if __name__ == "__main__":
    # configuracion de customtkinter
    ctk.set_appearance_mode("Dark")  # modos: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # temas: "blue" (default), "green", "dark-blue"

    # inicializar la base de datos si hace falta
    inicializar_base_de_datos()

    # arrancar la interfaz grafica
    print("Iniciando la aplicación...")
    app = VentanaPrincipal()
    app.mainloop()
