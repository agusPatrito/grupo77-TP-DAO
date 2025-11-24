import customtkinter as ctk
from PIL import Image
from gui.clients_view import VistaClientes
from gui.courts_view import VistaCanchas
from gui.reservations_view import VistaReservas
from gui.reporting_view import VistaReportes # Importar la nueva vista
from gui.estilos import FUENTE_BASE, FUENTE_BOTON_MENU, FUENTE_TITULO_APP, FUENTE_ESLOGAN # importamos las fuentes
from gui.tournaments_view import VistaTorneos


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Canchas")
        self.geometry("1100x768")
        self.minsize(800, 600)

        # contenedor principal que se expande con la ventana
        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True)

        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        # diccionario para guardar las diferentes pantallas
        self.vistas = {}

        # creamos y registramos las pantallas
        self.crear_vistas()
        
        # mostramos el menu principal al inicio
        self.mostrar_vista("menu_principal")

    def crear_vistas(self):
        # pantalla del menu principal
        menu_frame = ctk.CTkFrame(self.contenedor)
        self.vistas["menu_principal"] = menu_frame

        # configuramos la grilla del menu_frame para el nuevo diseño
        menu_frame.grid_columnconfigure(0, weight=0) # columna para los botones
        menu_frame.grid_columnconfigure(1, weight=0) # columna para la linea separadora
        menu_frame.grid_columnconfigure(2, weight=1) # columna para el logo
        menu_frame.grid_rowconfigure(0, weight=1) # fila principal para todo el contenido

        # cargamos las imagenes
        try:
            self.img_clientes = ctk.CTkImage(Image.open("gui/assets/clientes.png"), size=(48, 48))
            self.img_canchas = ctk.CTkImage(Image.open("gui/assets/canchas.png"), size=(48, 48))
            self.img_reservas = ctk.CTkImage(Image.open("gui/assets/reservas.png"), size=(48, 48))
            self.img_reportes = ctk.CTkImage(Image.open("gui/assets/reportes.png"), size=(48, 48)) # Nuevo icono
            self.img_logo = ctk.CTkImage(Image.open("gui/assets/logo.png"), size=(200, 200)) # tamaño para el logo
            self.img_torneos = ctk.CTkImage(Image.open("gui/assets/trofeo.png"), size=(48, 48))
        except Exception as e:
            print(f"Error al cargar imagenes: {e}")
            self.img_clientes = self.img_canchas = self.img_reservas = self.img_reportes = self.img_logo = self.img_torneos = None

        # contenedor para los botones (columna 0)
        frame_botones_menu = ctk.CTkFrame(menu_frame, fg_color="transparent")
        frame_botones_menu.grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        frame_botones_menu.grid_columnconfigure(0, weight=1)
        frame_botones_menu.grid_rowconfigure(0, weight=1) # espacio superior
        frame_botones_menu.grid_rowconfigure(6, weight=1) # espacio inferior

        btn_clientes = ctk.CTkButton(frame_botones_menu, text="Gestionar Clientes", image=self.img_clientes,
                                     compound="top", height=120, width=220, font=FUENTE_BOTON_MENU,
                                     command=lambda: self.mostrar_vista("vista_clientes"))
        btn_clientes.grid(row=1, column=0, pady=15)

        btn_canchas = ctk.CTkButton(frame_botones_menu, text="Gestionar Canchas", image=self.img_canchas,
                                    compound="top", height=120, width=220, font=FUENTE_BOTON_MENU,
                                    command=lambda: self.mostrar_vista("vista_canchas"))
        btn_canchas.grid(row=2, column=0, pady=15)

        btn_reservas = ctk.CTkButton(frame_botones_menu, text="Gestionar Reservas", image=self.img_reservas,
                                     compound="top", height=120, width=220, font=FUENTE_BOTON_MENU,
                                     command=lambda: self.mostrar_vista("vista_reservas"))
        btn_reservas.grid(row=3, column=0, pady=15)

        btn_torneo = ctk.CTkButton(frame_botones_menu, text=" Torneos", image=self.img_torneos, 
                                   compound="top", font=FUENTE_BOTON_MENU, width=220, height=120,
                                   command=lambda: self.mostrar_vista("vista_torneos"))
        btn_torneo.grid(row=4, column=0, pady=15)

        btn_reportes = ctk.CTkButton(frame_botones_menu, text="Ver Reportes", image=self.img_reportes,
                                     compound="top", height=120, width=220, font=FUENTE_BOTON_MENU,
                                     command=lambda: self.mostrar_vista("vista_reportes"))
        btn_reportes.grid(row=5, column=0, pady=15)

        # linea separadora (columna 1)
        linea_separadora = ctk.CTkFrame(menu_frame, width=2, fg_color="gray50") # linea delgada gris
        linea_separadora.grid(row=0, column=1, sticky="ns", padx=10) # se pega arriba y abajo

        # contenedor para el logo y titulos (columna 2)
        frame_logo_y_titulos = ctk.CTkFrame(menu_frame, fg_color="transparent")
        frame_logo_y_titulos.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
        frame_logo_y_titulos.grid_columnconfigure(0, weight=1)
        frame_logo_y_titulos.grid_rowconfigure(0, weight=1) # espacio superior
        frame_logo_y_titulos.grid_rowconfigure(1, weight=0) # fila del logo
        frame_logo_y_titulos.grid_rowconfigure(2, weight=0) # fila del titulo
        frame_logo_y_titulos.grid_rowconfigure(3, weight=0) # fila del eslogan
        frame_logo_y_titulos.grid_rowconfigure(4, weight=1) # espacio inferior

        # logo
        if self.img_logo:
            lbl_logo = ctk.CTkLabel(frame_logo_y_titulos, image=self.img_logo, text="")
            lbl_logo.grid(row=1, column=0, pady=(0, 10))
        else:
            lbl_logo = ctk.CTkLabel(frame_logo_y_titulos, text="LOGO", font=FUENTE_TITULO_APP)
            lbl_logo.grid(row=1, column=0, pady=(0, 10))

        # titulo de la aplicacion
        lbl_titulo_app = ctk.CTkLabel(frame_logo_y_titulos, text="Quierojugar", font=FUENTE_TITULO_APP, text_color="#FFD700")
        lbl_titulo_app.grid(row=2, column=0, pady=(0, 5))

        # eslogan
        lbl_eslogan = ctk.CTkLabel(frame_logo_y_titulos, text='"Reserva tu pasión, juega sin límites."', font=FUENTE_ESLOGAN, text_color="gray70")
        lbl_eslogan.grid(row=3, column=0, pady=(0, 0))


        # creamos y registramos las otras pantallas
        self.vistas["vista_clientes"] = VistaClientes(self.contenedor, self)
        self.vistas["vista_canchas"] = VistaCanchas(self.contenedor, self)
        self.vistas["vista_reservas"] = VistaReservas(self.contenedor, self)
        self.vistas["vista_reportes"] = VistaReportes(self.contenedor, self) # Registrar la nueva vista
        self.vistas["vista_torneos"] = VistaTorneos(self.contenedor, self) # Registrar la vista de torneos

    def mostrar_vista(self, nombre_vista):
        # muestra la pantalla que le pedimos y esconde las demas
        if nombre_vista in self.vistas:
            for vista in self.vistas.values():
                vista.grid_remove()
            
            vista_a_mostrar = self.vistas[nombre_vista]
            vista_a_mostrar.grid(row=0, column=0, sticky="nsew")
        else:
            print(f"Advertencia: La vista '{nombre_vista}' no existe.")
