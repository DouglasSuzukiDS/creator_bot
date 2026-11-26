import sys
from pathlib import Path

def get_path(file_name: str) -> Path:
   """
      Retorna o caminho correto de um arquivo ou imagem embutido,
      funcionando tanto ao rodar o script quanto dentro do .exe.
   """
   if hasattr(sys, "_MEIPASS"):
      # Rodando como executável empacotado: busca na pasta temporária
      base = Path(sys._MEIPASS)
   else:
      # Rodando como script normal no VS Code: busca na pasta do projeto
      # base = Path(__file__).resolve().parent
      base = Path(__file__).resolve().parent.parent

   return base / file_name