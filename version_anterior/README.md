# Versión anterior del proyecto

Copia del estado del repositorio en el commit `836d1ba` ("feat: informe pdf"), antes de que se simplificara el parser a la opción B. Se guarda para consulta; la versión vigente es la de la raíz del repositorio.

| Carpeta | Contenido |
|---|---|
| `informe/` | Informe en PDF de esa versión (13 páginas). Su Fase 3 describe las dos implementaciones. |
| `src/` | `parser.py` con las dos estrategias: el simulador del autómata a pila (opción B) y el analizador descendente recursivo de la gramática (opción A). Ejecuta ambas y verifica que coincidan. |
| `tests/` | 14 pruebas unitarias. |
| `diagramas/` | Script que genera los árboles de derivación y el diagrama del autómata, y las imágenes que genera. |
| `guias/` | Documentos de cada fase y el resumen para la defensa oral de esa versión. |

Para ejecutarla, entrar primero a esta carpeta:

```bash
cd version_anterior
python src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
python -m unittest tests/test_parser.py
```
