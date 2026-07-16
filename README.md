# shrinkit

[![CI](https://github.com/charlyrmz/shrinkit/actions/workflows/ci.yml/badge.svg)](https://github.com/charlyrmz/shrinkit/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Herramienta de línea de comandos en Python para comprimir archivos y reducir el tamaño de imágenes. Pensada como utilidad ligera para uso diario y como proyecto de aprendizaje sobre CLIs, compresión y manejo de archivos.

> **Nota:** shrinkit realiza operaciones de E/S con los privilegios del proceso actual. Como cualquier herramienta que lee y escribe archivos, accederá a los recursos que el proceso pueda acceder. Sanitiza tus entradas en entornos no confiables.

## Características

- Empaquetado en `.zip` con compresión configurable (sin pérdida).
- Compresión a `.gz` para archivos individuales (sin pérdida).
- Reducción de imágenes con ajuste de calidad y redimensionado (con pérdida).
- Reporte automático de ahorro de espacio (original vs. final).
- Comando `info` para inspeccionar el tamaño de archivos y carpetas.

## ¿Por qué dos modos: con y sin pérdida?

No son lo mismo. La compresión sin pérdida, como `.zip` y `.gz`, reconstruye el archivo bit a bit, pero su efectividad cae mucho con archivos ya comprimidos (JPG, PNG, MP4, PDF moderno, XLSX). La reducción con pérdida, como ajustar calidad de JPEG, reduce mucho más a costa de información. shrinkit te deja elegir el enfoque correcto según el archivo.

## Requisitos

- Python 3.10 o superior.
- Pillow, opcional, solo si vas a usar el subcomando `image`.

## Instalación

### Desde el código fuente

```bash
git clone https://github.com/<tu-usuario>/shrinkit.git
cd shrinkit
pip install .
```

Esto instala el comando `shrinkit` en tu PATH.

### En modo desarrollo

```bash
pip install -e .
```

### Ejecutar como módulo

Una vez instalado, también puedes invocarlo como módulo:

```bash
python -m shrinkit --help
```

### Ver versión

```bash
shrinkit --version
```

## Uso

### Empaquetar a ZIP

```bash
shrinkit zip mi_carpeta -o backup.zip
shrinkit zip archivo.csv -l 9
```

Opciones:

- `-o, --output`: ruta del archivo `.zip` de salida.
- `-l, --level`: nivel de compresión, 0 a 9. Default: 6.

### Comprimir a GZIP

```bash
shrinkit gzip dataset.csv
shrinkit gzip log.txt -o log.txt.gz -l 9
```

Opciones:

- `-o, --output`: ruta del archivo `.gz` de salida.
- `-l, --level`: nivel de compresión, 1 a 9. Default: 9.

### Reducir imágenes

Requiere instalar Pillow: `pip install Pillow`.

```bash
shrinkit image foto.jpg -q 75
shrinkit image banner.png -q 80 --max-width 1600 -o banner_web.jpg
```

Opciones:

- `-o, --output`: ruta de la imagen de salida.
- `-q, --quality`: calidad, 1 a 95. Default: 80. Solo aplica a JPEG y WEBP.
- `--max-width`: ancho máximo en píxeles. Si la imagen es más ancha, se redimensiona conservando proporción.

### Consultar tamaño

```bash
shrinkit info mi_carpeta
shrinkit info dataset.csv
```

## Ejemplo de salida

```
$ shrinkit gzip dataset.csv
Archivo creado: dataset.csv.gz
  Original: 1.53 MB
  Final:    403.84 KB
  Ahorro:   74.3 %
```

## Estructura del proyecto

```
shrinkit/
├── .github/workflows/    Workflows de GitHub Actions (CI).
├── src/shrinkit/         Codigo fuente del paquete.
│   ├── __init__.py       Version del paquete.
│   ├── __main__.py       Entry point para `python -m shrinkit`.
│   ├── cli.py            Parser de argumentos y funcion main.
│   ├── commands.py       Implementacion de los subcomandos.
│   └── utils.py          Funciones auxiliares.
└── tests/                Suite de tests con pytest.
```

## Roadmap

Funcionalidad planeada para próximas versiones:

- Soporte para `tar.gz` y `tar.bz2`.
- Compresión de PDFs con `pikepdf`.
- Procesamiento batch de carpetas de imágenes en paralelo, usando `concurrent.futures`.
- Modo dry-run para estimar ahorro sin escribir archivos.

## Desarrollo

### Configurar entorno

```bash
git clone https://github.com/charlyrmz/shrinkit.git
cd shrinkit
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,image]"
```

### Ejecutar tests

```bash
pytest
```

Para ver detalle de cada test:

```bash
pytest -v
```

Para ejecutar solo un archivo:

```bash
pytest tests/test_utils.py
```

### Linting

```bash
ruff check .
```

### Integración continua

Cada push y cada PR a `main` dispara el workflow de GitHub Actions definido en `.github/workflows/ci.yml`. Este corre los tests en Python 3.10, 3.11 y 3.12, y valida el estilo con ruff.

## Contribuir

Las contribuciones son bienvenidas. Lee [CONTRIBUTING.md](CONTRIBUTING.md) para los lineamientos.

## Seguridad

Si encuentras una vulnerabilidad, sigue el proceso descrito en [SECURITY.md](SECURITY.md).

## Código de conducta

Este proyecto sigue el [Código de Conducta](CODE_OF_CONDUCT.md) basado en Contributor Covenant.

## Licencia

Distribuido bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## Autor

Carlos Isaac Ramírez Santamaría (@charlyrmz)
