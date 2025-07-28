import customtkinter as ctk
from selecao_janelas import TelaSelecaoJanela

class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(self, text="Bot_Farm", font=("Arial", 28, "bold"), text_color="black")
        titulo.pack(pady=40)

        botao_iniciar = ctk.CTkButton(
            self,
            text="Iniciar Farm",
            fg_color="#0F52BA",
            hover_color="#1E90FF",
            text_color="white",
            font=("Arial", 18),
            command=self.ir_para_selecao
        )
        botao_iniciar.pack(pady=20)

    def ir_para_selecao(self):
        self.master.mostrar_tela(TelaSelecaoJanela)

    