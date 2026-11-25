from pathlib import Path

def format_mb(archives: list[Path]) -> float:
   total_bytes = sum(arc.stat().st_size for arc in archives)
   
   return total_bytes / (1024 * 1024)