# Guía de estudio para la defensa — MiniHTML Parser

> **Para preparar la defensa, estudiá la [Guía para la defensa](Guia_Defensa.md).** Este archivo queda como material de consulta.

Esta guía alcanza por sí sola para preparar el oral: explica la teoría desde cero, la gramática, el autómata, el código y las modificaciones en vivo, que se detallan en la [Guía del código](Guia_del_Codigo.md). Usa la misma numeración de reglas y transiciones que el [informe](../entregables/Informe%20miniparser-html.pdf), porque es lo que la profe va a tener enfrente.

> **Para estudiar el código y practicar cambios en profundidad, usá la [Guía del código](Guia_del_Codigo.md).**
>
> **Material interno: no se entrega.** Las cadenas de la sección 7 se ejecutaron sobre el código real del proyecto. Las líneas citadas son las de [src/parser.py](../src/parser.py) sin modificar.

## Índice

1. [Qué te van a evaluar](#1-qué-te-van-a-evaluar)
2. [El proyecto en 1 minuto](#2-el-proyecto-en-1-minuto)
3. [Teoría desde cero](#3-teoría-desde-cero)
4. [La gramática G](#4-la-gramática-g)
5. [El autómata a pila M](#5-el-autómata-a-pila-m)
6. [El código](#6-el-código)
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
| **Modificación en vivo** | Pide un cambio menor en el código: una etiqueta nueva, una regla de producción o una validación. | Sección 8 y [Guía del código](Guia_del_Codigo.md) |
| **Preguntas individuales** | Sobre la relación entre G, M y el código. | Secciones 3 a 5, 9 y [Guía del código](Guia_del_Codigo.md) |

### Lo que hay que cumplir además del oral

- **Informe en PDF:** carátula con los integrantes, fases 1 y 2, y la explicación de por qué un autómata finito no alcanza. Sin transcribir la consigna. **Se carga en el aula virtual.**
- **Entrevista:** la coordina el grupo con uno de los docentes.
- **Rúbrica:** modelado formal 35 %, implementación 35 %, defensa y demostración 30 %.
- **Para qué sirve aprobarlo (consigna y syllabus):** reemplaza al segundo parcial para la regularidad, con el primero en 4 o más y 65 % de asistencia. Para la promoción directa baja la nota mínima de los parciales de 7 a 6, con 80 % de asistencia.

### Plan de estudio (unas 5 horas y media)

| Etapa | Qué hacer | Tiempo | Cómo sabés que terminaste |
|---|---|---|---|
| 1 | Correr el programa (sección 7.1) y leer las secciones 2 y 3 | 1 h | Explicás sin leer por qué un autómata finito no alcanza. |
| 2 | Sección 4 | 45 min | Hacés en papel el árbol y la derivación de α. |
| 3 | Sección 5 | 1 h | Hacés en papel la traza de γ y la de una cadena inválida. |
| 4 | [Guía del código](Guia_del_Codigo.md), secciones 1 a 4 | 1 h | Señalás la línea exacta donde apila, desapila y de cada error. |
| 5 | [Guía del código](Guia_del_Codigo.md), secciones 5 a 8 | 1 h 30 | Hacés las 4 modificaciones más probables sin mirar. |
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
| 3 | Programa en Python | Simula **M** con una pila (opción B de la consigna). |

**La frase que tenés que poder decir de memoria:**

> MiniHTML no es un lenguaje regular: para saber si las etiquetas cierran bien hay que recordar cuántas y cuáles se abrieron, sin límite, y un autómata finito tiene memoria finita. Por eso lo describimos con una gramática libre de contexto y lo reconocemos con un autómata a pila: la pila es una memoria LIFO, igual que el orden en que se cierran las etiquetas.

---

## 3. Teoría desde cero

### 3.1 Alfabeto, cadena y lenguaje

- **Alfabeto (Σ):** conjunto finito no vacío de símbolos. Acá cada símbolo es un *token* entero: `<b>` es **un** símbolo, no tres caracteres.
- **Cadena:** secuencia finita de símbolos. `<p> TEXTO </p>` tiene longitud 3.
- **λ (lambda):** la cadena vacía, de longitud 0.
- **Σ\*:** todas las cadenas posibles con ese alfabeto, válidas o no.
- **Lenguaje (L):** un subconjunto de Σ\*. MiniHTML son las cadenas de Σ\* bien anidadas.
- **w ∈ L:** "la cadena w pertenece al lenguaje". Es exactamente lo que responde el programa.

### 3.2 Dos formas de describir un lenguaje

- **Modelo generativo (gramática):** reglas que producen todas las cadenas válidas. Es G.
- **Modelo reconocedor (autómata):** máquina que lee una cadena y dice sí o no. Es M.

### 3.3 Jerarquía de Chomsky

Clasifica los lenguajes según su dificultad: qué tan sofisticado es el modelo computacional necesario para computarlos. Cada tipo contiene a los de las filas de abajo, y los regulares son los más restringidos:

| Tipo | Lenguajes | Gramática | Máquina | Memoria |
|---|---|---|---|---|
| 0 | Recursivamente enumerables | Sin restricciones | Máquina de Turing | Cinta |
| 1 | Sensibles al contexto | Sensible al contexto | Autómata finito con n pilas | n pilas |
| **2** | **Libres de contexto (LIC)** | **Libre de contexto** | **Autómata a pila** | **Pila sin límite** |
| 3 | Regulares | Regular | Autómata finito | Solo los estados |

**MiniHTML es de tipo 2**: no es regular y una pila alcanza.

> La fila del tipo 1 sigue la Clase 0. El syllabus nombra ahí a los autómatas linealmente acotados: si lo preguntan, aclará que la clase dice "n pilas".

### 3.4 Por qué un autómata finito no alcanza

Esto lo pide la consigna y tiene su propia sección en el informe.

**Intuición.** (Es el principio del palomar, aunque las clases no usan ese nombre.) Un autómata finito solo recuerda en qué estado está. Si tiene k estados y lee más de k etiquetas `<p>` seguidas, dos cantidades distintas de `<p>` abiertos lo dejan en el **mismo estado**. Desde ahí ya no sabe cuántos cierres faltan, así que acepta alguna cadena mal cerrada o rechaza alguna correcta.

**Demostración (lema de bombeo).** Si L es regular, existe un n tal que toda ω ∈ L con |ω| ≥ n se puede escribir ω = αβγ con |αβ| ≤ n, β ≠ λ y αβⁱγ ∈ L para todo i ≥ 0.

1. Supongamos que MiniHTML es regular, con constante n.
2. Tomamos ω = `<p>`ⁿ `TEXTO` `</p>`ⁿ, que es válida y tiene longitud 2n + 1 ≥ n.
3. Como |αβ| ≤ n, α y β caen dentro de los primeros n símbolos, que son todos `<p>`. Entonces β = `<p>`ˢ con s ≥ 1.
4. Con i = 0 queda `<p>`ⁿ⁻ˢ `TEXTO` `</p>`ⁿ, con más cierres que aperturas: no pertenece al lenguaje.
5. Contradice el lema, así que MiniHTML **no es regular**. ∎

Es el mismo argumento que para aⁿbⁿ y para los paréntesis balanceados.

> **Importante:** esto depende de que la profundidad **no tenga límite**. Si se limita a 3 niveles, el lenguaje pasa a ser regular (ver la receta C6 de la [Guía del código](Guia_del_Codigo.md)).

### 3.5 Gramáticas

Una gramática es una 4-tupla **G = (V, Σ, S, P)**: variables, terminales, símbolo inicial y producciones.

- **Derivación (⇒):** aplicar una regla reemplazando una variable. `S ⇒* w` significa que de S se llega a w en cero o más pasos.
- **Derivación más a la izquierda:** en cada paso se reemplaza la variable que está más a la izquierda.
- **Árbol de derivación:** la raíz es S, los nodos internos son variables y las hojas son terminales o λ. Leyendo las hojas de izquierda a derecha sale la cadena.
- **Ambigua:** alguna cadena tiene dos árboles distintos (o dos derivaciones más a la izquierda distintas).
- **Regular o libre de contexto:** una regular es lineal por derecha (`A → aB`, `A → B`, `A → a`, `A → λ`) o lineal por izquierda (`A → Ba`, `A → B`, `A → a`, `A → λ`). Una libre de contexto admite `A → α`, con una sola variable a la izquierda y cualquier cosa a la derecha. "Libre de contexto" significa que A se reemplaza sin importar qué tiene alrededor.

La regla que una gramática regular **no** puede tener es del tipo `S → a S b`, con la variable en el medio: eso es lo que empareja aperturas con cierres. `E → <b> S </b>` es justamente de ese tipo.

### 3.6 Autómatas a pila

Es un autómata finito **más una pila**. Lee la entrada de izquierda a derecha y de la pila solo ve el **tope**. Es una 7-tupla. La escribimos en el orden de la consigna, que es el mismo del informe:

**M = (Q, Σ, Γ, δ, q₀, Z₀, F)**

En las clases aparece como `M = (Σ, Γ, Q, q₀, Z₀, F, δ)`, y para el no determinista con Δ en lugar de δ. Son los mismos 7 componentes en otro orden.

| Símbolo | Qué es |
|---|---|
| Σ | alfabeto de entrada |
| Γ | alfabeto de la pila |
| Q | estados |
| q₀ | estado inicial |
| Z₀ | símbolo que está en el fondo de la pila al empezar |
| F | estados finales |
| δ | función de transición |

**Cómo se lee una transición:** `δ(q, a, z) = (q', γ)` significa "en el estado q, leyendo a y con z en el tope, paso a q' y **reemplazo z por γ**".

| γ | Operación | Ejemplo nuestro |
|---|---|---|
| `Y z` | **PUSH**: apila Y | leer `<b>` apila B |
| `z` | **sin cambios** | leer TEXTO |
| `λ` | **POP**: saca el tope | leer `</b>` con B en el tope |

- **Bloqueo:** si no hay transición (δ = ∅), la máquina se detiene y rechaza.
- **Transición λ o espontánea:** se aplica **sin consumir** nada de la entrada.
- **Determinista (AFPD):** a lo sumo una opción en cada situación y sin transiciones λ.
- **No determinista (AFPNλ):** puede tener varias opciones, incluidas transiciones λ, así que δ devuelve un **conjunto**: `δ: Q × (Σ ∪ {λ}) × Γ → P(Q × Γ*)`. Acepta si **alguna** rama acepta.
- A diferencia de los autómatas finitos, acá **no** son equivalentes: hay lenguajes libres de contexto que solo se reconocen con no determinismo (por ejemplo, las cadenas capicúas, porque no se sabe cuándo empieza la segunda mitad).
- **Configuración instantánea:** la "foto" **(q, ω, γ)**: estado, lo que falta leer y la pila con el **tope a la izquierda**. Un paso se escribe con ⊢.
- **Aceptación por estado final, L(M):** termina de leer en un estado de F. **Es la que usamos.**
- **Aceptación por pila vacía, N(M):** termina de leer con la pila vacía. Ambos criterios reconocen la misma clase de lenguajes.
- **Teoremas de equivalencia (Clase 8):** L es LIC **si y solo si** existe un autómata a pila M tal que L = N(M). Además, para los AFPNλ, L(M) y N(M) son equivalentes. Por eso es válido aceptar por estado final.

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
M = (Q, Σ, Γ, δ, q0, Z0, F)
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
Γ = { Z0, B, I, P }     B = "hay un <b> abierto", y así con los demás
Q = { q0, qf }          q0 inicial: ahí se procesa toda la entrada
F = { qf }              Z0 = marca del fondo de la pila
```

| N° | Estado | Entrada | Tope | δ(q, a, z) | Operación |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | q0 | TEXTO | X | (q0, X) | Sin cambios |
| 2 | q0 | `<b>` | X | (q0, B X) | Apila B |
| 3 | q0 | `<i>` | X | (q0, I X) | Apila I |
| 4 | q0 | `<p>` | X | (q0, P X) | Apila P |
| 5 | q0 | `</b>` | B | (q0, λ) | Desapila B |
| 6 | q0 | `</i>` | I | (q0, λ) | Desapila I |
| 7 | q0 | `</p>` | P | (q0, λ) | Desapila P |
| 8 | q0 | **λ** | Z0 | (qf, Z0) | Acepta |

X es cualquier símbolo de Γ. Cada fila tiene una sola opción, así que `(q0, X)` abrevia el conjunto `{(q0, X)}`. Cualquier otra combinación da **δ = ∅: bloqueo y rechazo**.

**En criollo:** cada vez que abro algo lo anoto arriba de la pila; cada vez que cierro, me fijo que sea lo que está arriba y lo tacho. Si al terminar solo queda Z0, está todo bien.

```
        TEXTO, X, X
        <b>, X, B X     </b>, B, λ
        <i>, X, I X     </i>, I, λ
        <p>, X, P X     </p>, P, λ
           ┌────────┐
           ▼        │
  ──►  ( q0 ) ──────┘
          │
          │  λ, Z0, Z0
          ▼
       (( qf ))
```

Se lee `entrada, tope, reemplazo`, como en la Clase 8. El diagrama prolijo está en [automata.png](diagramas/automata.png).

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
   Bloqueo: δ(q0, </p>, B) = ∅          RECHAZA
```

Las de α, β y γ están en el informe. **Practicalas en papel**: es muy probable que pidan una en el momento.

### La tabla clave: G ↔ M ↔ código

Responde a la pregunta típica de la evaluación. Conviene saberla de memoria:

| Gramática G | Autómata M | Código (`simular`) |
|---|---|---|
| Terminales Σ | Alfabeto de entrada Σ | Lo que devuelve `tokenizar()` |
| `S → E S` (hermanos) | Lecturas en q0 con la pila a la misma altura | Vueltas del `for` |
| `E → TEXTO` | Regla 1 | `if token == "TEXTO"` |
| Apertura en `E → <x> S </x>` | Apila (reglas 2 a 4) | `pila.append(APERTURAS[token])` |
| La S del medio | La pila crece | Tokens que se leen hasta el cierre |
| Cierre en `E → <x> S </x>` | Desapila si coincide (reglas 5 a 7) | `tope == CIERRES[token]` y `pila.pop()` |
| `S → λ` | Vuelve al símbolo contenedor o a Z0 | Sale del `for`, o el cierre desapila |
| λ ∈ L(G) | `(q0, λ, Z0) ⊢ (qf, λ, Z0)` | Lista de tokens vacía: acepta |
| Ninguna regla genera un cruce | δ vacía, bloqueo | `return False, mensaje, traza` |

---

## 6. El código

El programa está en [src/parser.py](../src/parser.py), tiene unas 80 líneas y solo usa la biblioteca estándar de Python 3. Implementa la **opción B de la consigna: el simulador del autómata M**.

```
"<p>Hola <b>mundo</b></p>"
        │  tokenizar()      análisis léxico
        ▼
['<p>', 'TEXTO', '<b>', 'TEXTO', '</b>', '</p>']
        │  simular()        aplica la tabla δ con una pila
        ▼
ACEPTADA / RECHAZADA + mensaje + traza
```

**La explicación línea por línea está en la [Guía del código](Guia_del_Codigo.md).**

---

## 7. La demo en vivo

### 7.1 Comandos

Ejecutalos **desde la carpeta raíz del repo**. Las **comillas son obligatorias**: sin ellas, la terminal interpreta `<` y `>` como redirecciones.

Modo interactivo, el de la defensa:

```bash
python3 src/parser.py
```

Una cadena:

```bash
python3 src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```

La cadena vacía:

```bash
python3 src/parser.py ""
```

Los 12 tests:

```bash
python3 -m unittest tests/test_parser.py
```

### 7.2 Salida real, explicada

```
Tokens: ['<p>', '<b>', 'TEXTO', '</p>', '</b>']        ← análisis léxico
(q0, <p> <b> TEXTO </p> </b>, Z0)                      ← traza de M
⊢ (q0, <b> TEXTO </p> </b>, P Z0)                      ← apiló P
⊢ (q0, TEXTO </p> </b>, B P Z0)                        ← apiló B
⊢ (q0, </p> </b>, B P Z0)                              ← TEXTO: pila igual
RECHAZADA (w ∉ L(M)). Error de anidamiento: se leyó '</p>' con B en el tope.
```

La traza termina donde no hay transición: acá, `δ(q0, </p>, B) = ∅`.

### 7.3 Cadenas que puede probar, y qué pasa

Probalas todas antes del oral. Están ejecutadas.

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
| `<p> <b> TEXTO </p> </b>` | ❌ anidamiento | Cruce |
| `<p> TEXTO </b>` | ❌ anidamiento | Cierre de otro tipo |
| `<p> <b> TEXTO </b>` | ❌ sintáctico | `<p>` sin cerrar |
| `<p>>` | ❌ sintáctico | El `>` es TEXTO y `<p>` queda abierto |
| `<u> TEXTO </u>` | ❌ léxico | `<u>` no está en Σ |
| `<br>` | ❌ léxico | `<br>` no está en Σ |
| `<p> TEXTO <b </p>` | ❌ léxico | `<b` mal formada |
| `< b > TEXTO </b>` | ❌ léxico | Tiene espacios adentro |
| `<p class=x> TEXTO </p>` | ❌ léxico | No admite atributos |
| `<p/>` y `<>` | ❌ léxico | No son etiquetas válidas |
| `1 < 2` | ❌ léxico | `<` siempre inicia una etiqueta |

**En el modo interactivo, Enter sin escribir nada analiza la cadena vacía**, y `salir` termina.

### 7.4 Léxico o sintáctico

- **Error léxico:** el token ni siquiera es una palabra del alfabeto (`<u>`, `<b`).
- **Error sintáctico:** las palabras son válidas, pero la estructura no (cruce, cierre sin apertura, sin cerrar).

---

## 8. Modificaciones en vivo

**Todo el método, las recetas y los ejercicios están en la [Guía del código](Guia_del_Codigo.md#5-cómo-pensar-cualquier-cambio).** El resumen, que se aplica siempre:

1. **Repetí el pedido** y aclará los casos dudosos.
2. **¿Cambia Σ?** Si aparece un símbolo nuevo.
3. **¿Cambia G?** Qué producciones se agregan o cambian.
4. **¿Cambia M?** Qué transiciones se agregan, se sacan o si hace falta un estado.
5. **Tocá el código** en `tokenizar` o en `simular`.
6. **Probá** una cadena válida y una inválida, y corré los tests.

**Si tenés poco tiempo, practicá en este orden:**

1. **`<u>`** (receta A1): "incorporar una nueva etiqueta" es el primer ejemplo de la consigna.
2. **`<br>`** (B1): "agregar una regla de producción".
3. **`<p>` dentro de `<p>`** (C1): "ajustar una validación", y da el molde de cualquier restricción.
4. **Todo dentro de `<p>`** (D1) o **profundidad** (C6).

---

## 9. Preguntas probables

**¿Por qué un autómata finito no alcanza?**
Tiene memoria finita y MiniHTML permite anidar sin límite. Con `<p>ⁿ TEXTO </p>ⁿ` y n mayor que la cantidad de estados, confunde dos profundidades. Formalmente, por el lema de bombeo: β = `<p>ˢ` y con i = 0 queda desbalanceada.

**¿Por qué una pila y no otra estructura?**
Porque el orden de cierre es LIFO. Con una cola (FIFO) aceptaríamos `<p> <b> </p> </b>`.

**¿Qué es Z0?**
El símbolo de fondo. Si está en el tope, no hay nada abierto. Sirve para aceptar (regla 8) y para detectar cierres sin apertura.

**¿Estado final o pila vacía?**
Estado final: se llega a qf y en la pila queda Z0. Para pasar a pila vacía, ver la receta E3 de la [Guía del código](Guia_del_Codigo.md).

**¿Su autómata es determinista?**
No, es un AFPNλ, por la regla 8, que compite con leer cuando el tope es Z0. Es el único punto no determinista.

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

**¿Por qué no usaron el análisis sintáctico exhaustivo de la Clase 7?**
Porque tiene complejidad exponencial, y G tiene una regla `S → λ`, así que el teorema de la clase no garantiza que termine. El simulador recorre cada token una sola vez.

**¿Implementaron la opción A o la B?**
La opción B: el simulador del autómata a pila. Procesa los tokens en orden y usa una lista como pila, igual que la tabla δ del informe.

**¿Por qué eligieron la opción B?**
Porque cada rama del código corresponde a filas de la tabla δ, y la pila queda a la vista. La consigna pedía una de las dos opciones.

**Si no programaron G, ¿cómo se relaciona el código con la gramática?**
G y M describen el mismo lenguaje. Cada `E → <x> S </x>` corresponde a apilar al leer `<x>` y desapilar al leer `</x>`, y la S del medio son los tokens que se leen entre ambos.

**¿Qué hace el tokenizador?**
El análisis léxico: pasa de texto a símbolos de Σ, normaliza etiquetas y convierte cada palabra en TEXTO. No decide la estructura.

**La consigna toma "Error de anidamiento" como un solo TEXTO. ¿Por qué ustedes generan tres?**
Porque cada palabra es un token, y así γ, que trae `TEXTO TEXTO`, conserva sus dos lecturas. No cambia la clasificación: `S → E S` admite cualquier cantidad de TEXTO seguidos, y la regla 1 no toca la pila.

**¿Por qué mantiene las etiquetas mal formadas?**
Para que el analizador las rechace como error léxico. Si fueran texto, se aceptarían cadenas mal escritas.

**¿Dónde se ve la 7-tupla en el código?**
Q son los textos `"q0"` y `"qf"`. Σ y Γ salen de `ETIQUETAS`, δ son `APERTURAS`, `CIERRES` y las ramas de `simular`, q0 y Z0 son la configuración inicial, y F = {qf} se ve en la regla 8.

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

M          M = (Q, Σ, Γ, δ, q0, Z0, F)     AFPNλ por ESTADO FINAL
           Γ = {Z0,B,I,P}   Q = {q0,qf}   F = {qf}
           (1)   TEXTO, X, X        sin cambios
           (2-4) <x>,   X, Y X      PUSH
           (5-7) </x>,  Y, λ        POP
           (8)   λ,    Z0, Z0 → qf  acepta; único no determinismo
           Otro caso: δ = ∅, bloqueo.

NO REGULAR <p>ⁿ TEXTO </p>ⁿ, β = <p>ˢ, i = 0: desbalance, contradicción.

CÓDIGO     ETIQUETAS :13 → tokenizar :19 → simular :35
           apila :45 · compara :48 · desapila :49 · regla 8 :59

MODIFICAR  Σ? → G? → M? → tokenizar o simular → probar → tests
           Etiqueta común: una entrada en ETIQUETAS.
           Sin pila (<br>): condición de la línea 42.
           Restricción: if antes de apilar (45) con return False, "...", traza.
```

### El día de la defensa

- [ ] Leer este machete.
- [ ] Informe cargado en el aula virtual y entrevista coordinada.
- [ ] Compu cargada, repo actualizado y Python 3.8 o más nuevo.
- [ ] `git status` sin cambios de prácticas en `src/parser.py` ni en los tests.
- [ ] `python3 -m unittest tests/test_parser.py` pasa los 12 tests.
- [ ] Editor abierto en `parser.py` y una terminal en la carpeta raíz del repo.
- [ ] Papel y lapicera para trazas y derivaciones.
- [ ] Todos saben responder la tabla G ↔ M ↔ código: las preguntas son individuales.
