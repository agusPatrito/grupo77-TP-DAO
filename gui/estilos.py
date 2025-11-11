import customtkinter as ctk
from CTkMessagebox import CTkMessagebox # necesitamos esto para los mensajes personalizados

# fuentes para toda la app
FUENTE_BASE = ("Arial", 14)
FUENTE_BOTON_MENU = ("Arial", 18, "bold")
FUENTE_TITULO_VISTA = ("Arial", 24, "bold")
FUENTE_TITULO_APP = ("Arial", 36, "bold")
FUENTE_ESLOGAN = ("Arial", 16, "italic")

# colores que vamos a usar
COLOR_PRINCIPAL = "#FFD700"  # amarillo
COLOR_FONDO_OSCURO = "#2a2d2e" # gris oscuro
COLOR_TEXTO_CLARO = "white"
COLOR_TEXTO_OSCURO = "black"
COLOR_BOTON_NORMAL = "#3484F0" # azul
COLOR_BOTON_HOVER = "#2cb67d" # verde

def mostrar_mensaje_personalizado(app_root, titulo, mensaje, tipo="info", **kwargs):
    # muestra un mensaje con el estilo de la app
    # tipo puede ser 'info', 'warning', 'error', 'question'
    # si es 'question' devuelve True o False
    
    icon_type = "info"
    if tipo == "warning":
        icon_type = "warning"
    elif tipo == "error":
        icon_type = "cancel"
    elif tipo == "question":
        icon_type = "question"
    
    # colores para los botones del mensaje
    button_color = COLOR_PRINCIPAL if tipo == "question" else COLOR_BOTON_NORMAL
    
    msg = CTkMessagebox(
        master=app_root, # importante pasar el master para que se centre bien
        title=titulo, 
        message=mensaje,
        icon=icon_type,
        option_1="Aceptar" if tipo != "question" else "No",
        option_2="Sí" if tipo == "question" else None,
        button_color=button_color,
        button_hover_color=COLOR_BOTON_HOVER,
        text_color=COLOR_TEXTO_CLARO,
        fg_color=COLOR_FONDO_OSCURO,
        **kwargs
    )
    
    if tipo == "question":
        response = msg.get()
        return response == "Sí"
    else:
        msg.get() # esperamos a que el usuario cierre el mensaje
        return None
