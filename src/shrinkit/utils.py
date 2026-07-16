"""Funciones utilitarias compartidas entre subcomandos."""

from pathlib import Path


def human_size(num_bytes: int) -> str:
    """Convierte bytes a una representacion legible (KB, MB, GB)."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} PB"


def path_size(path: Path) -> int:
    """Calcula el tamano total de un archivo o, recursivamente, de una carpeta."""
    if path.is_file():
        return path.stat().st_size
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def report(original: int, final: int) -> None:
    """Imprime un resumen de la reduccion de tamano."""
    if original == 0:
        print("Archivo original vacio, nada que comparar.")
        return
    ratio = (1 - final / original) * 100
    print(f"  Original: {human_size(original)}")
    print(f"  Final:    {human_size(final)}")
    print(f"  Ahorro:   {ratio:.1f} %")
