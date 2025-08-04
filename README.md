# 🖱️ Bot de Clique por Reconhecimento de Ícones

Este projeto é um bot que utiliza **visão computacional** para identificar ícones na tela e realizar **cliques automáticos**, sem mover o cursor do usuário. Ideal para automações em jogos (como *Duel Links*) ou tarefas repetitivas em ambientes gráficos do Windows.

## 🚀 Funcionalidades

- Captura a tela de uma janela ou monitor específico
- Reconhece ícones usando **template matching (OpenCV)**
- Realiza cliques invisíveis com `SendInput` (sem mover o cursor)
- Interface em `customtkinter` para seleção da janela/monitor
- Possibilidade de expandir com IA para decisões mais complexas

## 🧠 Tecnologias e Bibliotecas

- `Python 3.13+`
- `opencv-python`
- `numpy`
- `mss`
- `Pillow`
- `customtkinter`
- `pywin32` (win32gui, win32api, win32con)
- `ctypes` para clique invisível

## 📦 Instalação

1. Clone o repositório:

```bash

