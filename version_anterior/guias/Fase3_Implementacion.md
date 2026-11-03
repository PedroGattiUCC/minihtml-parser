# Fase 3: Implementación del Analizador Sintáctico (Parser)

**Materia:** Lenguajes Formales y Autómatas (2026)  
**Proyecto:** Analizador Sintáctico para MiniHTML  
**Documento:** Manual Técnico de Implementación y Correspondencia con Clases 7 y 8

---

## 1. Enfoque de Implementación y Correspondencia Teórica

La consigna de la cátedra solicita implementar el reconocedor ejecutable en Python evaluando dos alternativas:
* **Opción A (Analizador sintáctico a partir de $G$ - Clase 7):** Funciones recursivas para las variables no terminales (`parse_S()`, `parse_E()`).
* **Opción B (Simulador de AP a partir de $M$ - Clase 8):** Procesamiento secuencial con estructura de datos tipo Pila (*Stack*), modelando la 7-upla $M = (\Sigma, \Gamma, Q, q_0, Z_0, F, \Delta)$.

### Diseño Limpio y sin Sobreingeniería
Siguiendo lo visto en clase y las recomendaciones de código limpio, unificamos la implementación en un **único archivo claro y directo:** [`src/parser.py`](../src/parser.py):
1. **Diccionario `ETIQUETAS`:** Única definición de las etiquetas del lenguaje (`{"b": "B", "i": "I", "p": "P"}`), de la que $M$ y $G$ construyen sus alfabetos.
2. **Tokenizador:** Extrae las etiquetas y el texto plano mediante una expresión regular sencilla.
3. **Clase `AutomataPilaMiniHTML` (Modelo Clase 8):** Implementa el AFPN-$\lambda$ con una lista estándar de Python como pila (`pila = ['Z0']`), ejecutando las operaciones PUSH y POP de la función $\Delta$ y emitiendo la traza de configuraciones instantáneas $(q, \omega, \gamma) \vdash (q', \omega', \gamma')$.
4. **Clase `AnalizadorRecursivoMiniHTML` (Modelo Clase 7):** Implementa las reglas de producción de la gramática $S \rightarrow E S \mid \lambda$ mediante llamadas recursivas.
5. **Verificación de Equivalencia:** Ambas estrategias se ejecutan sobre la misma entrada para demostrar que $w \in L(G) \iff w \in L(M)$.

---

## 2. Detalle del Código Fuente (`src/parser.py`)

### 2.1. Tokenizador / Analizador Léxico
```python
PATRON_TOKEN = re.compile(r'<[^<>]*>?|[^<]+')               # "<...>" o texto plano
PATRON_ETIQUETA = re.compile(r'<([/\\]?)([a-zA-Z0-9]+)>')    # etiqueta bien formada
```
* Reconoce tanto cadenas formales (`<p> TEXTO <b> TEXTO </b> </p>`) como código HTML real (`<p>Hola <b>mundo</b></p>`). Cada palabra de texto se convierte en un token `TEXTO`.
* Admite `<\p>` como notación alternativa de `</p>` (la usada en la consigna).
* Una etiqueta mal formada (`<b`, `< b >`, `<p class=x>`) **no** se descarta ni se toma como texto: se conserva como token para que ambos analizadores la rechacen con un error léxico.

### 2.2. Simulador del AFPN-$\lambda$ (`AutomataPilaMiniHTML`)
Traduce fielmente la 7-upla $M = (\Sigma, \Gamma, Q, q_0, Z_0, F, \Delta)$ de la Clase 8:
* **Pila:** Se inicializa con `['Z0']`.
* **Lectura de `TEXTO`:** Operación no-op, el tope de la pila se conserva.
* **Lectura de `<tag>`:** Operación **PUSH**: apila el marcador ($B, I, P$) en el tope.
* **Lectura de `</tag>`:** Operación **POP**: si el tope coincide con el marcador de la etiqueta, se desapila. Si no coincide, $\Delta = \emptyset$, produciendo el **bloqueo y rechazo** inmediato de la cadena.
* **Fin de lectura:** Si la pila contiene únicamente `['Z0']`, aplica la transición espontánea $\Delta(q_0, \lambda, Z_0) = \{(q_f, Z_0)\}$ y la cadena es aceptada ($w \in L(M)$). Es el único punto no determinista de $M$: el simulador la toma solo con la entrada consumida porque es la única rama que puede aceptar (ver Fase 2, sección 1).
* **Traza:** cada paso registra la configuración $(q, \omega, \gamma)$ **resultante** (entrada que falta leer y pila con el tope a la izquierda) junto con la transición de $\Delta$ aplicada.

### 2.3. Analizador Descendente Recursivo (`AnalizadorRecursivoMiniHTML`)
Traduce las producciones de la Clase 7:
* `parse_S()`: Aplica $S \rightarrow E S$ mientras haya texto o apertura; si encuentra cierre o fin de archivo, aplica la regla nula $S \rightarrow \lambda$.
* `parse_E()`: Aplica $E \rightarrow \text{TEXTO}$ o $E \rightarrow \langle\text{tag}\rangle S \langle/\text{tag}\rangle$, exigiendo que el cierre coincida con la apertura. Un token que no es terminal de $G$ produce un error léxico.

---

## 3. Manejo de Errores Sintácticos

El reconocedor clasifica la cadena como válida o inválida e indica claramente el motivo del fallo:

| Error Sintáctico | Ejemplo de Entrada | Mensaje Emitido por el Programa |
|:---|:---|:---|
| **Violación LIFO (Anidamiento cruzado)** | `<p> <b> TEXTO </p> </b>` | `Error de anidamiento LIFO: Se leyó '</p>' pero en el tope está 'B' (se esperaba cerrar '<b>' primero).` |
| **Etiqueta huérfana de cierre** | `<p> TEXTO </p> </b>` | `Error sintáctico: Se intentó cerrar '</b>' sin apertura previa (pila vacía).` |
| **Etiquetas sin cerrar (fin de la entrada)** | `<p> <b> TEXTO </b>` | `Error sintáctico: Fin de la entrada con etiquetas sin cerrar (del tope al fondo): <p>.` |
| **Token no reconocido** | `<unk> TEXTO </unk>` | `Error léxico: El token '<unk>' no pertenece al alfabeto Σ del lenguaje.` |
| **Etiqueta mal formada** | `<p> TEXTO <b </p>` | `Error léxico: El token '<b' no pertenece al alfabeto Σ del lenguaje.` |

---

## 4. Modificación en Vivo (Preparación para la Defensa Oral)

La consigna estipula:
> *"Se solicitará al grupo realizar una modificación menor en el momento, sobre el código fuente (por ejemplo, incorporar una nueva etiqueta al lenguaje)."*

En nuestro código, incorporar una nueva etiqueta (por ejemplo `<u>` para texto subrayado) requiere **una sola línea**, en el diccionario `ETIQUETAS` al comienzo de `src/parser.py`:

```python
ETIQUETAS: Dict[str, str] = {
    "b": "B",
    "i": "I",
    "p": "P",
    "u": "U",   # <u> y </u>, con marcador de pila 'U'
}
```
Como el autómata $M$ y la gramática $G$ construyen sus alfabetos a partir de este diccionario, el cambio actualiza a la vez el alfabeto de entrada $\Sigma$, el alfabeto de pila $\Gamma$, las transiciones de $\Delta$ y las producciones $E \rightarrow \langle u\rangle S \langle/u\rangle$ de $G$, permitiendo validar cadenas como `<p> <u> TEXTO </u> </p>` en tiempo real frente al docente.

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
Ejecuta 14 pruebas unitarias que validan todos los casos borde y la extensión en vivo.
