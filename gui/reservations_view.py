import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from services.reservation_service import ReservationService
from tkcalendar import Calendar
import datetime
from gui.estilos import FUENTE_BASE, FUENTE_TITULO_VISTA
from gui.custom_messagebox import mostrar_mensaje_personalizado

class VistaReservas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.servicio = ReservationService()

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

        titulo = ctk.CTkLabel(frame_superior, text="Gestion de Reservas", font=FUENTE_TITULO_VISTA)
        titulo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # frame principal para el contenido
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        # configuracion de la grilla principal: la columna 1 (tabla) se expande, la 0 (formulario) no
        self.frame_principal.grid_columnconfigure(0, weight=0) # formulario con peso 0
        self.frame_principal.grid_columnconfigure(1, weight=1) # tabla con peso 1
        self.frame_principal.grid_rowconfigure(0, weight=1)


        # frame del formulario (izquierda)
        frame_formulario = ctk.CTkScrollableFrame(self.frame_principal, width=380)
        frame_formulario.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        frame_formulario.grid_columnconfigure(0, weight=1)


        # campos del formulario
        self.id_var = ctk.StringVar()
        self.cliente_var = ctk.StringVar()
        self.cancha_var = ctk.StringVar()
        self.hora_var = ctk.StringVar()
        self.duracion_var = ctk.StringVar(value="1")
        self.monto_var = ctk.StringVar()

        ctk.CTkLabel(frame_formulario, text="ID", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkEntry(frame_formulario, textvariable=self.id_var, state='disabled', font=FUENTE_BASE).pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Cliente", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        self.combo_cliente = ctk.CTkComboBox(frame_formulario, variable=self.cliente_var, font=FUENTE_BASE)
        self.combo_cliente.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Cancha", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        self.combo_cancha = ctk.CTkComboBox(frame_formulario, variable=self.cancha_var, command=self.al_cambiar_cancha_o_duracion, font=FUENTE_BASE)
        self.combo_cancha.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Fecha", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        self.calendario = Calendar(frame_formulario, selectmode='day', date_pattern='yyyy-mm-dd', mindate=datetime.date.today(), font=FUENTE_BASE)
        self.calendario.pack(fill="x", padx=10)
        self.calendario.bind("<<CalendarSelected>>", self.actualizar_horarios_disponibles)

        ctk.CTkLabel(frame_formulario, text="Hora", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        self.combo_hora = ctk.CTkComboBox(frame_formulario, variable=self.hora_var, font=FUENTE_BASE)
        self.combo_hora.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Duracion (hs)", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        self.combo_duracion = ctk.CTkComboBox(frame_formulario, variable=self.duracion_var, values=["1", "2", "3", "4"], command=self.al_cambiar_cancha_o_duracion, font=FUENTE_BASE)
        self.combo_duracion.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Monto Total", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5,0))
        self.entrada_monto = ctk.CTkEntry(frame_formulario, textvariable=self.monto_var, state='disabled', font=FUENTE_BASE)
        self.entrada_monto.pack(fill="x", padx=10)

        frame_botones = ctk.CTkFrame(frame_formulario)
        frame_botones.pack(fill="x", padx=10, pady=15)
        frame_botones.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(frame_botones, text="Agregar Reserva", command=self.agregar_reserva, font=FUENTE_BASE).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Cancelar Reserva", command=self.cancelar_reserva, font=FUENTE_BASE).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Limpiar", command=self.limpiar_formulario, font=FUENTE_BASE).grid(row=0, column=2, padx=5)

        # frame de la tabla (derecha)
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame_tabla.grid_rowconfigure(1, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        frame_filtros = ctk.CTkFrame(frame_tabla)
        frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.filtro_estado_var = ctk.StringVar(value="Todas")
        ctk.CTkLabel(frame_filtros, text="Filtrar:", font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Todas", variable=self.filtro_estado_var, value="Todas", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Confirmadas", variable=self.filtro_estado_var, value="Confirmada", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Canceladas", variable=self.filtro_estado_var, value="Cancelada", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Finalizadas", variable=self.filtro_estado_var, value="Finalizada", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        
        ctk.CTkButton(frame_filtros, text="Eliminar Canceladas", command=self.eliminar_reservas_canceladas, font=FUENTE_BASE, fg_color="red").pack(side="right", padx=5)
        ctk.CTkButton(frame_filtros, text="Refrescar Datos", command=self.refrescar_datos, font=FUENTE_BASE).pack(side="right", padx=5)

        # treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", borderwidth=0, font=FUENTE_BASE)
        style.map('Treeview', background=[('selected', '#2cb67d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=FUENTE_BASE)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.arbol = ttk.Treeview(frame_tabla, columns=("ID", "Cliente", "Cancha", "Fecha", "Hora", "Duracion", "Estado", "Monto"), show="headings")
        self.arbol.heading("ID", text="ID"); self.arbol.heading("Cliente", text="Cliente"); self.arbol.heading("Cancha", text="Cancha"); self.arbol.heading("Fecha", text="Fecha"); self.arbol.heading("Hora", text="Hora"); self.arbol.heading("Duracion", text="Duracion"); self.arbol.heading("Estado", text="Estado"); self.arbol.heading("Monto", text="Monto")
        self.arbol.grid(row=1, column=0, sticky="nsew")

        self.refrescar_datos()

    def refrescar_datos(self):
        self.clientes = {f"{c.id_cliente} - {c.nombre} {c.apellido}": c.id_cliente for c in self.servicio.obtener_todos_los_clientes()}
        self.combo_cliente.configure(values=list(self.clientes.keys()))
        
        self.canchas_map = {f"{c.id_cancha} - {c.nombre}": c.id_cancha for c in self.servicio.obtener_todas_las_canchas()}
        self.combo_cancha.configure(values=list(self.canchas_map.keys()))

        self.cargar_reservas()
        self.actualizar_horarios_disponibles()

    def actualizar_horarios_disponibles(self, event=None):
        id_cancha_str = self.cancha_var.get()
        fecha_seleccionada_str = self.calendario.get_date()
        duracion_str = self.duracion_var.get()

        if not id_cancha_str or not fecha_seleccionada_str or not duracion_str:
            self.combo_hora.configure(values=[])
            self.hora_var.set("")
            return

        try:
            id_cancha = self.canchas_map.get(id_cancha_str)
            duracion = int(duracion_str)
            fecha_seleccionada = datetime.datetime.strptime(fecha_seleccionada_str, '%Y-%m-%d').date()
            dia_semana = fecha_seleccionada.weekday() + 1

            cancha = self.servicio.servicio_cancha.obtener_cancha_por_id(id_cancha)
            if not cancha: return

            horarios_base_libres = self.servicio.obtener_horarios_disponibles_para_cancha(id_cancha, fecha_seleccionada_str)
            
            horas_disponibles = []
            ahora = datetime.datetime.now()
            hora_minima = ahora + datetime.timedelta(hours=2)

            for horario_obj in horarios_base_libres:
                hora_inicio_op = int(horario_obj.hora_inicio.split(':')[0])
                
                # Verificamos si el bloque de 'duracion' horas a partir de hora_inicio_op esta disponible
                bloque_disponible = True
                for i in range(duracion):
                    hora_slot_check = hora_inicio_op + i
                    hora_slot_str_check = f"{hora_slot_check:02d}:00"

                    # Restriccion de 2 horas para el dia actual
                    if fecha_seleccionada == ahora.date() and hora_slot_check < hora_minima.hour:
                        bloque_disponible = False
                        break
                    
                    # Restriccion de luz
                    if not cancha.tiene_luz and hora_slot_check >= 18: # Si cualquier slot del bloque es >= 18 y sin luz
                        bloque_disponible = False
                        break
                    
                    # Verificamos si el slot individual esta ocupado en HorariosXCanchas
                    horario_check_obj = self.servicio.horarios_dao.obtener_por_hora_inicio(hora_slot_str_check)
                    if not horario_check_obj or self.servicio.horarios_x_canchas_dao.verificar_ocupacion(id_cancha, horario_check_obj.id_horario, fecha_seleccionada_str, self.servicio.id_estado_confirmada):
                        bloque_disponible = False
                        break

                if bloque_disponible:
                    horas_disponibles.append(horario_obj.hora_inicio)
            
            self.combo_hora.configure(values=horas_disponibles)
            if horas_disponibles:
                self.hora_var.set(horas_disponibles[0])
            else:
                self.hora_var.set("")
                mostrar_mensaje_personalizado(self.controller, "Sin Disponibilidad", "Disculpe no existen turnos disponibles para esa cantidad de horas este dia. Pruebe con otro dia u otra duracion", tipo="info")
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error: {e}", tipo="error")
            self.combo_hora.configure(values=[])
            self.hora_var.set("")
        
        self.calcular_monto_total()

    def calcular_monto_total(self, event=None):
        id_cancha_str = self.cancha_var.get()
        duracion_str = self.duracion_var.get()

        if not id_cancha_str or not duracion_str:
            self.monto_var.set("0.00")
            return

        try:
            id_cancha = self.canchas_map.get(id_cancha_str)
            duracion = float(duracion_str)
            cancha = self.servicio.servicio_cancha.obtener_cancha_por_id(id_cancha)
            if cancha:
                monto_total = cancha.tarifa_hora * duracion
                self.monto_var.set(f"{monto_total:.2f}")
            else:
                self.monto_var.set("0.00")
        except Exception:
            self.monto_var.set("0.00")

    def al_cambiar_cancha_o_duracion(self, choice):
        self.actualizar_horarios_disponibles()

    def cargar_reservas(self):
        for i in self.arbol.get_children():
            self.arbol.delete(i)
        
        reservas = self.servicio.obtener_detalles_reservas()
        filtro = self.filtro_estado_var.get()
        hoy_str = datetime.date.today().strftime('%Y-%m-%d')

        for res in reservas:
            mostrar = False
            if filtro == "Todas":
                mostrar = True
            elif filtro == "Finalizada":
                if res['fecha'] < hoy_str:
                    mostrar = True
            elif res['estado_reserva_nombre'] == filtro and res['fecha'] >= hoy_str:
                mostrar = True
            
            if mostrar:
                self.arbol.insert("", "end", values=(res['id_reserva'], res['cliente_nombre'], res['cancha_nombre'], res['fecha'], res['hora_inicio'], res['duracion_horas'], res['estado_reserva_nombre'], res['monto_total']))

    def agregar_reserva(self):
        try:
            id_cliente = self.clientes.get(self.cliente_var.get())
            id_cancha = self.canchas_map.get(self.cancha_var.get())
            fecha = self.calendario.get_date()
            hora = self.hora_var.get()
            duracion = self.duracion_var.get()
            monto = self.monto_var.get()
            
            self.servicio.agregar_reserva(id_cliente, id_cancha, fecha, hora, duracion, monto)
            mostrar_mensaje_personalizado(self.controller, "Exito", "Reserva agregada", tipo="info")
            self.refrescar_datos()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", str(e), tipo="error")

    def cancelar_reserva(self):
        item_seleccionado = self.arbol.focus()
        if not item_seleccionado:
            mostrar_mensaje_personalizado(self.controller, "Advertencia", "Seleccione una reserva para cancelar", tipo="warning")
            return
        
        respuesta = mostrar_mensaje_personalizado(self.controller, "Confirmar", "¿Esta seguro de que desea cancelar esta reserva?", tipo="question")
        if respuesta:
            try:
                item = self.arbol.item(item_seleccionado)['values']
                id_reserva = item[0]
                self.servicio.cancelar_reserva(id_reserva)
                mostrar_mensaje_personalizado(self.controller, "Exito", "Reserva cancelada", tipo="info")
                self.refrescar_datos()
            except Exception as e:
                mostrar_mensaje_personalizado(self.controller, "Error", str(e), tipo="error")

    def eliminar_reservas_canceladas(self):
        respuesta = mostrar_mensaje_personalizado(self.controller, "Confirmar Eliminacion", 
                                                  "¿Esta seguro de que desea eliminar TODAS las reservas canceladas del historial? Esta accion es irreversible", 
                                                  tipo="question")
        if respuesta:
            try:
                self.servicio.eliminar_reservas_canceladas()
                mostrar_mensaje_personalizado(self.controller, "Exito", "Reservas canceladas eliminadas correctamente", tipo="info")
                self.refrescar_datos()
            except Exception as e:
                mostrar_mensaje_personalizado(self.controller, "Error", f"Ocurrio un error al eliminar reservas canceladas: {e}", tipo="error")

    def limpiar_formulario(self):
        self.id_var.set("")
        self.cliente_var.set("")
        self.cancha_var.set("")
        self.hora_var.set("")
        self.duracion_var.set("1")
        self.monto_var.set("0.00")
        self.combo_hora.configure(values=[])
        self.calendario.selection_set(datetime.date.today())
    


    
