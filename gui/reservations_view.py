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
        frame_superior.grid_columnconfigure(1, weight=1)  # la columna del titulo se expande

        try:
            img_volver_pil = Image.open("gui/assets/volver.png")
            img_volver = ctk.CTkImage(img_volver_pil)
        except Exception as e:
            print(f"Error al cargar imagen de volver: {e}")
            img_volver = None

        btn_volver = ctk.CTkButton(
            frame_superior,
            text="",
            image=img_volver,
            command=lambda: controller.mostrar_vista("menu_principal"),
            width=40,
            height=40
        )
        btn_volver.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        titulo = ctk.CTkLabel(
            frame_superior,
            text="Gestion de Reservas",
            font=FUENTE_TITULO_VISTA
        )
        titulo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # frame principal para el contenido
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        # configuracion de la grilla principal: la columna 1 (tabla) se expande, la 0 (formulario) no
        self.frame_principal.grid_columnconfigure(0, weight=0)  # formulario con peso 0
        self.frame_principal.grid_columnconfigure(1, weight=1)  # tabla con peso 1
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

        ctk.CTkLabel(frame_formulario, text="ID", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        ctk.CTkEntry(frame_formulario, textvariable=self.id_var, state='disabled', font=FUENTE_BASE).pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Cliente", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_cliente = ctk.CTkComboBox(frame_formulario, variable=self.cliente_var, font=FUENTE_BASE)
        self.combo_cliente.pack(fill="x", padx=10)
        # autocomplete mientras escribe
        self.combo_cliente.bind("<KeyRelease>", self._filtrar_clientes_por_texto)

        ctk.CTkLabel(frame_formulario, text="Cancha", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_cancha = ctk.CTkComboBox(
            frame_formulario,
            variable=self.cancha_var,
            command=self.al_cambiar_cancha_o_duracion,
            font=FUENTE_BASE,
            state="readonly"
        )
        self.combo_cancha.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Fecha", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        self.calendario = Calendar(
            frame_formulario,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            mindate=datetime.date.today(),
            font=FUENTE_BASE
        )
        self.calendario.pack(fill="x", padx=10)
        self.calendario.bind("<<CalendarSelected>>", self.actualizar_horarios_disponibles)

        ctk.CTkLabel(frame_formulario, text="Hora", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_hora = ctk.CTkComboBox(frame_formulario, variable=self.hora_var, font=FUENTE_BASE)
        self.combo_hora.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Duracion (hs)", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_duracion = ctk.CTkComboBox(
            frame_formulario,
            variable=self.duracion_var,
            values=["1", "2", "3", "4"],
            command=self.al_cambiar_cancha_o_duracion,
            font=FUENTE_BASE,
            state="readonly"
        )
        self.combo_duracion.pack(fill="x", padx=10)

        ctk.CTkLabel(frame_formulario, text="Monto Total", font=FUENTE_BASE).pack(anchor="w", padx=10, pady=(5, 0))
        self.entrada_monto = ctk.CTkEntry(frame_formulario, textvariable=self.monto_var, state='disabled', font=FUENTE_BASE)
        self.entrada_monto.pack(fill="x", padx=10)

        frame_botones = ctk.CTkFrame(frame_formulario)
        frame_botones.pack(fill="x", padx=10, pady=15)
        frame_botones.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(frame_botones, text="Agregar", command=self.agregar_reserva, font=FUENTE_BASE).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Confirmar", command=self.confirmar_pago, font=FUENTE_BASE).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_botones, text="Cancelar", command=self.cancelar_reserva, font=FUENTE_BASE).grid(row=0, column=2, padx=5)
        ctk.CTkButton(frame_botones, text="Limpiar", command=self.limpiar_formulario, font=FUENTE_BASE).grid(row=0, column=3, padx=5)

        # frame de la tabla (derecha)
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # 👉 todas las filas de filtros con weight 0
        frame_tabla.grid_rowconfigure(0, weight=0)   # fila filtros estado
        frame_tabla.grid_rowconfigure(1, weight=0)   # fila filtro fecha
        frame_tabla.grid_rowconfigure(2, weight=0)   # fila filtro cancha

        # 👉 solo la fila de la tabla se expande
        frame_tabla.grid_rowconfigure(3, weight=1)

        frame_tabla.grid_columnconfigure(0, weight=1)

        # ----- FILTROS (PRIMERA FILA) -----
        frame_filtros = ctk.CTkFrame(frame_tabla)
        frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.filtro_estado_var = ctk.StringVar(value="Todas")
        self.filtro_fecha_var = ctk.StringVar()  # nueva variable para filtrar por fecha (YYYY-MM-DD)
        ctk.CTkLabel(frame_filtros, text="Filtrar:", font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Todas", variable=self.filtro_estado_var, value="Todas", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Confirmadas", variable=self.filtro_estado_var, value="Confirmada", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Canceladas", variable=self.filtro_estado_var, value="Cancelada", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)
        ctk.CTkRadioButton(frame_filtros, text="Finalizadas", variable=self.filtro_estado_var, value="Finalizada", command=self.cargar_reservas, font=FUENTE_BASE).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_filtros,
            text="Eliminar Finalizadas",
            command=self.eliminar_reservas_finalizadas,
            font=FUENTE_BASE,
            fg_color="#FF8800"
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            frame_filtros,
            text="Eliminar Canceladas",
            command=self.eliminar_reservas_canceladas,
            font=FUENTE_BASE,
            fg_color="red"
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            frame_filtros,
            text="Refrescar Datos",
            command=self.refrescar_datos,
            font=FUENTE_BASE
        ).pack(side="right", padx=5)

        # ----- Filtro por fecha (fila 1) -----
        self.fecha_filtro_var = ctk.StringVar()

        frame_filtro_fecha = ctk.CTkFrame(frame_tabla)
        frame_filtro_fecha.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        frame_filtro_fecha.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_filtro_fecha.grid_columnconfigure(4, weight=1)  # empuja a la derecha los botones

        ctk.CTkLabel(frame_filtro_fecha, text="Fecha (YYYY-MM-DD):",
                    font=FUENTE_BASE).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entrada_fecha_filtro = ctk.CTkEntry(frame_filtro_fecha,
                                                textvariable=self.fecha_filtro_var,
                                                width=140,
                                                font=FUENTE_BASE)
        self.entrada_fecha_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkButton(frame_filtro_fecha, text="Aplicar fecha",
                    command=self.cargar_reservas,
                    font=FUENTE_BASE, width=110).grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkButton(frame_filtro_fecha, text="Quitar filtro",
                    command=self._limpiar_filtro_fecha,
                    font=FUENTE_BASE, width=110).grid(row=0, column=3, padx=5, pady=5)

        # === 3) FILTRO POR CANCHA (TERCERA FILA) ===
        frame_filtro_cancha = ctk.CTkFrame(frame_tabla)
        frame_filtro_cancha.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        frame_filtro_cancha.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_filtro_cancha, text="Cancha:", font=FUENTE_BASE).grid(row=0, column=0, padx=5)

        self.filtro_cancha_var = ctk.StringVar()
        self.combo_filtro_cancha = ctk.CTkComboBox(
            frame_filtro_cancha,
            variable=self.filtro_cancha_var,
            values=[],
            state="readonly",
            font=FUENTE_BASE,
            command=lambda _: self.cargar_reservas()
        )
        self.combo_filtro_cancha.grid(row=0, column=1, padx=5, sticky="ew")

        # botón limpiar filtro cancha
        ctk.CTkButton(
            frame_filtro_cancha,
            text="Limpiar cancha",
            width=120,
            font=FUENTE_BASE,
            command=self._limpiar_filtro_cancha
        ).grid(row=0, column=2, padx=5)


        # treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", borderwidth=0, font=FUENTE_BASE)
        style.map('Treeview', background=[('selected', '#2cb67d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=FUENTE_BASE)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.arbol = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Cliente", "Cancha", "Fecha", "Hora", "Duracion", "Estado", "Monto"),
            show="headings"
        )
        self.arbol.heading("ID", text="ID")
        self.arbol.heading("Cliente", text="Cliente")
        self.arbol.heading("Cancha", text="Cancha")
        self.arbol.heading("Fecha", text="Fecha")
        self.arbol.heading("Hora", text="Hora")
        self.arbol.heading("Duracion", text="Duracion")
        self.arbol.heading("Estado", text="Estado")
        self.arbol.heading("Monto", text="Monto")
        

        self.arbol.column("ID", width=50, anchor="center", stretch=False)
        self.arbol.column("Hora", width=70, anchor="center", stretch=False)
        self.arbol.column("Duracion", width=80, anchor="center", stretch=False)
        self.arbol.column("Cliente", width=180, anchor="w")
        self.arbol.column("Cancha", width=200, anchor="w")
        self.arbol.column("Fecha", width=100, anchor="center")
        self.arbol.column("Estado", width=110, anchor="center")
        self.arbol.column("Monto", anchor="center", width=90)


        self.arbol.grid(row=3, column=0, sticky="nsew")

        # estructuras auxiliares
        self.clientes = {}
        self.lista_clientes_nombres = []
        self.canchas_map = {}

        self.refrescar_datos()

    def refrescar_datos(self):
        # Mapear clientes por "Nombre Apellido" -> id_cliente
        self.clientes = {
            f"{c.nombre} {c.apellido}".strip(): c.id_cliente
            for c in self.servicio.obtener_todos_los_clientes()
        }
        self.lista_clientes_nombres = list(self.clientes.keys())
        self.combo_cliente.configure(values=self.lista_clientes_nombres)

        # Mapear canchas por "id - nombre" -> id_cancha (o podrías también usar solo nombre)
        self.canchas_map = {
            f"{c.id_cancha} - {c.nombre}": c.id_cancha
            for c in self.servicio.obtener_todas_las_canchas()
        }
        self.combo_cancha.configure(values=list(self.canchas_map.keys()))
        # Cargar nombres de canchas en el filtro
        self.combo_filtro_cancha.configure(values=list(self.canchas_map.keys()))

        self.cargar_reservas()
        self.actualizar_horarios_disponibles()

    def _filtrar_clientes_por_texto(self, event=None):
        """
        Filtra la lista de clientes del combo según lo que se va escribiendo.
        No rompe la opción de crear un cliente nuevo: si no coincide con nadie,
        igual se puede usar ese texto.
        """
        texto = self.cliente_var.get().strip()
        if not texto:
            valores = self.lista_clientes_nombres
        else:
            t = texto.lower()
            valores = [n for n in self.lista_clientes_nombres if t in n.lower()]
            if not valores:
                # si no hay matches, dejamos la lista completa para el dropdown
                valores = self.lista_clientes_nombres

        self.combo_cliente.configure(values=valores)

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
            if not cancha:
                return

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
                    if not cancha.tiene_luz and hora_slot_check >= 18:  # Si cualquier slot del bloque es >= 18 y sin luz
                        bloque_disponible = False
                        break

                    # Verificamos si el slot individual esta ocupado en HorariosXCanchas
                    horario_check_obj = self.servicio.horarios_dao.obtener_por_hora_inicio(hora_slot_str_check)
                    if not horario_check_obj or self.servicio.horarios_x_canchas_dao.verificar_ocupacion(
                        id_cancha,
                        horario_check_obj.id_horario,
                        fecha_seleccionada_str,
                        self.servicio.id_estado_confirmada
                    ):
                        bloque_disponible = False
                        break

                if bloque_disponible:
                    horas_disponibles.append(horario_obj.hora_inicio)

            self.combo_hora.configure(values=horas_disponibles)
            if horas_disponibles:
                self.hora_var.set(horas_disponibles[0])
            else:
                self.hora_var.set("")
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Sin Disponibilidad",
                    "Disculpe no existen turnos disponibles para esa cantidad de horas este dia. "
                    "Pruebe con otro dia u otra duracion",
                    tipo="info"
                )
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
        # limpiar tabla
        for item in self.arbol.get_children():
            self.arbol.delete(item)

        reservas = self.servicio.obtener_detalles_reservas()
        filtro_estado = self.filtro_estado_var.get()
        fecha_filtro = self.fecha_filtro_var.get().strip()
        hoy_str = datetime.date.today().strftime('%Y-%m-%d')

        # 👇 nuevo: valor del filtro de cancha
        cancha_filtro = ""
        if hasattr(self, "filtro_cancha_var"):
            cancha_filtro = self.filtro_cancha_var.get().strip()

        reservas_filtradas = []

        for res in reservas:
            fecha = res["fecha"]
            estado = res["estado_reserva_nombre"]

            # 1) filtro por estado
            mostrar = False
            if filtro_estado == "Todas":
                mostrar = True
            elif filtro_estado == "Finalizada":
                if fecha < hoy_str:
                    mostrar = True
            elif estado == filtro_estado and fecha >= hoy_str:
                mostrar = True

            if not mostrar:
                continue

            # 2) filtro por fecha (si hay algo escrito)
            if fecha_filtro:
                # la fecha tiene que ser EXACTAMENTE igual al texto ingresado
                if fecha != fecha_filtro:
                    continue

            # 3) filtro por cancha (si hay algo elegido)
            if cancha_filtro:
                # en el combo guardamos "id - nombre", en la BD sólo el nombre
                nombre_cancha_filtro = (
                    cancha_filtro.split(" - ", 1)[1]
                    if " - " in cancha_filtro
                    else cancha_filtro
                )
                if res["cancha_nombre"] != nombre_cancha_filtro:
                    continue

            reservas_filtradas.append(res)

        # 4) ordenar por fecha y hora DESCENDENTE
        reservas_ordenadas = sorted(
            reservas_filtradas,
            key=lambda r: (r["fecha"], r["hora_inicio"]),
            reverse=True,
        )

        # 5) cargar a la tabla
        for res in reservas_ordenadas:
            self.arbol.insert(
                "",
                "end",
                values=(
                    res["id_reserva"],
                    res["cliente_nombre"],
                    res["cancha_nombre"],
                    res["fecha"],
                    res["hora_inicio"],
                    res["duracion_horas"],
                    res["estado_reserva_nombre"],
                    res["monto_total"],
                ),
            )

    def _limpiar_filtro_fecha(self):
        self.fecha_filtro_var.set("")
        self.cargar_reservas()


    def _obtener_o_crear_cliente(self):
        texto = self.cliente_var.get().strip()
        if not texto:
            raise ValueError("Debe ingresar o seleccionar un cliente.")

        # Si coincide exactamente con uno existente, usamos ese
        if texto in self.clientes:
            return self.clientes[texto]

        # Si no existe: crear cliente nuevo
        partes = texto.split()
        if len(partes) == 1:
            nombre = partes[0]
            apellido = ""
        else:
            nombre = " ".join(partes[:-1])
            apellido = partes[-1]

        # crear cliente nuevo (devuelve un int)
        nuevo_id = self.servicio.agregar_cliente(nombre, apellido)
        if nuevo_id is None:
            raise ValueError("No se pudo crear el cliente.")

        # si querés dejarlo explícito como int:
        nuevo_id = int(nuevo_id)

        # refrescar mapas y valores del combo
        self.refrescar_datos()
        self.cliente_var.set(f"{nombre} {apellido}".strip())

        return nuevo_id

    def agregar_reserva(self):
        try:
            id_cliente = self._obtener_o_crear_cliente()

            id_cancha = self.canchas_map.get(self.cancha_var.get())
            if not id_cancha:
                raise ValueError("Debe seleccionar una cancha.")

            fecha = self.calendario.get_date()
            hora = self.hora_var.get()
            duracion = self.duracion_var.get()
            monto = self.monto_var.get()

            if not hora:
                raise ValueError("Debe seleccionar un horario.")

            self.servicio.agregar_reserva(
                id_cliente, id_cancha, fecha, hora, duracion, monto
            )

            mostrar_mensaje_personalizado(
                self.controller, "Exito", "Reserva agregada", tipo="info"
            )
            self.refrescar_datos()
            self.limpiar_formulario()

        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", str(e), tipo="error")

    def cancelar_reserva(self):
        item_seleccionado = self.arbol.focus()
        if not item_seleccionado:
            mostrar_mensaje_personalizado(
                self.controller, "Advertencia",
                "Seleccione una reserva para cancelar", tipo="warning"
            )
            return

        respuesta = mostrar_mensaje_personalizado(
            self.controller, "Confirmar",
            "¿Esta seguro de que desea cancelar esta reserva?", tipo="question"
        )
        if respuesta:
            try:
                item = self.arbol.item(item_seleccionado)['values']
                id_reserva = item[0]
                self.servicio.cancelar_reserva(id_reserva)
                mostrar_mensaje_personalizado(
                    self.controller, "Exito", "Reserva cancelada", tipo="info"
                )
                self.refrescar_datos()
            except Exception as e:
                mostrar_mensaje_personalizado(self.controller, "Error", str(e), tipo="error")
    
    def confirmar_pago(self):
        item_seleccionado = self.arbol.focus()
        if not item_seleccionado:
            mostrar_mensaje_personalizado(self.controller, "Advertencia", "Seleccione una reserva para confirmar pago", tipo="warning")
            return

        respuesta = mostrar_mensaje_personalizado(self.controller, "Confirmar Pago", "¿Simular pago y confirmar esta reserva?", tipo="question")
        if not respuesta:
            return

        try:
            item = self.arbol.item(item_seleccionado)['values']
            id_reserva = item[0]
            self.servicio.confirmar_pago(id_reserva)
            mostrar_mensaje_personalizado(self.controller, "Éxito", "Reserva confirmada y paga", tipo="info")
            self.refrescar_datos()
        except Exception as e:
            mostrar_mensaje_personalizado(self.controller, "Error", f"No se pudo confirmar el pago: {e}", tipo="error")


    def eliminar_reservas_canceladas(self):
        respuesta = mostrar_mensaje_personalizado(
            self.controller,
            "Confirmar Eliminacion",
            "¿Esta seguro de que desea eliminar TODAS las reservas canceladas del historial? Esta accion es irreversible",
            tipo="question"
        )
        if respuesta:
            try:
                self.servicio.eliminar_reservas_canceladas()
                mostrar_mensaje_personalizado(
                    self.controller, "Exito",
                    "Reservas canceladas eliminadas correctamente", tipo="info"
                )
                self.refrescar_datos()
            except Exception as e:
                mostrar_mensaje_personalizado(
                    self.controller, "Error",
                    f"Ocurrio un error al eliminar reservas canceladas: {e}", tipo="error"
                )

    def eliminar_reservas_finalizadas(self):
        respuesta = mostrar_mensaje_personalizado(
            self.controller,
            "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar TODAS las reservas finalizadas (fechas pasadas)? Esta acción es irreversible.",
            tipo="question"
        )
        if respuesta:
            try:
                self.servicio.eliminar_reservas_finalizadas()
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Éxito",
                    "Reservas finalizadas eliminadas correctamente",
                    tipo="info"
                )
                self.refrescar_datos()
            except Exception as e:
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Error",
                    f"Ocurrió un error al eliminar reservas finalizadas: {e}",
                    tipo="error"
                )

    def _limpiar_filtro_cancha(self):
        self.filtro_cancha_var.set("")
        self.cargar_reservas()

    def limpiar_formulario(self):
        self.id_var.set("")
        self.cliente_var.set("")
        self.cancha_var.set("")
        self.hora_var.set("")
        self.duracion_var.set("1")
        self.monto_var.set("0.00")
        self.combo_hora.configure(values=[])
        self.calendario.selection_set(datetime.date.today())
