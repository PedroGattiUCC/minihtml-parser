# Clase 7: Lenguajes Independientes de Contexto (Gramáticas Libres de Contexto)

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase 7 2026.pdf` (Clase 7)

---

## 1. Definición de Gramáticas Independientes de Contexto (GIC) (Diapositiva 2)

Un lenguaje es **independiente de contexto (LIC)** cuando es generado por una gramática donde las reglas de producción tienen la forma:
$$A \to \alpha$$
donde:
- $A \in V$ es una variable no terminal aislada en la parte izquierda.
- $\alpha \in (V \cup \Sigma)^*$ es una cadena (posiblemente vacía $\lambda$) de variables y terminales.

> **Observación:** Las reglas de una gramática regular también tienen esa forma ($A \to aB \mid a \mid \lambda$). Por lo tanto, **toda gramática regular es independiente de contexto**, y **todo lenguaje regular es independiente de contexto** ($\mathcal{LR} \subset \mathcal{LIC}$).

---

## 2. Ejemplos Fundamentales de GIC y LIC (Diapositivas 3 - 7)

### 2.1 Conteo Balanceado: $L = \{a^n b^n : n \ge 0\}$ (Diapositiva 3)
- $V = \{S\}$, $\Sigma = \{a, b\}$, Axioma: $S$.
- Reglas:
  $$S \to a S b \mid \lambda$$
- **Árboles de derivación:**
  - Para $\lambda$: $S \xrightarrow{\lambda} \lambda$
  - Para $ab$: $S \Rightarrow aSb \Rightarrow ab$
  - Para $aabb$: $S \Rightarrow aSb \Rightarrow a(aSb)b \Rightarrow aabb$

---

### 2.2 Lenguaje de Palíndromos (Diapositivas 4 y 5)
- Si consideramos $P = \{S \to aSa \mid bSb \mid \lambda\}$: **solo genera palíndromos de longitud par**.
- Para generar **todas las cadenas capicúas** $L = \{\alpha \in \{a, b\}^* : \alpha = \alpha^R\}$:
  $$S \to aSa \mid bSb \mid a \mid b \mid \lambda$$
- **Derivaciones:**
  - $aba$: $S \Rightarrow aSa \Rightarrow aba$
  - $abbba$: $S \Rightarrow aSa \Rightarrow abSba \Rightarrow abbba$
  - $abaaba$: $S \Rightarrow aSa \Rightarrow abSba \Rightarrow abaSaba \Rightarrow abaaba$

---

### 2.3 Estructuras de Control (`if`, `else`, `end`) (Diapositivas 6 y 7)
Sea $L = \{\text{cadenas de 'if', 'else', 'end' sintácticamente válidas}\}$.
- **Reglas del lenguaje:**
  1. *Balance:* Todo `if` debe cerrarse con un único `end` posterior.
  2. *Rama opcional:* Entre un `if` y su `end` puede aparecer a lo sumo un `else`.
  3. *Anidamiento y secuencia:* Dentro del cuerpo del `if` o `else` (y a nivel principal) pueden ir cero, uno o más bloques anidados/concatenados.
- **GIC Correcta (Diapositiva 6):**
  $V = \{S, A\}$, $\Sigma = \{\text{if, else, end}\}$, Axioma: $S$.
  $$S \to S A \mid \lambda$$
  $$A \to \text{if } S \text{ end} \mid \text{if } S \text{ else } S \text{ end}$$

> **Análisis del Intento Erróneo (Diapositiva 7):**  
> Si se define $S \to \text{if } A \text{ end} \mid SS$ y $A \to \text{else } A \mid \text{if } A \text{ end} \mid \lambda$, la gramática es **incorrecta** porque permite derivar cadenas inválidas con múltiples `else` consecutivos para un mismo `if` (`if else else end`).

---

## 3. GIC en Lenguajes de Programación y Forma BNF (Diapositivas 8 - 10)

La sintaxis de los lenguajes de programación se presenta usualmente por medio de GIC en **Forma Backus-Naur (BNF)**. Los terminales se denominan *tokens* o componentes léxicos.

### 3.1 Gramática de Números Reales (Diapositiva 9):
- $V = \{\langle\text{real}\rangle, \langle\text{dígitos}\rangle, \langle\text{decimal}\rangle, \langle\text{exp}\rangle, \langle\text{sgn}\rangle\}$
- $\Sigma = \{0, 1, \dots, 9, ., +, -, E\}$
- $S = \langle\text{real}\rangle$
- **Reglas:**
  $$\langle\text{real}\rangle \to \langle\text{sgn}\rangle \langle\text{dígitos}\rangle \langle\text{decimal}\rangle \langle\text{exp}\rangle$$
  $$\langle\text{dígitos}\rangle \to \langle\text{dígitos}\rangle \langle\text{dígitos}\rangle \mid 0 \mid 1 \mid \dots \mid 9$$
  $$\langle\text{decimal}\rangle \to . \langle\text{dígitos}\rangle \mid \lambda$$
  $$\langle\text{exp}\rangle \to E \langle\text{dígitos}\rangle \mid E+ \langle\text{dígitos}\rangle \mid E- \langle\text{dígitos}\rangle \mid \lambda$$
  $$\langle\text{sgn}\rangle \to + \mid - \mid \lambda$$
- **Cadenas válidas generadas:** `34.2`, `27.0E-2`, `-1.54E1`.
- **Cadenas inválidas (no generadas):** `.325`, `E125`, `42.5E`, `0.1E+`.

### 3.2 Gramática de Expresiones Aritméticas (Diapositiva 10):
- $\Sigma = \{0, 1, +, *, (, )\}$, Axioma: $\langle\text{expresión}\rangle$
- **Reglas:**
  $$\langle\text{expresión}\rangle \to \langle\text{término}\rangle \mid \langle\text{expresión}\rangle + \langle\text{término}\rangle$$
  $$\langle\text{término}\rangle \to \langle\text{factor}\rangle \mid \langle\text{término}\rangle * \langle\text{factor}\rangle$$
  $$\langle\text{factor}\rangle \to \langle\text{número}\rangle \mid (\langle\text{expresión}\rangle)$$
  $$\langle\text{número}\rangle \to 1\langle\text{número}\rangle \mid 0\langle\text{número}\rangle \mid 0 \mid 1$$
- Válidas: `10+101*10`, `(101+10*10)`.
- Inválidas: `+10`, `1*(0+)`.

---

## 4. Ejemplo de Gramática Sensible al Contexto (No GIC) (Diapositiva 11)

Para generar $L = \{a^k b^k c^k : k \ge 1\}$ (tres conteos simultáneos):
- $V = \{S, B, C\}$, $\Sigma = \{a, b, c\}$
- **Reglas:**
  $$S \to aSBC \mid abC$$
  $$CB \to BC \quad (\text{regla sensible al contexto: el no terminal permuta con contexto})$$
  $$bB \to bb, \quad bC \to bc, \quad cC \to cc$$

---

## 5. Propiedades de Clausura de los LICs (Diapositivas 12 - 16)

### 5.1 Unión de LICs es LIC:
Sean $L_1$ generado por $G_1$ y $L_2$ generado por $G_2$ ($V_1 \cap V_2 = \emptyset$).  
Se construye $G$ con variable inicial $S$ y reglas:
$$S \to S_1 \mid S_2$$
- **Ejemplo (Diapositiva 12):** $L_1 = \{a^n b^m : m > n \ge 0\}$ con $S_1 \to aS_1 b \mid B, B \to bB \mid b$, y $L_2 = \{a^n b^m : n = m\}$ con $S_2 \to aS_2 b \mid \lambda$.  
  $L_1 \cup L_2 = \{a^n b^m : m \ge n \ge 0\}$ es generado por $S \to S_1 \mid S_2$.

### 5.2 Concatenación de LICs es LIC (Diapositivas 14 y 15):
Se define la nueva regla:
$$S \to S_1 S_2$$
- **Ejemplo:** $L_1 = \{a^n b^n : n \ge 0\}$ y $L_2 = \{a^n b^{2n} : n \ge 0\} \implies L_1 L_2 = \{a^n b^n a^m b^{2m} : n, m \ge 0\}$ con $S \to S_1 S_2$.

### 5.3 Clausura de Kleene de LICs es LIC (Diapositiva 16):
Se definen las reglas:
$$S \to S_1 S \mid \lambda$$

---

## 6. Ambigüedad en Gramáticas (Diapositivas 17 - 21)

Una gramática formal es **ambigua** si existe al menos una cadena en su lenguaje que admite **dos o más árboles de derivación sintáctica distintos**, o equivalentemente, dos o más derivaciones más a la izquierda (*leftmost derivations*) diferentes.

### Ejemplo 1 (Diapositiva 18):
Producciones: $S \to aSb \mid SS \mid \lambda$.  
La cadena $aabb$ tiene dos árboles distintos:
1. $S \Rightarrow aSb \Rightarrow a(aSb)b \Rightarrow aabb$
2. $S \Rightarrow SS \Rightarrow (aSb)S \Rightarrow ab(aSb) \dots$

### Ejemplo 2: Expresiones Aritméticas (Diapositiva 19):
Reglas: $E \to E + E \mid E * E \mid a$.  
La cadena $a + a * a$ admite dos árboles:
- Uno interpretado como $(a + a) * a$.
- Otro interpretado como $a + (a * a)$.

### Desambiguación por Precedencia (Diapositiva 21):
Para eliminar la ambigüedad, se asocian niveles sintácticos a distintas variables:
$$E \to E + T \mid T \quad (\text{Nivel superior: suma})$$
$$T \to T * F \mid F \quad (\text{Nivel inferior: multiplicación subordinada})$$
$$F \to a \mid (E)$$

---

## 7. El Problema de Decisión: ¿$w \in L(G)$? (Diapositivas 22 - 28)

Dada una cadena $w \in \Sigma^*$ y una GIC $G$, ¿cómo determinar si $w \in L(G)$?

### 7.1 Análisis Sintáctico Exhaustivo:
- Generar todas las formas sentenciales en 1 paso, luego en 2 pasos, luego en 3 pasos...
- **Teorema de Terminación (Diapositiva 24):** Si una GIC $G$ **no tiene reglas de la forma $A \to \lambda$ ni $A \to B$**, el análisis sintáctico exhaustivo **siempre termina en una cantidad finita de pasos** (decidible).

### Ejemplos Resueltos de Cátedra:
- **Ejemplo 1 (Diapositiva 25):** $w = aabcc$ con $S \to aSbc \mid abc$.  
  - En 1 paso: $S \Rightarrow abc \neq w$.  
  - En 2 pasos: $S \Rightarrow aSbc \Rightarrow a(abc)bc = aabcc = w$. **Aceptada en 2 pasos.**
- **Ejemplo 2 (Diapositiva 26):** $w = ababcc$ con $S \to XSc \mid abc$, $X \to aXb \mid ab$.  
  - $S \Rightarrow XSc \Rightarrow abSc \Rightarrow ab(abc)c = ababcc = w$. **Aceptada en 3 pasos.**
- **Ejemplo 3 (Diapositiva 27):** $w = abacc$ con la misma gramática.  
  - El análisis exhaustivo de todas las ramas posibles hasta longitud 5 termina sin coincidencia. **Rechazada ($w \notin L(G)$).**

---

## 8. Problemas Decidibles vs. Indecidibles (Diapositivas 29 - 33)

### Decidibles en Gramáticas Regulares:
1. **¿Es $L(G) \neq \emptyset$?** Se construye el AF equivalente; es no vacío si existe un camino de $q_0$ a un estado final.
2. **¿Es $L(G)$ infinito?** Si y solo si existe algún ciclo en el camino hacia un estado final en el grafo de $M$.
3. **¿$L(G_1) = L(G_2)$?** Se construye el AF para $L_3 = (L_1 \cap L_2^c) \cup (L_1^c \cap L_2)$. Si $L_3 = \emptyset \implies L_1 = L_2$.

### Indecidibles en Gramáticas Libres de Contexto (Diapositiva 33):
Para gramáticas Tipo 2 (GIC), **no existe ningún algoritmo general que responda**:
1. **¿Es $G$ ambigua? $\implies$ INDECIDIBLE.**
2. **¿Genera $G$ todas las cadenas ($L(G) = \Sigma^*$)? $\implies$ INDECIDIBLE.**
3. **Dadas $G_1$ y $G_2$, ¿$L(G_1) = L(G_2)$? $\implies$ INDECIDIBLE.**

---

## 9. Bibliografía de la Cátedra (Diapositiva 34)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*.
- **Peter Linz:** *An Introduction to Formal Languages and Automata*. Capítulo 5.
