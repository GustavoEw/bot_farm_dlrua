import customtkinter as ctk
import win32gui

class TelaSelecaoJanela(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(self, text="Selecione a janela do jogo", font=("Arial", 20))
        titulo.pack(pady=20)

        self.janelas = self.listar_janelas()
        self.criar_combobox()

    def listar_janelas(self):
        janelas = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                titulo = win32gui.GetWindowText(hwnd)
                if titulo:
                    janelas.append((hwnd, titulo))

        win32gui.EnumWindows(callback, None)
        return janelas

    def criar_combobox(self):
    # Extrai só os títulos para colocar no ComboBox
        titulos = [titulo for hwnd, titulo in self.janelas]
        
        # Cria o ComboBox com os títulos
        self.combo = ctk.CTkComboBox(self, values=titulos)
        self.combo.pack(pady=10)
        
        # Botão para confirmar seleção
        botao_selecionar = ctk.CTkButton(self, text="Selecionar Janela", command=self.confirmar_selecao)
        botao_selecionar.pack(pady=10)
    def confirmar_selecao(self):
        selecionado = self.combo.get()  # Título selecionado no ComboBox
        
        # Procura o hwnd correspondente ao título selecionado
        hwnd_selecionado = None
        for hwnd, titulo in self.janelas:
            if titulo == selecionado:
                hwnd_selecionado = hwnd
                break

        if hwnd_selecionado is not None:
            self.selecionar_janela(hwnd_selecionado, selecionado)
        else:
            print("Nenhuma janela selecionada ou inválida.")
        
    def selecionar_janela(self, hwnd, titulo):
        print(f"Janela selecionada: {titulo} (HWND: {hwnd})")

if __name__ == "__main__":
    import customtkinter as ctk

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("600x400")
    root.configure(fg_color="#FFD700")

    frame = TelaSelecaoJanela(root)  # ou TelaSelecaoJanela(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()