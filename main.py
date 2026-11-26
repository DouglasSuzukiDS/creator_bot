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
def files_validation() -> list[Path] | None:
   folder = Path('producao')
   allowed_extenssions = ['.png', '.jpg', '.mp3', '.txt', '.pdf']

   if not folder.is_dir():
      print('Diretorio nao existe')
      return None

   files = [
      file 
      for file in folder.iterdir() 
      if file.is_file() 
      and file.stat().st_size > 0
      and file.suffix.lower() in allowed_extenssions
   ]

   if not files:
      print('Pasta existe, mas esta vazia')
      return None

   print(f'Arquivo(s) encontrado(s): {len(files)} totalizando {format_mb(files):.2f}mb')
   
   for index, file in enumerate(files, start=1):
      print(f'{index:02d} => Nome: {file.name} - Tamanho: {format_mb([file]):.2f}mb')

   return files

''' 2. Geração do Pacote do Episódio (datetime e shutil)
   - Capturar a data atual.
   - Gerar um arquivo .zip na pasta pacotes_zip/ com a convenção:
      drop_vip_YYYY_MM_DD.zip (ex: drop_vip_2026_09_14.zip).
   - Adicionar apenas os arquivos válidos dentro do arquivo comprimido mantendo nomes limpos (sem a pasta local no caminho).
'''
def create_zip_file() -> str | None:
   date_now = datetime.now().strftime('%Y_%m_%d_%H%M%S')
   files = files_validation()

   if not files:
      return None

   zip_folder_path = get_path('pacotes_zip')
   zip_folder_path.mkdir(parents=True, exist_ok=True) # Cria a pasta se ela nao existir
   file_name = f'drop_vip_{date_now}.zip'
   zip_file_name = str(zip_folder_path / file_name)

   # shutil.make_filehive(
   #    base_name = str(zip_folder_path / file_name),
   #    format = 'zip',
   #    root_dir = production_path
   # )

   with zipfile.ZipFile (zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
      for file in files:
         zip.write(file, filename = file.name)

   return zip_file_name

''' 3. Arquivamento e Limpeza (shutil e pathlib)
      Após a criação bem-sucedida do .zip, mover os arquivos originais de producao/ para entregues/, deixando a pasta de produção pronta para o próximo dia de gravação.
'''
def move_production_files() -> str | None:
   production_folder = Path('producao')
   destiny_folder = Path('entregues')
   destiny_folder.mkdir(exist_ok=True)

   if not production_folder.exists():
      print('Diretorio nao existe')
      return None

   date_now = datetime.now().strftime('%Y_%m_%d_%H%M%S')

   current_folder = Path(date_now) # Pasta que vai receber os arquivos de producao
   current_folder.mkdir(parents=True, exist_ok=True)

   moved_files = 0

   # Move os arquivos de producao para a pasta com a data atual
   for file in production_folder.iterdir():
      origin = production_folder / file.name
      destiny = current_folder / file.name
      
      shutil.move(origin, destiny) 
      moved_files += 1

   # Move a pasta com a data atual para a pasta entregues
   shutil.move(current_folder, destiny_folder)

   message = 'Pasta vazia nenhum, arquivo foi movido' if moved_files == 0 else f'{moved_files} movido(s) para a pasta {destiny_folder.name}.'

   return message

# create_zip_file()
print(move_production_files())