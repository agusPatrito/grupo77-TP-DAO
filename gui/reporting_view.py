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

        # configuramos el grid principal de esta vista
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # frame superior con titulo y boton de volver
        frame_superior = ctk.CTkFrame(self)
        frame_superior.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        frame_superior.grid_columnconfigure(1, weight=1)

        try:
            img_volver_pil = Image.open("gui/assets/volver.png")
            img_volver = ctk.CTkImage(img_volver_pil)
        except Exception as e:
            img_volver = None

        btn_volver = ctk.CTkButton(frame_superior, text="", image=img_volver,
                                   command=lambda: controller.mostrar_vista("menu_principal"),
                                   width=40, height=40)
        btn_volver.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        titulo = ctk.CTkLabel(frame_superior, text="Reportes y Estadísticas", font=FUENTE_TITULO_VISTA)
        titulo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Botón para refrescar los reportes
        btn_refrescar = ctk.CTkButton(frame_superior, text="Refrescar Reportes", command=self.cargar_reportes, font=FUENTE_BASE)
        btn_refrescar.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # frame principal para el contenido
        frame_principal = ctk.CTkFrame(self)
        frame_principal.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        frame_principal.grid_columnconfigure(0, weight=1)
        frame_principal.grid_columnconfigure(1, weight=1)
        frame_principal.grid_rowconfigure(0, weight=1)

        # frame para el ranking de canchas (izquierda)
        frame_ranking = ctk.CTkFrame(frame_principal)
        frame_ranking.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_ranking.grid_rowconfigure(1, weight=1)
        frame_ranking.grid_columnconfigure(0, weight=1)

        lbl_ranking = ctk.CTkLabel(frame_ranking, text="Canchas Más Utilizadas", font=FUENTE_BASE)
        lbl_ranking.grid(row=0, column=0, padx=10, pady=10)

        # treeview para el ranking
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", borderwidth=0, font=FUENTE_BASE)
        style.map('Treeview', background=[('selected', '#2cb67d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=FUENTE_BASE)
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.arbol_ranking = ttk.Treeview(frame_ranking, columns=("Cancha", "Total Reservas"), show="headings")
        self.arbol_ranking.heading("Cancha", text="Cancha")
        self.arbol_ranking.heading("Total Reservas", text="Total Reservas")
        self.arbol_ranking.grid(row=1, column=0, sticky="nsew")
        
        # frame para el grafico (derecha)
        self.frame_grafico = ctk.CTkFrame(frame_principal)
        self.frame_grafico.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.cargar_reportes()

    def cargar_reportes(self):
        # cargar datos del ranking
        for i in self.arbol_ranking.get_children():
            self.arbol_ranking.delete(i)
        
        nombres, totales = self.servicio_reportes.get_canchas_mas_utilizadas()
        
        # Ordenar datos para el ranking
        ranking_data = sorted(zip(nombres, totales), key=lambda item: item[1], reverse=True)
        
        for nombre, total in ranking_data:
            self.arbol_ranking.insert("", "end", values=(nombre, total))

        # cargar datos y generar grafico de torta
        # limpiar el frame del grafico antes de dibujar uno nuevo
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        if nombres and totales:
            fig = Figure(figsize=(5, 4), dpi=100, facecolor="#2a2d2e")
            ax = fig.add_subplot(111)
            
            # Colores para el gráfico de torta
            colors = plt.cm.viridis_r([i/float(len(nombres)) for i in range(len(nombres))])
            
            ax.pie(totales, labels=nombres, autopct='%1.1f%%', startangle=90, colors=colors,
                   textprops={'color':"w"})
            
            ax.set_title("Distribución de Uso de Canchas", color="white")
            
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        else:
            lbl_no_data = ctk.CTkLabel(self.frame_grafico, text="No hay datos suficientes para generar el gráfico.", font=FUENTE_BASE)
            lbl_no_data.pack(expand=True)
