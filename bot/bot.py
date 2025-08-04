import cv2
import numpy as np
import os
import mss
import time
import ctypes
import win32gui
import pyautogui
import keyboard

# Estrutura para o clique invisível (com ctypes)
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class _INPUT(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(ctypes.Structure):
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("_input", _INPUT)
    ]

# ⬇ Clique invisível sem mover cursor
def click_in_window(hwnd, rel_x, rel_y):
    # Pega a posição absoluta da janela
    win_left, win_top, _, _ = win32gui.GetWindowRect(hwnd)
    abs_x = win_left + rel_x
    abs_y = win_top + rel_y
    pyautogui.click(abs_x,abs_y)
    pyautogui.click(abs_x,abs_y)
    # Converte para coordenadas absolutas da tela virtual
    user32 = ctypes.windll.user32
    virt_left = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
    virt_top = user32.GetSystemMetrics(77)   # SM_YVIRTUALSCREEN
    virt_width = user32.GetSystemMetrics(78) # SM_CXVIRTUALSCREEN
    virt_height = user32.GetSystemMetrics(79)# SM_CYVIRTUALSCREEN

    # Transforma (x, y) em valores normalizados de 0 a 65535
    scaled_x = int((abs_x - virt_left) * 65535 / virt_width)
    scaled_y = int((abs_y - virt_top) * 65535 / virt_height)

    # Cria evento de mouse com ctypes
    def send(flags):
        extra = ctypes.c_ulong(0)
        mi = MOUSEINPUT(
            dx=scaled_x, dy=scaled_y, mouseData=0,
            dwFlags=flags | 0x8000,  # MOUSEEVENTF_ABSOLUTE
            time=0,
            dwExtraInfo=ctypes.pointer(extra)
        )
        inp = INPUT(type=0, mi=mi)
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    # Envia os eventos: mover, pressionar e soltar
    send(0x0001)  # MOVE
    send(0x0002)  # LEFTDOWN
    send(0x0004)  # LEFTUP
    print(f"[✔] Clique invisível em ({abs_x}, {abs_y})")

# ⬇ Função principal do bot: procura templates e clica
def rodar_bot_na_janela(bbox):
    hwnd = win32gui.WindowFromPoint((bbox['left'] + 10, bbox['top'] + 10))
    if hwnd == 0:
        print("[ERRO] HWND não encontrado para bbox fornecido!")
        return

    caminho_templates = os.path.join(os.path.dirname(__file__), "templates")
    if not os.path.exists(caminho_templates):
        print(f"[ERRO] Pasta de templates não encontrada: {caminho_templates}")
        return

    with mss.mss() as sct:
        screenshot = np.array(sct.grab(bbox))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        imagem_debug = screenshot.copy()

        for nome_arquivo in os.listdir(caminho_templates):
            if not nome_arquivo.endswith(".png"):
                continue

            caminho = os.path.join(caminho_templates, nome_arquivo)
            template = cv2.imread(caminho, cv2.IMREAD_COLOR)

            if template is None:
                print(f"[ERRO] Falha ao carregar template: {nome_arquivo}")
                continue

            if screenshot.shape[0] < template.shape[0] or screenshot.shape[1] < template.shape[1]:
                continue

            resultado = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            localizacoes = np.where(resultado >= 0.9)

            h, w = template.shape[:2]
            for pt in zip(*localizacoes[::-1]):
                rel_x = pt[0] + w // 2
                rel_y = pt[1] + h // 2
                cv2.rectangle(imagem_debug, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                print(f"[✔] Encontrado: {nome_arquivo} em {rel_x},{rel_y}")

                click_in_window(hwnd, rel_x, rel_y)
                time.sleep(5)