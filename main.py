import os, sys
import shutil, smtplib
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from utils.html_body import html_body
from utils.send_email import send_email
from utils.format_mb import format_mb

load_dotenv()
date_now = date.today()


''' 1. Varredura e Validação (pathlib e stat)
   Varrer a pasta producao/ filtrando extensões válidas de mídia (como .png, .jpg, .mp3, .txt, .pdf).
   Descartar arquivos com 0 bytes (gravações corrompidas ou incompletas).
   Exibir no console o resumo dos arquivos encontrados e o tamanho total do pacote em Megabytes (MB).
'''
def archives_validation() -> list[Path] | None:
   folder = Path('producao')
   allowed_extenssions = ['.png', '.jpg', '.mp3', '.txt', '.pdf']

   if not folder.is_dir():
      print('Diretorio nao existe')
      return None

   archives = [
      arc 
      for arc in folder.iterdir() 
      if arc.is_file() 
      and arc.stat().st_size > 0
      and arc.suffix.lower() in allowed_extenssions
   ]

   if not archives:
      print('Pasta existe, mas esta vazia')
      return None

   print(f'Arquivo(s) encontrado(s): {len(archives)} totalizando {format_mb(archives):.2f}mb')
   
   for index, arc in enumerate(archives, start=1):
      print(f'{index:02d} => Nome: {arc.name} - Tamanho: {format_mb([arc]):.2f}mb')

   return archives

archives_validation()