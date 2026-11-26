import os, sys, subprocess
import shutil, smtplib
import zipfile
from pathlib import Path
from datetime import date, datetime
from dotenv import load_dotenv
from utils.html_body import html_body
from utils.send_email import send_email
from utils.format_mb import format_mb
from utils.get_path import get_path

load_dotenv()

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

''' 2. Geração do Pacote do Episódio (datetime e shutil)
   - Capturar a data atual.
   - Gerar um arquivo .zip na pasta pacotes_zip/ com a convenção:
      drop_vip_YYYY_MM_DD.zip (ex: drop_vip_2026_09_14.zip).
   - Adicionar apenas os arquivos válidos dentro do arquivo comprimido mantendo nomes limpos (sem a pasta local no caminho).
'''
def create_zip_file():
   date_now = datetime.now().strftime('%Y_%m_%d_%H%M%S')
   archives = archives_validation()

   if not archives:
      return None

   zip_folder_path = get_path('pacotes_zip')
   zip_folder_path.mkdir(parents=True, exist_ok=True) # Cria a pasta se ela nao existir
   archive_name = f'drop_vip_{date_now}.zip'
   zip_archive_name = str(zip_folder_path / archive_name)

   # shutil.make_archive(
   #    base_name = str(zip_folder_path / archive_name),
   #    format = 'zip',
   #    root_dir = production_path
   # )

   with zipfile.ZipFile (zip_archive_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
      for arc in archives:
         zip.write(arc, arcname = arc.name)

   return zip_archive_name

create_zip_file()