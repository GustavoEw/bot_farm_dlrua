import os
import time
from bot.bot import rodar_bot_em_area
from bot.winutils import clicar_invisivel

# TESTE DE CLIQUE INVISÍVEL
print("Testando clique invisível em (500, 500) em 3 segundos...")
time.sleep(3)
clicar_invisivel(500, 500)

# TESTE DE DETECÇÃO DE TEMPLATE NA TELA
# Use seu monitor inteiro ou parte da tela, ajuste conforme necessário
bbox_teste = (0, 0, 1280, 720)  # ajuste conforme sua resolução

print(f"Rodando bot na região: {bbox_teste}")
rodar_bot_em_area(bbox_teste)
