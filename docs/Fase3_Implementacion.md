# Fase 3: Implementación del Analizador Sintáctico (Parser)

**Materia:** Lenguajes Formales y Autómatas (2026)  
**Proyecto:** Analizador Sintáctico para MiniHTML  
**Documento:** Manual Técnico de Implementación y Correspondencia con Clases 7 y 8

---

## 1. Enfoque de Implementación y Correspondencia Teórica

La consigna de la cátedra solicita implementar el reconocedor ejecutable en Python evaluando dos alternativas:
* **Opción A (Analizador sintáctico a partir de $G$ - Clase 7):** Funciones recursivas para las variables no terminales (`parse_S()`, `parse_E()`).
* **Opción B (Simulador de APD a partir de $M$ - Clase 8):** Procesamiento secuencial con estructura de datos tipo Pila (*Stack*), modelando la 7-upla $M = (\Sigma, \Gamma, Q, q_0, Z_0, F, \delta)$.

### Diseño Limpio y sin Sobreingeniería
Siguiendo lo visto en clase y las recomendaciones de código limpio, unificamos la implementación en un **único archivo claro y directo:** [`src/parser.py`](../src/parser.py):
1. **Tokenizador:** Extrae las etiquetas y el texto plano mediante una expresión regular sencilla.
2. **Clase `AutomataPilaMiniHTML` (Modelo Clase 8):** Implementa el AFPD con una lista estándar de Python como pila (`stack = ['Z0']`), ejecutando las operaciones PUSH y POP de la función $\delta$ y emitiendo la traza de configuraciones instantáneas $(q, \omega, \gamma) \vdash (q', \omega', \gamma')$.
3. **Clase `AnalizadorRecursivoMiniHTML` (Modelo Clase 7):** Implementa las reglas de producción de la gramática $S \rightarrow E S \mid \lambda$ mediante llamadas recursivas.
4. **Verificación de Equivalencia:** Ambas estrategias se ejecutan sobre la misma entrada para demostrar que $w \in L(G) \iff w \in L(M)$.

---

## 2. Detalle del Código Fuente (`src/parser.py`)

### 2.1. Tokenizador / Analizador Léxico
```python
def tokenizar(cadena: str) -> List[str]:
    patron = re.compile(r'(</?[a-zA-Z0-9]+>|[^<]+)')
    # Separa etiquetas <p>, <b>, etc. y clasifica el texto plano como TEXTO
```
* Reconoce tanto cadenas formales (`<p> TEXTO <b> TEXTO </b> </p>`) como código HTML real (`<p>Hola <b>mundo</b></p>`).

### 2.2. Simulador del AFPD (`AutomataPilaMiniHTML`)
Traduce fielmente la 7-upla $M = (\Sigma, \Gamma, Q, q_0, Z_0, F, \delta)$ de la Clase 8:
* **Pila:** Se inicializa con `['Z0']`.
* **Lectura de `TEXTO`:** Operación no-op, el tope de la pila se conserva.
* **Lectura de `<tag>`:** Operación **PUSH**: apila el marcador ($B, I, P$) en el tope.
* **Lectura de `</tag>`:** Operación **POP**: si el tope coincide con el marcador de la etiqueta, se desapila. Si no coincide, la función $\delta$ está indefinida, produciendo el **bloqueo y rechazo** inmediato de la cadena.
* **Fin de lectura:** Si la pila contiene únicamente `['Z0']`, transiciona a $q_f$ y la cadena es aceptada ($w \in L(M)$).

### 2.3. Analizador Descendente Recursivo (`AnalizadorRecursivoMiniHTML`)
Traduce las producciones de la Clase 7:
* `parse_S()`: Aplica $S \rightarrow E S$ mientras haya texto o apertura; si encuentra cierre o fin de archivo, aplica la regla nula $S \rightarrow \lambda$.
* `parse_E()`: Aplica $E \rightarrow \text{TEXTO}$ o $E \rightarrow \langle\text{tag}\rangle S \langle/\text{tag}\rangle$, exigiendo que el cierre coincida con la apertura.

---

## 3. Manejo de Errores Sintácticos

El reconocedor clasifica la cadena como válida o inválida e indica claramente el motivo del fallo:

| Error Sintáctico | Ejemplo de Entrada | Mensaje Emitido por el Programa |
|:---|:---|:---|
| **Violación LIFO (Anidamiento cruzado)** | `<p> <b> TEXTO </p> </b>` | `Error de anidamiento LIFO: Se leyó '</p>' pero en el tope está 'B' (etiqueta no cerrada a tiempo).` |
| **Etiqueta huérfana de cierre** | `<p> TEXTO </p> </b>` | `Error sintáctico: Se intentó cerrar '</b>' sin apertura previa (pila vacía).` |
| **Etiquetas sin cerrar (EOF prematuro)** | `<p> <b> TEXTO </p>` | `Error de anidamiento LIFO: Se leyó '</p>' pero en el tope está 'B'.` |
| **Token no reconocido** | `<unk> TEXTO </unk>` | `Error léxico: El token '<unk>' no pertenece al alfabeto Σ del lenguaje.` |

---

## 4. Modificación en Vivo (Preparación para la Defensa Oral)

La consigna estipula:
> *"Se solicitará al grupo realizar una modificación menor en el momento, sobre el código fuente (por ejemplo, incorporar una nueva etiqueta al lenguaje)."*

En nuestro código, incorporar una nueva etiqueta (por ejemplo `<u>` para texto subrayado) se realiza de forma directa en solo dos líneas:

```python
# En src/parser.py:
automata.agregar_etiqueta("u", "U")  # Agrega <u> y </u> asociadas al marcador 'U'
```
O directamente editando los diccionarios en `AutomataPilaMiniHTML`:
```python
self.apertura_a_pila["<u>"] = "U"
self.cierre_a_pila["</u>"] = "U"
```
Ambos métodos actualizan de inmediato el alfabeto de entrada $\Sigma$, el alfabeto de pila $\Gamma$ y la función de transición $\delta$, permitiendo validar cadenas como `<p> <u> TEXTO </u> </p>` en tiempo real frente al docente.

---

## 5. Guía de Ejecución y Pruebas

El código utiliza únicamente la **librería estándar de Python 3** (sin dependencias externas requeridas).

### 5.1. Ejecutar las Pruebas Oficiales
Valida las cadenas oficiales de la cátedra ($\alpha, \beta, \gamma$), la cadena vacía y casos inválidos:
```bash
python src/parser.py --test
```

### 5.2. Probar una Cadena Específica con su Traza de Pila
```bash
python src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```
Muestra la traza de configuraciones instantáneas $(q, \omega, \gamma)$ paso a paso y los diagnósticos de $M$ y $G$.

### 5.3. Modo Interactivo en Vivo
```bash
python src/parser.py
```
Abre un menú interactivo en consola para ingresar cualquier cadena en tiempo real durante la entrevista oral.

### 5.4. Suite de Tests Automatizados
```bash
python -m unittest tests/test_parser.py
```
Ejecuta 9 pruebas unitarias que validan todos los casos borde y la extensión en vivo.
