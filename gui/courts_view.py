import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from services.court_service import CourtService
from gui.estilos import FUENTE_BASE, FUENTE_TITULO_VISTA, mostrar_mensaje_personalizado # importamos la funcion de mensaje

class VistaCanchas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # controller es la VentanaPrincipal
        self.servicio_cancha = CourtService()

        # configuramos el grid principal de esta vista
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # frame superior con titulo y boton de volver
        frame_superior = ctk.CTkFrame(self)
        frame_superior.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        frame_superior.grid_columnconfigure(1, weight=1) # la columna del titulo se expande

        try:
            img_volver_pil = Image.open("gui/assets/volver.png")
            img_volver = ctk.CTkImage(img_volver_pil)
        except Exception as e:
            print(f"Error al cargar imagen de volver: {e}")
            img_volver = None

        btn_volver = ctk.CTkButton(frame_superior, text="", image=img_volver,
                                   command=lambda: controller.mostrar_vista("menu_principal"),
                                   width=40, height=40)
        btn_volver.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        titulo = ctk.CTkLabel(frame_superior, text="Gestion de Canchas", font=FUENTE_TITULO_VISTA)
        titulo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # frame principal para el contenido
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        # configuracion de la grilla principal: la columna 1 (tabla) se expande, la 0 (formulario) no
        self.frame_principal.grid_columnconfigure(0, weight=0) # formulario con peso 0
        self.frame_principal.grid_columnconfigure(1, weight=1) # tabla con peso 1
        self.frame_principal.grid_rowconfigure(0, weight=1)

        # frame del formulario (izquierda)
        frame_formulario = ctk.CTkFrame(self.frame_principal, width=300) # ancho fijo para el formulario
        frame_formulario.grid(row=0, column=0, padx=20, pady=20, sticky="ns") # se pega arriba y abajo, pero no se estira horizontalmente
        frame_formulario.grid_columnconfigure(0, weight=1)

        # campos del formulario
        self.id_var = ctk.StringVar()
        self.nombre_var = ctk.StringVar()
        self.luz_var = ctk.BooleanVar()
        self.tarifa_var = ctk.StringVar()

        '''
        ctk.CTkLabel(frame_formulario, text="ID", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        self.entrada_id = ctk.CTkEntry(frame_formulario, textvariable=self.id_var, state='disabled', font=FUENTE_BASE)
        self.entrada_id.pack(fill="x", padx=10)
        '''

        ctk.CTkLabel(frame_formulario, text="Nombre", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(frame_formulario, textvariable=self.nombre_var, font=FUENTE_BASE).pack(fill="x", padx=10)

        ctk.CTkCheckBox(frame_formulario, text="Tiene Luz", variable=self.luz_var, font=FUENTE_BASE).pack(anchor="w", padx=10, pady=10)

        ctk.CTkLabel(frame_formulario, text="Tarifa por Hora", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(frame_formulario, textvariable=self.tarifa_var, font=FUENTE_BASE).pack(fill="x", padx=10)

        # botones del formulario
        frame_botones = ctk.CTkFrame(frame_formulario)
        frame_botones.pack(fill="x", padx=10, pady=20)
        frame_botones.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(frame_botones, text="Agregar", command=self.agregar_cancha, font=FUENTE_BASE).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Actualizar", command=self.actualizar_cancha, font=FUENTE_BASE).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Eliminar", command=self.eliminar_cancha, font=FUENTE_BASE).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="Limpiar", command=self.limpiar_formulario, font=FUENTE_BASE).grid(row=0, column=3, padx=5)

        # frame de la tabla (derecha)
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame_tabla.grid_rowconfigure(1, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # filtros para la tabla
        frame_filtros = ctk.CTkFrame(frame_tabla)
        frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.filtro_luz_var = ctk.StringVar(value="Todas")
        ctk.CTkLabel(frame_filtros, text="Filtrar por luz:", font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Todas", variable=self.filtro_luz_var, value="Todas", command=self.cargar_canchas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Con Luz", variable=self.filtro_luz_var, value="Con Luz", command=self.cargar_canchas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Sin Luz", variable=self.filtro_luz_var, value="Sin Luz", command=self.cargar_canchas, font=FUENTE_BASE).pack(side="left", padx=5)

        # treeview para la lista de canchas
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", borderwidth=0, font=FUENTE_BASE)
        style.map('Treeview', background=[('selected', '#2cb67d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=FUENTE_BASE)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.arbol = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Tiene Luz", "Tarifa"), show="headings")
        self.arbol.heading("ID", text="ID")
        self.arbol.heading("Nombre", text="Nombre")
        self.arbol.heading("Tiene Luz", text="Tiene Luz")
        self.arbol.heading("Tarifa", text="Tarifa/Hora")
        self.arbol.grid(row=1, column=0, sticky="nsew")

        self.arbol.bind("<<TreeviewSelect>>", self.al_seleccionar_cancha)

        self.cargar_canchas()

    def cargar_canchas(self):
        for i in self.arbol.get_children():
            self.arbol.delete(i)
        
        canchas = self.servicio_cancha.obtener_todas_las_canchas()
        filtro = self.filtro_luz_var.get()

        for cancha in canchas:
            luz_str = "Si" if cancha['tiene_luz'] else "No"
            
            if (filtro == "Todas" or
                (filtro == "Con Luz" and cancha['tiene_luz']) or
                (filtro == "Sin Luz" and not cancha['tiene_luz'])):
                self.arbol.insert("", "end", values=(cancha['id_cancha'], cancha['nombre'], luz_str, cancha['tarifa_hora']))

    def agregar_cancha(self):
        try:
            self.servicio_cancha.agregar_cancha(self.nombre_var.get(), self.luz_var.get(), self.tarifa_var.get())
            mostrar_mensaje_personalizado(self.controller, "Exito", "Cancha agregada correctamente", tipo="info")
            self.cargar_canchas()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")

    def actualizar_cancha(self):
        if not self.id_var.get():
            mostrar_mensaje_personalizado(self.controller, "Advertencia", "Seleccione una cancha para actualizar", tipo="warning")
            return
        try:
            self.servicio_cancha.actualizar_cancha(self.id_var.get(), self.nombre_var.get(), self.luz_var.get(), self.tarifa_var.get())
            mostrar_mensaje_personalizado(self.controller, "Exito", "Cancha actualizada correctamente", tipo="info")
            self.cargar_canchas()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")

    def eliminar_cancha(self):
        if not self.id_var.get():
            mostrar_mensaje_personalizado(self.controller, "Advertencia", "Seleccione una cancha para eliminar", tipo="warning")
            return
        
        respuesta = mostrar_mensaje_personalizado(self.controller, "Confirmar", "¿Esta seguro de que desea eliminar esta cancha?", tipo="question")
        if respuesta:
            try:
                self.servicio_cancha.eliminar_cancha(self.id_var.get())
                mostrar_mensaje_personalizado(self.controller, "Exito", "Cancha eliminada correctamente", tipo="info")
                self.cargar_canchas()
                self.limpiar_formulario()
            except Exception as e:
                mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")

    def al_seleccionar_cancha(self, event):
        item_seleccionado = self.arbol.focus()
        if item_seleccionado:
            item = self.arbol.item(item_seleccionado)['values']
            self.id_var.set(item[0])
            self.nombre_var.set(item[1])
            self.luz_var.set(True if item[2] == "Si" else False)
            self.tarifa_var.set(item[3])

    def limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.luz_var.set(False)
        self.tarifa_var.set("")
        self.arbol.selection_remove(self.arbol.selection())
