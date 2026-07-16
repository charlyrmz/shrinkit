"""Tests para las funciones utilitarias de shrinkit."""

from shrinkit.utils import human_size, path_size


class TestHumanSize:
    """Pruebas para la conversion de bytes a formato legible."""

    def test_bytes_simples(self):
        assert human_size(0) == "0.00 B"
        assert human_size(500) == "500.00 B"
        assert human_size(1023) == "1023.00 B"

    def test_kilobytes(self):
        assert human_size(1024) == "1.00 KB"
        assert human_size(1536) == "1.50 KB"

    def test_megabytes(self):
        assert human_size(1024 * 1024) == "1.00 MB"
        assert human_size(int(2.5 * 1024 * 1024)) == "2.50 MB"

    def test_gigabytes(self):
        assert human_size(1024 ** 3) == "1.00 GB"

    def test_terabytes(self):
        assert human_size(1024 ** 4) == "1.00 TB"


class TestPathSize:
    """Pruebas para el calculo de tamano de archivos y carpetas."""

    def test_archivo_individual(self, tmp_path):
        archivo = tmp_path / "test.txt"
        archivo.write_bytes(b"a" * 100)
        assert path_size(archivo) == 100

    def test_archivo_vacio(self, tmp_path):
        archivo = tmp_path / "vacio.txt"
        archivo.write_bytes(b"")
        assert path_size(archivo) == 0

    def test_carpeta_con_archivos(self, tmp_path):
        (tmp_path / "a.txt").write_bytes(b"a" * 50)
        (tmp_path / "b.txt").write_bytes(b"b" * 30)
        assert path_size(tmp_path) == 80

    def test_carpeta_anidada(self, tmp_path):
        subdir = tmp_path / "sub"
        subdir.mkdir()
        (tmp_path / "raiz.txt").write_bytes(b"a" * 10)
        (subdir / "anidado.txt").write_bytes(b"b" * 20)
        assert path_size(tmp_path) == 30

    def test_carpeta_vacia(self, tmp_path):
        assert path_size(tmp_path) == 0
