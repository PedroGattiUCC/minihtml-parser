# Clase 3b: Autómatas Finitos No Deterministas (AFN y AFN-$\lambda$)

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase 3b 2026.pdf` (Clase 3b)

---

## 1. Determinismo vs. No-Determinismo (Diapositiva 2)

- **Determinismo:** Dado un estado y un símbolo de entrada, existe un **único estado** al cual el autómata puede transicionar. Por lo tanto, la traza de procesamiento de una cadena es única:
  $$\delta(q, a) = q' \quad (\text{un único estado})$$
- **No-Determinismo:** Dado un estado y un símbolo, existen **varios estados posibles** a los cuales el autómata puede transicionar. Por lo tanto, existen múltiples trazas de procesamiento posibles para una misma cadena:
  $$\Delta(q, a) = \{q_1, \dots, q_k\} \quad (\text{un subconjunto de estados})$$

---

## 2. Definición Formal de un AFN (Diapositivas 3 - 8)

Un **Autómata Finito no Determinístico (AFN)** es una 5-tupla:
$$M = (\Sigma, Q, q_0, F, \Delta)$$
Donde:
- $\Sigma$: Alfabeto de entrada.
- $Q$: Conjunto finito y no vacío de estados.
- $q_0 \in Q$: Estado inicial.
- $F \subseteq Q$: Conjunto de estados de aceptación o finales.
- $\Delta: Q \times \Sigma \to \mathcal{P}(Q)$: Función de transición hacia el conjunto de partes de $Q$.
  $$\Delta(q, a) = \{q_1, \dots, q_k\}$$
  significa que en el estado $q$, al leer $a$, el autómata puede pasar a cualquiera de los estados $\{q_1, \dots, q_k\}$.

### Criterio de Aceptación:
Una cadena $\alpha \in \Sigma^*$ es aceptada por el AFN $M$ si **existe al menos una forma de procesar la cadena** partiendo desde $q_0$ tal que el estado alcanzado sea un estado de aceptación:
$$L(M) = \{\alpha \in \Sigma^* : \text{existe una traza de ejecución desde } q_0 \text{ hasta un estado final al leer los caracteres de } \alpha\}$$

En el grafo de transición, una palabra $\alpha$ es aceptada si existe **algún camino** cuyas aristas estén etiquetadas secuencialmente con los caracteres de $\alpha$, que comience en $q_0$ y termine en un estado de $F$.

---

## 3. Determinización de un AFN (Diapositivas 9 - 11)

> **Teorema:** Dado un AFN $M = (\Sigma, Q, q_0, F, \Delta)$, se puede construir un AFD $M' = (\Sigma, Q', q_0', F', \delta)$ equivalente tal que $L(M) = L(M')$.

### Construcción Formal:
- $Q' \subseteq \mathcal{P}(Q)$ (superestados formados por conjuntos de estados de $M$).
- $q_0' = \{q_0\}$
- $F' = \{S \in Q' : S \cap F \neq \emptyset\}$ (superestados que contienen al menos un estado final).
- $\delta(S, a) = \bigcup_{q \in S} \Delta(q, a)$ para todo $a \in \Sigma$.

### Ejemplo Completo de Cátedra (Diapositivas 10 y 11):
Dado un AFN con estados $Q = \{q_0, q_1, q_2\}$ y $F = \{q_1, q_2\}$:

| Superestado en $Q'$ | Transición con $a$ | Transición con $b$ | Renombrado | ¿Es Final? |
|:---:|:---:|:---:|:---:|:---:|
| $\{q_0\}$ | $\{q_1, q_2\}$ | $\emptyset$ | $p_0$ | No |
| $\{q_1\}$ | $\emptyset$ | $\{q_1\}$ | $p_1^*$ | **Sí** |
| $\{q_2\}$ | $\{q_2\}$ | $\emptyset$ | $p_2^*$ | **Sí** |
| $\{q_0, q_1\}$ | $\{q_1, q_2\}$ | $\{q_1\}$ | $p_3^*$ | **Sí** |
| $\{q_0, q_2\}$ | $\{q_2\}$ | $\emptyset$ | $p_4^*$ | **Sí** |
| $\{q_1, q_2\}$ | $\{q_2\}$ | $\{q_1\}$ | $p_5^*$ | **Sí** |
| $\{q_0, q_1, q_2\}$ | $\{q_1, q_2\}$ | $\{q_1\}$ | $p_6^*$ | **Sí** |
| $\emptyset$ | $\emptyset$ | $\emptyset$ | $p_7$ | No |

### Simplificación del AFD Resultante:
- Los estados **inalcanzables** desde el estado inicial $p_0 = \{q_0\}$ se eliminan del AFD.
- Los estados desde los cuales no se puede alcanzar ningún estado final se eliminan.

---

## 4. Transiciones Espontáneas: AFN-$\lambda$ (Diapositivas 12 - 16)

En una **transición espontánea o transición-$\lambda$**, el autómata puede cambiar de estado (o no) sin procesar ningún carácter de la cinta:
$$\Delta(q, \lambda) = \{q_1, \dots, q_k\}$$

Un AFN con transiciones espontáneas (AFN-$\lambda$) es una 5-tupla $M = (\Sigma, Q, q_0, F, \Delta)$ con:
$$\Delta: Q \times (\Sigma \cup \{\lambda\}) \to \mathcal{P}(Q)$$

### Ejemplo de Diapositiva 13:
| Estado | Entrada $a$ | Entrada $b$ | Transición $\lambda$ |
|:---:|:---:|:---:|:---:|
| $q_0$ | $\{q_3\}$ | $\{q_1\}$ | $\emptyset$ |
| $q_1$ | $\{q_1\}$ | $\{q_2\}$ | $\emptyset$ |
| $* q_2$ | $\{q_2\}$ | $\emptyset$ | $\emptyset$ |
| $q_3$ | $\{q_2\}$ | $\{q_4\}$ | $\emptyset$ |
| $* q_4$ | $\emptyset$ | $\{q_4\}$ | $\emptyset$ |

- **Cadenas aceptadas:** $\alpha = aab$, $\beta = abaa$.

### Otros Ejemplos de Diapositivas 14 - 16:
- **AFN-$\lambda$ para $L(a^* b^* c^*)$:** Tres estados conectados linealmente mediante transiciones-$\lambda$.
- **AFN-$\lambda$ para $L_a \cup L_b$:** Unión del autómata que cuenta cantidad par de $a$ con el que cuenta cantidad par de $b$, bifurcando desde un estado inicial común mediante $\lambda$.
- **AFN-$\lambda$ para constantes numéricas con signo:** Manejo opcional del signo $+$ o $-$ mediante transición-$\lambda$.

---

## 5. Equivalencia entre AFN y AFN-$\lambda$ (Diapositivas 17 - 20)

> **Teorema:** Dado un AFN-$\lambda$ $M = (\Sigma, Q, q_0, F, \Delta)$, se puede construir un AFN equivalente $M' = (\Sigma, Q, q_0, F', \Delta')$ sin transiciones-$\lambda$ tal que $L(M) = L(M')$.

### 5.1 Concepto de Clausura-$\lambda$:
- **Clausura de un estado $q$ ($[q]$):** Conjunto de estados a los que puede llegar $M$ desde $q$ sin consumir ningún símbolo (usando transiciones espontáneas).  
  *Atención:* Siempre $q \in [q]$.
- **Clausura de un conjunto de estados ($[S]$):**
  $$[\{q_1, \dots, q_k\}] = [q_1] \cup \dots \cup [q_k]$$

### 5.2 Construcción del AFN Equivalente $M' = (\Sigma, Q, q_0, F', \Delta')$:
- **Nueva función de transición:**
  $$\Delta'(q, a) = [\Delta([q], a)]$$
  *(Conjunto de estados a los que puede llegar el AF leyendo un símbolo $a$ y haciendo transiciones espontáneas antes o después de leer dicho carácter).*
- **Nuevos estados finales:**
  $$F' = \{q \in Q : [q] \cap F \neq \emptyset\}$$
  *(Estados desde los cuales es posible alcanzar algún estado de aceptación de $M$ haciendo solo transiciones espontáneas).*

### Ejemplo de Cálculo Paso a Paso (Diapositivas 19 y 20):
Sean las clausuras:
- $[q_0] = \{q_0, q_1, q_2\}$
- $[q_1] = \{q_1, q_2\}$
- $[q_2] = \{q_2\}$

Cálculo de $\Delta'$ para cada símbolo sobre $\Sigma = \{a, b, c\}$:
- $\Delta'(q_0, a) = [\Delta(\{q_0, q_1, q_2\}, a)] = [q_0] = \{q_0, q_1, q_2\}$
- $\Delta'(q_0, b) = [\Delta(\{q_0, q_1, q_2\}, b)] = [q_1] = \{q_1, q_2\}$
- $\Delta'(q_0, c) = [\Delta(\{q_0, q_1, q_2\}, c)] = [q_2] = \{q_2\}$
- $\Delta'(q_1, a) = [\Delta(\{q_1, q_2\}, a)] = [\emptyset] = \emptyset$
- $\Delta'(q_1, b) = [\Delta(\{q_1, q_2\}, b)] = [q_1] = \{q_1, q_2\}$
- $\Delta'(q_1, c) = [\Delta(\{q_1, q_2\}, c)] = [q_2] = \{q_2\}$
- $\Delta'(q_2, a) = [\Delta(q_2, a)] = \emptyset$
- $\Delta'(q_2, b) = [\Delta(q_2, b)] = \emptyset$
- $\Delta'(q_2, c) = [\Delta(q_2, c)] = [q_2] = \{q_2\}$

---

## 6. Equivalencia General y Complejidad (Diapositivas 21 - 22)

$$\mathbf{AFD \equiv AFN \equiv AFN\text{-}\lambda}$$

### ¿Para qué definir distintos tipos de autómatas si son equivalentes?
1. Dada una ER es trivial y directo construir un AFN-$\lambda$ (Algoritmo de Thompson).
2. Dado un AFD se puede armar su ER mediante ecuaciones o eliminación de estados.
3. Los AFN son mucho más compactos en número de estados que los AFD.

### Implementación Algorítmica y Complejidad:
- **AFD:** Decidir si una cadena de longitud $n$ es aceptada toma **tiempo lineal $\mathcal{O}(n)$**.
- **AFN:** La simulación ingenua de no-determinismo implica explorar un árbol de búsqueda en profundidad de altura $n$, requiriendo **tiempo exponencial $\mathcal{O}(b^n)$**.

---

## 7. Bibliografía de la Cátedra (Diapositiva 23)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*. Capítulo 1: Alfabetos, cadenas y lenguajes. Secciones 2.4 a 2.12.
- **Peter Linz:** *An Introduction to Formal Languages and Automata*. Capítulo 2.2.
- **Lorena Bergamini:** *Autómatas, Lenguajes y Gramáticas*.
