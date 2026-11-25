import os, sys
import shutil, smtplib
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from utils.html_body import html_body
from utils.send_email import send_email

load_dotenv()
date_now = date.today()

def archives_validation():
   folder = Path('producao')
   allowed_extenssions = ['.png', '.jpg', '.mp3', '.txt', '.pdf']

   if not folder.is_dir():
      print('Diretorio nao existe')
      return

   archives = [
      arc 
      for arc in folder.iterdir() 
      if arc.is_file() and arc.suffix.lower() in allowed_extenssions
   ]

   if not archives:
      print('Pasta existe, mas esta vazia')
      return

   print(f'Arquivo(s) encontrado(s): {len(archives)}')
   
   for index, arc in enumerate(archives, start=1):
      print(f'{index:02d}: {arc.name}')

archives_validation()

# 1. Varredura e Validação (pathlib e stat)
#    Varrer a pasta producao/ filtrando extensões válidas de mídia (como .png, .jpg, .mp3, .txt, .pdf).
#    Descartar arquivos com 0 bytes (gravações corrompidas ou incompletas).
#    Exibir no console o resumo dos arquivos encontrados e o tamanho total do pacote em Megabytes (MB).