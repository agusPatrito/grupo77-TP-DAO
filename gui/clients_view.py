import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from services.client_service import ClientService
from gui.estilos import FUENTE_BASE, FUENTE_TITULO_VISTA, mostrar_mensaje_personalizado # importamos la funcion de mensaje

class VistaClientes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # controller es la VentanaPrincipal
        self.servicio_cliente = ClientService()

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

        titulo = ctk.CTkLabel(frame_superior, text="Gestion de Clientes", font=FUENTE_TITULO_VISTA)
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
        self.apellido_var = ctk.StringVar()
        self.dni_var = ctk.StringVar()

        ctk.CTkLabel(frame_formulario, text="ID", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        self.entrada_id = ctk.CTkEntry(frame_formulario, textvariable=self.id_var, state='disabled', font=FUENTE_BASE)
        self.entrada_id.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Nombre", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(frame_formulario, textvariable=self.nombre_var, font=FUENTE_BASE).pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Apellido", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(frame_formulario, textvariable=self.apellido_var, font=FUENTE_BASE).pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="DNI", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(frame_formulario, textvariable=self.dni_var, font=FUENTE_BASE).pack(fill="x", padx=10)

        # botones del formulario
        frame_botones = ctk.CTkFrame(frame_formulario)
        frame_botones.pack(fill="x", padx=10, pady=20)
        frame_botones.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(frame_botones, text="Agregar", command=self.agregar_cliente, font=FUENTE_BASE).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Actualizar", command=self.actualizar_cliente, font=FUENTE_BASE).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Eliminar", command=self.eliminar_cliente, font=FUENTE_BASE).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="Limpiar", command=self.limpiar_formulario, font=FUENTE_BASE).grid(row=0, column=3, padx=5)

        # frame de la tabla (derecha)
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # treeview para la lista de clientes
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", borderwidth=0, font=FUENTE_BASE)
        style.map('Treeview', background=[('selected', '#2cb67d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=FUENTE_BASE)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.arbol = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "DNI"), show="headings")
        self.arbol.heading("ID", text="ID")
        self.arbol.heading("Nombre", text="Nombre")
        self.arbol.heading("Apellido", text="Apellido")
        self.arbol.heading("DNI", text="DNI")
        self.arbol.grid(row=0, column=0, sticky="nsew")

        self.arbol.bind("<<TreeviewSelect>>", self.al_seleccionar_cliente)

        self.cargar_clientes()

    def cargar_clientes(self):
        for i in self.arbol.get_children():
            self.arbol.delete(i)
        clientes = self.servicio_cliente.obtener_todos_los_clientes()
        for cliente in clientes:
            self.arbol.insert("", "end", values=(cliente.id_cliente, cliente.nombre, cliente.apellido, cliente.dni))

    def agregar_cliente(self):
        try:
            self.servicio_cliente.agregar_cliente(self.nombre_var.get(), self.apellido_var.get(), self.dni_var.get())
            mostrar_mensaje_personalizado(self.controller, "Exito", "Cliente agregado correctamente", tipo="info")
            self.cargar_clientes()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")

    def actualizar_cliente(self):
        if not self.id_var.get():
            mostrar_mensaje_personalizado(self.controller, "Advertencia", "Seleccione un cliente para actualizar", tipo="warning")
            return
        try:
            self.servicio_cliente.actualizar_cliente(self.id_var.get(), self.nombre_var.get(), self.apellido_var.get(), self.dni_var.get())
            mostrar_mensaje_personalizado(self.controller, "Exito", "Cliente actualizado correctamente", tipo="info")
            self.cargar_clientes()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")

    def eliminar_cliente(self):
        if not self.id_var.get():
            mostrar_mensaje_personalizado(self.controller, "Advertencia", "Seleccione un cliente para eliminar", tipo="warning")
            return
        
        respuesta = mostrar_mensaje_personalizado(self.controller, "Confirmar", "¿Esta seguro de que desea eliminar este cliente?", tipo="question")
        if respuesta:
            try:
                self.servicio_cliente.eliminar_cliente(self.id_var.get())
                mostrar_mensaje_personalizado(self.controller, "Exito", "Cliente eliminado correctamente", tipo="info")
                self.cargar_clientes()
                self.limpiar_formulario()
            except Exception as e:
                mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")

    def al_seleccionar_cliente(self, event):
        item_seleccionado = self.arbol.focus()
        if item_seleccionado:
            item = self.arbol.item(item_seleccionado)
            values = item['values']
            self.id_var.set(values[0])
            self.nombre_var.set(values[1])
            self.apellido_var.set(values[2])
            self.dni_var.set(values[3])

    def limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.dni_var.set("")
        self.arbol.selection_remove(self.arbol.selection())
