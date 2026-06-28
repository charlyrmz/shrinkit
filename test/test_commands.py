"""Tests para los subcomandos de shrinkit (zip, gzip, info)."""

import argparse
import gzip
import zipfile

from shrinkit import cmd_gzip, cmd_info, cmd_zip


def make_args(**kwargs):
    """Construye un argparse.Namespace para invocar los comandos directamente."""
    return argparse.Namespace(**kwargs)


class TestCmdZip:
    """Pruebas para el subcomando zip."""

    def test_comprime_archivo_individual(self, tmp_path):
        source = tmp_path / "datos.txt"
        source.write_text("contenido de prueba" * 100)
        output = tmp_path / "salida.zip"

        args = make_args(source=str(source), output=str(output), level=6)
        result = cmd_zip(args)

        assert result == 0
        assert output.exists()
        assert zipfile.is_zipfile(output)

    def test_comprime_carpeta_completa(self, tmp_path):
        carpeta = tmp_path / "proyecto"
        carpeta.mkdir()
        (carpeta / "a.txt").write_text("archivo a")
        (carpeta / "b.txt").write_text("archivo b")
        subdir = carpeta / "sub"
        subdir.mkdir()
        (subdir / "c.txt").write_text("archivo c")

        output = tmp_path / "backup.zip"
        args = make_args(source=str(carpeta), output=str(output), level=6)
        result = cmd_zip(args)

        assert result == 0
        with zipfile.ZipFile(output) as zf:
            nombres = zf.namelist()
            assert len(nombres) == 3
            assert any("a.txt" in n for n in nombres)
            assert any("c.txt" in n for n in nombres)

    def test_falla_si_ruta_no_existe(self, tmp_path, capsys):
        args = make_args(
            source=str(tmp_path / "no_existe"),
            output=str(tmp_path / "salida.zip"),
            level=6,
        )
        result = cmd_zip(args)
        captured = capsys.readouterr()

        assert result == 1
        assert "no existe" in captured.err

    def test_genera_output_por_defecto_si_no_se_especifica(self, tmp_path):
        source = tmp_path / "datos.txt"
        source.write_text("hola")
        args = make_args(source=str(source), output=None, level=6)

        result = cmd_zip(args)

        assert result == 0
        assert (tmp_path / "datos.zip").exists()


class TestCmdGzip:
    """Pruebas para el subcomando gzip."""

    def test_comprime_archivo(self, tmp_path):
        source = tmp_path / "log.txt"
        # Contenido repetitivo para que se note la compresion
        source.write_text("linea de log\n" * 1000)
        output = tmp_path / "log.txt.gz"

        args = make_args(source=str(source), output=str(output), level=9)
        result = cmd_gzip(args)

        assert result == 0
        assert output.exists()
        # Verificar que el archivo es un gzip valido y descomprime al original
        with gzip.open(output, "rb") as f:
            assert f.read() == source.read_bytes()

    def test_reduce_tamano_en_contenido_repetitivo(self, tmp_path):
        source = tmp_path / "repetitivo.txt"
        source.write_text("a" * 100_000)
        output = tmp_path / "repetitivo.txt.gz"

        args = make_args(source=str(source), output=str(output), level=9)
        cmd_gzip(args)

        assert output.stat().st_size < source.stat().st_size

    def test_rechaza_carpetas(self, tmp_path, capsys):
        args = make_args(source=str(tmp_path), output=None, level=9)
        result = cmd_gzip(args)
        captured = capsys.readouterr()

        assert result == 1
        assert "archivos individuales" in captured.err


class TestCmdInfo:
    """Pruebas para el subcomando info."""

    def test_muestra_tamano_de_archivo(self, tmp_path, capsys):
        archivo = tmp_path / "test.txt"
        archivo.write_bytes(b"x" * 2048)

        args = make_args(source=str(archivo))
        result = cmd_info(args)
        captured = capsys.readouterr()

        assert result == 0
        assert "2.00 KB" in captured.out
        assert "2048 bytes" in captured.out

    def test_muestra_tamano_de_carpeta(self, tmp_path, capsys):
        (tmp_path / "a.txt").write_bytes(b"x" * 1024)
        (tmp_path / "b.txt").write_bytes(b"y" * 1024)

        args = make_args(source=str(tmp_path))
        result = cmd_info(args)
        captured = capsys.readouterr()

        assert result == 0
        assert "carpeta" in captured.out
        assert "2.00 KB" in captured.out

    def test_falla_si_no_existe(self, tmp_path, capsys):
        args = make_args(source=str(tmp_path / "fantasma"))
        result = cmd_info(args)
        captured = capsys.readouterr()

        assert result == 1
        assert "no existe" in captured.err
