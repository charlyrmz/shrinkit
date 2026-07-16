"""Definicion del parser de argumentos y punto de entrada de la CLI."""

import argparse

from shrinkit import __version__
from shrinkit.commands import cmd_gzip, cmd_image, cmd_info, cmd_zip


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser principal con todos los subcomandos."""
    parser = argparse.ArgumentParser(
        prog="shrinkit",
        description="Herramienta CLI para comprimir y reducir el tamano de archivos.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_zip = sub.add_parser("zip", help="Empaqueta en .zip (sin perdida).")
    p_zip.add_argument("source", help="Archivo o carpeta a comprimir.")
    p_zip.add_argument("-o", "--output", help="Ruta del .zip de salida.")
    p_zip.add_argument(
        "-l", "--level", type=int, default=6, choices=range(0, 10),
        help="Nivel de compresion 0-9 (default 6).",
    )
    p_zip.set_defaults(func=cmd_zip)

    p_gz = sub.add_parser("gzip", help="Comprime un archivo a .gz (sin perdida).")
    p_gz.add_argument("source", help="Archivo a comprimir.")
    p_gz.add_argument("-o", "--output", help="Ruta del .gz de salida.")
    p_gz.add_argument(
        "-l", "--level", type=int, default=9, choices=range(1, 10),
        help="Nivel de compresion 1-9 (default 9).",
    )
    p_gz.set_defaults(func=cmd_gzip)

    p_img = sub.add_parser("image", help="Reduce el tamano de una imagen (con perdida).")
    p_img.add_argument("source", help="Imagen de entrada (jpg, png, webp, etc).")
    p_img.add_argument("-o", "--output", help="Ruta de la imagen de salida.")
    p_img.add_argument(
        "-q", "--quality", type=int, default=80,
        help="Calidad 1-95 (default 80, solo aplica a JPEG/WEBP).",
    )
    p_img.add_argument(
        "--max-width", type=int, default=None,
        help="Ancho maximo en pixeles. Si la imagen es mas ancha, se redimensiona.",
    )
    p_img.set_defaults(func=cmd_image)

    p_info = sub.add_parser("info", help="Muestra el tamano de un archivo o carpeta.")
    p_info.add_argument("source", help="Ruta a inspeccionar.")
    p_info.set_defaults(func=cmd_info)

    return parser


def main() -> int:
    """Punto de entrada principal de la CLI."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)
