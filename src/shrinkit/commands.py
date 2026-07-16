"""Implementacion de los subcomandos de la CLI."""

import argparse
import gzip
import shutil
import sys
import zipfile
from pathlib import Path

from shrinkit.utils import human_size, path_size, report


def cmd_zip(args: argparse.Namespace) -> int:
    """Empaqueta un archivo o carpeta a un .zip."""
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


def cmd_gzip(args: argparse.Namespace) -> int:
    """Comprime un archivo individual a .gz."""
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


def cmd_image(args: argparse.Namespace) -> int:
    """Reduce el tamano de una imagen ajustando calidad y dimensiones."""
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow no esta instalado. Instalalo con: pip install Pillow", file=sys.stderr)
        return 1

    source = Path(args.source)
    if not source.is_file():
        print(f"Error: '{source}' no es un archivo valido.", file=sys.stderr)
        return 1

    output = (
        Path(args.output)
        if args.output
        else source.with_name(f"{source.stem}_compressed{source.suffix}")
    )
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


def cmd_info(args: argparse.Namespace) -> int:
    """Muestra el tamano de un archivo o carpeta."""
    path = Path(args.source)
    if not path.exists():
        print(f"Error: la ruta '{path}' no existe.", file=sys.stderr)
        return 1
    size = path_size(path)
    tipo = "carpeta" if path.is_dir() else "archivo"
    print(f"{tipo}: {path}")
    print(f"tamano: {human_size(size)} ({size} bytes)")
    return 0
