"""Tests para el parser de la CLI."""

import pytest

from shrinkit.cli import build_parser


class TestParser:
    """Verifica que el parser de argumentos respete el contrato publico de la CLI."""

    def test_subcomandos_disponibles(self):
        parser = build_parser()
        # Estos no deben lanzar SystemExit
        for cmd in ["zip", "gzip", "image", "info"]:
            args = parser.parse_args([cmd, "fake_source"])
            assert args.command == cmd

    def test_zip_nivel_default(self):
        args = build_parser().parse_args(["zip", "carpeta"])
        assert args.level == 6
        assert args.output is None

    def test_gzip_nivel_default(self):
        args = build_parser().parse_args(["gzip", "archivo.txt"])
        assert args.level == 9

    def test_image_calidad_default(self):
        args = build_parser().parse_args(["image", "foto.jpg"])
        assert args.quality == 80
        assert args.max_width is None

    def test_image_argumentos_completos(self):
        args = build_parser().parse_args([
            "image", "foto.jpg",
            "-q", "65",
            "--max-width", "1200",
            "-o", "salida.jpg",
        ])
        assert args.quality == 65
        assert args.max_width == 1200
        assert args.output == "salida.jpg"

    def test_falta_subcomando_falla(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args([])

    def test_subcomando_invalido_falla(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args(["transmogrify", "archivo"])

    def test_nivel_fuera_de_rango_falla(self):
        # zip acepta solo 0-9
        with pytest.raises(SystemExit):
            build_parser().parse_args(["zip", "x", "-l", "15"])
