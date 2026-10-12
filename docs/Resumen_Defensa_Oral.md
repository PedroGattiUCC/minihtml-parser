# Resumen para la Defensa Oral — MiniHTML Parser

> Guía de estudio del grupo: primero la **teoría mínima** que hace falta (explicada desde cero), después **qué hicimos en cada fase** y **cómo está hecho el código**, y al final **las preguntas que probablemente haga el docente** y **cómo resolver la modificación en vivo**.
>
> Fuentes: la consigna (`Proyecto_Integrador_Lenguajes.md`), las fases (`docs/Fase1..3`), el código (`src/parser.py`) y las clases transcriptas (`docs/Presentaciones/`).

---

## Índice

1. [El proyecto en 1 minuto](#1-el-proyecto-en-1-minuto)
2. [Teoría desde cero](#2-teoría-desde-cero)
3. [Fase 1 — La gramática G](#3-fase-1--la-gramática-g)
4. [Fase 2 — El autómata a pila M](#4-fase-2--el-autómata-a-pila-m)
5. [Fase 3 — El código](#5-fase-3--el-código)
6. [La tabla clave: G ↔ M ↔ código](#6-la-tabla-clave-g--m--código)
7. [Modificaciones en vivo](#7-modificaciones-en-vivo)
8. [Preguntas probables y respuestas](#8-preguntas-probables-y-respuestas)
9. [Machete de una página](#9-machete-de-una-página)
10. [Reparto sugerido para la exposición](#10-reparto-sugerido-para-la-exposición)

---

## 1. El proyecto en 1 minuto

**Problema:** en HTML las etiquetas tienen que estar bien anidadas. `<p><b>hola</b></p>` está bien; `<p><b>hola</p></b>` está mal porque se cerró `<p>` antes que `<b>`, que fue la última en abrirse.

**MiniHTML** es un HTML de juguete con solo 7 "palabras" (tokens):

```
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
```

Una cadena es válida si:
1. Puede tener texto, etiquetas anidadas o estar vacía.
2. Toda etiqueta que se abre se cierra con la del mismo tipo.
3. Se cierran en orden **LIFO** (*Last-In, First-Out*): la última que se abrió es la primera que se cierra.

**Lo que hicimos (3 fases):**

| Fase | Qué es | En una frase |
|---|---|---|
| 1 | Gramática libre de contexto **G** | Las **reglas que generan** todas las cadenas válidas. |
| 2 | Autómata a pila **M** | La **máquina que reconoce** (acepta o rechaza) cadenas usando una pila. |
| 3 | Programa en Python | Implementamos **las dos cosas** (la opción A y la B de la consigna) y verificamos que siempre dan el mismo resultado. |

**La idea central que tienen que poder decir de memoria:**
> MiniHTML **no es un lenguaje regular**, porque para saber si las etiquetas cierran bien hay que *recordar* cuántas y cuáles se abrieron, y un autómata finito tiene memoria finita. Por eso usamos una **gramática libre de contexto** para describirlo y un **autómata a pila** para reconocerlo: la pila es justamente una memoria LIFO, igual que el orden en que se cierran las etiquetas.

---

## 2. Teoría desde cero

### 2.1 Alfabeto, cadena, lenguaje (Clase 1)

- **Alfabeto (Σ):** conjunto finito de símbolos. En nuestro caso cada símbolo es un *token* entero (`<b>` es **un** símbolo, no tres caracteres).
- **Cadena (palabra):** secuencia finita de símbolos del alfabeto. Ej: `<p> TEXTO </p>` es una cadena de longitud 3.
- **λ (lambda):** la **cadena vacía**, de longitud 0. En MiniHTML es válida (un documento vacío).
- **Σ\*:** el conjunto de **todas** las cadenas posibles con ese alfabeto (válidas o no).
- **Lenguaje (L):** un subconjunto de Σ\*; las cadenas "que nos interesan". MiniHTML = las cadenas de Σ\* bien anidadas.
- **w ∈ L** se lee "la cadena w pertenece al lenguaje". Nuestro programa responde exactamente esa pregunta.

### 2.2 Dos formas de describir un lenguaje (Clase 0)

| Modelo **generativo** | Modelo **reconocedor** |
|---|---|
| **Gramática**: reglas para *producir* todas las cadenas válidas. | **Autómata**: máquina que *lee* una cadena y dice sí/no. |
| Fase 1: G | Fase 2: M |

### 2.3 Jerarquía de Chomsky (Clase 0)

Clasifica lenguajes según qué tan "poderosa" tiene que ser la máquina que los reconoce. Cada nivel contiene a los de abajo:

| Tipo | Lenguajes | Gramática | Máquina | Memoria |
|---|---|---|---|---|
| 3 | **Regulares** | Regular | Autómata Finito (AFD/AFN) | Solo los estados (finita) |
| 2 | **Independientes / Libres de contexto (LIC)** | **Libre de contexto (GIC/GLC)** | **Autómata a Pila (AP)** | **Una pila (LIFO), sin límite** |
| 1 | Sensibles al contexto | Sensible al contexto | Autómata linealmente acotado | Cinta acotada |
| 0 | Recursivamente enumerables | Sin restricciones | Máquina de Turing | Cinta infinita |

**MiniHTML es Tipo 2.** No es Tipo 3 (lo demostramos abajo) y alcanza con Tipo 2.

### 2.4 Autómata finito y su límite (Clases 3, 3b y 6)

Un **autómata finito (AF)** es una máquina con una cantidad **fija** de estados que lee la cadena de izquierda a derecha y en cada símbolo cambia de estado. Al terminar, acepta si quedó en un estado final. Su **única memoria es el estado en el que está**.

Sirve para cosas como "¿tiene una cantidad par de `a`?" (dos estados: par/impar). **No sirve** para contar sin límite.

#### ¿Por qué un AF no puede validar MiniHTML? (esto lo pide el informe)

Explicación intuitiva:
- Pensá en la cadena `<p><p><p>…<p> TEXTO </p>…</p></p></p>` con **n** aperturas y **n** cierres.
- Para aceptarla, la máquina tiene que "acordarse" de **n** al terminar de leer las aperturas.
- Un AF tiene, digamos, **k** estados. Si n > k, por el **principio del palomar** dos cantidades distintas de `<p>` abiertos lo dejan en el **mismo estado**, así que la máquina ya no las distingue → acepta algo mal cerrado o rechaza algo bien cerrado.

Explicación formal con el **Lema de Bombeo** (Clase 6):

> Si L es regular, existe un número n tal que toda cadena ω ∈ L con |ω| ≥ n se puede partir como ω = αβγ con:
> 1. |αβ| ≤ n
> 2. β ≠ λ
> 3. αβⁱγ ∈ L para todo i ≥ 0 (se puede "bombear" β).

Para demostrar que algo **no** es regular, se elige una cadena larga donde **ninguna** partición se pueda bombear:
1. Sea n cualquiera. Tomamos ω = `<p>`ⁿ `TEXTO` `</p>`ⁿ, que es válida y tiene longitud ≥ n.
2. Como |αβ| ≤ n, α y β caen dentro de los primeros n símbolos, que son todos `<p>`. Entonces β = `<p>`ˢ con s ≥ 1.
3. Bombeamos con i = 0 (sacamos β): queda `<p>`ⁿ⁻ˢ `TEXTO` `</p>`ⁿ → hay **más cierres que aperturas** → no pertenece a MiniHTML.
4. Contradicción → **MiniHTML no es regular.** ∎

(Es el mismo argumento de la Clase 6 para `aⁿbⁿ` y para paréntesis balanceados: MiniHTML "contiene" a esos lenguajes.)

### 2.5 Gramáticas (Clases 5 y 7)

Una **gramática** es una 4-tupla **G = (V, Σ, S, P)**:

| Símbolo | Qué es | En nuestro proyecto |
|---|---|---|
| **V** | Variables / no terminales (se siguen reemplazando) | `{S, E}` |
| **Σ** | Terminales (los símbolos finales de la cadena) | los 7 tokens |
| **S** | Símbolo inicial / axioma | `S` |
| **P** | Reglas de producción `A → α` | las 6 reglas |

- **Derivación (⇒):** aplicar una regla reemplazando una variable. `S ⇒* w` significa "de S se llega a w en cero o más pasos".
- **L(G):** todas las cadenas de terminales que se pueden derivar desde S.
- **Derivación más a la izquierda (leftmost):** en cada paso se reemplaza la variable que está más a la izquierda.
- **Árbol de derivación:** la raíz es S, los nodos internos son variables, las hojas son terminales o λ. Leyendo las hojas de izquierda a derecha se obtiene la cadena.
- **Gramática ambigua:** si alguna cadena tiene **dos árboles distintos** (o dos derivaciones leftmost distintas). Ej. clásico: `E → E+E | E*E | a` con `a+a*a`.

**Gramática regular vs. libre de contexto:**
- **Regular:** reglas muy restringidas, tipo `A → aB`, `A → a`, `A → λ` (a lo sumo una variable y siempre en el mismo extremo).
- **Libre de contexto (GIC):** a la izquierda hay **una sola variable** y a la derecha **cualquier cosa**: `A → α`. "Libre de contexto" = la variable se reemplaza sin importar qué tenga alrededor.
- La regla típica que una regular **no** puede tener: `S → a S b` (la variable en el medio, rodeada de terminales). Eso es lo que permite "emparejar" aperturas con cierres. Nuestras reglas `E → <b> S </b>` son exactamente de ese tipo.

### 2.6 Autómata a pila (Clase 8)

Es un autómata finito **más una pila**. Tiene dos "cintas":
1. **Cinta de entrada:** la cadena, que se lee de izquierda a derecha.
2. **Pila:** memoria LIFO sin límite. Solo se ve el **tope**.

Definición de la cátedra — **7-tupla**: **M = (Σ, Γ, Q, q₀, Z₀, F, Δ)**

| Símbolo | Qué es |
|---|---|
| Σ | alfabeto de entrada |
| Γ | alfabeto de la **pila** (lo que se puede apilar) |
| Q | estados |
| q₀ | estado inicial |
| Z₀ | símbolo que está al **fondo** de la pila al empezar (marcador de fondo) |
| F | estados finales / de aceptación |
| Δ (o δ) | función de transición |

**Cómo se lee una transición:** `Δ(q, a, z) = (q', γ)` → "estando en el estado **q**, leyendo **a** de la entrada y con **z** en el tope de la pila, paso al estado **q'** y **reemplazo z por γ**". Según γ:

| γ | Operación | Ejemplo nuestro |
|---|---|---|
| `Y z` | **PUSH** (apila Y encima) | leer `<b>`: apila `B` |
| `z` | **no-op** (deja todo igual) | leer `TEXTO` |
| `λ` | **POP** (saca el tope) | leer `</b>` con `B` en el tope |

Si para la combinación (estado, símbolo, tope) **no hay transición** (Δ = ∅), la máquina **se bloquea** y la cadena se rechaza.

**Transición λ (espontánea):** `Δ(q, λ, z)` = la máquina cambia de estado **sin leer** nada de la entrada.

**Determinista vs. no determinista:**
- **AFPD (determinista):** en cada situación hay **a lo sumo una** opción y **no** hay transiciones λ. `δ: Q × Σ × Γ → Q × Γ*`.
- **AFPN-λ (no determinista con λ):** puede haber **varias** opciones, incluidas transiciones λ. `Δ: Q × (Σ ∪ {λ}) × Γ → P(Q × Γ*)` (el resultado es un **conjunto** de opciones). Acepta si **alguna** de las ramas acepta.
- ⚠️ A diferencia de los AF (donde AFD ≡ AFN), en autómatas a pila **AFPD ⊂ AFPN-λ**: hay lenguajes libres de contexto que solo se reconocen con no determinismo (ej. palíndromos pares `wwᴿ`, porque no se sabe dónde está la mitad).

**Configuración instantánea:** la "foto" de la máquina en un momento: **(q, ω, γ)** = (estado actual, lo que falta leer, contenido de la pila con el **tope a la izquierda**). Un paso se escribe con **⊢**:
```
(q0, <b> TEXTO </b>, Z0)  ⊢  (q0, TEXTO </b>, B Z0)
```
Una **traza** es la secuencia de configuraciones desde `(q₀, w, Z₀)` hasta el final.

**Dos formas de aceptar:**
- **Por estado final, L(M):** termina de leer y está en un estado de F. ← **la que usamos**
- **Por vaciado de pila, N(M):** termina de leer y la pila quedó vacía (no importa el estado).
- Para un mismo M pueden dar lenguajes distintos, pero el **teorema** dice que cualquier AP de un tipo se puede convertir en uno del otro tipo que acepta lo mismo.

**Teorema de equivalencia (Clase 8, diap. 21):** un lenguaje es libre de contexto **si y solo si** existe un autómata a pila que lo reconoce. GIC ↔ AP. Por eso tiene sentido hacer G y M para el mismo lenguaje y comprobar que coinciden.

---

## 3. Fase 1 — La gramática G

📄 Detalle completo: [Fase1_Gramatica.md](Fase1_Gramatica.md)

```
G = (V, Σ, S, P)
V = { S, E }
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
Símbolo inicial: S
```

| N° | Regla | Significado |
|:-:|---|---|
| 1 | `S → E S` | Una secuencia es un elemento seguido de más secuencia. |
| 2 | `S → λ` | …o nada (permite documento vacío y `<p></p>`). |
| 3 | `E → TEXTO` | Un elemento puede ser texto. |
| 4 | `E → <b> S </b>` | …o una negrita con contenido adentro. |
| 5 | `E → <i> S </i>` | …o una cursiva con contenido adentro. |
| 6 | `E → <p> S </p>` | …o un párrafo con contenido adentro. |

**Cómo explicarla:**
- **S = "secuencia / contenido"**: cero o más elementos uno al lado del otro (hermanos). Sirve tanto para el documento entero como para lo que va dentro de una etiqueta.
- **E = "elemento"**: una sola cosa: un texto o un bloque `<tag> … </tag>`.

**¿Por qué garantiza LIFO?** En las reglas 4–6 la apertura y el cierre **aparecen juntos en la misma regla**, con S en el medio. Todo lo que se genere dentro de S queda **encerrado** entre esa apertura y ese cierre, así que no hay forma de generar `<p> <b> … </p> </b>` (habría que "cruzar" dos reglas).

**¿Por qué no es ambigua?** Mirando el próximo token siempre se sabe qué regla usar:
- Viene `TEXTO` o una apertura → `S → E S`, y después la regla de E que corresponda a ese token.
- Viene un cierre o se terminó la cadena → `S → λ`.
Como siempre hay una sola opción, cada cadena tiene un único árbol.

**Ejemplo — derivación leftmost de α = `<p> TEXTO <b> TEXTO </b> </p>`:**
```
S ⇒ E S                                   (1)
  ⇒ <p> S </p> S                          (6)
  ⇒ <p> E S </p> S                        (1)
  ⇒ <p> TEXTO S </p> S                    (3)
  ⇒ <p> TEXTO E S </p> S                  (1)
  ⇒ <p> TEXTO <b> S </b> S </p> S         (4)
  ⇒ <p> TEXTO <b> E S </b> S </p> S       (1)
  ⇒ <p> TEXTO <b> TEXTO S </b> S </p> S   (3)
  ⇒ <p> TEXTO <b> TEXTO </b> S </p> S     (2)  S → λ
  ⇒ <p> TEXTO <b> TEXTO </b> </p> S       (2)
  ⇒ <p> TEXTO <b> TEXTO </b> </p>         (2)
```
Árbol (simplificado):
```
              S
           /     \
          E       S
       /  |  \    |
    <p>   S  </p> λ
        /   \
       E     S
       |    /  \
    TEXTO  E     S
         / | \    |
      <b>  S </b> λ
          / \
         E   S
         |   |
       TEXTO λ
```
Tip para el oral: **cada `E` con 3 hijos es un par apertura/cierre**; cada `S` que va a λ es "acá no hay más hermanos".

---

## 4. Fase 2 — El autómata a pila M

📄 Detalle completo: [Fase2_AutomataPila.md](Fase2_AutomataPila.md)

```
M = (Σ, Γ, Q, q0, Z0, F, Δ)
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
Γ = { Z0, B, I, P }        ← B = "hay un <b> abierto", etc.
Q = { q0, qf }
q0 = estado inicial (donde se procesa todo)
Z0 = fondo de la pila
F  = { qf }
```

**Tabla de transiciones** (X = cualquier símbolo de pila):

| N° | Estado | Lee | Tope | → Nuevo estado, reemplazo | Operación |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | q0 | TEXTO | X | (q0, X) | no-op |
| 2 | q0 | `<b>` | X | (q0, B X) | PUSH B |
| 3 | q0 | `<i>` | X | (q0, I X) | PUSH I |
| 4 | q0 | `<p>` | X | (q0, P X) | PUSH P |
| 5 | q0 | `</b>` | B | (q0, λ) | POP |
| 6 | q0 | `</i>` | I | (q0, λ) | POP |
| 7 | q0 | `</p>` | P | (q0, λ) | POP |
| 8 | q0 | **λ** | Z0 | (qf, Z0) | aceptar |

Cualquier otra combinación → **Δ = ∅ → bloqueo → rechazo**. Ej: leer `</p>` con `B` en el tope.

**La idea en criollo:** "cada vez que abro algo, lo anoto arriba de la pila; cada vez que cierro algo, me fijo que sea lo que está arriba de todo y lo tacho. Si al final solo queda el fondo Z0, está todo bien".

**Diagrama:**
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
(rótulo: `lo que leo, tope / con qué lo reemplazo`)

**Decisiones de diseño que hay que saber justificar:**
- **Aceptación por estado final** (no por vaciado): al final la pila tiene `Z0` (no está vacía) y pasamos a `qf`.
- **¿Por qué es no determinista?** Por la regla 8. Cuando el tope es `Z0` y estoy en `q0`, puedo **leer** el siguiente token (ej. `<p>` con regla 4) **o** saltar a `qf` sin leer (regla 8). Dos opciones = no determinismo. Es el **único** punto no determinista.
- **¿Eso causa problemas?** No: si salta a `qf` antes de terminar la entrada, se queda trabado (qf no tiene transiciones) con entrada sin leer → esa rama no acepta. La única rama que puede aceptar es la que salta a `qf` **al final**, y esa es la que sigue el programa.

**Traza de α = `<p> TEXTO <b> TEXTO </b> </p>`:**
```
   (q0, <p> TEXTO <b> TEXTO </b> </p>, Z0)       inicial
⊢  (q0, TEXTO <b> TEXTO </b> </p>,     P Z0)     regla 4  PUSH P
⊢  (q0, <b> TEXTO </b> </p>,           P Z0)     regla 1  TEXTO
⊢  (q0, TEXTO </b> </p>,             B P Z0)     regla 2  PUSH B
⊢  (q0, </b> </p>,                   B P Z0)     regla 1  TEXTO
⊢  (q0, </p>,                          P Z0)     regla 5  POP B
⊢  (q0, λ,                               Z0)     regla 7  POP P
⊢  (qf, λ,                               Z0)     regla 8  ACEPTA
```

**Traza de una inválida `<p> <b> TEXTO </p> </b>`:**
```
   (q0, <p> <b> TEXTO </p> </b>, Z0)
⊢  (q0, <b> TEXTO </p> </b>,   P Z0)
⊢  (q0, TEXTO </p> </b>,     B P Z0)
⊢  (q0, </p> </b>,           B P Z0)
   BLOQUEO: Δ(q0, </p>, B) = ∅ → se esperaba cerrar <b> primero
```

Las trazas de β y γ están en la Fase 2 y se leen igual. **Practiquen hacer una traza a mano en el pizarrón**: es muy probable que la pidan.

---

## 5. Fase 3 — El código

📄 Detalle: [Fase3_Implementacion.md](Fase3_Implementacion.md) · Código: [src/parser.py](../src/parser.py)

La consigna pedía la opción A **o** la B. **Hicimos las dos** y el programa compara los resultados (`L(G) = L(M)`).

### Flujo de una cadena

```
"<p>Hola <b>mundo</b></p>"
        │
        ▼  tokenizar()                         (análisis léxico)
['<p>', 'TEXTO', '<b>', 'TEXTO', '</b>', '</p>']
        │
        ├──► AutomataPilaMiniHTML.simular()     (opción B: el autómata M)
        └──► AnalizadorRecursivoMiniHTML.validar() (opción A: la gramática G)
        │
        ▼
ACEPTADA / RECHAZADA + diagnóstico + ¿coinciden?
```

### Las 4 partes de `parser.py`

**0. `ETIQUETAS`** ([parser.py:32](../src/parser.py#L32)) — diccionario `{"b": "B", "i": "I", "p": "P"}`: etiqueta → símbolo de pila. Es la **única** definición del lenguaje; M y G se arman a partir de acá. Por eso agregar una etiqueta es una línea.

**1. Tokenizador** ([parser.py:49](../src/parser.py#L49)) — el **analizador léxico**. Convierte el texto en la lista de tokens de Σ:
- Etiquetas válidas `<b>`, `</b>`, etc. → se normalizan (minúscula; también acepta `<\b>` como cierre, la notación de la consigna).
- Cada **palabra** de texto → un token `TEXTO` (así funciona tanto con `TEXTO` literal como con HTML real como `Hola mundo`).
- Algo mal formado (`<b`, `< b >`, `<p class=x>`) se deja tal cual, para que después se rechace como **error léxico**.

**2. `AutomataPilaMiniHTML`** ([parser.py:83](../src/parser.py#L83)) — el **autómata M** (opción B). La pila es una lista de Python: `pila = ["Z0"]`, el tope es `pila[-1]`. El método `simular` ([parser.py:131](../src/parser.py#L131)) recorre los tokens:

| Token | Código | Regla de Δ |
|---|---|---|
| `TEXTO` | no toca la pila ([:160](../src/parser.py#L160)) | regla 1 |
| apertura | `pila.append(marcador)` ([:164](../src/parser.py#L164)) | reglas 2–4 PUSH |
| cierre que coincide con el tope | `pila.pop()` ([:172](../src/parser.py#L172)) | reglas 5–7 POP |
| cierre que **no** coincide | error y `return` | Δ = ∅, bloqueo |
| cualquier otra cosa | error léxico | símbolo fuera de Σ |
| fin de la entrada y `pila == ["Z0"]` ([:193](../src/parser.py#L193)) | pasa a `qf`, acepta | regla 8 (λ) |
| fin con cosas en la pila | error "sin cerrar" | no hay transición |

Además va guardando cada configuración `(q, ω, γ)` para imprimir la **traza**.

**3. `AnalizadorRecursivoMiniHTML`** ([parser.py:224](../src/parser.py#L224)) — la **gramática G** (opción A), un **analizador descendente recursivo**: **una función por cada variable** de la gramática.
- `parse_S()` ([:241](../src/parser.py#L241)): mientras el próximo token no sea un cierre ni el final, llama a `parse_E()` (eso es `S → E S` repetido); cuando ve un cierre o el final, termina (`S → λ`). La recursión por derecha `S → E S` se escribe como un `while`.
- `parse_E()` ([:248](../src/parser.py#L248)): si es `TEXTO`, lo consume (`E → TEXTO`). Si es una apertura `<x>`: la consume, llama a `parse_S()` para el contenido, y exige que el siguiente sea `</x>` (`E → <x> S </x>`).
- **¿Dónde está la pila acá?** En la **pila de llamadas** de Python: cada `parse_E` abierto "recuerda" qué etiqueta tiene que cerrar. Es la misma idea LIFO que el autómata.

**4. Interfaz** — `analizar_cadena()` corre los dos analizadores y muestra resultados; `ejecutar_casos_oficiales()` prueba α, β, γ, λ y 4 inválidas; `modo_interactivo()` es la consola para la defensa.

### Errores que reporta

| Error | Ejemplo | Qué dice |
|---|---|---|
| Anidamiento cruzado (LIFO) | `<p> <b> TEXTO </p> </b>` | se leyó `</p>` pero el tope es `B` |
| Cierre sin apertura | `<p> TEXTO </p> </b>` | cerrar `</b>` con pila vacía |
| Quedó algo sin cerrar | `<p> <b> TEXTO </b>` | etiquetas sin cerrar: `<p>` |
| Etiqueta desconocida | `<u> TEXTO </u>` | `<u>` no pertenece a Σ |
| Mal formada | `<p> TEXTO <b </p>` | `<b` no pertenece a Σ |

**Léxico vs. sintáctico:** error **léxico** = el token ni siquiera es una palabra del alfabeto (`<u>`, `<b`). Error **sintáctico** = las palabras son válidas pero el **orden/estructura** está mal (`<p> <b> </p> </b>`).

### Cómo correrlo (para la demo)

```bash
python3 src/parser.py
```
(corre los casos oficiales y abre el modo interactivo; escribir `salir` para terminar, `test` para repetir los casos)

```bash
python3 src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```
(una cadena con su traza)

```bash
python3 -m unittest tests/test_parser.py
```
(14 tests automáticos; hoy pasan todos)

---

## 6. La tabla clave: G ↔ M ↔ código

Esta tabla responde la típica pregunta "¿cómo se relaciona la gramática con el autómata y con el código?":

| Gramática G | Autómata M | Código |
|---|---|---|
| Terminales Σ | Alfabeto de entrada Σ | tokens que devuelve `tokenizar()` |
| Variable S (secuencia) | quedarse en q0 leyendo hermanos | `parse_S()` / el `for` de `simular` |
| Variable E (elemento) | — | `parse_E()` |
| `E → TEXTO` | regla 1: no-op | `if token == "TEXTO"` |
| apertura en `E → <x> S </x>` | PUSH X | `pila.append(...)` / `parse_E` consume `<x>` |
| cierre en `E → <x> S </x>` | POP si el tope es X | `pila.pop()` / `parse_E` exige `</x>` |
| la S del medio (anidamiento) | la pila crece en profundidad | recursión `parse_E → parse_S → parse_E…` |
| `S → λ` | vuelvo al tope de la etiqueta padre o a Z0 | `parse_S` sale del `while` |
| λ ∈ L(G) (documento vacío) | `(q0, λ, Z0) ⊢ (qf, λ, Z0)` | lista vacía → acepta |
| No hay regla que genere un cruce | Δ = ∅ → bloqueo | `return False, mensaje` |
| L(G) | L(M) | "Equivalencia L(G) = L(M): VERIFICADA" |

---

## 7. Modificaciones en vivo

La consigna dice que el docente va a pedir **una modificación menor** en el momento. Las más probables:

### 7.1 Agregar una etiqueta nueva (ej. `<u>`) — una línea

En [parser.py:32](../src/parser.py#L32):
```python
ETIQUETAS: Dict[str, str] = {
    "b": "B",
    "i": "I",
    "p": "P",
    "u": "U",   # nueva
}
```
**Qué decir:** "esto agrega `<u>` y `</u>` a Σ, `U` a Γ, las transiciones PUSH/POP de `U` a Δ, y la regla `E → <u> S </u>` a G". Probar con `<p> <u> TEXTO </u> </p>`.

### 7.2 Agregar una etiqueta **autocerrada** (ej. `<br>`, que no tiene cierre)

En teoría: nueva regla **`E → <br>`** en G, y en M una transición **no-op** `Δ(q0, <br>, X) = (q0, X)` (igual que TEXTO, no toca la pila).

En código (probado, funciona):
```python
# debajo de ETIQUETAS
VACIAS = {"<br>"}

# en simular(), línea ~160:
if token == "TEXTO" or token in VACIAS:

# en parse_E(), línea ~252:
if tok == "TEXTO" or tok in VACIAS:
```
`<p> TEXTO <br> TEXTO </p>` → aceptada; `<p> </br> </p>` → rechazada.

### 7.3 Agregar una restricción (ej. "no puede haber un `<p>` dentro de otro `<p>`")

En el autómata, antes de apilar ([parser.py:164](../src/parser.py#L164)), dentro del `elif token in self.apertura_a_pila:` (probado, funciona):
```python
marcador = self.apertura_a_pila[token]
if marcador == "P" and "P" in pila:
    msg = "Error sintáctico: no se permite un <p> dentro de otro <p>."
    traza.append(f"BLOQUEO: Δ({estado}, {token}, {tope}) = ∅. {msg}")
    return finalizar(False, msg)
```
Ojo: si solo se cambia el autómata, el programa va a mostrar **DISCREPANCIA** con G (porque G sigue aceptándolo). Está bien explicarlo: "para G habría que separar el contenido de un párrafo en otra variable, por ejemplo `E → <p> S' </p>` donde `S'` no puede generar `<p>`".

> **Consejo:** antes del oral, practiquen las 3 en una rama aparte y después hagan `git checkout -- src/parser.py` para volver atrás.

---

## 8. Preguntas probables y respuestas

**¿Por qué un autómata finito no alcanza?**
Porque tiene memoria finita (solo estados) y MiniHTML permite anidar sin límite. Para cerrar bien hay que recordar cuántas y cuáles etiquetas se abrieron. Con `<p>ⁿ TEXTO </p>ⁿ` y n mayor que la cantidad de estados, el AF confunde dos profundidades distintas. Formalmente: lema de bombeo, bombeando β = `<p>`ˢ con i = 0 queda desbalanceada.

**¿Por qué una pila y no otra estructura?**
Porque el orden de cierre es LIFO: la última abierta es la primera que se cierra, y la pila es exactamente LIFO. Con una cola (FIFO) aceptaríamos `<p> <b> </p> </b>`.

**¿Qué es Z0 y para qué sirve?**
El símbolo de fondo de pila. Sirve para saber cuándo la pila está "vacía" de etiquetas: si el tope es Z0, no hay nada abierto. Lo usamos para aceptar (regla 8) y para detectar cierres sin apertura.

**¿Aceptan por estado final o por vaciado de pila?**
Por estado final (llegar a qf). La pila termina con Z0. Si quisiéramos vaciado de pila, cambiaríamos la regla 8 por `Δ(q0, λ, Z0) = (q0, λ)` (sacar Z0); por el teorema de la Clase 8 ambos criterios reconocen la misma clase de lenguajes.

**¿Su autómata es determinista?**
No, es un AFPN-λ. El único no determinismo es la regla 8 (λ con tope Z0), que compite con leer el siguiente token cuando el tope es Z0. En la práctica no molesta porque saltar a qf antes de terminar deja entrada sin leer y esa rama muere.

**¿Se podría hacer determinista?** *(pregunta difícil, por si acaso)*
Sí. Con la definición de la cátedra (AFPD sin transiciones λ), usando dos estados: q0 = "no hay nada abierto" (final) y q1 = "hay algo abierto". Al abrir una etiqueta desde q0 se apila una marca especial de "primer nivel" (ej. `B̂`); al cerrar esa marca se vuelve a q0. Así no hace falta la λ y q0 ∈ F acepta al terminar.

**¿Su gramática es ambigua? ¿Cómo lo saben?**
No. Con el próximo token siempre hay una sola regla posible (apertura/texto → `S → E S`; cierre/fin → `S → λ`), así que cada cadena tiene un único árbol / una única derivación leftmost. (En general decidir si una GIC es ambigua es *indecidible*, pero para esta se ve a mano.)

**¿Por qué dos variables (S y E) y no una sola?**
Para separar "secuencia de hermanos" de "un elemento". Si usáramos algo como `S → SS | <b> S </b> | TEXTO | λ`, sería **ambigua** (`SS` permite agrupar hermanos de varias formas, como el ejemplo `S → aSb | SS | λ` de la Clase 7).

**¿Por qué S → λ?**
Para permitir el documento vacío, etiquetas vacías (`<p></p>`), y para "cortar" la secuencia de hermanos.

**¿Qué relación hay entre G y M?**
El teorema de la Clase 8: un lenguaje es libre de contexto si y solo si lo reconoce un autómata a pila. Concretamente: cada `E → <x> S </x>` es un PUSH al leer `<x>` y un POP al leer `</x>`; la S del medio es la pila creciendo; ver tabla de la sección 6. El programa corre los dos y verifica que siempre coinciden.

**¿Dónde está la pila en el analizador recursivo?**
Es implícita: la pila de llamadas de Python. Cada `parse_E` que está esperando su cierre es como un símbolo en la pila.

**¿Qué diferencia hay entre error léxico y sintáctico?**
Léxico: el token no es del alfabeto (`<u>`, `<b`). Sintáctico: los tokens son válidos pero la estructura no (cruce, cierre sin apertura, sin cerrar).

**¿Qué pasa con la cadena vacía?**
Es válida. En G: `S ⇒ λ`. En M: `(q0, λ, Z0) ⊢ (qf, λ, Z0)`.

**¿Qué pasa con `<p></p>`?**
Válida: `E → <p> S </p>` con `S → λ`. En M: PUSH P, POP P, queda Z0, acepta.

**¿Qué pasa si escribo HTML real, tipo `<p>Hola <b>mundo</b></p>`?**
El tokenizador convierte cada palabra en `TEXTO`, así que funciona igual que la versión con tokens.

**¿Qué es una configuración instantánea?**
La terna (estado, entrada que falta leer, contenido de la pila con el tope a la izquierda). La traza es la secuencia de configuraciones unidas por ⊢.

---

## 9. Machete de una página

```
LENGUAJE      Σ = {<b>,<i>,<p>,</b>,</i>,</p>,TEXTO}   — es Tipo 2 (libre de contexto), NO regular

GRAMÁTICA     G = (V, Σ, S, P),  V = {S, E}
              S → E S | λ
              E → TEXTO | <b> S </b> | <i> S </i> | <p> S </p>
              no ambigua · apertura y cierre en la misma regla ⇒ LIFO

AUTÓMATA      M = (Σ, Γ, Q, q0, Z0, F, Δ)       AFPN-λ, acepta por ESTADO FINAL
              Γ = {Z0, B, I, P}   Q = {q0, qf}   F = {qf}
              TEXTO, X / X          (no-op)
              <x>,   X / Xmay X     (PUSH)
              </x>,  Xmay / λ       (POP)
              λ,     Z0 / Z0  → qf  (aceptar; único no determinismo)
              otro caso: Δ = ∅ → bloqueo → rechazo

TRAZA         (q, lo que falta, pila con tope a la izq.)  ⊢  …

NO REGULAR    <p>ⁿ TEXTO </p>ⁿ, β = <p>ˢ, bombeo i=0 ⇒ desbalance ⇒ contradicción

CÓDIGO        ETIQUETAS (una fuente de verdad) → tokenizar() → 
              AutomataPilaMiniHTML.simular()   [opción B, pila = lista]
              AnalizadorRecursivoMiniHTML      [opción A, parse_S / parse_E]
              → compara L(G) = L(M)

AGREGAR TAG   una línea en ETIQUETAS: "u": "U"
```

---

## 10. Reparto sugerido para la exposición

La consigna exige que **participen todos**. Una forma de dividirlo (4 personas):

| Integrante | Parte | Secciones |
|---|---|---|
| 1 | Problema + por qué no alcanza un AF (Chomsky, lema de bombeo) | 1, 2.1–2.4 |
| 2 | Fase 1: gramática, árbol y derivación de α | 2.5, 3 |
| 3 | Fase 2: autómata, tabla, traza en el pizarrón | 2.6, 4 |
| 4 | Fase 3: código, demo en vivo, modificación | 5, 7 |

Igual **todos** deberían poder responder la sección 8 y la tabla de la sección 6, porque las preguntas pueden ser individuales.

### Detalles a revisar antes de entregar
- El `README.md` figura con un solo autor; para la carátula del informe pongan a todos los integrantes.
- Llevar la compu con Python 3 andando y probar `python3 src/parser.py` antes de entrar.
