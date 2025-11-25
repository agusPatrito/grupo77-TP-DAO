import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from services.reporting_service import ReportingService
from gui.estilos import FUENTE_BASE, FUENTE_TITULO_VISTA
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class VistaReportes(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.servicio_reportes = ReportingService()

        # GRID BASE
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- BARRA SUPERIOR ---
        frame_superior = ctk.CTkFrame(self)
        frame_superior.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        frame_superior.grid_columnconfigure(1, weight=1)

        # botón volver
        try:
            img_volver_pil = Image.open("gui/assets/volver.png")
            img_volver = ctk.CTkImage(img_volver_pil)
        except:
            img_volver = None

        btn_volver = ctk.CTkButton(
            frame_superior, text="", image=img_volver,
            command=lambda: controller.mostrar_vista("menu_principal"),
            width=40, height=40
        )
        btn_volver.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        titulo = ctk.CTkLabel(frame_superior, text="Reportes y Estadísticas", font=FUENTE_TITULO_VISTA)
        titulo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkButton(
            frame_superior, text="Refrescar Reportes",
            command=self.cargar_reportes, font=FUENTE_BASE
        ).grid(row=0, column=2, padx=10, pady=10)

        # --- TABVIEW ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_canchas = self.tabview.add("Uso de Canchas")
        self.tab_horarios = self.tabview.add("Reservas por Horario")

        # ================================
        #   TAB 1 — USO DE CANCHAS
        # ================================
        self._construir_tab_canchas()

        # ================================
        #   TAB 2 — HORARIOS USADOS
        # ================================
        self._construir_tab_horarios()

        # CARGA INICIAL
        self.cargar_reportes()

    # ------------------------------------------------------------------
    #   TAB 1 — CANCHAS MÁS USADAS + INGRESOS
    # ------------------------------------------------------------------
    def _construir_tab_canchas(self):

        frame = self.tab_canchas
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # TÍTULO TABLA
        lbl = ctk.CTkLabel(frame, text="Ranking de Canchas (Uso + Ingresos)", font=FUENTE_BASE)
        lbl.grid(row=0, column=0, pady=10)

        # TABLA
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e",
                        borderwidth=0,
                        font=FUENTE_BASE)
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        font=FUENTE_BASE)

        self.tabla_canchas = ttk.Treeview(
            frame,
            columns=("Cancha", "Reservas", "Ingresos"),
            show="headings"
        )
        self.tabla_canchas.heading("Cancha", text="Cancha")
        self.tabla_canchas.heading("Reservas", text="Total Reservas")
        self.tabla_canchas.heading("Ingresos", text="Ingresos Totales ($)")

        self.tabla_canchas.column("Cancha", width=200)
        self.tabla_canchas.column("Reservas", width=120, anchor="center")
        self.tabla_canchas.column("Ingresos", width=150, anchor="center")

        self.tabla_canchas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # GRÁFICO TORTA
        self.frame_grafico_canchas = ctk.CTkFrame(frame)
        self.frame_grafico_canchas.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # ------------------------------------------------------------------
    #   TAB 2 — RESERVAS POR HORARIO
    # ------------------------------------------------------------------
    def _construir_tab_horarios(self):

        frame = self.tab_horarios
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        lbl = ctk.CTkLabel(frame, text="Reservas por Franja Horaria", font=FUENTE_BASE)
        lbl.grid(row=0, column=0, pady=10)

        self.tabla_horarios = ttk.Treeview(
            frame,
            columns=("Hora", "Total"),
            show="headings"
        )
        self.tabla_horarios.heading("Hora", text="Hora")
        self.tabla_horarios.heading("Total", text="Total Reservas")
        self.tabla_horarios.column("Hora", width=120, anchor="center")
        self.tabla_horarios.column("Total", width=120, anchor="center")
        self.tabla_horarios.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.frame_grafico_horas = ctk.CTkFrame(frame)
        self.frame_grafico_horas.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # ------------------------------------------------------------------
    #   CARGAR REPORTES EN AMBAS PESTAÑAS
    # ------------------------------------------------------------------
    def cargar_reportes(self):

        # ================= TAB 1 =================
        for i in self.tabla_canchas.get_children():
            self.tabla_canchas.delete(i)

        data = self.servicio_reportes.get_canchas_mas_utilizadas_con_ingresos()

        # tabla
        for row in data:
            self.tabla_canchas.insert("", "end",
                                      values=(row["nombre"], row["total_reservas"], row["ingresos"]))

        # gráfico torta
        for w in self.frame_grafico_canchas.winfo_children():
            w.destroy()

        if data:
            nombres = [r["nombre"] for r in data]
            totales = [r["total_reservas"] for r in data]

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(totales, labels=nombres, autopct="%1.1f%%")
            ax.set_title("Distribución de Uso")

            canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico_canchas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        # ================= TAB 2 =================
        for i in self.tabla_horarios.get_children():
            self.tabla_horarios.delete(i)

        horas, totales_horas = self.servicio_reportes.get_reservas_por_hora()

        for h, t in zip(horas, totales_horas):
            self.tabla_horarios.insert("", "end", values=(h, t))

        for w in self.frame_grafico_horas.winfo_children():
            w.destroy()

        if horas:
            fig2 = Figure(figsize=(5, 4), dpi=100)
            ax2 = fig2.add_subplot(111)
            ax2.bar(horas, totales_horas)
            ax2.set_title("Reservas por Horario")
            ax2.set_xlabel("Hora")
            ax2.set_ylabel("Cantidad de Reservas")
            fig2.tight_layout()

            canvas2 = FigureCanvasTkAgg(fig2, master=self.frame_grafico_horas)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True)
