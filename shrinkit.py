#!/usr/bin/env python3
"""
shrinkit: herramienta CLI para comprimir archivos y reducir el tamano de imagenes.

Subcomandos:
  zip      Empaqueta archivos o carpetas en un .zip (sin perdida).
  gzip     Comprime un archivo individual a .gz (sin perdida).
  image    Reduce el tamano de imagenes (con perdida, ajustando calidad/dimensiones).
  info     Muestra el tamano de un archivo o carpeta.

Uso rapido:
  python shrinkit.py zip mi_carpeta -o salida.zip
  python shrinkit.py gzip archivo.csv
  python shrinkit.py image foto.jpg -q 75 --max-width 1600
  python shrinkit.py info mi_carpeta
"""

import argparse
import gzip
import shutil
import sys
import zipfile
from pathlib import Path


# Utilidades comunes

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


# Subcomando: zip

def cmd_zip(args: argparse.Namespace) -> int:
    source = Path(args.source)
    if not source.exists():
        print(f"Error: la ruta '{source}' no existe.", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else source.with_suffix(".zip")
    original = path_size(source)

    # ZIP_DEFLATED usa el algoritmo deflate, mismo que gzip. Nivel 0-9.
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=args.level) as zf:
        if source.is_file():
            zf.write(source, arcname=source.name)
        else:
            for file_path in source.rglob("*"):
                if file_path.is_file():
                    zf.write(file_path, arcname=file_path.relative_to(source.parent))

    final = output.stat().st_size
    print(f"Archivo creado: {output}")
    report(original, final)
    return 0


# Subcomando: gzip

def cmd_gzip(args: argparse.Namespace) -> int:
    source = Path(args.source)
    if not source.is_file():
        print("Error: gzip solo acepta archivos individuales, no carpetas.", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else source.with_suffix(source.suffix + ".gz")
    original = source.stat().st_size

    # gzip soporta niveles 1-9. 9 es maxima compresion pero mas lento.
    with open(source, "rb") as f_in, gzip.open(output, "wb", compresslevel=args.level) as f_out:
        shutil.copyfileobj(f_in, f_out)

    final = output.stat().st_size
    print(f"Archivo creado: {output}")
    report(original, final)
    return 0


# Subcomando: image

def cmd_image(args: argparse.Namespace) -> int:
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow no esta instalado. Instalalo con: pip install Pillow", file=sys.stderr)
        return 1

    source = Path(args.source)
    if not source.is_file():
        print(f"Error: '{source}' no es un archivo valido.", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else source.with_name(f"{source.stem}_compressed{source.suffix}")
    original = source.stat().st_size

    with Image.open(source) as img:
        # Conversion necesaria para guardar como JPEG si la imagen tiene canal alfa.
        if output.suffix.lower() in (".jpg", ".jpeg") and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Redimensionar si se especifico un ancho maximo.
        if args.max_width and img.width > args.max_width:
            ratio = args.max_width / img.width
            new_size = (args.max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            print(f"  Redimensionado a {new_size[0]}x{new_size[1]}")

        save_kwargs = {"optimize": True}
        if output.suffix.lower() in (".jpg", ".jpeg"):
            save_kwargs["quality"] = args.quality
            save_kwargs["progressive"] = True
        elif output.suffix.lower() == ".webp":
            save_kwargs["quality"] = args.quality

        img.save(output, **save_kwargs)

    final = output.stat().st_size
    print(f"Imagen creada: {output}")
    report(original, final)
    return 0


# Subcomando: info

def cmd_info(args: argparse.Namespace) -> int:
    path = Path(args.source)
    if not path.exists():
        print(f"Error: la ruta '{path}' no existe.", file=sys.stderr)
        return 1
    size = path_size(path)
    tipo = "carpeta" if path.is_dir() else "archivo"
    print(f"{tipo}: {path}")
    print(f"tamano: {human_size(size)} ({size} bytes)")
    return 0


# Parser principal

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shrinkit",
        description="Herramienta CLI para comprimir y reducir el tamano de archivos.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_zip = sub.add_parser("zip", help="Empaqueta en .zip (sin perdida).")
    p_zip.add_argument("source", help="Archivo o carpeta a comprimir.")
    p_zip.add_argument("-o", "--output", help="Ruta del .zip de salida.")
    p_zip.add_argument("-l", "--level", type=int, default=6, choices=range(0, 10),
                       help="Nivel de compresion 0-9 (default 6).")
    p_zip.set_defaults(func=cmd_zip)

    p_gz = sub.add_parser("gzip", help="Comprime un archivo a .gz (sin perdida).")
    p_gz.add_argument("source", help="Archivo a comprimir.")
    p_gz.add_argument("-o", "--output", help="Ruta del .gz de salida.")
    p_gz.add_argument("-l", "--level", type=int, default=9, choices=range(1, 10),
                      help="Nivel de compresion 1-9 (default 9).")
    p_gz.set_defaults(func=cmd_gzip)

    p_img = sub.add_parser("image", help="Reduce el tamano de una imagen (con perdida).")
    p_img.add_argument("source", help="Imagen de entrada (jpg, png, webp, etc).")
    p_img.add_argument("-o", "--output", help="Ruta de la imagen de salida.")
    p_img.add_argument("-q", "--quality", type=int, default=80,
                       help="Calidad 1-95 (default 80, solo aplica a JPEG/WEBP).")
    p_img.add_argument("--max-width", type=int, default=None,
                       help="Ancho maximo en pixeles. Si la imagen es mas ancha, se redimensiona.")
    p_img.set_defaults(func=cmd_image)

    p_info = sub.add_parser("info", help="Muestra el tamano de un archivo o carpeta.")
    p_info.add_argument("source", help="Ruta a inspeccionar.")
    p_info.set_defaults(func=cmd_info)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
