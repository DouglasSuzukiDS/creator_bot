import os
import shutil, smtplib
import zipfile
import mimetypes
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from email.message import EmailMessage
from utils.html_body import html_body
from utils.send_email import send_email
from utils.format_mb import format_mb
from utils.get_path import get_path
from utils.email_config import email_config

load_dotenv()

date_format = '%Y_%m_%d_%H%M%S'
allowed_extenssions = ['.png', '.jpg', '.mp3', '.txt', '.pdf']

''' 1. Varredura e Validação (pathlib e stat)
   Varrer a pasta producao/ filtrando extensões válidas de mídia (como .png, .jpg, .mp3, .txt, .pdf).
   Descartar arquivos com 0 bytes (gravações corrompidas ou incompletas).
   Exibir no console o resumo dos arquivos encontrados e o tamanho total do pacote em Megabytes (MB).
'''
def files_validation() -> list[Path] | None:
   folder = Path('producao')

   if not folder.is_dir():
      print('Diretorio nao existe ❌')
      return None

   files = [
      file 
      for file in folder.iterdir() 
      if file.is_file() 
      and file.stat().st_size > 0
      and file.suffix.lower() in allowed_extenssions
   ]

   if not files:
      print('Pasta existe, mas esta vazia ∅')
      return None

   print(f'Arquivo(s) encontrado(s) 🔍: {len(files)} totalizando {format_mb(files):.2f}mb')
   
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
   date_now = datetime.now().strftime(date_format)
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

   # Cria o zip
   with zipfile.ZipFile (zip_file_name, 'w', compression = zipfile.ZIP_DEFLATED) as zip:
      for file in files:
         zip.write(file, arcname = file.name)

   print(move_production_files()) # Move a pasta com os arquivos para pasta entregues

   return 'Automacao finalizada sem nenhum problema ✅'

''' 3. Arquivamento e Limpeza (shutil e pathlib)
      Após a criação bem-sucedida do .zip, mover os arquivos originais de producao/ para entregues/, deixando a pasta de produção pronta para o próximo dia de gravação.
'''
def move_production_files() -> str | None:
   production_folder = Path('producao')
   destiny_folder = Path('entregues')
   destiny_folder.mkdir(exist_ok=True)

   if not production_folder.exists():
      print('Diretorio nao existe ❌')
      return None

   date_complete = datetime.now().strftime(date_format)
  
   current_folder = destiny_folder / date_complete
   moved_files = 0

   # Move os arquivos de producao para a pasta com a data atual
   for file in production_folder.iterdir():
      current_folder.mkdir(parents=True, exist_ok=True)

      destiny = current_folder / file.name

      if file.is_file() and file.stat().st_size > 0 and file.suffix.lower() in allowed_extenssions: 
         moved_files += 1 
      
      shutil.move(str(file), str(destiny)) 

   message = 'Pasta vazia ∅, nenhum arquivo foi movido' if moved_files == 0 else f'Pasta {date_complete} gerada com {moved_files} e movida para a pasta {destiny_folder.name}. ✅'

   print(message)

   return send_email(date_complete, moved_files)

''' 4. Disparo do E-mail VIP (smtplib e EmailMessage)e)
   Assunto: 🚀 Drop VIP Liberado! Conteúdos Exclusivos de [DD/MM/AAAA]
   Título com destaque visual (Drop de Conteúdo Liberado).
   Badge/card informando a data e a quantidade de arquivos inclusos.
   Mensagem descontraída agradecendo o apoio da comunidade.
   Anexo: Detectar o tipo MIME dinamicamente e anexar o arquivo .zip gerado.
'''
def send_email(date: str, moved_files: int) -> str | None:
   date_br_format = datetime.strptime(date, date_format).strftime('%d/%m/%Y')
   body_content = html_body(date_br_format, moved_files)
   email_conf = email_config()

   SMTP_SERVER = email_conf.SMTP_SERVER
   SMTP_PORT = int(email_conf.SMTP_PORT)
   EMAIL_USER = email_conf.EMAIL_USER
   EMAIL_PASSWORD = email_conf.EMAIL_PASSWORD

   message = EmailMessage()
   message['Subject'] = f'🚀 Drop VIP Liberado! Conteúdos Exclusivos de {date_br_format}'
   message['From'] = EMAIL_USER
   message['To'] = email_conf.EMAIL_RECIPIENT
   message.set_content(
      f"Drop VIP Liberado em {date_br_format} ({moved_files} arquivos inclusos).\n"
      "O pacote .zip segue em anexo."
   )

   message.add_alternative(body_content, subtype='html')

   zip_file = Path('pacotes_zip', f'drop_vip_{date}.zip')

   binary_content = zip_file.read_bytes()
   mimetype, _ = mimetypes.guess_type(zip_file) # application/zip
   type = mimetype or 'application/octet-stream' # application/zip | application/octet-stream
   maintype, subtype = type.split('/', 1) # application, zip (or octet-stream)

   message.add_attachment(
      binary_content,
      maintype,
      subtype,
      filename = zip_file.name
   )

   with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
      server.login(EMAIL_USER, EMAIL_PASSWORD)
      server.send_message(message)

      return 'Email enviado 📨'

   return None

print(create_zip_file())