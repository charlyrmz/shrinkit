"""Tests para el subcomando image. Se saltan si Pillow no esta instalado."""

import argparse

import pytest

# Skip todo el modulo si Pillow no esta disponible
PIL = pytest.importorskip("PIL", reason="Pillow no instalado; instala con pip install '.[image]'")
from PIL import Image  # noqa: E402

from shrinkit.commands import cmd_image  # noqa: E402


def make_args(**kwargs):
    return argparse.Namespace(**kwargs)


@pytest.fixture
def imagen_jpg(tmp_path):
    """Crea una imagen JPEG de prueba con contenido aleatorio para que tenga peso."""
    import random
    ruta = tmp_path / "original.jpg"
    img = Image.new("RGB", (2000, 1500))
    # Pixeles aleatorios para que JPEG no pueda comprimir tanto
    pixels = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
              for _ in range(2000 * 1500)]
    img.putdata(pixels)
    img.save(ruta, quality=95)
    return ruta


class TestCmdImage:
    def test_reduce_calidad_jpeg(self, imagen_jpg, tmp_path):
        salida = tmp_path / "comprimida.jpg"
        args = make_args(
            source=str(imagen_jpg),
            output=str(salida),
            quality=30,
            max_width=None,
        )

        result = cmd_image(args)

        assert result == 0
        assert salida.exists()
        # A calidad 30 debe pesar significativamente menos que el original a 95
        assert salida.stat().st_size < imagen_jpg.stat().st_size

    def test_redimensiona_con_max_width(self, imagen_jpg, tmp_path):
        salida = tmp_path / "redim.jpg"
        args = make_args(
            source=str(imagen_jpg),
            output=str(salida),
            quality=80,
            max_width=500,
        )

        cmd_image(args)

        with Image.open(salida) as img:
            assert img.width == 500
            # La altura debe escalar proporcionalmente: 1500 * (500/2000) = 375
            assert img.height == 375

    def test_no_redimensiona_si_imagen_es_mas_pequena(self, tmp_path):
        # Imagen de 400px de ancho con max_width=800: no debe cambiar
        ruta = tmp_path / "small.jpg"
        Image.new("RGB", (400, 300), color="red").save(ruta)
        salida = tmp_path / "out.jpg"

        args = make_args(
            source=str(ruta),
            output=str(salida),
            quality=80,
            max_width=800,
        )
        cmd_image(args)

        with Image.open(salida) as img:
            assert img.width == 400
            assert img.height == 300

    def test_falla_si_archivo_no_existe(self, tmp_path, capsys):
        args = make_args(
            source=str(tmp_path / "fantasma.jpg"),
            output=None,
            quality=80,
            max_width=None,
        )
        result = cmd_image(args)
        captured = capsys.readouterr()

        assert result == 1
        assert "archivo valido" in captured.err
