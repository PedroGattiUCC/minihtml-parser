# Guía para la defensa: MiniHTML Parser

Esta es **la única guía que hace falta estudiar**. Se lee y se practica en **1 h 30**, y cubre lo que se evalúa en la entrevista.

> **Material interno: no se entrega.** Los comandos, cadenas, mensajes y recetas se ejecutaron sobre el código real. Los números de línea son los de [src/parser.py](../src/parser.py) sin modificar.

## Cómo estudiarla

| Tiempo | Qué hacer | Sabés que está cuando... |
|---|---|---|
| 15 min | Secciones 1 a 3 | Explicás sin mirar por qué un AF no alcanza. |
| 20 min | Sección 4 (G) y 5 (M) | Escribís G y las 8 reglas de memoria. |
| 10 min | Sección 6 (traza) | Hacés en papel la traza de `<p> <b> TEXTO </b> </p>`. |
| 15 min | Sección 7 (código), con `parser.py` abierto | Señalás dónde apila, dónde desapila y de dónde sale cada error. |
| 20 min | Sección 9, haciendo los cambios en la compu | Hacés las recetas 1, 2 y 3 sin mirar. |
| 10 min | Sección 10, tapando las respuestas | Respondés cada pregunta en dos frases. |

**Lo mínimo si hay muy poco tiempo:** sección 3, las 8 reglas de M, la tabla de la sección 7 y las recetas 1 y 2.

---

## 1. Qué evalúa la profe

| Parte | Peso | Qué pasa |
|---|---|---|
| Modelado (G y M) | 35 % | Sale del informe: 4-upla y 7-upla, tabla δ y trazas sin errores. |
| Implementación | 35 % | Código limpio y modular, que sigue fielmente a M y maneja bien los errores. |
| Defensa oral | 30 % | **Testeo en vivo:** ella escribe cadenas. **Modificación en vivo:** pide un cambio menor. **Preguntas individuales:** relación entre G, M y el código. |

Participan todos y las preguntas pueden ser para cualquiera, así que **todos** tienen que saber la tabla de la sección 7.

---

## 2. El proyecto en un minuto

MiniHTML es un HTML reducido con tres etiquetas. Su alfabeto es:

```
Σ = { <b>, <i>, <p>, </b>, </i>, </p>, TEXTO }
```

Una cadena es válida si toda etiqueta que se abre se cierra, y **en orden inverso**: la última que se abrió es la primera que se cierra. `<p> <b> TEXTO </b> </p>` es válida; `<p> <b> TEXTO </p> </b>` no.

Hicimos tres cosas:

1. Una **gramática libre de contexto G** que genera el lenguaje.
2. Un **autómata a pila M** que lo reconoce.
3. Un **programa en Python** que simula M (la **opción B** de la consigna). La opción A era programar una función por cada variable de G.

---

## 3. Por qué hace falta una pila

**La idea.** Para saber si un cierre es correcto hay que recordar qué etiquetas siguen abiertas, y la profundidad no tiene límite. Un autómata finito solo recuerda con sus estados, que son finitos.

**La demostración: lema de bombeo (clase 6).** Supongamos que L es regular, con constante n.

1. Tomamos ω = `<p>ⁿ TEXTO </p>ⁿ`, que está en L y tiene longitud mayor que n.
2. El lema dice que ω = xyz con |xy| ≤ n, y ≠ λ, y que xyⁱz está en L para todo i ≥ 0. (El lema de la clase usa α, β, γ; acá va con x, y, z para no confundirlo con las cadenas α, β, γ de la consigna.)
3. Como |xy| ≤ n, y cae dentro de las aperturas: y = `<p>ˢ` con s ≥ 1.
4. Con i = 0 quedan menos aperturas que cierres, y esa cadena no está en L. **Contradicción.**

Es el mismo argumento de aⁿbⁿ y de los paréntesis balanceados. MiniHTML no es regular.

> **Si limitaran la profundidad** (por ejemplo, 3 niveles), el lenguaje pasa a ser regular: alcanza con un estado por cada contenido posible de la pila.

**Por qué una pila y no una cola.** Los cierres siguen el orden último en entrar, primero en salir. Con una cola se aceptaría `<p> <b> TEXTO </p> </b>`.

**Chomsky (clase 0).** Tipo 3: regulares, AF. **Tipo 2: libres de contexto, AF con una pila. Acá está MiniHTML.** Tipo 1: sensibles al contexto. Tipo 0: recursivamente enumerables, máquina de Turing.

---

## 4. La gramática G (fase 1)

G = (V, Σ, S, P), con V = {S, E}.

```
(1) S → E S       (3) E → TEXTO
(2) S → λ         (4) E → <b> S </b>
                  (5) E → <i> S </i>
                  (6) E → <p> S </p>
```

- **S** es una secuencia de elementos, que puede ser vacía.
- **E** es un elemento: un texto o una etiqueta con contenido.
- **Es libre de contexto** porque a la izquierda de cada producción hay una sola variable.
- **No es regular:** en (4) a (6) la variable queda en el medio, entre dos terminales.
- **No es ambigua:** el próximo símbolo decide la producción (cierre o fin: `S → λ`; cualquier otro: `S → E S`). Por eso cada cadena tiene una sola derivación más a la izquierda.
- **Por qué dos variables:** `S → S S` sería ambigua, porque permite agrupar los hermanos de varias formas.

**Derivación más a la izquierda de α** = `<p> TEXTO <b> TEXTO </b> </p>`. Producciones: 1, 6, 1, 3, 1, 4, 1, 3, 2, 2, 2.

```
S ⇒ E S
  ⇒ <p> S </p> S
  ⇒ <p> E S </p> S
  ⇒ <p> TEXTO S </p> S
  ⇒ <p> TEXTO E S </p> S
  ⇒ <p> TEXTO <b> S </b> S </p> S
  ⇒ <p> TEXTO <b> E S </b> S </p> S
  ⇒ <p> TEXTO <b> TEXTO S </b> S </p> S
  ⇒ <p> TEXTO <b> TEXTO </b> S </p> S
  ⇒ <p> TEXTO <b> TEXTO </b> </p> S
  ⇒ <p> TEXTO <b> TEXTO </b> </p>
```

El árbol está en [diagramas/arbol_alfa.png](diagramas/arbol_alfa.png).

---

## 5. El autómata M (fase 2)

M = (Q, Σ, Γ, δ, q0, Z0, F), con Q = {q0, qf}, Γ = {Z0, B, I, P} y F = {qf}. Es un **AFPNλ que acepta por estado final**.

La **idea**: al abrir se apila, al cerrar se desapila si coincide, y al terminar debe quedar solo Z0.

| Regla | Transición | Qué hace |
|---|---|---|
| 1 | δ(q0, TEXTO, X) = (q0, X) | El texto no toca la pila. X es cualquier símbolo de Γ. |
| 2 | δ(q0, `<b>`, X) = (q0, BX) | Apila B. |
| 3 | δ(q0, `<i>`, X) = (q0, IX) | Apila I. |
| 4 | δ(q0, `<p>`, X) = (q0, PX) | Apila P. |
| 5 | δ(q0, `</b>`, B) = (q0, λ) | Desapila B. |
| 6 | δ(q0, `</i>`, I) = (q0, λ) | Desapila I. |
| 7 | δ(q0, `</p>`, P) = (q0, λ) | Desapila P. |
| 8 | δ(q0, λ, Z0) = (qf, Z0) | Acepta si no queda nada abierto. |

Cualquier otro caso es δ = ∅: no hay transición y la cadena se rechaza.

En el diagrama, según la clase 8, los rótulos son `entrada, tope, reemplazo` (con comas): por ejemplo `<b>, X, BX`. Está en [diagramas/automata.png](diagramas/automata.png).

**Tres cosas que suelen preguntar:**

- **Aceptación:** la cadena se acepta si se leyó toda y se llegó a qf. Z0 sigue en la pila; eso está bien porque aceptamos por estado final.
- **No determinismo:** solo en q0 con Z0 en el tope, donde se puede leer un símbolo o tomar la regla 8. Si se toma antes de terminar, queda entrada sin leer y qf no tiene salidas, así que esa forma de procesar la cadena no acepta.
- **Rol de Z0:** marca el fondo. Si está en el tope, no hay etiquetas abiertas.

---

## 6. Cómo hacer una traza

Una configuración es (estado, lo que falta leer, pila con el tope a la izquierda). Se aplica la regla que corresponde al símbolo y al tope, y se escribe ⊢.

**Aceptada**, α = `<p> TEXTO <b> TEXTO </b> </p>`. Reglas: 4, 1, 2, 1, 5, 7, 8.

```
(q0, <p> TEXTO <b> TEXTO </b> </p>, Z0)
⊢ (q0, TEXTO <b> TEXTO </b> </p>, P Z0)     regla 4
⊢ (q0, <b> TEXTO </b> </p>, P Z0)           regla 1
⊢ (q0, TEXTO </b> </p>, B P Z0)             regla 2
⊢ (q0, </b> </p>, B P Z0)                   regla 1
⊢ (q0, </p>, P Z0)                          regla 5
⊢ (q0, λ, Z0)                               regla 7
⊢ (qf, λ, Z0)                               regla 8: ACEPTA
```

**Rechazada**, `<p> <b> TEXTO </p> </b>`. Reglas: 4, 2, 1 y después nada.

```
(q0, <p> <b> TEXTO </p> </b>, Z0)
⊢ (q0, <b> TEXTO </p> </b>, P Z0)           regla 4
⊢ (q0, TEXTO </p> </b>, B P Z0)             regla 2
⊢ (q0, </p> </b>, B P Z0)                   regla 1
δ(q0, </p>, B) = ∅: RECHAZA
```

Las otras cadenas de la consigna: **β** usa las reglas 4, 1, 2, 1, 5, 3, 1, 6, 7, 8 y **γ** usa 4, 1, 1, 7, 3, 1, 6, 8.

---

## 7. El código

Abrí [src/parser.py](../src/parser.py). Tiene dos pasos: `tokenizar` convierte el texto en tokens de Σ y `simular` aplica δ.

| Líneas | Qué hace |
|---|---|
| 13 | `ETIQUETAS`: cada etiqueta con su símbolo de pila. **Agregar una etiqueta es tocar solo esta línea.** |
| 15-16 | `APERTURAS` y `CIERRES`, armados a partir de `ETIQUETAS`. |
| 19-27 | `tokenizar`. Lo que empieza con `<` queda como etiqueta (línea 24: sin espacios en los extremos, en minúscula y con `\` pasada a `/`). Cada palabra se vuelve `TEXTO` (línea 26). Lo mal escrito queda igual, para rechazarlo después. |
| 37 | La pila arranca con Z0. **El tope es el último elemento de la lista.** |
| 40-54 | El recorrido, un token por vez. |
| 59 | Regla 8: pasa a qf. |

**La tabla clave.** G no está programada; la relación con G es conceptual.

| G | M | Código |
|---|---|---|
| `E → TEXTO` | Regla 1 | Líneas 42-43: no hace nada con la pila |
| Apertura de `E → <x> S </x>` | Reglas 2 a 4 | Líneas 44-45: `pila.append` |
| Cierre de `E → <x> S </x>` | Reglas 5 a 7 | Líneas 48-49: `pila.pop` |
| `S → E S` | Leer un símbolo más | Línea 40: el `for` |
| `S → λ` al final de la cadena | Regla 8 | Línea 59 |
| Símbolo fuera de Σ | No es una entrada posible | Líneas 46-47: error léxico |
| Sin derivación | δ = ∅ | Líneas 50-53: cierre sin apertura o cruce |
| Falta cerrar | No se puede aplicar la regla 8 | Líneas 56-58: etiquetas sin cerrar |

La S del medio de `E → <x> S </x>` es todo lo que pasa mientras el símbolo de esa etiqueta está en la pila.

### La demo

Probá antes de entrar. **Las comillas son obligatorias**, porque para la consola `<` y `>` son redirecciones.

```bash
python3 src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```

```bash
python3 src/parser.py
```

```bash
python3 -m unittest tests/test_parser.py
```

El segundo es el modo interactivo: Enter solo analiza la cadena vacía y `salir` termina. El tercero corre los 12 tests.

| Resultado | Cadenas |
|---|---|
| **Aceptada** | vacía, `TEXTO`, `Hola mundo`, `<p></p>`, `<p>Hola <b>mundo</b></p>`, `<P> TEXTO </P>`, `<p> TEXTO <\p>`, `a > b` |
| **Error sintáctico** | `</p>`, `<p> <b> TEXTO </b>`, `<p>>` |
| **Error de anidamiento** | `<p> <b> TEXTO </p> </b>`, `<p> TEXTO </b>` |
| **Error léxico** | `<u> TEXTO </u>`, `<br>`, `<p> TEXTO <b </p>`, `< b > TEXTO </b>`, `<p class=x> TEXTO </p>`, `<p/>`, `<>`, `1 < 2` |

Por qué parecen raras algunas:

- `<P>` y `<\p>` se aceptan porque la línea 24 las normaliza a `<p>` y `</p>`.
- `a > b` son tres palabras: un `>` suelto no abre nada y cuenta como `TEXTO`.
- `<p>>` es `<p>` seguido de un `TEXTO`, y falta cerrar.
- `1 < 2` da error léxico porque `<` siempre empieza una etiqueta, y `< 2` no está en Σ.

---

## 8. Cómo pensar cualquier cambio

Antes de tocar el código, respondé **en voz alta** y en este orden:

1. **¿Cambia Σ?** Hay un símbolo nuevo, y hay que ver si cambia `tokenizar`.
2. **¿Cambia G?** Qué producción se agrega o se quita.
3. **¿Cambia M?** Qué transición se agrega, o cuál pasa a ser ∅.
4. **Código:** ¿se reconoce distinto (`tokenizar`) o se decide distinto (`simular`)?
5. **Probá** una cadena válida, una inválida y los tests.

Si es una restricción nueva, va dentro del `for` de `simular`, y estos datos están a mano:

| Dato | Para qué sirve |
|---|---|
| `token` | El símbolo actual |
| `tope` | La etiqueta abierta más interna |
| `"P" in pila` | Si hay un `<p>` abierto en cualquier nivel |
| `len(pila) - 1` | La profundidad actual |
| `i` y `tokens[i - 1]` | La posición y el token anterior (si `i > 0`) |

Si la práctica sale mal, esto deshace los cambios:

```bash
git restore src/parser.py tests/test_parser.py
```

---

## 9. Las modificaciones más probables

Los números de línea son del código sin tocar. **Si un test falla porque lo que pide la profe cambia el lenguaje, no está mal:** hay que explicar que el test describía la regla vieja.

### Receta 1: etiqueta nueva `<u>`

```python
ETIQUETAS = {"b": "B", "i": "I", "p": "P", "u": "U"}   # línea 13
```

- G: `E → <u> S </u>`.
- M: U en Γ, `δ(q0, <u>, X) = (q0, UX)` y `δ(q0, </u>, U) = (q0, λ)`.
- Para `<h1>`, usá `"h1": "H1"`: la línea 57 arma el nombre de la etiqueta desde el símbolo, así que `"div": "D"` mostraría `<d>`.

### Receta 2: etiqueta sin cierre `<br>`

```python
VACIAS = {"<br>"}                                       # debajo de la línea 13
if token == "TEXTO" or token in VACIAS:                 # línea 42
```

- G: `E → <br>`.
- M: `δ(q0, <br>, X) = (q0, X)`. No toca la pila, igual que `TEXTO`.

### Receta 3: prohibir `<p>` directamente dentro de `<p>`

Va entre las líneas 44 y 45:

```python
        elif token in APERTURAS:              # reglas 2 a 4: apila
            if token == "<p>" and tope == "P":
                return False, "Error sintáctico: <p> dentro de <p>.", traza
            pila.append(APERTURAS[token])
```

- M: `δ(q0, <p>, P) = ∅`.
- G: el contenido de `<p>` necesita su propia variable, que no permita un `<p>` como elemento directo.
- Para prohibirlo **en cualquier nivel**, cambiá `tope == "P"` por `"P" in pila`. Ahí M necesita más estados, porque el tope ya no alcanza para saberlo.

### Receta 4: todo tiene que estar dentro de `<p>`

Va debajo de la línea 41:

```python
        if tope == "Z0" and token != "<p>":
            return False, f"Error sintáctico: '{token}' fuera de <p>.", traza
```

- M: con Z0 en el tope solo se puede leer `<p>`.
- G: un nuevo símbolo inicial, `D → <p> S </p> D | λ`.
- Fallan 4 tests, porque el lenguaje cambió: por ejemplo, γ tiene un `<i>` fuera de `<p>`. Es esperable.

### Otros cambios

| Pedido | Cambio | Qué pasa |
|---|---|---|
| Token nuevo `NUM` | Línea 26: `tokens.append("NUM" if trozo.isdigit() else "TEXTO")`. Línea 42: `if token in ("TEXTO", "NUM"):` | G: `E → NUM`. M: `δ(q0, NUM, X) = (q0, X)`. |
| Sin texto suelto afuera | Línea 43, en lugar de `pass`: `if tope == "Z0": return False, "Error sintáctico: texto fuera de una etiqueta.", traza` | M: `δ(q0, TEXTO, Z0) = ∅`. Fallan 2 tests. |
| Profundidad máxima | Antes de la línea 45: `if len(pila) - 1 >= MAX: return False, "Error sintáctico: demasiada profundidad.", traza`, con `MAX` definido arriba | **El lenguaje pasa a ser regular.** Con `MAX = 2` falla `test_etiquetas_sin_cerrar`, que abre tres niveles. |
| Distinguir mayúsculas | Línea 24: sacar `.lower()` | `<P>` pasa a ser error léxico. Falla `test_html_real`, que usa `<P>`. |
| Aceptar por pila vacía | Línea 59: `pila.pop()` y `traza.append(configuracion("q0", [], pila))` | M: `δ(q0, λ, Z0) = (q0, λ)`. Falla `test_traza`. |

---

## 10. Preguntas probables

Tapá la respuesta e intentá contestar en dos frases.

**¿Qué relación hay entre G y M?**
Describen el mismo lenguaje. Es coherente con el teorema de la clase 8: L es libre de contexto si y solo si lo reconoce un autómata a pila. El teorema no asegura que *estas dos* coincidan; eso sale de que apertura y cierre de `E → <x> S </x>` corresponden a apilar y desapilar.

**¿Por qué eligieron la opción B?**
Porque el código sigue la tabla δ: cada rama del `if` corresponde a reglas de M, y la pila queda a la vista.

**¿Por qué dos estados?**
q0 procesa toda la cadena y qf solo marca la aceptación. La memoria necesaria está en la pila, no en los estados.

**¿Su autómata es determinista?**
No, es un AFPNλ: en q0 con Z0 en el tope se puede leer o tomar la regla 8. El programa no prueba alternativas porque solo toma la regla 8 al terminar la entrada, que es la única forma de procesar la cadena que puede aceptar.

**En clase, ¿AFPD y AFPNλ reconocen lo mismo?**
No. El ejemplo de la clase 8 son las capicúas. Por eso no alcanza con decir "un autómata a pila" sin aclarar cuál.

**¿Estado final o pila vacía?**
Usamos estado final. La clase 8 muestra que en AFPNλ los dos criterios son equivalentes. Para pasar a pila vacía, la regla 8 sería `δ(q0, λ, Z0) = (q0, λ)`.

**¿Por qué `S → λ`?**
Permite la cadena vacía y `<p></p>`, y es lo que termina una secuencia de elementos.

**¿Qué pasa con la cadena vacía?**
Es válida. En G: `S ⇒ λ`. En M: `(q0, λ, Z0) ⊢ (qf, λ, Z0)`. En el código, el `for` no da vueltas y se llega a la línea 59.

**¿Cómo saben que G no es ambigua?**
Porque con el próximo símbolo hay una sola producción posible. En general, decidir si una GIC es ambigua es indecidible (clase 7), pero acá se puede ver directamente.

**¿Por qué no usaron análisis exhaustivo?**
Es exponencial, y el teorema de terminación de la clase 7 no cubre a G porque tiene `S → λ`. Con la pila se hace una sola pasada, lineal en la cantidad de tokens.

**¿Qué diferencia hay entre los errores?**
Léxico: el símbolo no está en Σ (`<u>`). Sintáctico: los símbolos son válidos, pero falta un cierre o sobra uno. Anidamiento: se cerró una etiqueta que no es la última abierta.

**¿Por qué la pila termina con Z0 si la cadena es válida?**
Porque Z0 es el fondo y aceptamos por estado final; la regla 8 no lo saca.

**¿En qué orden está escrita M?**
En el de la consigna, (Q, Σ, Γ, δ, q0, Z0, F). En clase aparece como (Σ, Γ, Q, q0, Z0, F, Δ). Son los mismos componentes.

**¿Qué pasa con una entrada enorme?**
La profundidad no tiene límite en el modelo. En el programa, la pila es una lista que crece según haga falta.

---

## 11. Machete

```
G:  S → E S | λ
    E → TEXTO | <b> S </b> | <i> S </i> | <p> S </p>

M:  Q = {q0, qf}   Γ = {Z0, B, I, P}   F = {qf}
    1  (q0, TEXTO, X) → (q0, X)
    2  (q0, <b>,  X)  → (q0, BX)      5  (q0, </b>, B) → (q0, λ)
    3  (q0, <i>,  X)  → (q0, IX)      6  (q0, </i>, I) → (q0, λ)
    4  (q0, <p>,  X)  → (q0, PX)      7  (q0, </p>, P) → (q0, λ)
    8  (q0, λ, Z0)    → (qf, Z0)
    Otro caso: δ = ∅

parser.py:
    13     ETIQUETAS            44-45  apila (2 a 4)
    22-26  tokenizar            46-47  error léxico
    37     pila = ["Z0"]        48-49  desapila (5 a 7)
    40     for token            50-53  cierre sin apertura o cruce
    42-43  TEXTO (1)            56-58  sin cerrar
                                59     regla 8

Cambio: ¿Σ? → ¿G? → ¿M? → código → válida, inválida y tests
```

### Antes de entrar

- [ ] Compu cargada, con Python 3.8 o más nuevo. Solo se probó en Linux: si usan otra compu, probala antes.
- [ ] `python3 -m unittest tests/test_parser.py` da 12 tests OK.
- [ ] `git status` limpio, sin restos de la práctica.
- [ ] `parser.py` abierto y una consola en la carpeta del proyecto.
- [ ] Informe a mano, con el diagrama de M.

### Reparto sugerido

| Integrante | Parte | Secciones |
|---|---|---|
| 1 | Problema y por qué no alcanza un AF | 2 y 3 |
| 2 | Gramática y derivación | 4 |
| 3 | Autómata y traza | 5 y 6 |
| 4 | Código, demo y modificación | 7 a 9 |

Todos tienen que poder responder la sección 10 y la tabla de la sección 7.
