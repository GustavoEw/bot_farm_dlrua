import customtkinter as ctk
import threading
import time
import win32gui
import mss
import keyboard  # Importa o keyboard para detectar tecla Q
from bot.bot import rodar_bot_na_janela

class TelaSelecaoJanela(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.janelas = self.listar_janelas()
        self.monitores = self.listar_monitores()

        self.hwnd_selecionado = None
        self.monitor_selecionado = None
        self.selecionado = None
        self.bot_ativo = threading.Event()

        # Interface
        ctk.CTkLabel(self, text="Selecione a janela ou o monitor", font=("Arial", 20)).pack(pady=20)

        ctk.CTkLabel(self, text="Janelas Visíveis:").pack()
        titulos = [titulo for hwnd, titulo in self.janelas]
        self.combo_janela = ctk.CTkComboBox(self, values=titulos)
        self.combo_janela.pack(pady=5)
        ctk.CTkButton(self, text="Selecionar Janela", command=self.confirmar_selecao_janela).pack(pady=10)

        ctk.CTkLabel(self, text="Monitores Disponíveis:").pack(pady=(20, 0))
        nomes_monitores = [f"Monitor {i+1}" for i in range(len(self.monitores))]
        self.combo_monitor = ctk.CTkComboBox(self, values=nomes_monitores)
        self.combo_monitor.pack(pady=5)
        ctk.CTkButton(self, text="Selecionar Monitor", command=self.confirmar_selecao_monitor).pack(pady=10)

        self.btn_iniciar = ctk.CTkButton(self, text="Iniciar Bot", command=self.iniciar_bot)
        self.btn_iniciar.pack(pady=10)

        self.btn_parar = ctk.CTkButton(self, text="Parar Bot", command=self.parar_bot)
        self.btn_parar.pack(pady=10)

        # Inicia thread que escuta a tecla Q para parar o bot
        threading.Thread(target=self.verificar_tecla_q, daemon=True).start()

    def listar_janelas(self):
        janelas = []
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                titulo = win32gui.GetWindowText(hwnd)
                if titulo:
                    janelas.append((hwnd, titulo))
        win32gui.EnumWindows(callback, None)
        return janelas

    def listar_monitores(self):
        with mss.mss() as sct:
            return sct.monitors

    def confirmar_selecao_janela(self):
        self.selecionado = self.combo_janela.get()
        for hwnd, titulo in self.janelas:
            if titulo == self.selecionado:
                self.hwnd_selecionado = hwnd
                self.monitor_selecionado = None
                print(f"🪟 Janela selecionada: {titulo} (HWND: {hwnd})")
                return

    def confirmar_selecao_monitor(self):
        index = self.combo_monitor.cget("values").index(self.combo_monitor.get())
        self.monitor_selecionado = self.monitores[index]
        self.hwnd_selecionado = None
        print(f"🖥️ Monitor selecionado: Monitor {index}")

    def get_bbox(self):
        if self.monitor_selecionado:
            return {
                "left": self.monitor_selecionado["left"],
                "top": self.monitor_selecionado["top"],
                "width": self.monitor_selecionado["width"],
                "height": self.monitor_selecionado["height"]
            }
        elif self.hwnd_selecionado:
            rect = win32gui.GetWindowRect(self.hwnd_selecionado)
            return {
                "left": rect[0],
                "top": rect[1],
                "width": rect[2] - rect[0],
                "height": rect[3] - rect[1]
            }
        return None

    def iniciar_bot(self):
        if not self.bot_ativo.is_set():
            bbox = self.get_bbox()
            if bbox:
                self.bot_ativo.set()
                thread = threading.Thread(target=self.loop_bot, args=(bbox,), daemon=True)
                thread.start()
                print("🤖 Bot iniciado.")
            else:
                print("Nenhuma área selecionada.")
        else:
            print("Bot já está rodando.")

    def parar_bot(self):
        if self.bot_ativo.is_set():
            self.bot_ativo.clear()
            print("⛔ Bot parado.")

    def loop_bot(self, bbox):
        print("🔁 Loop rodando (pressione Q para parar)")
        while self.bot_ativo.is_set():
            rodar_bot_na_janela(bbox)
            time.sleep(1)
        print("🔚 Loop finalizado.")

    def verificar_tecla_q(self):
        # Thread que fica escutando a tecla Q para parar o bot
        while True:
            if keyboard.is_pressed("q"):
                if self.bot_ativo.is_set():
                    print("⛔ Tecla Q pressionada. Parando o bot...")
                    self.parar_bot()
                    break
            time.sleep(0.1)
