# Clase 1: Alfabetos, Lenguajes y sus Operadores

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase1 2026.pdf` (Clase 1b)

---

## 1. Conjuntos y Operaciones (Diapositivas 2 - 4)

Un **conjunto** es una colección de elementos de un universo $U$ (sin estructura interna).  
Dado un conjunto $A$, para todo $x \in U$ se cumple: $x \in A$ o $x \notin A$.

### Ejemplos introductorios:
- $U = \mathbb{R}$ (números reales), $A = \{x \in U : x > 0\} \implies 2.56 \in A$, $-1/3 \notin A$.
- $U = \{a, b, \dots, z\}$, $A = \{\text{vocales}\} \implies i \in A$, $p \notin A$.

### Definición de Operaciones entre Conjuntos ($A, B \subseteq U$):
- **Unión:** $A \cup B = \{x \in U : x \in A \lor x \in B\}$
- **Intersección:** $A \cap B = \{x \in U : x \in A \land x \in B\}$
- **Diferencia:** $A - B = \{x \in U : x \in A \land x \notin B\}$
- **Complemento:** $A^c = \{x \in U : x \notin A\}$
- **Producto Cartesiano:** $A \times B = \{(x, y) : x \in A, y \in B\}$
- **Conjunto de Partes:** $\mathcal{P}(A) = \{B : B \subseteq A\}$ (todos los subconjuntos de $A$).

### Ejemplo Detallado en $U = \{\text{letras minúsculas del abecedario}\}$:
Sean $A = \{a, b\}$ y $B = \{a, e, i, o, u\}$:
- **Unión:** $A \cup B = \{a, b, e, i, o, u\}$
- **Intersección:** $A \cap B = \{a\}$
- **Diferencia:** $A - B = \{b\}$, mientras que $B - A = \{e, i, o, u\}$
- **Complemento:** $A^c = \{c, d, e, \dots, x, y, z\}$
- **Producto Cartesiano:**
  $$A \times B = \{(a, a), (a, e), (a, i), (a, o), (a, u), (b, a), (b, e), (b, i), (b, o), (b, u)\}$$
- **Conjunto de Partes:**
  - $\mathcal{P}(A) = \{\emptyset, \{a\}, \{b\}, \{a, b\}\}$ ($2^2 = 4$ elementos).
  - $\mathcal{P}(B) = \{\emptyset, \{a\}, \{e\}, \{i\}, \{o\}, \{u\}, \{a, e\}, \dots, \{a, e, i, o, u\}\}$ ($2^5 = 32$ subconjuntos).

---

## 2. Funciones entre Conjuntos (Diapositiva 5)

Una **función** $f: A \to B$ es un conjunto de pares ordenados de $A \times B$ donde cada elemento del dominio tiene exactamente una única imagen.  
Si $(x, y) \in f$, escribimos $y = f(x)$.

### Definición Formal:
Sea $f \subseteq A \times B$, $f$ es una función si y solo si:
$$(x, y) \in f \land (x, z) \in f \implies y = z$$
- **Dominio:** $\text{Dom}(f) = \{x \in A : \exists y \in B, (x, y) \in f\}$
- **Imagen:** $\text{Im}(f) = \{y \in B : \exists x \in A, (x, y) \in f\}$

---

## 3. Alfabetos y Cadenas (Diapositivas 6 - 8)

### 3.1 Alfabeto ($\Sigma$)
Cualquier conjunto finito y no vacío de símbolos elementales (denotado $\Sigma$).

#### Ejemplos de Alfabetos:
- $\Sigma_1 = \{a, b, c\}$ (3 símbolos)
- $\Sigma_2 = \{\&, \#\}$ (2 símbolos)
- $\Sigma_3 = \{0, 1\}$ (alfabeto binario)
- $\Sigma_4 = \{0, 1, \dots, 9, +, -\}$
- $\Sigma_5 = \{a, b, \dots, z\}$
- $\Sigma_6 = \{(, )\}$
- $\Sigma_7 = \{-, --\}$

### 3.2 Cadenas
Cualquier secuencia finita de símbolos tomados de un alfabeto $\Sigma$ (denotadas $\alpha, \beta, \gamma, w$).

#### Ejemplos de Cadenas:
- $\alpha = abb$ es una cadena sobre $\Sigma_1$
- $\beta = \&\#\#\&$ es una cadena sobre $\Sigma_2$
- $\gamma = (())()$ es una cadena sobre $\Sigma_6$
- $\phi = 121+36$ es una cadena sobre $\Sigma_4$
- $\eta = - - -- --$ es una cadena sobre $\Sigma_7$

### 3.3 Universo de Cadenas y Cadena Vacía ($\Sigma^*$, $\lambda$, $\Sigma^+$)
- **$\Sigma^*$:** Conjunto de todas las cadenas posibles formables con el alfabeto $\Sigma$ (universo de cadenas).
- **$\lambda$:** La única **cadena vacía** (longitud 0, sin símbolos).
- **$\Sigma^+$:** Conjunto de todas las cadenas no vacías:
  $$\Sigma^+ = \Sigma^* - \{\lambda\}$$

#### Ejemplo con $\Sigma_3 = \{0, 1\}$:
- $\Sigma_3^* = \{\lambda, 0, 1, 00, 01, 10, 11, 000, 001, \dots\}$
- $\Sigma_3^+ = \{0, 1, 00, 01, 10, 11, 000, 001, \dots\}$

---

## 4. Operaciones entre Cadenas (Diapositivas 9 - 14)

### 4.1 Concatenación ($\cdot$)
Sean $\alpha, \beta \in \Sigma^*$, con $\alpha = a_1 a_2 \dots a_n$ y $\beta = b_1 b_2 \dots b_m$:
$$\alpha \cdot \beta = a_1 a_2 \dots a_n b_1 b_2 \dots b_m$$
- **Propiedades:**
  - *Asociativa:* $\alpha \cdot (\beta \cdot \gamma) = (\alpha \cdot \beta) \cdot \gamma$
  - *No conmuta:* En general $\alpha \cdot \beta \neq \beta \cdot \alpha$
  - *Elemento neutro:* $\lambda \implies \alpha \cdot \lambda = \lambda \cdot \alpha = \alpha$
  - Habitualmente se escribe directamente $\alpha \beta$.

### 4.2 Potencia ($\alpha^n$)
Sea $\alpha \in \Sigma^*$, la potencia enésima es $\alpha$ concatenada consigo misma $n$ veces:
$$\alpha^n = \underbrace{\alpha \alpha \dots \alpha}_{n \text{ veces}}, \quad \text{con } \alpha^0 = \lambda$$
- **Propiedades:**
  - $\alpha^n \alpha^m = \alpha^{n+m}$
  - $(\alpha^n)^m = \alpha^{nm}$

### 4.3 Longitud ($|\alpha|$)
Sea $\alpha = a_1 a_2 \dots a_n$, su longitud es $|\alpha| = n$.
- **Propiedades:**
  - $|\alpha \beta| = |\alpha| + |\beta|$
  - $|\alpha^n| = n \cdot |\alpha|$
  - $|\alpha^{n+m}| = (n+m) \cdot |\alpha|$
  - $|(\alpha^n)^m| = |\alpha| \cdot n \cdot m$
  - Si $\alpha = \lambda \implies |\lambda| = 0$
- **Conteo específico:** $|\alpha|_a$ denota la cantidad de ocurrencias del símbolo $a$ en $\alpha$.  
  *Ejemplo:* $|abbab|_a = 2$, $|abbab|_b = 3$.

### 4.4 Reversa ($\alpha^R$)
Sea $\alpha = a_1 a_2 \dots a_n$, su reversa es $\alpha^R = a_n \dots a_2 a_1$.
- **Propiedades:**
  - $(\alpha \beta)^R = \beta^R \alpha^R$
  - $(\alpha^R)^R = \alpha$
  - $|\alpha^R| = |\alpha|$
  - $\lambda^R = \lambda$

### 4.5 Subcadenas, Prefijos y Sufijos
Sean $\alpha, \alpha' \in \Sigma^*$:
- $\alpha'$ es **subcadena** de $\alpha$ si $\alpha = \beta_1 \alpha' \beta_2$ para algunas cadenas $\beta_1, \beta_2 \in \Sigma^*$.
- $\alpha'$ es **prefijo** de $\alpha$ si $\alpha = \alpha' \beta$ para alguna cadena $\beta \in \Sigma^*$.
- $\alpha'$ es **sufijo** de $\alpha$ si $\alpha = \beta \alpha'$ para alguna cadena $\beta \in \Sigma^*$.
- $\lambda$ es subcadena, prefijo y sufijo de toda cadena.
- $\alpha$ es subcadena, prefijo y sufijo de sí misma.

*Ejemplo de la cátedra:* Si $\alpha = acbcb$:
- $cbc$ es subcadena de $\alpha$
- $acb$ es prefijo de $\alpha$
- $b$ es sufijo de $\alpha$

---

## 5. Lenguajes y Ejemplos de Cátedra (Diapositivas 15 - 18)

Un **lenguaje** sobre un alfabeto $\Sigma$ es cualquier subconjunto $L \subseteq \Sigma^*$.

### Lenguajes Triviales:
- $L_1 = \emptyset$ (lenguaje vacío, sin cadenas).
- $L_2 = \Sigma^*$ (lenguaje universal de todas las cadenas).

### Ejemplos sobre $\Sigma = \{a, b\}$:
- $L_3 = \{aa, ab, ba, bb\}$ (cadenas de longitud 2).
- $L_4 = \{\lambda, a, a^2, a^3, a^4, \dots\}$ (cadenas que no contienen el símbolo 'b').
- $L_5 = \{\alpha \in \Sigma^* : |\alpha|_a \text{ es par}\}$ (cadenas con cantidad par de símbolos 'a').
- $L_6 = \{\alpha \in \Sigma^* : \alpha = \alpha^R\}$ (cadenas capicúas / palíndromas).

### Ejemplo $L_7$ sobre $\Sigma = \{0, 1, \dots, 9, +, -, *, /, (, )\}$:
- $L_7 = \{\text{expresiones aritméticas válidas}\}$.
  - $17*(3-74) \in L_7$, con $|17*(3-74)| = 9$
  - $10-98/6 \in L_7$, con $|10-98/6| = 7$
  - $2/*3 \notin L_7$
  - $*33 \notin L_7$
  - $015-3 \notin L_7$

### Ejemplo $L_8$ sobre $\Sigma = \{(, )\}$:
- $L_8 = \{\text{paréntesis balanceados}\}$.
  - $()(()) \in L_8$
  - $(()()) \in L_8$
  - $(() \notin L_8$
  - $)()( \notin L_8$
  - $(()()) ) \notin L_8$

---

## 6. Operadores sobre Lenguajes y Ejercicios (Diapositivas 19 - 26)

### 6.1 Operadores de Conjuntos en Lenguajes:
Si $L_1, L_2 \subseteq \Sigma^*$, entonces $L_1 \cup L_2$, $L_1 \cap L_2$, $L_1 - L_2$ y $L_1^c$ son lenguajes.

#### Ejercicio resuelto de diapositiva 20 sobre los lenguajes $L_3, L_4, L_5, L_6$:
- $L_3 \cup L_4 = \{aa, ab, ba, bb, \lambda, a, a^3, a^4, \dots\}$
- $L_3 \cap L_4 = \{aa\}$
- $L_4 - L_5 = \{a, a^3, a^5, a^7, \dots\} = \{a^{2k+1} : k \ge 0\}$ (cadenas de solo 'a' con longitud impar).
- $L_5^c = \{\alpha \in \Sigma^* : |\alpha|_a \text{ es impar}\}$.

### 6.2 Concatenación de Lenguajes ($L_1 \cdot L_2$)
$$L_1 \cdot L_2 = \{\alpha \beta : \alpha \in L_1 \land \beta \in L_2\}$$
- **Propiedades:**
  - *Elemento absorbente:* $L \emptyset = \emptyset L = \emptyset$
  - *Elemento neutro:* $L \{\lambda\} = \{\lambda\} L = L$
  - *Asociativa:* $L_1 (L_2 L_3) = (L_1 L_2) L_3$
  - *Distributiva con $\cup$:* $L_1(L_2 \cup L_3) = L_1 L_2 \cup L_1 L_3$, y $(L_2 \cup L_3)L_1 = L_2 L_1 \cup L_3 L_1$
  - *No conmuta y no es distributiva con $\cap$*.

### 6.3 Potencia de Lenguajes ($L^n$)
$L^n = \underbrace{L L \dots L}_{n \text{ veces}}$, con:
- Si $L = \emptyset \implies L^n = \emptyset$ (para $n \ge 1$)
- Si $L = \{\lambda\} \implies L^n = \{\lambda\}$
- Si $n = 0 \implies L^0 = \{\lambda\}$

### 6.4 Clausuras de Lenguajes
- **Clausura de Kleene:**
  $$L^* = \bigcup_{n=0}^{\infty} L^n = L^0 \cup L^1 \cup L^2 \cup \dots$$
- **Clausura positiva:**
  $$L^+ = \bigcup_{n=1}^{\infty} L^n = L^1 \cup L^2 \cup \dots = L L^* = L^* L$$
- **Relaciones:**
  - $L^* = L^+ \cup \{\lambda\}$
  - $L^* - \{\lambda\} = L^+$ (cuando $\lambda \notin L$)
- **Propiedades de clausura:**
  - $L^* L^* = L^*$
  - $(L^*)^* = L^*$
  - $(L^+)^+ = L^+$
  - $L^+ = L L^*$
  - $(L^+)^* = L^*$
  - $(L^*)^+ = L^*$

### 6.5 Reversa de un Lenguaje ($L^R$)
$$L^R = \{\alpha^R : \alpha \in L\}$$
- **Propiedades:**
  - $(L_1 \cup L_2)^R = L_1^R \cup L_2^R$
  - $(L_1 \cap L_2)^R = L_1^R \cap L_2^R$
  - $(L_1 L_2)^R = L_2^R L_1^R$
  - $(L^R)^R = L$
  - $(L^*)^R = (L^R)^*$
  - $(L^+)^R = (L^R)^+$

### 6.6 Precedencia de los Operadores (Diapositiva 26)
En ausencia de paréntesis:
1. **Potencia ($L^n$), Reversa ($L^R$), Clausuras ($L^*, L^+$)**
2. **Concatenación ($L_1 L_2$)**
3. **Unión ($L_1 \cup L_2$), Intersección ($L_1 \cap L_2$), Resta ($L_1 - L_2$)**

---

## 7. Bibliografía de la Cátedra (Diapositiva 27)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*. Capítulo 1: Alfabetos, cadenas y lenguajes. Secciones 1.1 hasta 1.12.
- **Peter Linz:** *An Introduction to Formal Languages and Automata*. Capítulo 1.2.
- **Lorena Bergamini:** *Autómatas, Lenguajes y Gramáticas*. Sección 1.
