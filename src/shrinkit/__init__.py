"""shrinkit: herramienta CLI para comprimir archivos y reducir el tamano de imagenes."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("shrinkit")
except PackageNotFoundError:
    # Ocurre si el paquete no esta instalado (ejecutandose desde el fuente sin pip install).
    __version__ = "unknown"

__all__ = ["__version__"]
