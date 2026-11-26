import subprocess

def create_exe():
   return subprocess.run(['pyinstaller', '--onefile', 'main.py']) # Para empacotar