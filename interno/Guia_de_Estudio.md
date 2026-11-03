# Guía de estudio para la defensa — MiniHTML Parser

Esta guía alcanza por sí sola para preparar el oral: explica la teoría desde cero, la gramática, el autómata, **todo el código** y **cómo hacer las modificaciones en vivo**. Usa la misma numeración de reglas y transiciones que el [informe](../entregables/Informe%20miniparser-html.pdf), porque es lo que la profe va a tener enfrente.

> **Material interno: no se entrega.** Todas las modificaciones de la sección 8 y las cadenas de la sección 7 se ejecutaron sobre el código real del proyecto. Las líneas citadas son las de [src/parser.py](../src/parser.py) sin modificar.

## Índice

1. [Qué te van a evaluar](#1-qué-te-van-a-evaluar)
2. [El proyecto en 1 minuto](#2-el-proyecto-en-1-minuto)
3. [Teoría desde cero](#3-teoría-desde-cero)
4. [La gramática G](#4-la-gramática-g)
5. [El autómata a pila M](#5-el-autómata-a-pila-m)
6. [El código, parte por parte](#6-el-código-parte-por-parte)
7. [La demo en vivo](#7-la-demo-en-vivo)
8. [Modificaciones en vivo](#8-modificaciones-en-vivo)
9. [Preguntas probables](#9-preguntas-probables)
10. [Machete y checklist](#10-machete-y-checklist)

---

## 1. Qué te van a evaluar

La entrevista vale el **30 %** de la nota, pero también defiende el otro 70 %. Según la consigna, hay tres pruebas y participan **todos los integrantes**:

| Prueba | Qué va a pasar | Dónde prepararla |
|---|---|---|
| **Testeo en vivo** | La profe escribe cadenas válidas e inválidas. El programa tiene que clasificarlas y explicar el error. | Sección 7 |
| **Modificación en vivo** | Pide un cambio menor en el código: una etiqueta nueva, una regla de producción o una validación. | Sección 8 |
| **Preguntas individuales** | Sobre la relación entre G, M y el código. | Secciones 3 a 6 y 9 |

### Plan de estudio (unas 6 horas)

| Etapa | Qué hacer | Tiempo | Cómo sabés que terminaste |
|---|---|---|---|
| 1 | Correr el programa (sección 7.1) y leer las secciones 2 y 3 | 1 h | Explicás sin leer por qué un autómata finito no alcanza. |
| 2 | Sección 4 | 45 min | Hacés en papel el árbol y la derivación de α. |
| 3 | Sección 5 | 1 h | Hacés en papel la traza de γ y la de una cadena inválida. |
| 4 | Sección 6, con `parser.py` abierto al lado | 1 h 30 | Señalás la línea exacta del PUSH, del POP y de cada error. |
| 5 | Sección 8: hacer de verdad las modificaciones | 1 h 30 | Hacés las 4 más probables sin mirar. |
| 6 | Sección 9 en voz alta, de a dos | 30 min | Respondés sin leer. |

---

## 2. El proyecto en 1 minuto

**El problema.** En HTML las etiquetas deben estar bien anidadas: `<p><b>hola</b></p>` está bien, y `<p><b>hola</p></b>` está mal porque cierra `<p>` antes que `<b>`, que fue la última en abrirse.

**MiniHTML** es un HTML reducido con solo 7 símbolos:

```
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
```

Una cadena es válida si toda etiqueta abierta se cierra con una del mismo tipo, en orden **LIFO** (*Last In, First Out*: la última que se abrió es la primera que se cierra). El documento vacío y el texto solo también son válidos.

**Lo que hicimos:**

| Fase | Qué es | En una frase |
|---|---|---|
| 1 | Gramática libre de contexto **G** | Las reglas que **generan** las cadenas válidas. |
| 2 | Autómata a pila **M** | La máquina que **reconoce** las cadenas válidas usando una pila. |
| 3 | Programa en Python | Implementa **G y M** (opciones A y B de la consigna) y comprueba que coinciden. |

**La frase que tenés que poder decir de memoria:**

> MiniHTML no es un lenguaje regular: para saber si las etiquetas cierran bien hay que recordar cuántas y cuáles se abrieron, sin límite, y un autómata finito tiene memoria finita. Por eso lo describimos con una gramática libre de contexto y lo reconocemos con un autómata a pila: la pila es una memoria LIFO, igual que el orden en que se cierran las etiquetas.

---

## 3. Teoría desde cero

### 3.1 Alfabeto, cadena y lenguaje

- **Alfabeto (Σ):** conjunto finito de símbolos. Acá cada símbolo es un *token* entero: `<b>` es **un** símbolo, no tres caracteres.
- **Cadena:** secuencia finita de símbolos. `<p> TEXTO </p>` tiene longitud 3.
- **λ (lambda):** la cadena vacía, de longitud 0.
- **Σ\*:** todas las cadenas posibles con ese alfabeto, válidas o no.
- **Lenguaje (L):** un subconjunto de Σ\*. MiniHTML son las cadenas de Σ\* bien anidadas.
- **w ∈ L:** "la cadena w pertenece al lenguaje". Es exactamente lo que responde el programa.

### 3.2 Dos formas de describir un lenguaje

- **Modelo generativo (gramática):** reglas que producen todas las cadenas válidas. Es G.
- **Modelo reconocedor (autómata):** máquina que lee una cadena y dice sí o no. Es M.

### 3.3 Jerarquía de Chomsky

Clasifica los lenguajes según la memoria que necesita la máquina que los reconoce. Cada tipo contiene a los de las filas de abajo, y los regulares son los más restringidos:

| Tipo | Lenguajes | Gramática | Máquina | Memoria |
|---|---|---|---|---|
| 0 | Recursivamente enumerables | Sin restricciones | Máquina de Turing | Cinta infinita |
| 1 | Sensibles al contexto | Sensible al contexto | Autómata linealmente acotado | Cinta acotada |
| **2** | **Libres de contexto (LIC)** | **Libre de contexto** | **Autómata a pila** | **Pila sin límite** |
| 3 | Regulares | Regular | Autómata finito | Solo los estados |

**MiniHTML es de tipo 2**: no es regular y una pila alcanza.

### 3.4 Por qué un autómata finito no alcanza

Esto lo pide la consigna y está en la sección 2 del informe.

**Intuición (principio del palomar).** Un autómata finito solo recuerda en qué estado está. Si tiene k estados y lee más de k etiquetas `<p>` seguidas, dos cantidades distintas de `<p>` abiertos lo dejan en el **mismo estado**. Desde ahí ya no sabe cuántos cierres faltan, así que acepta alguna cadena mal cerrada o rechaza alguna correcta.

**Demostración (lema de bombeo).** Si L es regular, existe un n tal que toda ω ∈ L con |ω| ≥ n se puede escribir ω = αβγ con |αβ| ≤ n, β ≠ λ y αβⁱγ ∈ L para todo i ≥ 0.

1. Supongamos que MiniHTML es regular, con constante n.
2. Tomamos ω = `<p>`ⁿ `TEXTO` `</p>`ⁿ, que es válida y tiene longitud 2n + 1 ≥ n.
3. Como |αβ| ≤ n, α y β caen dentro de los primeros n símbolos, que son todos `<p>`. Entonces β = `<p>`ˢ con s ≥ 1.
4. Con i = 0 queda `<p>`ⁿ⁻ˢ `TEXTO` `</p>`ⁿ, con más cierres que aperturas: no pertenece al lenguaje.
5. Contradice el lema, así que MiniHTML **no es regular**. ∎

Es el mismo argumento que para aⁿbⁿ y para los paréntesis balanceados.

> **Importante:** esto depende de que la profundidad **no tenga límite**. Si se limita a 3 niveles, el lenguaje pasa a ser regular (ver la modificación 8.11).

### 3.5 Gramáticas

Una gramática es una 4-tupla **G = (V, Σ, S, P)**: variables, terminales, símbolo inicial y producciones.

- **Derivación (⇒):** aplicar una regla reemplazando una variable. `S ⇒* w` significa que de S se llega a w en cero o más pasos.
- **Derivación más a la izquierda:** en cada paso se reemplaza la variable que está más a la izquierda.
- **Árbol de derivación:** la raíz es S, los nodos internos son variables y las hojas son terminales o λ. Leyendo las hojas de izquierda a derecha sale la cadena.
- **Ambigua:** alguna cadena tiene dos árboles distintos (o dos derivaciones más a la izquierda distintas).
- **Regular o libre de contexto:** una regular solo admite reglas como `A → aB`, `A → a` o `A → λ`. Una libre de contexto admite `A → α`, con una sola variable a la izquierda y cualquier cosa a la derecha. "Libre de contexto" significa que A se reemplaza sin importar qué tiene alrededor.

La regla que una gramática regular **no** puede tener es del tipo `S → a S b`, con la variable en el medio: eso es lo que empareja aperturas con cierres. `E → <b> S </b>` es justamente de ese tipo.

### 3.6 Autómatas a pila

Es un autómata finito **más una pila**. Lee la entrada de izquierda a derecha y de la pila solo ve el **tope**. Es una 7-tupla, en el orden de la cátedra:

**M = (Σ, Γ, Q, q₀, Z₀, F, Δ)**

| Símbolo | Qué es |
|---|---|
| Σ | alfabeto de entrada |
| Γ | alfabeto de la pila |
| Q | estados |
| q₀ | estado inicial |
| Z₀ | símbolo que está en el fondo de la pila al empezar |
| F | estados finales |
| Δ | función de transición |

> La consigna escribe `(Q, Σ, Γ, δ, q₀, Z₀, F)`. Son los mismos 7 componentes en otro orden.

**Cómo se lee una transición:** `Δ(q, a, z) = (q', γ)` significa "en el estado q, leyendo a y con z en el tope, paso a q' y **reemplazo z por γ**".

| γ | Operación | Ejemplo nuestro |
|---|---|---|
| `Y z` | **PUSH**: apila Y | leer `<b>` apila B |
| `z` | **sin cambios** | leer TEXTO |
| `λ` | **POP**: saca el tope | leer `</b>` con B en el tope |

- **Bloqueo:** si no hay transición (Δ = ∅), la máquina se detiene y rechaza.
- **Transición λ:** cambia de estado **sin leer** nada de la entrada.
- **Determinista (AFPD):** a lo sumo una opción en cada situación y sin transiciones λ.
- **No determinista (AFPN-λ):** puede tener varias opciones, incluidas transiciones λ. Acepta si **alguna** rama acepta.
- A diferencia de los autómatas finitos, acá **no** son equivalentes: hay lenguajes libres de contexto que solo se reconocen con no determinismo (por ejemplo, los palíndromos pares).
- **Configuración instantánea:** la "foto" **(q, ω, γ)**: estado, lo que falta leer y la pila con el **tope a la izquierda**. Un paso se escribe con ⊢.
- **Aceptación por estado final, L(M):** termina de leer en un estado de F. **Es la que usamos.**
- **Aceptación por pila vacía, N(M):** termina de leer con la pila vacía. Ambos criterios reconocen la misma clase de lenguajes.
- **Teorema de equivalencia:** un lenguaje es libre de contexto **si y solo si** lo reconoce un autómata a pila.

---

## 4. La gramática G

```
G = (V, Σ, S, P)
V = { S, E }
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
Símbolo inicial: S
```

| N° | Producción | Significado |
|:-:|---|---|
| 1 | `S → E S` | Una secuencia es un elemento seguido de otra secuencia. |
| 2 | `S → λ` | Una secuencia puede ser vacía. |
| 3 | `E → TEXTO` | Un elemento puede ser texto. |
| 4 | `E → <b> S </b>` | Bloque en negrita con contenido S. |
| 5 | `E → <i> S </i>` | Bloque en cursiva con contenido S. |
| 6 | `E → <p> S </p>` | Párrafo con contenido S. |

- **S (secuencia):** cero o más elementos uno al lado del otro. Sirve para el documento y para el contenido de una etiqueta.
- **E (elemento):** una sola cosa, un texto o un bloque.

### Decisiones que tenés que saber justificar

- **Garantiza LIFO** porque en las reglas 4 a 6 la apertura y el cierre nacen **en el mismo paso**, con S en el medio. Lo que se derive de esa S queda encerrado, así que no hay forma de generar un cruce como `<p> <b> </p> </b>`.
- **No es ambigua** porque el próximo símbolo decide la regla: si es TEXTO o una apertura, `S → E S` y la regla de E correspondiente; si es un cierre o terminó la cadena, `S → λ`. Hay una sola opción en cada paso, entonces un solo árbol.
- **Hay dos variables** para evitar `S → S S`, que sí es ambigua: tres elementos seguidos se podrían agrupar de dos maneras.
- **`S → λ` existe** para permitir el documento vacío y `<p></p>`, y para cortar la secuencia de hermanos.

### Ejemplo completo: α = `<p> TEXTO <b> TEXTO </b> </p>`

```
S ⇒ E S                                 (1)
  ⇒ <p> S </p> S                        (6)
  ⇒ <p> E S </p> S                      (1)
  ⇒ <p> TEXTO S </p> S                  (3)
  ⇒ <p> TEXTO E S </p> S                (1)
  ⇒ <p> TEXTO <b> S </b> S </p> S       (4)
  ⇒ <p> TEXTO <b> E S </b> S </p> S     (1)
  ⇒ <p> TEXTO <b> TEXTO S </b> S </p> S (3)
  ⇒ <p> TEXTO <b> TEXTO </b> S </p> S   (2)
  ⇒ <p> TEXTO <b> TEXTO </b> </p> S     (2)
  ⇒ <p> TEXTO <b> TEXTO </b> </p>       (2)
```

```
              S
           /     \
          E       S
       /  |  \    |
    <p>   S  </p> λ
        /   \
       E     S
       |    /  \
    TEXTO  E    S
         / | \  |
      <b>  S </b> λ
          / \
         E   S
         |   |
       TEXTO λ
```

**Truco para el oral:** cada `E` con 3 hijos es un par apertura/cierre, y cada `S` que va a λ significa "acá no hay más hermanos". Los árboles de α y β están en [arbol_alfa.png](diagramas/arbol_alfa.png) y [arbol_beta.png](diagramas/arbol_beta.png).

### Ejercicio

Hacé en papel la derivación de `<i> <b> TEXTO </b> </i> TEXTO` y recién después compará:

```
S ⇒ E S                                  (1)
  ⇒ <i> S </i> S                         (5)
  ⇒ <i> E S </i> S                       (1)
  ⇒ <i> <b> S </b> S </i> S              (4)
  ⇒ <i> <b> E S </b> S </i> S            (1)
  ⇒ <i> <b> TEXTO S </b> S </i> S        (3)
  ⇒ <i> <b> TEXTO </b> S </i> S          (2)
  ⇒ <i> <b> TEXTO </b> </i> S            (2)
  ⇒ <i> <b> TEXTO </b> </i> E S          (1)
  ⇒ <i> <b> TEXTO </b> </i> TEXTO S      (3)
  ⇒ <i> <b> TEXTO </b> </i> TEXTO        (2)
```

---

## 5. El autómata a pila M

```
M = (Σ, Γ, Q, q0, Z0, F, Δ)
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
Γ = { Z0, B, I, P }     B = "hay un <b> abierto", y así con los demás
Q = { q0, qf }          q0 inicial: ahí se procesa toda la entrada
F = { qf }              Z0 = marca del fondo de la pila
```

| N° | Estado | Entrada | Tope | Δ(q, a, z) | Operación |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | q0 | TEXTO | X | (q0, X) | Sin cambios |
| 2 | q0 | `<b>` | X | (q0, B X) | Apila B |
| 3 | q0 | `<i>` | X | (q0, I X) | Apila I |
| 4 | q0 | `<p>` | X | (q0, P X) | Apila P |
| 5 | q0 | `</b>` | B | (q0, λ) | Desapila B |
| 6 | q0 | `</i>` | I | (q0, λ) | Desapila I |
| 7 | q0 | `</p>` | P | (q0, λ) | Desapila P |
| 8 | q0 | **λ** | Z0 | (qf, Z0) | Acepta |

X es cualquier símbolo de Γ. Cualquier otra combinación da **Δ = ∅: bloqueo y rechazo**.

**En criollo:** cada vez que abro algo lo anoto arriba de la pila; cada vez que cierro, me fijo que sea lo que está arriba y lo tacho. Si al terminar solo queda Z0, está todo bien.

```
        TEXTO, X / X
        <b>, X / B X     </b>, B / λ
        <i>, X / I X     </i>, I / λ
        <p>, X / P X     </p>, P / λ
           ┌────────┐
           ▼        │
  ──►  ( q0 ) ──────┘
          │
          │  λ, Z0 / Z0
          ▼
       (( qf ))
```

Se lee `entrada, tope / reemplazo`. El diagrama prolijo está en [automata.png](diagramas/automata.png).

### Los tres errores posibles, en términos de M

1. **Cruce:** leer un cierre con otro símbolo en el tope, como `</p>` con B.
2. **Cierre sin apertura:** leer un cierre con Z0 en el tope.
3. **Etiquetas sin cerrar:** se termina la entrada y el tope no es Z0, así que la regla 8 no se puede aplicar.

### Por qué es no determinista

Por la regla 8 y nada más: en q0 con Z0 en el tope hay **dos opciones**, leer el próximo símbolo o saltar a qf sin leer. No causa aceptaciones incorrectas porque qf no tiene transiciones salientes: si salta antes de tiempo, queda con entrada sin leer y esa rama no acepta. La única rama que puede aceptar es la que salta **al final**, y es la que sigue el programa. Por eso el simulador no necesita explorar ramas ni hacer *backtracking*.

### Cómo hacer una traza a mano

Escribí tres columnas: estado, lo que falta leer y la pila con el tope a la izquierda. En cada paso sacá el primer símbolo de la entrada, buscá la regla según ese símbolo y el tope, y aplicala. Al final, si la pila es solo Z0, aplicá la regla 8.

**γ = `<p> TEXTO TEXTO </p> <i> TEXTO </i>`** (la pila vuelve a Z0 en el medio):

```
   (q0, <p> TEXTO TEXTO </p> <i> TEXTO </i>, Z0)   inicial
⊢  (q0, TEXTO TEXTO </p> <i> TEXTO </i>, P Z0)     (4)
⊢  (q0, TEXTO </p> <i> TEXTO </i>, P Z0)           (1)
⊢  (q0, </p> <i> TEXTO </i>, P Z0)                 (1)
⊢  (q0, <i> TEXTO </i>, Z0)                        (7)
⊢  (q0, TEXTO </i>, I Z0)                          (3)
⊢  (q0, </i>, I Z0)                                (1)
⊢  (q0, λ, Z0)                                     (6)
⊢  (qf, λ, Z0)                                     (8)    ACEPTA
```

**Inválida `<p> <b> TEXTO </p> </b>`:**

```
   (q0, <p> <b> TEXTO </p> </b>, Z0)    inicial
⊢  (q0, <b> TEXTO </p> </b>, P Z0)      (4)
⊢  (q0, TEXTO </p> </b>, B P Z0)        (2)
⊢  (q0, </p> </b>, B P Z0)              (1)
   Bloqueo: Δ(q0, </p>, B) = ∅          RECHAZA
```

Las de α y β están en el informe. **Practicalas en papel**: es muy probable que pidan una en el momento.

### La tabla clave: G ↔ M ↔ código

Responde a la pregunta típica de la evaluación. Conviene saberla de memoria:

| Gramática G | Autómata M | Código |
|---|---|---|
| Terminales Σ | Alfabeto de entrada Σ | Lo que devuelve `tokenizar()` |
| `S → E S` (hermanos) | Lecturas en q0 con la pila a la misma altura | El `for` de `simular` / el `while` de `parse_S` |
| `E → TEXTO` | Regla 1 | `if token == "TEXTO"` / `if tok == "TEXTO"` |
| Apertura en `E → <x> S </x>` | PUSH (reglas 2 a 4) | `pila.append(marcador)` / `pos += 1` en `parse_E` |
| La S del medio | La pila crece | Recursión `parse_E → parse_S → parse_E` |
| Cierre en `E → <x> S </x>` | POP si coincide (reglas 5 a 7) | `pila.pop()` / `tokens[pos] != esperado` |
| `S → λ` | Vuelve al símbolo padre o a Z0 | `parse_S` sale del `while` |
| λ ∈ L(G) | `(q0, λ, Z0) ⊢ (qf, λ, Z0)` | Lista de tokens vacía: acepta |
| Ninguna regla genera un cruce | Δ = ∅, bloqueo | `return finalizar(False, msg)` / `raise ValueError` |
| L(G) | L(M) | `Equivalencia L(G) = L(M): VERIFICADA` |

---

## 6. El código, parte por parte

Leé esta sección con [src/parser.py](../src/parser.py) abierto. Todo el programa está en ese archivo y solo usa la biblioteca estándar de Python 3.

```
"<p>Hola <b>mundo</b></p>"
        │  tokenizar()                               análisis léxico
        ▼
['<p>', 'TEXTO', '<b>', 'TEXTO', '</b>', '</p>']
        │
        ├─► AutomataPilaMiniHTML.simular()           opción B: el autómata M
        └─► AnalizadorRecursivoMiniHTML.validar()    opción A: la gramática G
        │
        ▼
ACEPTADA / RECHAZADA + diagnóstico + ¿coinciden?     analizar_cadena()
```

### 6.1 `ETIQUETAS`: la definición del lenguaje (línea 32)

```python
ETIQUETAS: Dict[str, str] = {
    "b": "B",
    "i": "I",
    "p": "P",
}
```

Es un diccionario de **etiqueta a símbolo de pila**. Es la única definición del lenguaje: M y G se arman desde acá. Por eso agregar una etiqueta es una sola línea. `Dict[str, str]` es solo una anotación de tipos, y no cambia lo que hace el programa.

### 6.2 `tokenizar`: el analizador léxico (líneas 44 a 76)

Convierte el texto en la lista de símbolos de Σ. Usa dos expresiones regulares:

```python
PATRON_TOKEN = re.compile(r'<[^<>]*>?|[^<]+')
PATRON_ETIQUETA = re.compile(r'<([/\\]?)([a-zA-Z0-9]+)>')
```

**`PATRON_TOKEN`** corta la entrada en trozos. El `|` significa "o":

| Parte | Significado |
|---|---|
| `<` | un `<` |
| `[^<>]*` | cero o más caracteres que no sean `<` ni `>` |
| `>?` | un `>` optativo: por eso también captura `<b` sin cerrar |
| `[^<]+` | **o** uno o más caracteres que no sean `<`: es el texto |

**`PATRON_ETIQUETA`** comprueba si un trozo es una etiqueta bien escrita:

| Parte | Significado |
|---|---|
| `<` y `>` | los delimitadores |
| `([/\\]?)` | grupo 1: `/` o `\` optativo (admite la notación `<\b>` de la consigna) |
| `([a-zA-Z0-9]+)` | grupo 2: el nombre, con letras y números |

```python
def tokenizar(cadena: str) -> List[str]:
    tokens: List[str] = []

    for coincidencia in PATRON_TOKEN.finditer(cadena):   # recorre cada trozo
        trozo = coincidencia.group().strip()             # le saca los espacios
        if not trozo:
            continue                                     # era solo espacio

        if trozo.startswith("<"):
            etiqueta = PATRON_ETIQUETA.fullmatch(trozo)  # ¿está bien escrita?
            if etiqueta:
                barra = "/" if etiqueta.group(1) else ""
                tokens.append(f"<{barra}{etiqueta.group(2).lower()}>")  # normaliza
            else:
                tokens.append(trozo)                     # mal escrita: queda igual
        else:
            tokens.extend("TEXTO" for _ in trozo.split())  # un TEXTO por palabra

    return tokens
```

(Los comentarios de la derecha son de esta guía.) Tres decisiones para saber explicar:

- **Normaliza:** `<P>` y `<\p>` pasan a `<p>` y `</p>`.
- **No descarta lo mal escrito.** Lo deja pasar tal cual para que después se rechace como error léxico. Si lo tratara como texto, aceptaría cosas como `<b`.
- **El tokenizador no decide si una etiqueta existe.** `<u>` sale como token `<u>`, y quien lo rechaza es el analizador.

Ejemplo de `<p> TEXTO <b </p>`: los trozos son `<p> `, `TEXTO `, `<b ` y `</p>`, y los tokens quedan `['<p>', 'TEXTO', '<b', '</p>']`.

### 6.3 `AutomataPilaMiniHTML`: el autómata M (líneas 83 a 218)

**`__init__` (línea 102)** carga la 7-tupla:

```python
self.gamma: Set[str] = {"Z0"}          # Γ
self.sigma: Set[str] = {"TEXTO"}       # Σ
self.estados: Set[str] = {"q0", "qf"}  # Q
self.q0 = "q0"
self.z0 = "Z0"
self.f: Set[str] = {"qf"}              # F

self.apertura_a_pila: Dict[str, str] = {}  # {"<b>": "B", ...}
self.cierre_a_pila: Dict[str, str] = {}    # {"</b>": "B", ...}
for etiqueta, simbolo in ETIQUETAS.items():
    self.agregar_etiqueta(etiqueta, simbolo)
```

**Dato fino:** las decisiones se toman con `apertura_a_pila` y `cierre_a_pila`, que **son la tabla Δ en forma compacta**. `sigma`, `gamma`, `estados` y `f` documentan la tupla, pero `simular` no los consulta.

**`agregar_etiqueta` (línea 117)** agrega `<tag>` y `</tag>` a Σ, su símbolo a Γ y sus transiciones PUSH y POP.

**`simular` (línea 131)** es el corazón del proyecto:

```python
estado = self.q0
pila = [self.z0]     # el ÚLTIMO elemento de la lista es el tope
traza: List[str] = []
```

Adentro hay tres funciones auxiliares: `configuracion` arma el texto `(q, ω, γ)`, `registrar` agrega un paso a la traza y `finalizar` imprime la traza y devuelve el resultado. Pueden usar `estado`, `pila` y `tokens` porque están definidas adentro de `simular`.

**Cada rama del `for` es un grupo de filas de la tabla Δ:**

```python
for idx, token in enumerate(tokens):     # idx = posición, token = símbolo
    tope = pila[-1]                      # mira el tope sin sacarlo

    # REGLA 1: TEXTO no toca la pila (línea 160)
    if token == "TEXTO":
        registrar(...)

    # REGLAS 2 a 4: PUSH (línea 164)
    elif token in self.apertura_a_pila:
        marcador = self.apertura_a_pila[token]
        pila.append(marcador)
        registrar(...)

    # REGLAS 5 a 7: POP si coincide (línea 170)
    elif token in self.cierre_a_pila:
        esperado = self.cierre_a_pila[token]
        if tope == esperado:
            pila.pop()
            registrar(...)
        else:                            # Δ = ∅
            if tope == self.z0:
                msg = "...sin apertura previa (pila vacía)."
            else:
                msg = "Error de anidamiento LIFO: ..."
            traza.append(f"BLOQUEO: ...")
            return finalizar(False, msg)

    # Fuera de Σ (línea 185)
    else:
        msg = "Error léxico: ..."
        traza.append(f"BLOQUEO: ...")
        return finalizar(False, msg)
```

**Al terminar el `for` se aplica la regla 8 (línea 193):**

```python
if pila == [self.z0]:              # solo queda el fondo
    estado = "qf"                  # Δ(q0, λ, Z0) = (qf, Z0)
    registrar(...)
    return finalizar(True, "Cadena VÁLIDA: ...")

# si no, quedaron etiquetas abiertas: error "sin cerrar"
```

**Las dos funciones de abajo son de apoyo:** `_etiqueta_de` traduce un símbolo a etiqueta (`B` a `<b>`) para los mensajes, e `_imprimir_traza_consola` muestra la traza.

### 6.4 `AnalizadorRecursivoMiniHTML`: la gramática G (líneas 224 a 281)

Es un **analizador descendente recursivo**: **una función por cada variable** de la gramática.

```python
def validar(self, tokens):
    pos = 0                               # próximo token a leer

    def es_cierre(tok):
        return tok.startswith("</") and tok[2:-1] in self.tags
```

`tok[2:-1]` saca el `</` del principio y el `>` del final: de `</b>` queda `b`. `nonlocal pos` permite que las funciones internas modifiquen esa variable.

**`parse_S` es la variable S:**

```python
def parse_S():
    nonlocal pos
    while pos < len(tokens) and not es_cierre(tokens[pos]):
        parse_E()
```

Mientras haya texto o una apertura, aplica `S → E S`. Ante un cierre o el final, sale: es `S → λ`. La recursión por derecha `S → E S` se puede escribir como un `while`, porque "un elemento seguido de más secuencia" es lo mismo que repetir elementos.

**`parse_E` es la variable E:**

```python
def parse_E():
    nonlocal pos
    tok = tokens[pos]

    if tok == "TEXTO":
        pos += 1                          # E → TEXTO
        return

    nombre_tag = tok[1:-1]                # de "<p>" queda "p"
    if not (tok.startswith("<") and tok.endswith(">") and nombre_tag in self.tags):
        raise ValueError("Error léxico: ...")
    pos += 1                              # consume la apertura

    parse_S()                             # la S del medio

    esperado = f"</{nombre_tag}>"
    if pos >= len(tokens):
        raise ValueError("...nunca fue cerrada...")
    if tokens[pos] != esperado:
        raise ValueError("Error de anidamiento: ...")
    pos += 1                              # consume el cierre
```

Las últimas líneas son `E → <x> S </x>` escrita en Python: apertura, S y cierre.

**Dónde está la pila acá:** en la **pila de llamadas** de Python. Cada `parse_E` abierto recuerda en `nombre_tag` qué etiqueta le falta cerrar. Es la misma idea LIFO que el autómata, pero implícita.

**El cierre de `validar`:**

```python
try:
    parse_S()
    if pos < len(tokens):                 # sobró un cierre en el nivel de afuera
        raise ValueError("Etiqueta de cierre ... sin apertura previa.")
    return True, "Cadena VÁLIDA: ..."
except ValueError as err:
    return False, f"Error sintáctico en G: {err}"
except RecursionError:
    return False, "Error en G: anidamiento demasiado profundo..."
```

`raise` corta todas las llamadas recursivas de una vez hasta el `except`. `RecursionError` aparece cuando se supera el límite de llamadas de Python (ver la sección 7.3).

### 6.5 La interfaz (líneas 287 a 368)

- **`analizar_cadena`:** tokeniza, corre M y G, imprime ambos resultados y `VERIFICADA` o `DISCREPANCIA`.
- **`ejecutar_casos_oficiales`:** prueba α, β, γ, λ y 4 inválidas.
- **`modo_interactivo`:** la consola para la defensa.
- **`if __name__ == "__main__":`** se ejecuta solo si corrés el archivo directamente, y mira los argumentos.

### 6.6 Los tests (`tests/test_parser.py`)

Son 14 tests con `unittest`. Cada uno pasa una cadena por `tokenizar`, `simular` y `validar`, y comprueba el resultado con `assertTrue`, `assertFalse` o `assertIn`. `setUp` crea un autómata y un analizador nuevos antes de cada test.

---

## 7. La demo en vivo

### 7.1 Comandos

Ejecutalos **desde la carpeta raíz del repo**, porque los tests importan `src.parser`. Las **comillas son obligatorias**: sin ellas, la terminal interpreta `<` y `>` como redirecciones.

Casos oficiales y después modo interactivo, que es el de la defensa:

```bash
python3 src/parser.py
```

Una cadena con su traza:

```bash
python3 src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```

Solo los casos oficiales:

```bash
python3 src/parser.py --test
```

La cadena vacía:

```bash
python3 src/parser.py ""
```

Los 14 tests:

```bash
python3 -m unittest tests/test_parser.py
```

### 7.2 Salida real, explicada

```
Cadena analizada: "<p> <b> TEXTO </p> </b>"
Tokens detectados: ['<p>', '<b>', 'TEXTO', '</p>', '</b>']        ← análisis léxico
     (q0, <p> <b> TEXTO </p> </b>, Z0)      Configuración inicial  ← traza de M
  |- (q0, <b> TEXTO </p> </b>, P Z0)        Δ(q0, <p>, Z0) = {(q0, P Z0)}  PUSH
  |- (q0, TEXTO </p> </b>, B P Z0)          Δ(q0, <b>, P) = {(q0, B P)}  PUSH
  |- (q0, </p> </b>, B P Z0)                Δ(q0, TEXTO, B) = {(q0, B)}
  BLOQUEO: Δ(q0, </p>, B) = ∅. Error de anidamiento LIFO: ...

[Resultado Autómata a Pila M]: RECHAZADA (w ∉ L(M))
[Resultado Gramática G]:      RECHAZADA (w ∉ L(G))
[Equivalencia L(G) = L(M)]:   VERIFICADA (Ambos coinciden)        ← M y G dan lo mismo
```

### 7.3 Cadenas que puede probar, y qué pasa

Probalas todas antes del oral. Están ejecutadas: M y G coinciden en todas.

| Cadena | Resultado | Por qué |
|---|---|---|
| (vacía) | ✅ | `S ⇒ λ` y regla 8 |
| `TEXTO` | ✅ | Texto solo |
| `Hola mundo` | ✅ | Cada palabra es un TEXTO |
| `<p></p>` | ✅ | `S → λ` adentro de `<p>` |
| `<p>Hola <b>mundo</b></p>` | ✅ | HTML real: se tokeniza igual |
| `<P> TEXTO </P>` | ✅ | Se pasa a minúscula |
| `<p> TEXTO <\p>` | ✅ | `<\p>` es la notación alternativa de cierre |
| `a > b` | ✅ | Un `>` suelto es texto |
| `</p>` | ❌ sintáctico | Cierre sin apertura |
| `<p> <b> TEXTO </p> </b>` | ❌ sintáctico | Cruce |
| `<p> TEXTO </b>` | ❌ sintáctico | Cierre de otro tipo |
| `<p> <b> TEXTO </b>` | ❌ sintáctico | `<p>` sin cerrar |
| `<p>>` | ❌ sintáctico | El `>` es TEXTO y `<p>` queda abierto |
| `<u> TEXTO </u>` | ❌ léxico | `<u>` no está en Σ |
| `<br>` | ❌ léxico | `<br>` no está en Σ |
| `<p> TEXTO <b </p>` | ❌ léxico | `<b` mal formada |
| `< b > TEXTO </b>` | ❌ léxico | Tiene espacios adentro |
| `<p class=x> TEXTO </p>` | ❌ léxico | No admite atributos |
| `<p/>` y `<>` | ❌ léxico | No son etiquetas válidas |
| `1 < 2` | ❌ léxico | `<` siempre inicia una etiqueta |

**Tres detalles que conviene conocer antes de que te agarren:**

1. **En el modo interactivo, una línea vacía no se analiza:** vuelve a pedir la cadena. Para mostrar λ usá `python3 src/parser.py ""`.
2. **`test` y `salir` son comandos del modo interactivo**, no se analizan como texto.
3. **Con un anidamiento de unos 500 niveles aparece `DISCREPANCIA`.** Lo comprobamos: con 495 niveles coinciden y con 500, M acepta y G informa "anidamiento demasiado profundo". No es que el lenguaje cambie: es un límite de Python, que corta la recursión en unas 1000 llamadas, y cada nivel usa dos (`parse_E` y `parse_S`). El simulador no sufre esto porque su pila es una lista.

### 7.4 Léxico o sintáctico

- **Error léxico:** el token ni siquiera es una palabra del alfabeto (`<u>`, `<b`).
- **Error sintáctico:** las palabras son válidas, pero la estructura no (cruce, cierre sin apertura, sin cerrar).

---

## 8. Modificaciones en vivo

### 8.1 El método: seis pasos, siempre iguales

La modificación evalúa si entendés la relación entre teoría y código, no solo si sabés Python. **Decí en voz alta** cada paso:

1. **Repetí el pedido** y aclará los casos dudosos. Por ejemplo: "¿prohibido solo directamente adentro, o en cualquier nivel?".
2. **¿Cambia Σ?** Si aparece un símbolo nuevo.
3. **¿Cambia G?** Qué producciones se agregan o cambian.
4. **¿Cambia M?** Qué transiciones se agregan, se sacan o si hace falta un estado.
5. **Tocá el código en los dos analizadores:** `simular` (M) **y** `validar` (G).
6. **Probá** una cadena válida y una inválida, y corré los tests.

> **Si te olvidás de cambiar uno de los dos analizadores**, el programa imprime `DISCREPANCIA`. Eso te avisa en vivo de que falta el otro.

**Dónde va cada cosa en el código:**

| Qué te piden | Dónde se toca |
|---|---|
| Una etiqueta común | `ETIQUETAS` (línea 32) |
| Cómo se reconoce la entrada (mayúsculas, atributos, texto) | `tokenizar` y los patrones (líneas 44 a 76) |
| Un símbolo que no toca la pila | Rama TEXTO de `simular` (160) y de `parse_E` (252) |
| Una restricción al **abrir** una etiqueta | Antes del `pila.append` (165) y antes de consumir la apertura (259) |
| Una restricción al **cerrar** | Rama de cierre de `simular` (171) y después de consumir la apertura en `parse_E` |
| El criterio de aceptación | Final de `simular` (193) |
| Un mensaje de error | El `msg` de `simular` y los `raise` de `parse_E` |

**Cuando termines de practicar, volvé al código original** (esto descarta los cambios de esos dos archivos):

```bash
git checkout -- src/parser.py tests/test_parser.py
```

**Si un test falla después del cambio, no siempre es un error.** Si cambiaste el lenguaje, un test que afirmaba lo contrario *tiene* que fallar. Explicalo y actualizalo. La tabla de la sección 8.17 dice cuáles fallan en cada caso.

### 8.2 Las restricciones en G: preparación común

`simular` ya tiene la pila a mano, pero `parse_E` no sabe qué etiquetas están abiertas. Para las modificaciones 8.6 a 8.9 y 8.11, primero agregale esa memoria a `validar`. Son 3 líneas:

```python
# en validar(), debajo de pos = 0 (línea 236)
abiertas: List[str] = []
```

```python
# en parse_E(), reemplazando la llamada a parse_S() (línea 262)
abiertas.append(nombre_tag)
parse_S()
abiertas.pop()
```

Ahora `abiertas` se comporta como la pila de M: `abiertas[-1]` es el tope y `"p" in abiertas` pregunta si hay un `<p>` abierto en cualquier nivel.

### 8.3 Agregar una etiqueta común: `<u>` ⭐ la más probable

**Σ** suma `<u>` y `</u>`. **G** suma `E → <u> S </u>`. **M** suma U a Γ, `Δ(q0, <u>, X) = (q0, U X)` y `Δ(q0, </u>, U) = (q0, λ)`.

**Código:** una línea, y los dos analizadores se actualizan solos.

```python
ETIQUETAS: Dict[str, str] = {
    "b": "B",
    "i": "I",
    "p": "P",
    "u": "U",
}
```

**Probar:** `<p> <u> TEXTO </u> </p>` es válida y `<u> </p>` no.

**⚠️ Falla un test, y es correcto:** `test_etiqueta_desconocida` usa `</u>` como ejemplo de etiqueta inexistente. Explicá el motivo y cambiá `</u>` por `</x>` en ese test ([tests/test_parser.py:100](../tests/test_parser.py#L100)).

**Con otros nombres:** `"h1": "H1"` funciona igual, porque el patrón admite números.

**Quitar una etiqueta** es lo inverso: borrar su línea. Si sacás `i`, fallan los tests que la usan (β, γ y `test_mensaje_etiquetas_pendientes`), como corresponde.

### 8.4 Etiqueta autocerrada: `<br>` ⭐

No tiene cierre, así que **no toca la pila**: se comporta como TEXTO.

**Σ** suma `<br>`. **G** suma `E → <br>`. **M** suma `Δ(q0, <br>, X) = (q0, X)`.

**Código, 3 cambios:**

```python
# debajo de ETIQUETAS
VACIAS: Set[str] = {"<br>"}
```

```python
# simular(), líneas 160 y 161: se cambia la condición y TEXTO por {token} en la traza
if token == "TEXTO" or token in VACIAS:
    registrar("|-", idx + 1, f"Δ({estado}, {token}, {tope}) = {{({estado}, {tope})}}")
```

```python
# parse_E(), línea 252
if tok == "TEXTO" or tok in VACIAS:
```

**Probar:** `<p> TEXTO <br> TEXTO </p>` y `<br>` son válidas; `<p> </br> </p>` da error léxico. No falla ningún test.

### 8.5 Un terminal nuevo que no es etiqueta: `NUM` ⭐

Pedido: "que los números sean un token aparte".

**Σ** suma `NUM`. **G** suma `E → NUM`. **M** suma `Δ(q0, NUM, X) = (q0, X)`.

**Código, 4 cambios:**

```python
# tokenizar(), línea 74
tokens.extend("NUM" if palabra.isdigit() else "TEXTO" for palabra in trozo.split())
```

```python
# __init__ del autómata, línea 105
self.sigma: Set[str] = {"TEXTO", "NUM"}
```

```python
# simular(), líneas 160 y 161
if token == "TEXTO" or token == "NUM":
    registrar("|-", idx + 1, f"Δ({estado}, {token}, {tope}) = {{({estado}, {tope})}}")
```

```python
# parse_E(), línea 252
if tok == "TEXTO" or tok == "NUM":
```

**Probar:** `<p> Tengo 20 anios </p>` da los tokens `<p>`, `TEXTO`, `NUM`, `TEXTO`, `</p>`. No falla ningún test.

### 8.6 Prohibir `<p>` **directamente** dentro de `<p>` ⭐

Primero la preparación de 8.2.

**G:** hace falta otra variable, porque el contenido de `<p>` ya no puede ser cualquier S:

```
E → TEXTO | <b> S </b> | <i> S </i> | <p> N </p>
N → F N | λ
F → TEXTO | <b> S </b> | <i> S </i>
```

**M:** alcanza con mirar el tope. La regla 4 deja de valer con X = P: `Δ(q0, <p>, P) = ∅`.

**Código:**

```python
# simular(), antes de marcador = ... (línea 165)
if token == "<p>" and tope == "P":
    msg = "Error sintáctico: no se permite un <p> directamente dentro de otro <p>."
    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
    return finalizar(False, msg)
```

```python
# parse_E(), antes de pos += 1  # Consumir apertura (línea 259)
if nombre_tag == "p" and abiertas and abiertas[-1] == "p":
    raise ValueError("no se permite un <p> directamente dentro de otro <p>.")
```

**Probar:** `<p> <p> </p> </p>` es inválida; `<p> <b> <p> </p> </b> </p>` y `<p> </p> <p> </p>` son válidas. No falla ningún test.

> **Este es el molde de cualquier restricción al abrir:** en M, un `if` antes del `marcador = ...` con el bloqueo; en G, un `if` antes de consumir la apertura con un `raise`.

### 8.7 Prohibir `<p>` dentro de `<p>` **en cualquier nivel**

Primero la preparación de 8.2.

**G:** toda una rama nueva que no pueda generar `<p>`:

```
E → TEXTO | <b> S </b> | <i> S </i> | <p> T </p>
T → F T | λ
F → TEXTO | <b> T </b> | <i> T </i>
```

**M:** **mirar el tope ya no alcanza** (en `<p> <b> <p>` el tope es B). Como solo puede haber un P a la vez, alcanza con un estado nuevo que recuerde que hay un párrafo abierto: `Δ(q0, <p>, X) = (q1, P X)` y `Δ(q1, </p>, P) = (q0, λ)`. En q1 se leen TEXTO, `<b>`, `<i>` y sus cierres como en q0, y `Δ(q1, <p>, X) = ∅`. Es un buen ejemplo: **los estados también son memoria, pero finita**.

**Código:** igual que 8.6, cambiando las condiciones:

```python
# simular()
if token == "<p>" and "P" in pila:
```

```python
# parse_E()
if nombre_tag == "p" and "p" in abiertas:
```

En el código se usa `"P" in pila` porque es más corto que simular q1, y tiene el mismo efecto. **Aclaralo si te lo preguntan:** un autómata real solo ve el tope.

**Probar:** `<p> <b> <p> </p> </b> </p>` es inválida; `<b> <p> </p> </b>` es válida. No falla ningún test.

### 8.8 `<i>` solo puede contener texto

Primero la preparación de 8.2.

**G:** `E → ... | <i> T </i>`, con `T → TEXTO T | λ`.

**M:** `Δ(q0, <x>, I) = ∅` para toda apertura.

**Código:**

```python
# simular(), antes de marcador = ...
if tope == "I":
    msg = "Error sintáctico: <i> solo puede contener texto."
    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
    return finalizar(False, msg)
```

```python
# parse_E(), antes de consumir la apertura
if abiertas and abiertas[-1] == "i":
    raise ValueError("<i> solo puede contener texto.")
```

**Probar:** `<i> <b> TEXTO </b> </i>` es inválida; `<b> <i> TEXTO </i> </b>` es válida. **Falla `test_mensaje_etiquetas_pendientes`**, que anida `<b>` dentro de `<i>`: correcto, porque esa cadena ahora es inválida por otro motivo.

### 8.9 Todo debe estar dentro de un `<p>`

Primero la preparación de 8.2. Pedido equivalente: "no puede haber texto suelto".

**G:** nuevo símbolo inicial D, y las reglas de S y E quedan igual: `D → <p> S </p> D | λ`.

**M:** con Z0 en el tope solo se puede abrir `<p>`: `Δ(q0, TEXTO, Z0) = Δ(q0, <b>, Z0) = Δ(q0, <i>, Z0) = ∅`.

**Código:**

```python
# simular(), debajo de tope = pila[-1] (línea 157)
if tope == self.z0 and token != "<p>":
    msg = "Error sintáctico: todo el contenido debe estar dentro de un <p>."
    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
    return finalizar(False, msg)
```

```python
# parse_E(), debajo de tok = tokens[pos] (línea 250)
if not abiertas and tok != "<p>":
    raise ValueError("todo el contenido debe estar dentro de un <p>.")
```

**Probar:** `<p> TEXTO </p>` es válida; `TEXTO` y `<b> TEXTO </b>` no. **Fallan 4 tests** (`test_cadena_gamma`, `test_texto_plano`, `test_anidamiento_profundo` y `test_etiquetas_mal_formadas`), porque usan contenido fuera de `<p>`. Es esperable. **Ojo:** γ empieza con `<p>` pero termina con `<i>` en el nivel de afuera, así que con esta regla **deja de ser válida**.

### 8.10 No permitir etiquetas vacías, como `<p></p>`

**G:** S se reemplaza por `E S` adentro de las etiquetas, para exigir al menos un elemento: `E → <b> E S </b> | <i> E S </i> | <p> E S </p> | TEXTO`.

**M:** hace falta un estado "recién abrí", q1. Las aperturas llevan a q1, TEXTO lleva a q0, y los cierres solo se pueden leer desde q0.

**Código:**

```python
# simular(), debajo de esperado = self.cierre_a_pila[token] (línea 171)
if idx > 0 and tokens[idx - 1] == "<" + token[2:]:
    msg = "Error sintáctico: la etiqueta no puede estar vacía."
    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
    return finalizar(False, msg)
```

`"<" + token[2:]` convierte `</p>` en `<p>`, para comparar con el token anterior.

```python
# parse_E(), debajo de pos += 1  # Consumir apertura (línea 259)
if pos < len(tokens) and tokens[pos] == f"</{nombre_tag}>":
    raise ValueError("la etiqueta no puede estar vacía.")
```

**Probar:** `<p></p>` y `<p> <b></b> </p>` son inválidas; `<p> TEXTO </p>` y la cadena vacía son válidas. **Falla `test_anidamiento_profundo`**, cuya cadena tiene un `<b></b>` en el centro.

### 8.11 Limitar la profundidad a 3 niveles

Primero la preparación de 8.2. **Tiene una pregunta teórica escondida.**

**G:** se necesita una familia de variables por nivel: `S₁`, `S₂`, `S₃`.

**M:** se bloquea el PUSH cuando ya hay 3 símbolos arriba de Z0.

**Código:**

```python
# debajo de ETIQUETAS
MAX_PROFUNDIDAD = 3
```

```python
# simular(), antes de marcador = ...
if len(pila) - 1 >= MAX_PROFUNDIDAD:
    msg = "Error sintáctico: se superó la profundidad máxima."
    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
    return finalizar(False, msg)
```

`len(pila) - 1` porque Z0 no cuenta como etiqueta.

```python
# parse_E(), antes de consumir la apertura
if len(abiertas) >= MAX_PROFUNDIDAD:
    raise ValueError("se superó la profundidad máxima.")
```

**Probar:** `<p><b><i>TEXTO</i></b></p>` es válida; `<p><b><i><p></p></i></b></p>` no. **Falla `test_anidamiento_profundo`.**

> **Lo que conviene decir sin que te lo pregunten:** con la profundidad acotada el lenguaje **pasa a ser regular**. Hay una cantidad finita de combinaciones de etiquetas abiertas (1 + 3 + 9 + 27 = 40), así que un autómata finito con un estado por combinación alcanza. La pila hacía falta justamente porque no había límite.

### 8.12 Permitir atributos: `<p class="x">`

**Σ, G y M no cambian.** Es un cambio **solo léxico**: el tokenizador reduce `<p class="x">` al token `<p>`. Es una muy buena observación para hacer en voz alta.

**Código:** una línea, el patrón de la línea 46.

```python
PATRON_ETIQUETA = re.compile(r'<([/\\]?)([a-zA-Z0-9]+)(?:\s+[^<>]*)?>')
```

`(?:\s+[^<>]*)?` significa: opcionalmente, un espacio o más y después cualquier cosa que no sea `<` ni `>`.

**Probar:** `<p class="x"> TEXTO </p>` es válida; `< b >` y `<b` siguen siendo errores. **Falla `test_etiquetas_mal_formadas`**, que usa `<p class=x>` como ejemplo de etiqueta mal formada: sacala de la lista.

### 8.13 Otros cambios solo léxicos

**Distinguir mayúsculas** (que `<P>` sea error léxico). En la línea 68, sacá `.lower()`:

```python
tokens.append(f"<{barra}{etiqueta.group(2)}>")
```

**Un solo TEXTO por fragmento** (que `Hola mundo` sea un token, no dos). En la línea 74:

```python
tokens.append("TEXTO")
```

Con este cambio, `<p> TEXTO TEXTO </p>` tiene un solo TEXTO y las trazas son más cortas que las del informe. Tampoco cambian G ni M, y no falla ningún test.

### 8.14 Aceptar por pila vacía

**G no cambia.** **M:** la regla 8 pasa a ser `Δ(q0, λ, Z0) = (q0, λ)`, que saca Z0. Ahora se acepta por N(M), y qf ya no hace falta: Q = {q0} y F = ∅.

**Código, final de `simular` (líneas 193 a 195):**

```python
if pila == [self.z0]:
    pila.pop()
    registrar("|-", len(tokens), f"Δ(q0, λ, {self.z0}) = {{(q0, λ)}}  Aceptación por pila vacía")
```

La traza termina en `(q0, λ, )`: la pila está vacía. **Falla `test_traza_configuraciones`**, que espera ver `qf`. Sigue siendo no determinista por el mismo motivo, y el lenguaje reconocido es el mismo.

### 8.15 Ajustar un mensaje de error

Por ejemplo, para indicar la posición, usá `idx`, que vale desde 0:

```python
msg = f"Error sintáctico en el token {idx + 1}: Se intentó cerrar '{token}' sin apertura previa (pila vacía)."
```

Los mensajes de M están en `simular` (líneas 177, 179 y 186), y los de G en los `raise` de `parse_E` y `validar`. Si cambiás palabras como "léxico", revisá los tests que las buscan con `assertIn`.

### 8.16 Documento no vacío (que λ ya no sea válida)

**G:** nuevo inicial `D → E S`.

**M:** un estado más, porque la regla 8 no debe poder usarse sin haber leído algo.

**Código:**

```python
# simular(), debajo de registrar("", 0, "Configuración inicial") (línea 154)
if not tokens:
    return finalizar(False, "Error sintáctico: el documento no puede estar vacío.")
```

```python
# validar(), primera línea adentro del try (línea 272)
if not tokens:
    raise ValueError("el documento no puede estar vacío.")
```

Falla `test_cadena_vacia`, como corresponde.

### 8.17 Resumen: qué cambia en cada una

| Modificación | ¿Cambia G? | ¿Cambia M? | Lugar | Tests que fallan |
|---|---|---|---|---|
| Etiqueta `<u>` | Regla nueva | PUSH y POP nuevos | `ETIQUETAS` | `test_etiqueta_desconocida` |
| Etiqueta `<h1>` | Regla nueva | PUSH y POP nuevos | `ETIQUETAS` | Ninguno |
| Quitar `<i>` | Saca regla | Saca reglas | `ETIQUETAS` | `test_cadena_beta`, `test_cadena_gamma`, `test_mensaje_etiquetas_pendientes` |
| Autocerrada `<br>` | `E → <br>` | Sin cambios en la pila | Rama TEXTO | Ninguno |
| Terminal `NUM` | `E → NUM` | Sin cambios en la pila | Tokenizador y rama TEXTO | Ninguno |
| `<p>` directo en `<p>` | Variables nuevas | `Δ(q0,<p>,P) = ∅` | Antes del PUSH | Ninguno |
| `<p>` en cualquier nivel | Variables nuevas | Estado nuevo | Antes del PUSH | Ninguno |
| `<i>` solo texto | Variable nueva | `Δ(q0,<x>,I) = ∅` | Antes del PUSH | `test_mensaje_etiquetas_pendientes` |
| Todo dentro de `<p>` | Inicial nuevo | Bloqueos con Z0 | Inicio del `for` y de `parse_E` | 4 tests (ver 8.9) |
| Sin etiquetas vacías | `E → <x> E S </x>` | Estado nuevo | Rama de cierre | `test_anidamiento_profundo` |
| Profundidad máxima | Variables por nivel | Bloqueo de PUSH | Antes del PUSH | `test_anidamiento_profundo` |
| Atributos | No | No | Patrón | `test_etiquetas_mal_formadas` |
| Mayúsculas | No | No | Tokenizador | Ninguno |
| TEXTO por fragmento | No | No | Tokenizador | Ninguno |
| Pila vacía | No | Regla 8 | Final de `simular` | `test_traza_configuraciones` |
| Mensaje con posición | No | No | `msg` | Ninguno |
| Documento no vacío | Inicial nuevo | Estado nuevo | Inicio de `simular` y `validar` | `test_cadena_vacia` |

### 8.18 Si te piden agregar un test

Copiá este molde adentro de la clase `TestMiniHTML`:

```python
def test_mi_caso(self):
    tokens = tokenizar("<p> <u> TEXTO </u> </p>")
    valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
    valida_g, _ = self.g.validar(tokens)
    self.assertTrue(valida_ap)
    self.assertTrue(valida_g)
```

Para una cadena inválida, cambiá `assertTrue` por `assertFalse`. Sin la modificación 8.3, este ejemplo con `<u>` falla.

### 8.19 Prioridades si tenés poco tiempo

1. **`<u>`** (8.3): la consigna la nombra como ejemplo.
2. **`<br>`** (8.4): "agregar una regla de producción".
3. **`<p>` dentro de `<p>`** (8.6): "ajustar una validación", y da el molde de cualquier restricción.
4. **Documento dentro de `<p>`** (8.9) o **profundidad** (8.11).

---

## 9. Preguntas probables

**¿Por qué un autómata finito no alcanza?**
Tiene memoria finita y MiniHTML permite anidar sin límite. Con `<p>ⁿ TEXTO </p>ⁿ` y n mayor que la cantidad de estados, confunde dos profundidades. Formalmente, por el lema de bombeo: β = `<p>ˢ` y con i = 0 queda desbalanceada.

**¿Por qué una pila y no otra estructura?**
Porque el orden de cierre es LIFO. Con una cola (FIFO) aceptaríamos `<p> <b> </p> </b>`.

**¿Qué es Z0?**
El símbolo de fondo. Si está en el tope, no hay nada abierto. Sirve para aceptar (regla 8) y para detectar cierres sin apertura.

**¿Estado final o pila vacía?**
Estado final: se llega a qf y en la pila queda Z0. Para pasar a pila vacía, ver la sección 8.14.

**¿Su autómata es determinista?**
No, es un AFPN-λ, por la regla 8, que compite con leer cuando el tope es Z0. Es el único punto no determinista.

**Si es no determinista, ¿por qué el programa no explora ramas?**
Porque la única rama que puede aceptar es la que toma la regla 8 con la entrada ya consumida. Cualquier salto anterior muere en qf.

**¿Se podría hacer determinista?** *(difícil)*
Sí, con la definición de la cátedra (sin transiciones λ) y dos estados: q0 = "no hay nada abierto", final, y q1 = "hay algo abierto". Al abrir desde q0 se apila una marca especial de primer nivel, y al cerrarla se vuelve a q0.

**¿Su gramática es ambigua?**
No: el próximo token determina la regla, entonces cada cadena tiene un único árbol. En general, decidir si una gramática es ambigua es indecidible, pero acá se ve a mano.

**¿Por qué S y E, y no una sola variable?**
Para separar secuencia de elemento. Con `S → S S` sería ambigua.

**¿Qué relación hay entre G y M?**
El teorema: un lenguaje es libre de contexto si y solo si lo reconoce un autómata a pila. Concretamente, cada `E → <x> S </x>` es un PUSH al leer `<x>` y un POP al leer `</x>`, y la S del medio es la pila creciendo.

**¿Implementaron la opción A o la B?**
Las dos, y el programa compara el resultado en cada cadena.

**¿Dónde está la pila en el analizador recursivo?**
Es la pila de llamadas de Python: cada `parse_E` que espera su cierre equivale a un símbolo en la pila.

**¿Por qué `parse_S` tiene un `while` y no se llama a sí misma?**
`S → E S` es recursión por derecha, que equivale a repetir E. Con el `while` se ahorran llamadas y se obtiene el mismo lenguaje.

**¿Qué hace el tokenizador?**
El análisis léxico: pasa de texto a símbolos de Σ, normaliza etiquetas y convierte cada palabra en TEXTO. No decide la estructura.

**¿Por qué mantiene las etiquetas mal formadas?**
Para que el analizador las rechace como error léxico. Si fueran texto, se aceptarían cadenas mal escritas.

**¿Por qué aparece "Error sintáctico en G: Error léxico"?**
Es un prefijo que `validar` agrega a todos los errores de G. El tipo real es el que viene después.

**¿Dónde se ve la 7-tupla en el código?**
En `__init__` del autómata. Δ son `apertura_a_pila`, `cierre_a_pila` y las ramas de `simular`.

**¿Cuánto tarda?**
La decisión es lineal: se recorre cada token una vez y cada operación de pila es de costo constante. Armar la traza de texto agrega trabajo, pero no cambia la decisión.

**¿Por qué TEXTO no modifica la pila?**
Porque no abre ni cierra nada: no afecta el anidamiento.

**¿Qué es una configuración instantánea?**
La terna (estado, entrada que falta, pila con el tope a la izquierda). La traza es la secuencia unida por ⊢.

---

## 10. Machete y checklist

```
LENGUAJE   Σ = {<b>,<i>,<p>,</b>,</i>,</p>,TEXTO}          Tipo 2, NO regular

G          G = (V, Σ, S, P)    V = {S, E}
           (1) S → E S    (2) S → λ    (3) E → TEXTO
           (4) E → <b> S </b>   (5) E → <i> S </i>   (6) E → <p> S </p>
           No ambigua. Apertura y cierre en la misma regla = LIFO.

M          M = (Σ, Γ, Q, q0, Z0, F, Δ)     AFPN-λ por ESTADO FINAL
           Γ = {Z0,B,I,P}   Q = {q0,qf}   F = {qf}
           (1)   TEXTO, X / X        sin cambios
           (2-4) <x>,   X / Y X      PUSH
           (5-7) </x>,  Y / λ        POP
           (8)   λ,    Z0 / Z0 → qf  acepta; único no determinismo
           Otro caso: Δ = ∅, bloqueo.

NO REGULAR <p>ⁿ TEXTO </p>ⁿ, β = <p>ˢ, i = 0: desbalance, contradicción.

CÓDIGO     ETIQUETAS :32 → tokenizar :49 → simular :131 (M) y validar :234 (G)
           PUSH :166 · POP :173 · regla 8 :193 · parse_S :241 · parse_E :248

MODIFICAR  Σ? → G? → M? → simular Y validar → probar → tests
           Etiqueta común: una línea en ETIQUETAS.
           Sin pila (<br>): rama TEXTO en simular (160) y en parse_E (252).
           Restricción: if antes del PUSH (165) y antes de consumir apertura (259).
           DISCREPANCIA = falta cambiar uno de los dos.
```

### El día de la defensa

- [ ] Leer este machete.
- [ ] Compu cargada y repo actualizado.
- [ ] `git status` sin cambios de prácticas en `src/parser.py` ni en los tests.
- [ ] `python3 src/parser.py --test` y `python3 -m unittest tests/test_parser.py` andando.
- [ ] Editor abierto en `parser.py` y una terminal en la carpeta raíz del repo.
- [ ] Papel y lapicera para trazas y derivaciones.
- [ ] Todos saben responder la tabla G ↔ M ↔ código: las preguntas son individuales.
