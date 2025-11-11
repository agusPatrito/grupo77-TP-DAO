import customtkinter as ctk
from gui.estilos import FUENTE_BASE # importamos la fuente base

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, titulo, mensaje, tipo="info"):
        super().__init__(parent)
        self.grab_set() # hace que la ventana sea modal
        self.title(titulo)
        self.transient(parent) # hace que la ventana sea transitoria respecto a su padre

        self.result = None # para guardar el resultado en caso de preguntas

        # centramos la ventana respecto a su padre
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"400x200+{x}+{y}")
        self.resizable(False, False)

        # configuramos el grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0) # para los botones

        # frame principal para el contenido del mensaje
        frame_contenido = ctk.CTkFrame(self)
        frame_contenido.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_contenido.grid_columnconfigure(0, weight=1)
        frame_contenido.grid_rowconfigure(0, weight=1)

        # mensaje
        lbl_mensaje = ctk.CTkLabel(frame_contenido, text=mensaje, font=FUENTE_BASE, wraplength=350)
        lbl_mensaje.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # frame para los botones
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frame_botones.grid_columnconfigure((0, 1), weight=1)

        if tipo == "info":
            btn_ok = ctk.CTkButton(frame_botones, text="Aceptar", command=self.destroy, font=FUENTE_BASE)
            btn_ok.grid(row=0, column=0, columnspan=2, pady=5)
        elif tipo == "warning":
            btn_ok = ctk.CTkButton(frame_botones, text="Aceptar", command=self.destroy, font=FUENTE_BASE, fg_color="orange")
            btn_ok.grid(row=0, column=0, columnspan=2, pady=5)
        elif tipo == "error":
            btn_ok = ctk.CTkButton(frame_botones, text="Aceptar", command=self.destroy, font=FUENTE_BASE, fg_color="red")
            btn_ok.grid(row=0, column=0, columnspan=2, pady=5)
        elif tipo == "question":
            btn_si = ctk.CTkButton(frame_botones, text="Si", command=lambda: self._set_result(True), font=FUENTE_BASE)
            btn_si.grid(row=0, column=0, padx=5, pady=5)
            btn_no = ctk.CTkButton(frame_botones, text="No", command=lambda: self._set_result(False), font=FUENTE_BASE)
            btn_no.grid(row=0, column=1, padx=5, pady=5)
        
    def _set_result(self, value):
        self.result = value
        self.destroy()

def mostrar_mensaje_personalizado(app_root, titulo, mensaje, tipo="info"):
    # muestra un mensaje personalizado con estilo CTk
    # tipo: "info", "warning", "error", "question"
    # retorna True/False para tipo "question", None para otros tipos
    msg_box = CustomMessageBox(app_root, titulo, mensaje, tipo)
    msg_box.wait_window()
    return msg_box.result
