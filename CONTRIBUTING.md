# Cómo contribuir a shrinkit

Gracias por tu interés en contribuir. Este documento describe el flujo recomendado.

## Reportar bugs

Antes de abrir un issue, revisa si ya existe uno similar en la [pestaña de Issues](https://github.com/charlyrmz/shrinkit/issues). Si no, abre uno nuevo incluyendo:

- Versión de Python, sistema operativo y versión de shrinkit.
- Comando exacto que ejecutaste.
- Resultado esperado vs. resultado obtenido.
- Si aplica, un archivo mínimo de ejemplo que reproduzca el problema.

## Proponer nuevas funcionalidades

Abre un issue describiendo el caso de uso antes de empezar a programar. Esto evita trabajo duplicado y permite discutir el diseño.

Funcionalidades actualmente abiertas a contribución:

- Soporte para `tar.gz` y `tar.bz2`.
- Compresión de PDFs.
- Procesamiento paralelo de carpetas de imágenes.
- Modo dry-run.

## Flujo de trabajo

1. Haz fork del repositorio.
2. Crea una rama descriptiva: `git checkout -b feature/soporte-targz` o `fix/zip-permisos`.
3. Haz tus cambios y agrega tests si aplica.
4. Asegúrate de que el código pase los checks: `ruff check .`.
5. Haz commit con un mensaje claro en presente: `Agrega soporte para tar.gz`.
6. Empuja tu rama y abre un Pull Request describiendo qué hiciste y por qué.

## Configuración del entorno de desarrollo

```bash
git clone https://github.com/<tu-usuario>/shrinkit.git
cd shrinkit
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -e ".[dev,all]"
```

## Estilo de código

- Sigue PEP 8.
- Usa `ruff` para linting.
- Nombra variables y funciones en inglés salvo que el contexto sea explicitamente en español.
- Documenta funciones públicas con docstrings.

## Tests

Cuando agregues tests, colócalos en `tests/` y ejecútalos con:

```bash
pytest
```

## Licencia

Al contribuir, aceptas que tu código se distribuya bajo la misma licencia MIT del proyecto.
