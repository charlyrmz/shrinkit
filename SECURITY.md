# Política de Seguridad

## Versiones soportadas

Al ser un proyecto en etapa temprana, solo la versión más reciente recibe parches de seguridad.

| Versión | Soportada |
|---------|-----------|
| 0.1.x   | Sí        |

## Reportar una vulnerabilidad

Si descubres una vulnerabilidad de seguridad en shrinkit, por favor **no** la reportes públicamente abriendo un issue. En su lugar:

1. Abre un [security advisory privado](https://github.com/cRamirez/shrinkit/security/advisories/new) en GitHub.
2. Alternativamente, contacta directamente al autor del repositorio.

Incluye en tu reporte:

- Descripción de la vulnerabilidad.
- Pasos para reproducirla.
- Versión afectada.
- Posible impacto.

Trataré de responder en un plazo de 7 días.

## Consideraciones de seguridad al usar shrinkit

shrinkit realiza operaciones de E/S con los privilegios del proceso que la ejecuta. Esto significa que:

- Leerá y escribirá cualquier archivo al que el proceso tenga acceso.
- No valida ni restringe las rutas de entrada más allá de verificar que existan.
- Al descomprimir archivos generados por terceros, no se incluye protección contra ataques tipo zip slip o zip bomb. En esta versión, shrinkit solo comprime, no descomprime, pero ten cuidado al manipular archivos de origen no confiable.

Recomendaciones:

- No ejecutes shrinkit con privilegios elevados a menos que sea estrictamente necesario.
- Sanitiza las rutas de entrada cuando integres shrinkit en pipelines automatizados.
- Verifica el origen de los archivos antes de procesarlos.
