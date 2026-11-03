# Fase 3: Implementación del analizador sintáctico

Elegimos la **opción B de la consigna: el simulador del autómata a pila M**. El programa está en [`src/parser.py`](../../src/parser.py), en Python 3 y sin dependencias externas. La explicación para la defensa está en la [Guía para la defensa](../Guia_Defensa.md).

## Partes del programa

1. **`ETIQUETAS`:** definición de las etiquetas del lenguaje (`{"b": "B", "i": "I", "p": "P"}`).
2. **`tokenizar`:** convierte el texto en tokens de Σ. Cada palabra pasa a `TEXTO`, las etiquetas se normalizan y lo mal escrito se conserva para rechazarlo.
3. **`simular`:** aplica la tabla δ con una lista de Python como pila, devuelve si la cadena es válida, el mensaje y la traza.

## Errores que informa

| Error | Ejemplo | Mensaje |
|---|---|---|
| Anidamiento cruzado | `<p> <b> TEXTO </p> </b>` | `Error de anidamiento: se leyó '</p>' con B en el tope.` |
| Cierre sin apertura | `<p> TEXTO </p> </b>` | `Error sintáctico: se cerró '</b>' sin apertura previa.` |
| Etiquetas sin cerrar | `<p> <b> TEXTO </b>` | `Error sintáctico: etiquetas sin cerrar: <p>.` |
| Etiqueta desconocida | `<u> TEXTO </u>` | `Error léxico: '<u>' no pertenece a Σ.` |
| Etiqueta mal formada | `<p> TEXTO <b </p>` | `Error léxico: '<b' no pertenece a Σ.` |

## Ejecución

```bash
python src/parser.py
```

```bash
python src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```

```bash
python -m unittest tests/test_parser.py
```
