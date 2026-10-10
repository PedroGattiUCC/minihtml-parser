# Clase 2: Definición de Lenguajes Regulares y Expresiones Regulares

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase2 2026.pdf` (Clase 2)

---

## 1. Definición Inductiva de Lenguajes Regulares (Diapositivas 2 - 4)

Los **lenguajes regulares** son aquellos que se pueden construir recursivamente a partir de ciertos lenguajes atómicos aplicando una cantidad finita de **operadores regulares** (unión, concatenación y clausura de Kleene).

### Definición Formal (Sea $\Sigma$ un alfabeto):
- **Casos Base:**
  1. $\emptyset$ es un lenguaje regular (lenguaje vacío).
  2. $\{\lambda\}$ es un lenguaje regular (lenguaje que solo contiene la cadena vacía).
  3. $\{a\}$ es un lenguaje regular, para todo $a \in \Sigma$ (lenguaje *singleton* o unitario).
- **Casos Recursivos:**
  Si $L_1$ y $L_2$ son lenguajes regulares, entonces:
  1. $L_1 \cup L_2$ es un lenguaje regular *(Unión)*.
  2. $L_1 L_2$ es un lenguaje regular *(Concatenación)*.
  3. $L_1^*$ es un lenguaje regular *(Clausura de Kleene)*.

El conjunto de todos los lenguajes regulares sobre $\Sigma$ se denota $\mathcal{LR}_\Sigma$.

### Ejemplos sobre $\Sigma = \{a, b\}$:
- $L_0 = \{a, b\}^* = (\{a\} \cup \{b\})^* = \Sigma^*$ (lenguaje universal en $\Sigma$, todas las cadenas posibles).
- $L_1 = \{b^n a a b^m : n, m \in \mathbb{N}\} \in \mathcal{LR}_\Sigma$, pues es la concatenación de $\{b\}^*$, $\{a\}$, $\{a\}$ y $\{b\}^*$.
- $L_2 = \{b\alpha : \alpha \in \Sigma^*\} \in \mathcal{LR}_\Sigma$, pues $L_2 = \{b\}(\{a\} \cup \{b\})^*$.
- $L_3 = \{b^n a^m : n, m \in \mathbb{N}\} \in \mathcal{LR}_\Sigma$, pues $L_3 = \{b\}^* \{a\}^*$.

---

## 2. Lenguajes No Regulares y Finitud (Diapositivas 5 - 7)

### ¿Existen lenguajes no regulares?
Sí. Requieren contar o verificar simetrías con memoria no acotada:
- $L_4 = \{a^n b^n : n \in \mathbb{N}\}$ es un lenguaje **no regular**.
- $L_5 = \{\text{cadenas palíndromas}\}$ es un lenguaje **no regular**.

### Teorema: Todo Lenguaje Finito es Regular (Diapositiva 6)
**Enunciado:** Si $L$ es un lenguaje finito, entonces $L$ es regular.

**Demostración:**  
Sea $L = \{\alpha_1, \dots, \alpha_k\}$ con $\alpha_i \in \Sigma^*$ y $k \ge 0$.  
- Si $k = 0 \implies L = \emptyset$, que es regular por caso base.  
- Si $k \ge 1 \implies L = \{\alpha_1\} \cup \dots \cup \{\alpha_k\}$, por lo que $L$ es la unión finita de conjuntos unitarios $\{\alpha_i\}$.  
Veamos que cada $\{\alpha_i\}$ es regular:
- Si $\alpha_i = \lambda \implies \{\lambda\} \in \mathcal{LR}_\Sigma$ por caso base.
- Si $\alpha_i = a_1 \dots a_r$ con $r \ge 1$, entonces $\{\alpha_i\} = \{a_1\} \dots \{a_r\}$. Como cada $\{a_j\} \in \mathcal{LR}_\Sigma$ por caso base, $\{\alpha_i\} \in \mathcal{LR}_\Sigma$ por caso recursivo de concatenación.  
Por lo tanto, al ser unión finita de lenguajes regulares, $L \in \mathcal{LR}_\Sigma$. $\blacksquare$

### Regularidad y Operaciones de Clausura (Diapositiva 7)
Si $L_1, L_2 \in \mathcal{LR}_\Sigma$, entonces:
1. $L_1 \cup L_2 \in \mathcal{LR}_\Sigma$
2. $L_1 \cap L_2 \in \mathcal{LR}_\Sigma$
3. $L_1 - L_2 \in \mathcal{LR}_\Sigma$
4. $L_1^c \in \mathcal{LR}_\Sigma$
5. $L_1^R \in \mathcal{LR}_\Sigma$

---

## 3. Expresiones Regulares (ER) (Diapositivas 8 - 11)

Una **expresión regular (ER)** es una notación descriptiva compacta que explicita el patrón o regularidad que cumplen las cadenas de un lenguaje regular. Se denota $L(E)$ al lenguaje denotado por la expresión regular $E$.

### Definición Constructiva (Sea $\Sigma$ un alfabeto):
- **Casos Base:**
  - $\emptyset$ es una ER y $L(\emptyset) = \emptyset = \{\}$
  - $\lambda$ es una ER y $L(\lambda) = \{\lambda\}$
  - $a$ es una ER (con $a \in \Sigma$) y $L(a) = \{a\}$
- **Casos Recursivos:**
  Si $E_1$ y $E_2$ son ER, entonces:
  - $(E_1)$ es una ER, con $L((E_1)) = L(E_1)$
  - $E_1 + E_2$ es una ER, con $L(E_1 + E_2) = L(E_1) \cup L(E_2)$
  - $E_1 E_2$ es una ER, con $L(E_1 E_2) = L(E_1) L(E_2)$
  - $E_1^*$ es una ER, con $L(E_1^*) = (L(E_1))^*$

### Ejemplos de Diapositiva 10:
- $a + b$ denota $\{a\} \cup \{b\} = \{a, b\}$.
- $a^* b b a^*$ denota $\{a\}^* \{b\} \{b\} \{a\}^* = \{a^n b b a^m : n, m \in \mathbb{N}\}$.
- $(a+b)^* a (a+b)$ denota $\{a, b\}^* \{a\} \{a, b\} = \Sigma^* \{a\} \Sigma$ (lenguaje de cadenas cuyo **anteúltimo carácter es $a$**).
- $(a+b)^* (aa + ab)$ es una expresión equivalente a la anterior.

### Precedencia de Operaciones entre ER (Diapositiva 11):
1. **Clausura ($^*$)**
2. **Concatenación**
3. **Suma ($+$)**

*Ejemplos de interpretación según paréntesis:*
- $b a + b \implies L = \{ba, b\}$
- $b(a+b) \implies L = \{ba, bb\}$
- $a b^* \implies L = \{a\}\{b\}^* = \{a, ab, abb, abbb, \dots\}$
- $(a b)^* \implies L = \{ab\}^* = \{\lambda, ab, abab, ababab, \dots\}$

---

## 4. De Lenguaje a Expresión Regular: Ejemplos de Cátedra (Diapositivas 12 - 15)

Para construir una ER a partir de un lenguaje descriptivo, deben cumplirse dos condiciones:
- **Correctitud:** Las cadenas generadas por la ER deben pertenecer al lenguaje.
- **Completitud:** Todas las cadenas del lenguaje deben estar representadas por la ER.

### Ejemplos Resueltos:

1. **$L_1 = \{\text{cadenas de } a, b, c \text{ que contengan la subcadena } bb\}$:**
   - Estructura: $\alpha = u bb w$ con $u, w \in \{a, b, c\}^*$.
   - **$E_1 = (a + b + c)^* bb (a + b + c)^*$**

2. **$L_2 = \{\text{cadenas de } a, b, c \text{ que NO contengan la subcadena } bb\}$:**
   - Las 'b' aisladas deben ir seguidas de 'a', 'c' o terminar la cadena:
   - **$E_2 = (a + c + ba + bc)^* (\lambda + b)$**
   - O equivalentemente comenzando por izquierda: **$E'_2 = (\lambda + b)(a + c + ab + cb)^*$**

3. **$L_3 = \{\text{cadenas de } a, b, c \text{ que contengan la subcadena } bb \text{ exactamente una sola vez}\}$:**
   - Estructura: $\alpha = u bb w$ donde $u, w \in L_2$, $u$ no termina en 'b', y $w$ no comienza en 'b':
   - **$E_3 = (a + c + ba + bc)^* bb (a + c + ab + cb)^*$**

4. **$L_4 = \{\text{cadenas de } a, b \text{ de la forma } a^{2n} b^{2m+1} \text{ con } n, m \in \mathbb{N}\}$:**
   - Cantidad par de 'a' seguida de cantidad impar de 'b':
   - **$E_4 = (aa)^* (bb)^* b$**
   - *(Atención: los paréntesis son indispensables. La expresión $E'_4 = aa^* bb^* b$ representaría cadenas con al menos una 'a' y al menos dos 'b': $a^+ b^+ b$).*

5. **$L_5 = \{\text{cadenas de } \{a, b\}^* \text{ que contengan } a \text{ y } b \text{ alternadas}\}$:**
   - Sin repeticiones de símbolos idénticos consecutivos:
   - **$E_5 = (\lambda + b)(ab)^*(a + \lambda)$**

---

## 5. Tabla de Equivalencias de Expresiones Regulares (Diapositivas 16 - 17)

Dos ER $E_1$ y $E_2$ son equivalentes si $L(E_1) = L(E_2)$.

### Tabla Fundamental de Identidades:
| Propiedad | Identidades Algebraicas |
|:---|:---|
| **Conmutatividad de $+$** | $R + S = S + R$ |
| **Elemento neutro de $+$** | $R + \emptyset = R$ |
| **Idempotencia de $+$** | $R + R = R$ |
| **Asociatividad de $+$** | $(R + S) + T = R + (S + T)$ |
| **Elemento neutro de concat.** | $R \lambda = \lambda R = R$ |
| **Elemento absorbente de concat.** | $R \emptyset = \emptyset R = \emptyset$ |
| **Asociatividad de concat.** | $(RS)T = R(ST)$ |
| **Distributividad** | $R(S + T) = RS + RT \quad \land \quad (R + S)T = RT + ST$ |
| **Propiedades de estrella ($^*$)** | $R^* = R^* R^* = (R^*)^*$ |
| **Estrella sobre neutros** | $\emptyset^* = \lambda^* = \lambda$ |
| **Suma bajo estrella** | $(R + S)^* = (R^* + S^*)^* = (R^* S^*)^*$ |
| **Desplazamiento** | $R(SR)^* = (RS)^* R$ |
| **Conmutación con estrella** | $R R^* = R^* R$ |
| **Desarrollo de estrella** | $R^* = \lambda + R R^*$ |
| **Inclusión** | Si $L(R) \subseteq L(S) \implies R + S = S$ |
| **Adición de vacía** | $\lambda + R^* = R^*$ |
| **Lema de Arden** | $S = RS + T \iff S = R^* T \quad (\text{si } \lambda \notin L(R))$<br>$S = SR + T \iff S = TR^*$ |

### Ejemplos de Simplificación Formal (Diapositiva 17):
1. $(a+b)^* (a+b)(a+c) = (a+b)^* (aa + ac + ba + bc) = (a+b)(a+b)^* (a+c)$
2. $(a^* + b^*) c = a^* c + b^* c$
3. $(a+b) + c(a+b) = \lambda(a+b) + c(a+b) = (\lambda + c)(a+b)$
4. $(a+b)^* c + (\lambda + (a+b)^* )(c+a) = (a+b)^* c + (a+b)^* (c+a) = (a+b)^* (c + c + a) = (a+b)^* (c+a)$

---

## 6. Bibliografía de la Cátedra (Diapositiva 18)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*. Capítulo 1: Alfabetos, cadenas y lenguajes. Secciones 1.13 - 1.14.
- **Peter Linz:** *An Introduction to Formal Languages and Automata*. Capítulo 3.1, 3.2.
- **Lorena Bergamini:** *Autómatas, Lenguajes y Gramáticas*.
