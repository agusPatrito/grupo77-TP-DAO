import customtkinter as ctk
from tkinter import ttk
from PIL import Image
import datetime
from tkcalendar import Calendar

from services.tournament_service import TournamentService
from gui.estilos import FUENTE_BASE, FUENTE_TITULO_VISTA, mostrar_mensaje_personalizado


class SelectorReservaTorneo(ctk.CTkToplevel):
    """
    Ventana emergente para seleccionar una reserva entre las disponibles
    dentro del rango de fechas del torneo.
    """
    def __init__(self, parent, servicio: TournamentService, id_torneo: int, callback):
        super().__init__(parent)
        self.title("Seleccionar reserva para torneo")
        self.servicio = servicio
        self.id_torneo = id_torneo
        self.callback = callback  # función que recibe id_reserva

        self.geometry("900x400")
        self.grab_set()  # modal

        lbl = ctk.CTkLabel(
            self,
            text="Reservas disponibles para este torneo",
            font=FUENTE_TITULO_VISTA
        )
        lbl.pack(pady=(10, 5))

        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id_reserva", "cliente", "cancha", "fecha", "hora", "duracion", "estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        encabezados = ["ID", "Cliente", "Cancha", "Fecha", "Hora", "Duración", "Estado"]
        for col, txt in zip(columnas, encabezados):
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, anchor="center", width=110)

        self.tabla.pack(fill="both", expand=True, padx=5, pady=5)

        # doble clic para seleccionar
        self.tabla.bind("<Double-1>", self._on_double_click)

        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(fill="x", padx=10, pady=(0, 10))
        frame_botones.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            frame_botones,
            text="Seleccionar",
            command=self._seleccionar
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self.destroy
        ).grid(row=0, column=1, padx=5)

        self._cargar_reservas()

    def _cargar_reservas(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        try:
            reservas = self.servicio.reservas_disponibles_para_torneo(self.id_torneo)
            for r in reservas:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        r["id_reserva"],
                        r["cliente"],
                        r["cancha"],
                        r["fecha"],
                        r["hora_inicio"],
                        r["duracion_horas"],
                        r["estado"],
                    ),
                )
        except Exception as e:
            mostrar_mensaje_personalizado(
                self,
                "Error",
                f"Ocurrió un error al cargar reservas: {e}",
                tipo="error"
            )

    def _obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        return int(valores[0])

    def _seleccionar(self):
        id_reserva = self._obtener_id_seleccionado()
        if id_reserva is None:
            mostrar_mensaje_personalizado(
                self,
                "Atención",
                "Seleccione una reserva",
                tipo="info"
            )
            return
        self.callback(id_reserva)
        self.destroy()

    def _on_double_click(self, event):
        self._seleccionar()


class VistaTorneos(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.servicio = TournamentService()

        # configuracion del grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)  # para el bloque de reservas

        # frame superior con boton volver y titulo
        frame_superior = ctk.CTkFrame(self)
        frame_superior.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        frame_superior.grid_columnconfigure(1, weight=1)

        try:
            img_volver_pil = Image.open("gui/assets/volver.png")
            img_volver = ctk.CTkImage(img_volver_pil)
        except Exception:
            img_volver = None

        btn_volver = ctk.CTkButton(
            frame_superior,
            text="",
            image=img_volver,
            command=lambda: controller.mostrar_vista("menu_principal"),
            width=40,
            height=40
        )
        btn_volver.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        titulo = ctk.CTkLabel(
            frame_superior,
            text="Gestión de Torneos",
            font=FUENTE_TITULO_VISTA
        )
        titulo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # ===================== BLOQUE SUPERIOR: formulario + tabla torneos =====================
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=0)
        self.frame_principal.grid_columnconfigure(1, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)

        # formulario (izquierda) con ancho fijo
        frame_formulario = ctk.CTkFrame(self.frame_principal, width=300)
        frame_formulario.grid(row=0, column=0, padx=20, pady=10, sticky="ns")
        frame_formulario.grid_columnconfigure(0, weight=1)

        # campos
        self.id_var = ctk.StringVar()
        self.nombre_var = ctk.StringVar()
        self.fi_var = ctk.StringVar()
        self.ff_var = ctk.StringVar()
        self.id_reserva_var = ctk.StringVar()  # para agregar por ID si querés

        # ID
        '''
        ctk.CTkLabel(
            frame_formulario,
            text="ID",
            font=FUENTE_BASE
        ).pack(anchor="w", padx=10, pady=(10, 0))
        self.entrada_id = ctk.CTkEntry(
            frame_formulario,
            textvariable=self.id_var,
            state='disabled',
            font=FUENTE_BASE
        )
        self.entrada_id.pack(fill="x", padx=10)
        '''
        
        # Nombre
        ctk.CTkLabel(
            frame_formulario,
            text="Nombre",
            font=FUENTE_BASE
        ).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(
            frame_formulario,
            textvariable=self.nombre_var,
            font=FUENTE_BASE
        ).pack(fill="x", padx=10)

        # Fecha inicio + calendario
        ctk.CTkLabel(
            frame_formulario,
            text="Fecha inicio (YYYY-MM-DD)",
            font=FUENTE_BASE
        ).pack(anchor="w", padx=10, pady=(10, 0))

        frame_fecha_inicio = ctk.CTkFrame(frame_formulario)
        frame_fecha_inicio.pack(fill="x", padx=10, pady=(0, 0))

        ctk.CTkEntry(
            frame_fecha_inicio,
            textvariable=self.fi_var,
            font=FUENTE_BASE
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            frame_fecha_inicio,
            text="📅",
            width=40,
            command=self.abrir_calendario_inicio
        ).pack(side="left", padx=(5, 0))

        # Fecha fin + calendario
        ctk.CTkLabel(
            frame_formulario,
            text="Fecha fin (YYYY-MM-DD)",
            font=FUENTE_BASE
        ).pack(anchor="w", padx=10, pady=(10, 0))

        frame_fecha_fin = ctk.CTkFrame(frame_formulario)
        frame_fecha_fin.pack(fill="x", padx=10, pady=(0, 0))

        ctk.CTkEntry(
            frame_fecha_fin,
            textvariable=self.ff_var,
            font=FUENTE_BASE
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            frame_fecha_fin,
            text="📅",
            width=40,
            command=self.abrir_calendario_fin
        ).pack(side="left", padx=(5, 0))

        # botones del formulario
        frame_botones = ctk.CTkFrame(frame_formulario)
        frame_botones.pack(fill="x", padx=10, pady=15)
        frame_botones.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(
            frame_botones,
            text="Agregar",
            command=self.agregar_torneo,
            font=FUENTE_BASE
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Actualizar",
            command=self.actualizar_torneo,
            font=FUENTE_BASE
        ).grid(row=0, column=1, padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Eliminar",
            command=self.eliminar_torneo,
            font=FUENTE_BASE
        ).grid(row=0, column=2, padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            command=self.limpiar_formulario,
            font=FUENTE_BASE
        ).grid(row=0, column=3, padx=5)

        # frame tabla (derecha)
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # estilo y treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            borderwidth=0,
            font=FUENTE_BASE
        )
        style.map('Treeview', background=[('selected', '#2cb67d')])
        style.configure(
            "Treeview.Heading",
            background="#565b5e",
            foreground="white",
            relief="flat",
            font=FUENTE_BASE
        )
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        columnas = ("ID", "Nombre", "Fecha inicio", "Fecha fin")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=120)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self._on_select_torneo)

        # ===================== BLOQUE INFERIOR: reservas del torneo =====================
        self.frame_reservas = ctk.CTkFrame(self)
        self.frame_reservas.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_reservas.grid_columnconfigure(0, weight=3)
        self.frame_reservas.grid_columnconfigure(1, weight=1)
        self.frame_reservas.grid_rowconfigure(0, weight=1)

        # tabla de reservas (izquierda)
        frame_tabla_res = ctk.CTkFrame(self.frame_reservas)
        frame_tabla_res.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        frame_tabla_res.grid_rowconfigure(0, weight=1)
        frame_tabla_res.grid_columnconfigure(0, weight=1)

        columnas_res = ("id_reserva", "cliente", "cancha", "fecha",
                        "hora", "duracion", "estado")
        self.tabla_reservas = ttk.Treeview(
            frame_tabla_res,
            columns=columnas_res,
            show="headings",
            height=8
        )
        encabezados_res = ["ID Reserva", "Cliente", "Cancha",
                           "Fecha", "Hora", "Duración", "Estado"]
        for col, txt in zip(columnas_res, encabezados_res):
            self.tabla_reservas.heading(col, text=txt)
            self.tabla_reservas.column(col, anchor="center", width=110)

        self.tabla_reservas.grid(row=0, column=0, sticky="nsew")

        # panel derecho: acciones sobre reservas
        frame_acciones_res = ctk.CTkFrame(self.frame_reservas)
        frame_acciones_res.grid(row=0, column=1, sticky="nsew")
        frame_acciones_res.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame_acciones_res,
            text="Reservas del torneo",
            font=FUENTE_BASE
        ).pack(anchor="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            frame_acciones_res,
            text="ID de reserva (opcional)",
            font=FUENTE_BASE
        ).pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkEntry(
            frame_acciones_res,
            textvariable=self.id_reserva_var,
            font=FUENTE_BASE
        ).pack(fill="x", padx=10, pady=(0, 10))

        btns_res = ctk.CTkFrame(frame_acciones_res)
        btns_res.pack(fill="x", padx=10, pady=10)
        btns_res.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            btns_res,
            text="Buscar reserva...",
            command=self.abrir_selector_reservas,
            font=FUENTE_BASE
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            btns_res,
            text="Agregar (ID)",
            command=self.agregar_reserva_a_torneo,
            font=FUENTE_BASE
        ).grid(row=0, column=1, padx=5)

        ctk.CTkButton(
            btns_res,
            text="Quitar seleccionada",
            command=self.quitar_reserva_de_torneo,
            font=FUENTE_BASE
        ).grid(row=0, column=2, padx=5)

        # cargar torneos al inicio
        self.cargar_torneos()

    # ===================== LÓGICA VISTA =====================
    def cargar_torneos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for t in self.servicio.listar_torneos():
            self.tabla.insert(
                "",
                "end",
                values=(t.id_torneo, t.nombre, t.fecha_inicio, t.fecha_fin)
            )

    def cargar_reservas_de_torneo(self, id_torneo: int):
        for item in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(item)

        try:
            reservas = self.servicio.listar_reservas_de_torneo(id_torneo)
            for r in reservas:
                self.tabla_reservas.insert(
                    "",
                    "end",
                    values=(
                        r["id_reserva"],
                        r["cliente"],
                        r["cancha"],
                        r["fecha"],
                        r["hora_inicio"],
                        r["duracion_horas"],
                        r["estado"],
                    ),
                )
        except Exception as e:
            mostrar_mensaje_personalizado(
                self.controller,
                "Error",
                f"Ocurrió un error al cargar reservas: {e}",
                tipo="error"
            )

    def _on_select_torneo(self, event):
        item_seleccionado = self.tabla.focus()
        if not item_seleccionado:
            return
        item = self.tabla.item(item_seleccionado)
        valores = item.get("values", ())
        if not valores:
            return

        self.id_var.set(valores[0])
        self.nombre_var.set(valores[1])
        self.fi_var.set(valores[2])
        self.ff_var.set(valores[3])

        # cargar reservas asociadas al torneo
        self.cargar_reservas_de_torneo(int(valores[0]))

    def agregar_torneo(self):
        try:
            self.servicio.crear_torneo(
                self.nombre_var.get(),
                self.fi_var.get(),
                self.ff_var.get()
            )
            mostrar_mensaje_personalizado(
                self.controller,
                "Éxito",
                "Torneo creado correctamente",
                tipo="info"
            )
            self.cargar_torneos()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(
                self.controller,
                "Error",
                f"Ocurrió un error: {e}",
                tipo="error"
            )

    def actualizar_torneo(self):
        try:
            if not self.id_var.get():
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Advertencia",
                    "Seleccione un torneo de la lista",
                    tipo="warning"
                )
                return
            self.servicio.actualizar_torneo(
                int(self.id_var.get()),
                self.nombre_var.get(),
                self.fi_var.get(),
                self.ff_var.get()
            )
            mostrar_mensaje_personalizado(
                self.controller,
                "Éxito",
                "Torneo actualizado",
                tipo="info"
            )
            self.cargar_torneos()
            self.limpiar_formulario()
        except Exception as e:
            mostrar_mensaje_personalizado(
                self.controller,
                "Error",
                f"Ocurrió un error: {e}",
                tipo="error"
            )

    def eliminar_torneo(self):
        if not self.id_var.get():
            mostrar_mensaje_personalizado(
                self.controller,
                "Advertencia",
                "Seleccione un torneo de la lista",
                tipo="warning"
            )
            return

        respuesta = mostrar_mensaje_personalizado(
            self.controller,
            "Confirmar",
            "¿Está seguro de que desea eliminar este torneo?",
            tipo="question"
        )
        if respuesta:
            try:
                self.servicio.eliminar_torneo(int(self.id_var.get()))
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Éxito",
                    "Torneo eliminado",
                    tipo="info"
                )
                self.cargar_torneos()
                self.limpiar_formulario()
            except Exception as e:
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Error",
                    f"Ocurrió un error: {e}",
                    tipo="error"
                )

    def limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.fi_var.set("")
        self.ff_var.set("")
        self.id_reserva_var.set("")
        try:
            self.tabla.selection_remove(self.tabla.selection())
        except Exception:
            pass
        for item in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(item)

    # ---------- Gestión de reservas en torneo ----------
    def abrir_selector_reservas(self):
        if not self.id_var.get():
            mostrar_mensaje_personalizado(
                self.controller,
                "Atención",
                "Primero seleccione un torneo",
                tipo="info"
            )
            return

        id_torneo = int(self.id_var.get())
        SelectorReservaTorneo(
            self,
            self.servicio,
            id_torneo,
            callback=self._reserva_seleccionada_desde_popup
        )

    def _reserva_seleccionada_desde_popup(self, id_reserva: int):
        try:
            id_torneo = int(self.id_var.get())
            self.servicio.agregar_reserva_a_torneo(id_torneo, id_reserva)
            mostrar_mensaje_personalizado(
                self.controller,
                "Éxito",
                f"Reserva {id_reserva} agregada al torneo {id_torneo}",
                tipo="info"
            )
            self.cargar_reservas_de_torneo(id_torneo)
        except Exception as e:
            mostrar_mensaje_personalizado(
                self.controller,
                "Error",
                f"Ocurrió un error: {e}",
                tipo="error"
            )

    def agregar_reserva_a_torneo(self):
        try:
            if not self.id_var.get():
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Atención",
                    "Primero seleccione un torneo",
                    tipo="info"
                )
                return
            if not self.id_reserva_var.get():
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Atención",
                    "Ingrese un ID de reserva o use 'Buscar reserva...'",
                    tipo="info"
                )
                return

            id_torneo = int(self.id_var.get())
            id_reserva = int(self.id_reserva_var.get())

            self.servicio.agregar_reserva_a_torneo(id_torneo, id_reserva)
            mostrar_mensaje_personalizado(
                self.controller,
                "Éxito",
                f"Reserva {id_reserva} agregada al torneo {id_torneo}",
                tipo="info"
            )
            self.id_reserva_var.set("")
            self.cargar_reservas_de_torneo(id_torneo)
        except Exception as e:
            mostrar_mensaje_personalizado(
                self.controller,
                "Error",
                f"Ocurrió un error: {e}",
                tipo="error"
            )

    def quitar_reserva_de_torneo(self):
        try:
            if not self.id_var.get():
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Atención",
                    "Primero seleccione un torneo",
                    tipo="info"
                )
                return

            seleccion = self.tabla_reservas.selection()
            if not seleccion:
                mostrar_mensaje_personalizado(
                    self.controller,
                    "Atención",
                    "Seleccione una reserva de la tabla",
                    tipo="info"
                )
                return

            valores = self.tabla_reservas.item(seleccion[0], "values")
            id_torneo = int(self.id_var.get())
            id_reserva = int(valores[0])

            self.servicio.quitar_reserva_de_torneo(id_torneo, id_reserva)
            mostrar_mensaje_personalizado(
                self.controller,
                "Éxito",
                f"Reserva {id_reserva} quitada del torneo {id_torneo}",
                tipo="info"
            )
            self.cargar_reservas_de_torneo(id_torneo)
        except Exception as e:
            mostrar_mensaje_personalizado(
                self.controller,
                "Error",
                f"Ocurrió un error: {e}",
                tipo="error"
            )

    # ================== Selección de fechas con calendario ==================
    def abrir_calendario_inicio(self):
        self._abrir_calendario(self.fi_var, "Seleccionar fecha de inicio")

    def abrir_calendario_fin(self):
        self._abrir_calendario(self.ff_var, "Seleccionar fecha de fin")

    def _abrir_calendario(self, target_var: ctk.StringVar, titulo: str):
        """
        Abre un pop-up con calendario y escribe la fecha seleccionada
        en el StringVar pasado (fi_var o ff_var).
        """
        top = ctk.CTkToplevel(self)
        top.title(titulo)
        top.geometry("320x320")
        top.grab_set()  # lo hace modal

        hoy = datetime.date.today()

        cal = Calendar(
            top,
            selectmode="day",
            year=hoy.year,
            month=hoy.month,
            day=hoy.day,
            date_pattern="yyyy-mm-dd"  # para que coincida con el formato del campo
        )
        cal.pack(padx=10, pady=10, fill="both", expand=True)

        frame_botones = ctk.CTkFrame(top)
        frame_botones.pack(fill="x", padx=10, pady=(0, 10))
        frame_botones.grid_columnconfigure((0, 1), weight=1)

        def confirmar():
            target_var.set(cal.get_date())
            top.destroy()

        def cancelar():
            top.destroy()

        ctk.CTkButton(
            frame_botones,
            text="Aceptar",
            command=confirmar
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=cancelar
        ).grid(row=0, column=1, padx=5)
