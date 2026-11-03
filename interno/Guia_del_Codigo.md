# Guía del código: entenderlo y modificarlo en vivo

Esta guía tiene un solo objetivo: que puedas abrir [src/parser.py](../src/parser.py), entender cada línea y hacer **cualquier cambio que pida la profe, incluso uno que no practicaste**. La teoría completa está en la [Guía de estudio](Guia_de_Estudio.md).

El programa implementa **solo la opción B de la consigna: el simulador del autómata a pila M**. La gramática G está en el informe y hay que saber explicarla, pero no está programada. Por eso **cada cambio se hace en un solo lugar**.

> **Material interno: no se entrega.** Todas las recetas y los errores de esta guía se ejecutaron sobre el código real. Los números de línea son los de `parser.py` sin modificar: apenas agregás algo, las líneas de abajo se corren.

## Cómo usar esta guía

| Paso | Qué hacer | Tiempo | Sabés que terminaste cuando... |
|---|---|---|---|
| 1 | Secciones 1 a 3: mapa, Python y código | 1 h | Explicás cada línea sin leer la explicación |
| 2 | Sección 4: seguir ejecuciones a mano | 20 min | Predecís la traza antes de correrla |
| 3 | Sección 5: cómo pensar un cambio | 20 min | Ubicás un pedido en la tabla de lugares |
| 4 | Sección 6: hacer los cambios ⭐ | 1 h | Hacés `<u>`, `<br>` y "`<p>` dentro de `<p>`" sin mirar |
| 5 | Secciones 7 y 8: errores y ejercicios | 30 min | Resolvés los pedidos nuevos de 8.2 |

## Antes de practicar: guardá una copia

**Practicá en la rama `simplificar-parser-e-informe`.** Esta versión ya está commiteada ahí, pero **`master` tiene el código viejo** hasta que se haga el merge. Si no sabés en qué rama estás:

```bash
git branch --show-current
```

Cuando termines un ejercicio, deshacé tus pruebas con este comando, que borra todo lo que no commiteaste en esos dos archivos:

```bash
git restore src/parser.py tests/test_parser.py
```

Si preferís no usar git, desde la carpeta raíz del repo guardá una copia afuera antes de empezar:

```bash
cp src/parser.py ../parser_original.py
```

Y restaurala al terminar:

```bash
cp ../parser_original.py src/parser.py
```

---

## 1. El mapa del programa

```
texto de entrada
   │
   ▼
tokenizar (19)        → lista de tokens: ['<p>', 'TEXTO', '</p>']
   │
   ▼
simular (35)          → recorre los tokens aplicando la tabla δ, con una pila
   │
   ▼
analizar_cadena (63)  → imprime los tokens, la traza y el resultado
```

**Las tres ideas que explican casi todo:**

1. **El lenguaje se define en un solo lugar:** `ETIQUETAS` (línea 13).
2. **`tokenizar` traduce y no decide.** Pasa el texto a símbolos. Si un cambio afecta solo cómo se lee el texto, se hace acá.
3. **`simular` es la tabla δ escrita en Python.** Cada rama del `for` es un grupo de filas de la tabla. Si un cambio afecta qué estructuras son válidas, se hace acá.

---

## 2. El Python que necesitás

Si alguna fila no te cierra, probala en una consola de `python3`.

| Concepto | Ejemplo | Qué hace | Línea |
|---|---|---|---|
| Diccionario | `APERTURAS["<b>"]` da `"B"` | Busca un valor por su clave | 45 |
| `in` en un diccionario | `token in APERTURAS` | Pregunta si esa **clave** existe | 44 |
| Comprensión de diccionario | `{f"<{e}>": s for e, s in ETIQUETAS.items()}` | Crea un diccionario a partir de otro | 15 |
| Lista como pila | `pila.append(x)`, `pila.pop()`, `pila[-1]` | Apilar, desapilar y mirar el tope | 45, 49, 41 |
| Comparar listas | `pila != ["Z0"]` | Compara todo el contenido | 56 |
| f-string | `f"<{s.lower()}>"` | Inserta valores en un texto | 57 |
| Porciones | `tokens[i + 1:]`, `pila[1:]` | Desde esa posición hasta el final | 54, 57 |
| `enumerate` | `for i, token in enumerate(tokens)` | Da la posición y el elemento | 40 |
| Devolver varios valores | `return False, mensaje, traza` | Devuelve una tupla de 3 valores | 47 |
| Desempaquetar | `valida, mensaje, traza = simular(tokens)` | Separa esos 3 valores | 65 |
| `join` y `reversed` | `" ".join(reversed(pila))` | Une al revés: el tope queda primero | 32 |
| `or` con vacío | `' '.join(resto) or 'λ'` | Si el texto es vacío, usa `λ` | 32 |
| Comprensión de lista | `[f"<{s.lower()}>" for s in ...]` | Crea una lista transformando otra | 57 |
| `pass` | `pass` | No hace nada: la regla 1 no toca la pila | 43 |
| `re.findall` | `re.findall(patrón, cadena)` | Devuelve todos los trozos que coinciden | 22 |

**Regla de oro de `simular`:** todos los `return` de error devuelven **tres valores**: `False`, el mensaje y `traza`. Si olvidás `traza` da `ValueError: not enough values to unpack`.

---

## 3. El código, línea por línea

### 3.1 Preparación y definición del lenguaje

```python
  5  import re
  6  import sys
  7
  8  # Para que δ y λ se vean bien también en la consola de Windows.
  9  if hasattr(sys.stdout, "reconfigure"):
 10      sys.stdout.reconfigure(encoding="utf-8")
 11
 12  # Etiqueta -> símbolo de pila. Para agregar una etiqueta alcanza con sumarla acá.
 13  ETIQUETAS = {"b": "B", "i": "I", "p": "P"}
 14
 15  APERTURAS = {f"<{e}>": s for e, s in ETIQUETAS.items()}
 16  CIERRES = {f"</{e}>": s for e, s in ETIQUETAS.items()}
```

- **8 a 10:** hacen que `δ` y `λ` se impriman bien también en una consola de Windows.
- **13:** la clave es el nombre de la etiqueta y el valor es su símbolo de pila.
- **15 y 16:** arman la tabla δ en forma compacta:

```python
APERTURAS = {'<b>': 'B', '<i>': 'I', '<p>': 'P'}    # reglas 2 a 4
CIERRES   = {'</b>': 'B', '</i>': 'I', '</p>': 'P'}  # reglas 5 a 7
```

Por eso agregar una etiqueta requiere una sola entrada.

### 3.2 `tokenizar`

```python
 19  def tokenizar(cadena):
 20      """Convierte el texto en tokens de Σ. Lo mal escrito queda igual para rechazarlo después."""
 21      tokens = []
 22      for trozo in re.findall(r"<[^<>]*>?|[^<\s]+", cadena):
 23          if trozo.startswith("<"):
 24              tokens.append(trozo.strip().lower().replace("\\", "/"))
 25          else:
 26              tokens.append("TEXTO")
 27      return tokens
```

La expresión regular de la línea 22 tiene dos alternativas, separadas por `|`:

| Parte | Significado | Ejemplos |
|---|---|---|
| `<[^<>]*>?` | Un `<`, cualquier cosa sin `<` ni `>`, y un `>` optativo | `<p>`, `<b `, `< b >` |
| `[^<\s]+` | Una palabra: caracteres que no son `<` ni espacios | `Hola`, `TEXTO`, `>` |

Para `<p>Hola <B>mundo</b> <b`, los trozos y los tokens quedan así:

| Trozo | Rama | Token | Por qué |
|---|---|---|---|
| `<p>` | 24 | `<p>` | Ya está bien |
| `Hola` | 26 | `TEXTO` | Es una palabra |
| `<B>` | 24 | `<b>` | `.lower()` lo pasa a minúscula |
| `mundo` | 26 | `TEXTO` | Es una palabra |
| `</b>` | 24 | `</b>` | Ya está bien |
| `<b` | 24 | `<b` | Queda igual, y `simular` lo rechaza después |

Tres detalles de la línea 24:

- **`.strip()`** saca los espacios del final: `<b ` pasa a `<b`.
- **`.replace("\\", "/")`** acepta la notación `<\p>` de la consigna. En Python, `"\\"` es una sola barra invertida.
- **No descarta lo mal escrito.** Si lo tratara como texto, aceptaría `<b`.

### 3.3 `configuracion`

```python
 30  def configuracion(estado, resto, pila):
 31      """Arma el texto (q, ω, γ), con el tope de la pila a la izquierda."""
 32      return f"({estado}, {' '.join(resto) or 'λ'}, {' '.join(reversed(pila))})"
```

Arma el texto `(q, ω, γ)`. `reversed` pone el tope a la izquierda, como en teoría, y `or 'λ'` muestra `λ` cuando ya no queda entrada.

### 3.4 `simular`: el corazón del programa

```python
 35  def simular(tokens):
 36      """Aplica δ token por token. Devuelve (es_valida, mensaje, traza)."""
 37      pila = ["Z0"]  # el tope es el último elemento
 38      traza = [configuracion("q0", tokens, pila)]
```

Es la configuración inicial `(q0, w, Z0)`. **El último elemento de la lista es el tope.** El estado no se guarda en una variable, porque se trabaja siempre en q0 hasta la regla 8.

```python
 40      for i, token in enumerate(tokens):
 41          tope = pila[-1]
 42          if token == "TEXTO":                  # regla 1: la pila no cambia
 43              pass
 44          elif token in APERTURAS:              # reglas 2 a 4: apila
 45              pila.append(APERTURAS[token])
 46          elif token not in CIERRES:
 47              return False, f"Error léxico: '{token}' no pertenece a Σ.", traza
 48          elif tope == CIERRES[token]:          # reglas 5 a 7: desapila
 49              pila.pop()
 50          elif tope == "Z0":
 51              return False, f"Error sintáctico: se cerró '{token}' sin apertura previa.", traza
 52          else:
 53              return False, f"Error de anidamiento: se leyó '{token}' con {tope} en el tope.", traza
 54          traza.append(configuracion("q0", tokens[i + 1:], pila))
```

**Cada token entra en una sola rama:**

| Línea | Pregunta | Si es sí | Regla |
|---|---|---|---|
| 42 | ¿Es `TEXTO`? | No toca la pila | 1 |
| 44 | ¿Es una apertura? | Apila su símbolo | 2 a 4 |
| 46 | ¿Tampoco es un cierre conocido? | Error léxico | Fuera de Σ |
| 48 | ¿El cierre coincide con el tope? | Desapila | 5 a 7 |
| 50 | ¿El tope es Z0? | Cierre sin apertura | δ vacía |
| 52 | Si no, el tope es otra etiqueta | Cruce | δ vacía |

**La línea 54 solo se ejecuta si hubo transición**, porque todos los errores salen antes con `return`. `tokens[i + 1:]` es lo que falta leer.

**La línea 48 es la más importante del programa:** esa comparación impone el orden LIFO.

```python
 56      if pila != ["Z0"]:
 57          abiertas = [f"<{s.lower()}>" for s in reversed(pila[1:])]
 58          return False, f"Error sintáctico: etiquetas sin cerrar: {', '.join(abiertas)}.", traza
 59      traza.append(configuracion("qf", [], pila))  # regla 8: δ(q0, λ, Z0) = (qf, Z0)
 60      return True, "Cadena válida (w ∈ L(M)).", traza
```

- **56 a 58:** terminó la entrada con etiquetas abiertas. `pila[1:]` deja afuera a Z0, `reversed` lista primero la más interna y `s.lower()` convierte `P` en `p`.
- **59:** la regla 8. Pasa a `qf` sin leer nada.

### 3.5 La interfaz

```python
 63  def analizar_cadena(cadena):
 64      tokens = tokenizar(cadena)
 65      valida, mensaje, traza = simular(tokens)
 66      print(f"Tokens: {tokens or 'λ'}")
 67      print("\n⊢ ".join(traza))
 68      print(f"{'ACEPTADA' if valida else 'RECHAZADA (w ∉ L(M))'}. {mensaje}")
 69
 70
 71  if __name__ == "__main__":
 72      if len(sys.argv) > 1:
 73          analizar_cadena(sys.argv[1])
 74      else:
 75          print("Escribí una cadena (Enter solo = cadena vacía) o 'salir' para terminar.")
 76          try:
 77              while (entrada := input("\nCadena MiniHTML > ").strip()).lower() != "salir":
 78                  analizar_cadena(entrada)
 79          except (KeyboardInterrupt, EOFError):
 80              pass
```

- **67:** une los pasos de la traza con `⊢`.
- **72 y 73:** si hay un argumento, analiza esa cadena.
- **77:** `:=` guarda lo que se escribió y a la vez lo compara con `salir`.
- **79:** Ctrl+C termina el programa sin mostrar un error.

| Comando | Qué hace |
|---|---|
| `python3 src/parser.py` | Abre el modo interactivo, el de la defensa |
| `python3 src/parser.py "<p> TEXTO </p>"` | Analiza una cadena |
| `python3 src/parser.py ""` | Analiza la cadena vacía |
| `python3 -m unittest tests/test_parser.py` | Corre los 12 tests, desde la carpeta raíz |

Las comillas son obligatorias: sin ellas, la terminal toma `<` y `>` como redirecciones. **En el modo interactivo, Enter sin escribir nada analiza la cadena vacía.**

---

## 4. Seguir una ejecución a mano

Hacé esto en papel antes de correrlo. Salida real de `<p> TEXTO <b> TEXTO </b> </p>`:

```
Tokens: ['<p>', 'TEXTO', '<b>', 'TEXTO', '</b>', '</p>']
(q0, <p> TEXTO <b> TEXTO </b> </p>, Z0)
⊢ (q0, TEXTO <b> TEXTO </b> </p>, P Z0)
⊢ (q0, <b> TEXTO </b> </p>, P Z0)
⊢ (q0, TEXTO </b> </p>, B P Z0)
⊢ (q0, </b> </p>, B P Z0)
⊢ (q0, </p>, P Z0)
⊢ (q0, λ, Z0)
⊢ (qf, λ, Z0)
ACEPTADA. Cadena válida (w ∈ L(M)).
```

Las variables por dentro:

| `i` | `token` | `tope` | Rama | `pila` después | Regla |
|---|---|---|---|---|---|
| - | - | - | Inicio | `['Z0']` | - |
| 0 | `<p>` | `Z0` | 45 | `['Z0', 'P']` | 4 |
| 1 | `TEXTO` | `P` | 43 | `['Z0', 'P']` | 1 |
| 2 | `<b>` | `P` | 45 | `['Z0', 'P', 'B']` | 2 |
| 3 | `TEXTO` | `B` | 43 | `['Z0', 'P', 'B']` | 1 |
| 4 | `</b>` | `B` | 49 | `['Z0', 'P']` | 5 |
| 5 | `</p>` | `P` | 49 | `['Z0']` | 7 |
| Fin | - | - | 59 | `['Z0']`, estado `qf` | 8 |

**Ojo con el orden:** la lista de Python tiene el tope a la derecha y la traza lo muestra a la izquierda.

**Dónde corta cada error:**

| Cadena | Línea | Mensaje |
|---|---|---|
| `<p> <b> TEXTO </p> </b>` | 53 | `se leyó '</p>' con B en el tope` |
| `<p> TEXTO </p> </b>` | 51 | `se cerró '</b>' sin apertura previa` |
| `<p> <b> TEXTO </b>` | 58 | `etiquetas sin cerrar: <p>` |
| `<u> TEXTO </u>` | 47 | `'<u>' no pertenece a Σ` |
| `<p> TEXTO <b </p>` | 47 | `'<b' no pertenece a Σ` |

### La relación con G

La profe puede preguntar cómo se relaciona el código con la gramática, aunque G no esté programada:

| Gramática G | Autómata M | Código |
|---|---|---|
| Terminales Σ | Alfabeto de entrada | Lo que devuelve `tokenizar` |
| `S → E S` | Lecturas sucesivas con la pila a la misma altura | Vueltas del `for` |
| `S → λ` | Se vuelve al símbolo contenedor o a Z0 | Sale del `for`, o el cierre desapila |
| `E → TEXTO` | Regla 1 | Línea 43 |
| Apertura de `E → <x> S </x>` | Reglas 2 a 4 | Línea 45 |
| La S del medio | La pila crece | Tokens que se leen hasta el cierre |
| Cierre de `E → <x> S </x>` | Reglas 5 a 7 | Líneas 48 y 49 |
| Ninguna regla genera un cruce | δ vacía | Línea 53 |
| λ ∈ L(G) | Regla 8 | Línea 59 |

---

## 5. Cómo pensar cualquier cambio

### 5.1 Las tres preguntas

**1. ¿Cambia cómo se lee el texto, sin cambiar qué estructuras son válidas?**
Es **léxico**: se toca `tokenizar`. Σ, G y M no cambian. Ejemplos: atributos, mayúsculas, comentarios.

**2. ¿Hay un símbolo nuevo?**
- ¿Se abre y se cierra? Una entrada en `ETIQUETAS`.
- ¿Va solo y no tiene cierre? Va en la condición de la línea 42.

**3. ¿Es una regla sobre qué puede ir dónde?**
Es una **restricción**. Agregás un `if` con un `return False, "mensaje", traza` en el lugar donde se detecta:

| Se detecta... | Dónde va el `if` |
|---|---|
| Al abrir una etiqueta | Antes de la línea 45 |
| Al leer texto | En la línea 43, en lugar de `pass` |
| Con cualquier token | Debajo de la línea 41 |
| Al cerrar | Antes de la línea 49 |
| Al terminar la entrada | Antes de la línea 59 |
| Antes de empezar | Antes de la línea 40 |

### 5.2 Qué información tenés

| Lo que necesito saber | Cómo se escribe |
|---|---|
| El token actual | `token` |
| Se está abriendo `<p>` | `token == "<p>"` |
| Lo último abierto es `<p>` | `tope == "P"` |
| No hay nada abierto | `tope == "Z0"` |
| Hay un `<p>` abierto en cualquier nivel | `"P" in pila` |
| Profundidad actual | `len(pila) - 1` |
| Es el primer token | `i == 0` |
| Token anterior | `tokens[i - 1]`, con `i > 0` |
| Lista completa | `tokens` |

**Los símbolos de pila van en mayúscula (`"P"`) y los tokens llevan los signos (`"<p>"`).** Confundirlos es el error más común.

### 5.3 Lo que tenés que decir en voz alta

1. **Σ:** "¿aparece un símbolo nuevo?"
2. **G:** "¿qué producción agrego o cambio?"
3. **M:** "¿qué transición agrego o saco? ¿Alcanza con el tope, o necesito otro estado?"
4. **Código:** "el cambio va en esta rama".
5. **Prueba:** una cadena válida, una inválida y los tests.

### 5.4 Si falla un test

No siempre es un error. **Si cambiaste el lenguaje, un test que afirmaba lo contrario tiene que fallar.** Explicalo y actualizá ese test.

### 5.5 Si el pedido es ambiguo

Preguntar suma puntos:

| Pedido | Preguntá |
|---|---|
| "Que `<p>` no vaya dentro de `<p>`" | ¿Directamente adentro, o en cualquier nivel? |
| "Que no haya texto suelto" | ¿Solo texto, o también `<b>` e `<i>` afuera de un `<p>`? |
| "Una etiqueta nueva" | ¿Tiene cierre? ¿Puede contener cosas? |
| "Que los números sean un token" | ¿`20` solo, o también `20años`? |

---

## 6. Recetario de cambios

**"Tests" dice cuáles fallan y son esperables.**

### A. Etiquetas

#### A1. Agregar una etiqueta común: `<u>` ⭐ la más probable

**Σ:** `<u>` y `</u>`. **G:** `E → <u> S </u>`. **M:** U en Γ, `δ(q0, <u>, X) = (q0, U X)` y `δ(q0, </u>, U) = (q0, λ)`.

```python
# línea 13
ETIQUETAS = {"b": "B", "i": "I", "p": "P", "u": "U"}
```

**Probar:** `<p> <u> TEXTO </u> </p>` es válida; `<u> </p>` no. **Tests:** no falla ninguno.

#### A2. Nombre con números: `<h1>`

```python
# línea 13
ETIQUETAS = {"b": "B", "i": "I", "p": "P", "h1": "H1"}
```

**Tests:** no falla ninguno.

**Trampa del símbolo:** usá como símbolo el nombre en mayúscula. Con `"b": "N"` todo valida igual, pero el mensaje dice `etiquetas sin cerrar: <n>`, porque la línea 57 arma el nombre desde el símbolo.

#### A3. Quitar una etiqueta: `<i>`

```python
# línea 13
ETIQUETAS = {"b": "B", "p": "P"}
```

**Tests:** fallan `test_cadena_beta`, `test_cadena_gamma` y `test_etiquetas_sin_cerrar`, porque usan `<i>`.

### B. Símbolos que no tocan la pila

#### B1. Etiqueta autocerrada: `<br>` ⭐

No tiene cierre, así que **se comporta como TEXTO**. **Σ:** `<br>`. **G:** `E → <br>`. **M:** `δ(q0, <br>, X) = (q0, X)`.

```python
# debajo de ETIQUETAS (línea 13). Si no piden <br/>, dejá solo "<br>"
VACIAS = {"<br>", "<br/>"}
```

```python
# línea 42
if token == "TEXTO" or token in VACIAS:
```

**Probar:** `<p> TEXTO <br> TEXTO </p>` y `<br>` son válidas; `<p> </br> </p>` da error léxico. **Tests:** no falla ninguno.

#### B2. Token nuevo que no es etiqueta: `NUM` ⭐

**Σ:** `NUM`. **G:** `E → NUM`. **M:** `δ(q0, NUM, X) = (q0, X)`.

```python
# línea 26
tokens.append("NUM" if trozo.isdigit() else "TEXTO")
```

```python
# línea 42
if token == "TEXTO" or token == "NUM":
```

**Probar:** `<p> Tengo 20 anios </p>` da `<p>`, `TEXTO`, `NUM`, `TEXTO`, `</p>`. **Tests:** no falla ninguno.

### C. Restricciones al abrir una etiqueta

**El molde, que sirve para cualquier restricción de este tipo:**

```python
# antes de pila.append (línea 45), con la misma sangría
if CONDICION:
    return False, "Error sintáctico: ...", traza
```

#### C1. `<p>` directamente dentro de `<p>` ⭐

**G:** el contenido de `<p>` necesita otra variable:

```
E → TEXTO | <b> S </b> | <i> S </i> | <p> N </p>
N → F N | λ
F → TEXTO | <b> S </b> | <i> S </i>
```

**M:** alcanza con el tope: `δ(q0, <p>, P) = ∅`.

```python
if token == "<p>" and tope == "P":
    return False, "Error sintáctico: no se permite un <p> directamente dentro de otro <p>.", traza
```

**Probar:** `<p> <p> </p> </p>` es inválida; `<p> <b> <p> </p> </b> </p>` y `<p> </p> <p> </p>` son válidas. **Tests:** no falla ninguno.

#### C2. `<p>` dentro de `<p>` en cualquier nivel

**G:** una rama entera que no pueda generar `<p>`:

```
E → TEXTO | <b> S </b> | <i> S </i> | <p> T </p>
T → F T | λ
F → TEXTO | <b> T </b> | <i> T </i>
```

**M:** **el tope ya no alcanza**, porque en `<p> <b> <p>` el tope es B. Hace falta un estado q1 que recuerde que hay un `<p>` abierto, y `δ(q1, <p>, X) = ∅`. Los estados también son memoria, pero finita.

```python
if token == "<p>" and "P" in pila:
    return False, "Error sintáctico: no se permite un <p> dentro de otro <p>.", traza
```

**Aclaralo si te preguntan:** `"P" in pila` mira toda la pila, y un autómata real solo ve el tope. Es un atajo con el mismo efecto que el estado q1.

**Probar:** `<p> <b> <p> </p> </b> </p>` es inválida; `<b> <p> </p> </b>` es válida. **Tests:** no falla ninguno.

#### C3. `<i>` solo puede contener texto

**G:** `E → ... | <i> T </i>`, con `T → TEXTO T | λ`. **M:** `δ(q0, <x>, I) = ∅` para toda apertura.

```python
if tope == "I":
    return False, "Error sintáctico: <i> solo puede contener texto.", traza
```

**Probar:** `<i> <b> TEXTO </b> </i>` es inválida; `<b> <i> TEXTO </i> </b>` es válida. **Tests:** falla `test_etiquetas_sin_cerrar`, porque anida `<b>` dentro de `<i>`.

#### C4. `<b>` solo puede ir dentro de un `<p>`

**G:** afuera de un párrafo no se genera `<b>`:

```
S → E S | λ
E → TEXTO | <i> S </i> | <p> T </p>
T → F T | λ
F → TEXTO | <b> T </b> | <i> T </i> | <p> T </p>
```

**M:** hace falta saber si hay un P en cualquier nivel, y el tope no alcanza.

```python
if token == "<b>" and "P" not in pila:
    return False, "Error sintáctico: <b> solo puede ir dentro de un <p>.", traza
```

**Probar:** `<p> <i> <b> TEXTO </b> </i> </p>` es válida; `<b> TEXTO </b>` no. **Tests:** no falla ninguno.

#### C5. `<p>` no puede ir directamente dentro de `<b>` ni de `<i>`

**G:** el contenido de `<b>` y de `<i>` usa una variable sin `<p>` directo:

```
E → TEXTO | <b> N </b> | <i> N </i> | <p> S </p>
N → F N | λ
F → TEXTO | <b> N </b> | <i> N </i>
```

**M:** `δ(q0, <p>, B) = δ(q0, <p>, I) = ∅`.

```python
if token == "<p>" and tope in ("B", "I"):
    return False, "Error sintáctico: <p> no puede ir directamente dentro de <b> ni de <i>.", traza
```

**Probar:** `<b> <p> </p> </b>` es inválida; `<p> <p> </p> </p>` es válida. **Tests:** no falla ninguno.

#### C6. Profundidad máxima de 3 niveles

**G:** una familia de variables por nivel: `S₁`, `S₂`, `S₃`. **M:** se bloquea el apilado con 3 símbolos arriba de Z0.

```python
# debajo de ETIQUETAS (línea 13)
MAX_PROFUNDIDAD = 3
```

```python
if len(pila) - 1 >= MAX_PROFUNDIDAD:
    return False, "Error sintáctico: se superó la profundidad máxima.", traza
```

**Probar:** `<p><b><i>TEXTO</i></b></p>` es válida; `<p><b><i><p></p></i></b></p>` no. **Tests:** no falla ninguno.

**Decilo sin que te lo pregunten:** con la profundidad acotada, el lenguaje **pasa a ser regular**. Las combinaciones de etiquetas abiertas son finitas (1 + 3 + 9 + 27 = 40), así que alcanza un autómata finito. La pila hacía falta porque no había límite.

### D. Restricciones según la posición

#### D1. Todo debe estar dentro de un `<p>`

**G:** nuevo símbolo inicial: `D → <p> S </p> D | λ`. **M:** con Z0 en el tope solo se puede abrir `<p>`.

```python
# debajo de tope = pila[-1] (línea 41)
if tope == "Z0" and token != "<p>":
    return False, "Error sintáctico: todo el contenido debe estar dentro de un <p>.", traza
```

**Probar:** `<p> TEXTO </p>` es válida; `TEXTO` y `<b> TEXTO </b>` no. **Tests:** fallan `test_cadena_gamma`, `test_texto_plano`, `test_cierre_sin_apertura` y `test_etiquetas_mal_formadas`. **γ deja de ser válida**, porque termina con un `<i>` afuera del `<p>`.

#### D2. No puede haber texto suelto

Se permiten `<b>` e `<i>` afuera. **G:** `D → F D | λ`, con `F → <b> S </b> | <i> S </i> | <p> S </p>`. **M:** `δ(q0, TEXTO, Z0) = ∅`.

```python
# línea 43: reemplazá pass
if tope == "Z0":
    return False, "Error sintáctico: no puede haber texto suelto.", traza
```

**Probar:** `<b> TEXTO </b>` es válida; `TEXTO` y `<p> </p> TEXTO` no. **Tests:** fallan `test_texto_plano` y `test_etiquetas_mal_formadas`.

#### D3. Un solo elemento raíz

**G:** nuevo símbolo inicial: `D → E | λ`. **M:** un estado nuevo para "ya terminó el primer elemento", desde el cual solo se puede aplicar la regla 8.

```python
# debajo de tope = pila[-1] (línea 41)
if tope == "Z0" and i > 0:
    return False, "Error sintáctico: el documento debe tener un solo elemento raíz.", traza
```

**Probar:** la cadena vacía, `TEXTO` y `<p> <b> </b> <i> </i> </p>` son válidas; `<p> </p> <p> </p>` y `TEXTO TEXTO` no. **Tests:** fallan `test_cadena_gamma`, `test_cierre_sin_apertura` y `test_etiquetas_mal_formadas`.

### E. Al cerrar, al empezar y al terminar

#### E1. Sin etiquetas vacías, como `<p></p>`

**G:** `E → <b> E S </b> | <i> E S </i> | <p> E S </p> | TEXTO`. **M:** un estado "recién abrí", q1: las aperturas llevan a q1, TEXTO lleva a q0 y los cierres solo se leen desde q0.

```python
# antes de pila.pop() (línea 49)
if i > 0 and tokens[i - 1] == "<" + token[2:]:
    return False, "Error sintáctico: la etiqueta no puede estar vacía.", traza
```

`"<" + token[2:]` convierte `</p>` en `<p>`, para compararlo con el token anterior.

**Probar:** `<p></p>` y `<p> <b></b> </p>` son inválidas; `<p> TEXTO </p>` y la cadena vacía son válidas. **Tests:** no falla ninguno.

#### E2. Documento no vacío

**G:** nuevo inicial `D → E S`. **M:** un estado más, para que la regla 8 no se pueda aplicar sin haber leído algo.

```python
# antes del for (línea 40)
if not tokens:
    return False, "Error sintáctico: el documento no puede estar vacío.", traza
```

**Tests:** falla `test_cadena_vacia`.

#### E3. Aceptar por pila vacía

**G no cambia. M:** la regla 8 pasa a ser `δ(q0, λ, Z0) = (q0, λ)`. El lenguaje reconocido es el mismo.

```python
# línea 59: reemplazala por estas dos
pila.pop()  # regla 8: δ(q0, λ, Z0) = (q0, λ)
traza.append(configuracion("q0", [], pila))
```

La traza termina en `(q0, λ, )`. **Tests:** falla `test_traza`, que espera ver `qf`.

### F. Cambios solo léxicos

Σ, G y M **no cambian**. Hacé esa observación en voz alta. Se tocan solo las líneas de `tokenizar`.

#### F1. Atributos: `<p class="x">`

```python
# línea 24
tokens.append(re.sub(r"\s+[^<>]*>$", ">", trozo.strip()).lower().replace("\\", "/"))
```

`re.sub` borra lo que hay desde el primer espacio hasta el `>`.

**Probar:** `<p class="x"> TEXTO </p>` es válida; `< b >` y `<b` siguen siendo errores. **Tests:** falla `test_etiquetas_mal_formadas`, que usaba `<p class=x>` como ejemplo: sacalo de la lista.

#### F2. Distinguir mayúsculas

```python
# línea 24: sacá .lower()
tokens.append(trozo.strip().replace("\\", "/"))
```

`<P> TEXTO </P>` pasa a ser error léxico. **Tests:** falla `test_html_real`.

#### F3. Un solo TEXTO por fragmento

Dos cambios, para que `Hola mundo` sea un solo token:

```python
# línea 22: el patrón toma todo hasta el próximo <
for trozo in re.findall(r"<[^<>]*>?|[^<]+", cadena):
```

```python
# línea 25: reemplazá el else
elif trozo.strip():
```

El `elif trozo.strip()` evita que un trozo de puros espacios cuente como TEXTO. **Tests:** no falla ninguno. **Aclaralo:** la clasificación no cambia, pero `TEXTO TEXTO` pasa a ser un solo token, así que la traza de γ queda más corta que la del informe.

#### F4. No aceptar `<\p>` como cierre

```python
# línea 24: sacá el replace
tokens.append(trozo.strip().lower())
```

**Tests:** falla `test_html_real`.

#### F5. Ignorar comentarios: `<!-- nota -->`

```python
# antes de la línea 23
if trozo.startswith("<!--"):
    continue
```

`continue` pasa directamente al próximo trozo. **Limitación:** el comentario no puede contener `<` ni `>`. **Tests:** no falla ninguno.

### G. Cambios en la salida

G y M no cambian.

#### G1. Mensaje con la posición del error

```python
# línea 51
return False, f"Error sintáctico en el token {i + 1}: se cerró '{token}' sin apertura previa.", traza
```

Sumá 1 porque `i` empieza en 0. Si cambiás palabras que los tests buscan con `assertIn`, como "léxico", actualizá el test.

#### G2. Mostrar la transición en la traza

```python
# línea 54
traza.append(configuracion("q0", tokens[i + 1:], pila) + f"  δ(q0, {token}, {tope})")
```

**Tests:** falla `test_traza`, que compara cada línea exacta.

#### G3. Informar la profundidad máxima

```python
# debajo de la línea 37
maxima = 0
```

```python
# debajo de pila.append (línea 45)
maxima = max(maxima, len(pila) - 1)
```

```python
# línea 60
return True, f"Cadena válida (w ∈ L(M)). Profundidad máxima: {maxima}.", traza
```

#### G4. Mostrar la cantidad de tokens

```python
# debajo de la línea 66
print(f"Cantidad de tokens: {len(tokens)}")
```

#### G5. Agregar un test

Adentro de la clase `TestMiniHTML`, en `tests/test_parser.py`:

```python
def test_mi_caso(self):
    self.assertTrue(es_valida("<p> <u> TEXTO </u> </p>"))
```

Para una cadena inválida, usá `assertFalse`. Este ejemplo requiere la receta A1.

### Resumen

| Receta | Pedido | Lugar | Tests que fallan |
|---|---|---|---|
| A1, A2 | `<u>`, `<h1>` | `ETIQUETAS` | Ninguno |
| A3 | Quitar `<i>` | `ETIQUETAS` | 3 tests |
| B1 | `<br>` | Línea 42 | Ninguno |
| B2 | `NUM` | Líneas 26 y 42 | Ninguno |
| C1 | `<p>` directo en `<p>` | Antes de 45 | Ninguno |
| C2 | `<p>` en cualquier nivel | Antes de 45 | Ninguno |
| C3 | `<i>` solo texto | Antes de 45 | `test_etiquetas_sin_cerrar` |
| C4, C5, C6 | Otras al abrir | Antes de 45 | Ninguno |
| D1 | Todo dentro de `<p>` | Debajo de 41 | 4 tests |
| D2 | Sin texto suelto | Línea 43 | 2 tests |
| D3 | Una sola raíz | Debajo de 41 | 3 tests |
| E1 | Sin etiquetas vacías | Antes de 49 | Ninguno |
| E2 | Documento no vacío | Antes de 40 | `test_cadena_vacia` |
| E3 | Pila vacía | Línea 59 | `test_traza` |
| F1 | Atributos | Línea 24 | `test_etiquetas_mal_formadas` |
| F2, F4 | Mayúsculas, sin `<\p>` | Línea 24 | `test_html_real` |
| F3, F5 | Fragmentos, comentarios | `tokenizar` | Ninguno |
| G1, G3, G4 | Mensajes y datos | Salida | Ninguno |
| G2 | Transición en la traza | Línea 54 | `test_traza` |

---

## 7. Cuando algo sale mal

Leé siempre **la última línea** del error y el número de línea que indica.

| Lo que ves | Causa probable | Arreglo |
|---|---|---|
| `NameError: name 'APERTURA' is not defined` | Nombre mal escrito; Python suele sugerir el correcto | Corregí el nombre |
| `NameError` por `marcador`, `bloqueo` o `abiertas` | Es de versiones anteriores del código | Usá `return False, "...", traza` |
| `ValueError: not enough values to unpack` | Un `return` de `simular` no tiene los 3 valores | Agregá `, traza` |
| `IndentationError` | La sangría no coincide | Alineá con las líneas vecinas: se usan 4 espacios por nivel |
| `IndexError: list index out of range` | Sacaste Z0 de la pila | Revisá la comparación antes del `pila.pop()` |
| `NameError` por `i` o `token` | Usaste esa variable afuera del `for` | Revisá dónde pusiste el `if` |
| La regla nueva no hace nada | El `if` está en otra rama, o `"p"` y `"P"` están al revés | Revisá la tabla 5.2 |

---

## 8. Ejercicios

### 8.1 ¿Qué pasa si...?

Respondé antes de abrir la respuesta. Después probalo: todas las respuestas son resultados reales.

<details>
<summary>1. Reemplazo la línea 48 por <code>elif True:</code> y corro <code>&lt;p&gt; &lt;b&gt; &lt;/p&gt; &lt;/b&gt;</code></summary>

**Acepta el cruce**, porque desapila sin comparar. Esa comparación es lo que impone el orden LIFO. Y con `</p> TEXTO` da `IndexError`, porque saca Z0 y la pila queda vacía.
</details>

<details>
<summary>2. Reemplazo <code>if pila != ["Z0"]:</code> por <code>if False:</code> y corro <code>&lt;p&gt;</code></summary>

Acepta, y termina en `(qf, λ, P Z0)`. Es incorrecto: la regla 8 exige Z0 en el tope.
</details>

<details>
<summary>3. Cambio <code>pila[1:]</code> por <code>pila</code> en la línea 57 y corro <code>&lt;p&gt;</code></summary>

Sigue rechazando, pero el mensaje dice `etiquetas sin cerrar: <p>, <z0>`.
</details>

<details>
<summary>4. Reemplazo la línea 45 por <code>pass</code> y corro <code>&lt;p&gt; &lt;/p&gt;</code></summary>

Rechaza con `se cerró '</p>' sin apertura previa`, porque nunca apiló.
</details>

<details>
<summary>5. Reemplazo la línea 49 por <code>pass</code> y corro <code>&lt;p&gt; &lt;/p&gt;</code></summary>

Rechaza con `etiquetas sin cerrar: <p>`: comparó bien, pero nunca desapiló.
</details>

<details>
<summary>6. Borro la línea 54 y corro <code>&lt;p&gt; &lt;/p&gt;</code></summary>

El resultado no cambia, pero la traza pierde los pasos intermedios. La traza solo muestra: no decide nada. Falla `test_traza`.
</details>

<details>
<summary>7. Saco <code>reversed</code> de la línea 32</summary>

El resultado no cambia, pero la traza muestra el tope a la derecha. Falla `test_traza`.
</details>

### 8.2 Pedidos nuevos, sin receta

Usá las preguntas de 5.1 y la tabla de 5.2. Probá con una cadena válida y una inválida.

<details>
<summary>1. <code>&lt;b&gt;</code> no puede ir dentro de <code>&lt;b&gt;</code>, en ningún nivel</summary>

```python
# antes de pila.append
if token == "<b>" and "B" in pila:
    return False, "Error sintáctico: no se permite un <b> dentro de otro <b>.", traza
```
</details>

<details>
<summary>2. Dentro de <code>&lt;b&gt;</code> no puede abrirse ninguna otra etiqueta</summary>

Es como C3, cambiando I por B.

```python
# antes de pila.append
if tope == "B":
    return False, "Error sintáctico: <b> solo puede contener texto.", traza
```
</details>

<details>
<summary>3. El documento tiene que empezar con <code>&lt;p&gt;</code></summary>

La cadena vacía sigue siendo válida.

```python
# debajo de tope = pila[-1]
if i == 0 and token != "<p>":
    return False, "Error sintáctico: el documento debe empezar con <p>.", traza
```

**Tests:** fallan `test_texto_plano` y `test_etiquetas_mal_formadas`.
</details>

<details>
<summary>4. Agregar <code>&lt;a&gt;</code> y <code>&lt;hr&gt;</code>, donde <code>&lt;hr&gt;</code> no tiene cierre</summary>

Combina A1 y B1: `"a": "A"` en `ETIQUETAS`, `VACIAS = {"<hr>"}` y la condición de la línea 42.
</details>

<details>
<summary>5. Que <code>&lt;i&gt;</code> no pueda ser lo primero dentro de un <code>&lt;p&gt;</code></summary>

```python
# antes de pila.append
if token == "<i>" and i > 0 and tokens[i - 1] == "<p>":
    return False, "Error sintáctico: <i> no puede ser lo primero dentro de <p>.", traza
```

**Tests:** falla `test_etiquetas_sin_cerrar`.
</details>

### 8.3 Simulacro

Con un compañero que elija pedidos al azar de la sección 6, y con 5 minutos por pedido:

1. Repetí el pedido y preguntá lo que sea ambiguo.
2. Decí en voz alta qué cambia en Σ, en G y en M.
3. Hacé el cambio **sin mirar la guía**.
4. Probá una cadena válida, una inválida y los tests.
5. Explicá cualquier test que falle.
6. Restaurá el código.

**Estás listo cuando** hacés bien 5 pedidos seguidos, incluido al menos uno de la sección 8.2.

---

## 9. Durante la defensa

**Antes de empezar:**

- [ ] `parser.py` abierto en el editor y una terminal en la carpeta raíz del repo.
- [ ] `python3 -m unittest tests/test_parser.py` pasa los 12 tests.
- [ ] Sin cambios de práctica en el código.

**Si te trabás:**

1. **Volvé a las tres preguntas** de la sección 5. Pensar en voz alta también se evalúa.
2. **Si no te sale el código, escribí la producción de G y la transición de M.** Eso demuestra que entendiste el modelo.
3. **Si aparece un error de Python, leé la última línea en voz alta** y buscá la causa en la sección 7. Nadie espera que escribas sin errores en vivo.

**El machete:**

```
LÍNEAS   ETIQUETAS 13 · tokenizar 19 · simular 35 · analizar_cadena 63
δ        TEXTO 42 · apila 45 · léxico 47 · compara 48 · desapila 49
         sin apertura 51 · cruce 53 · sin cerrar 58 · regla 8: 59

ABRIR    if antes de 45 → return False, "...", traza
TODO     if debajo de 41
CERRAR   if antes de 49
SIN PILA Agregar a la condición de la línea 42
LÉXICO   Solo tokenizar: Σ, G y M no cambian

DATOS    token=="<p>" · tope=="P" · tope=="Z0" · "P" in pila
         len(pila)-1 · i==0 · tokens[i-1]
```
