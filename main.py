import customtkinter as ctk
from telas.selecao_janelas import TelaSelecaoJanela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x500")
app.title("Bot Duel Links")

frame = TelaSelecaoJanela(app)
frame.pack(fill="both", expand=True)

app.mainloop()
