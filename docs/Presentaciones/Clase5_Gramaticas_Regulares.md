# Clase 5: Gramáticas Regulares y Gramáticas Formales

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase 5 2026.pdf` (Clase 5)

---

## 1. ¿Qué es una Gramática? (Diapositivas 2 - 4)

- Una **gramática** es un conjunto de reglas para formar correctamente las frases (cadenas) de un lenguaje.
- Una regla es una expresión de la forma $\alpha \to \beta$, donde $\alpha$ y $\beta$ son cadenas de símbolos del alfabeto (llamados **símbolos terminales**) o variables (**símbolos no terminales**).

### Ejemplo de Reglas de Gramática Castellana:
- $R_1: \text{frase} \to \text{sujeto} + \text{predicado}$
- $R_2: \text{sujeto} \to \text{artículo} + \text{sustantivo} + \text{adjetivo}$
- $R_3: \text{sujeto} \to \text{artículo} + \text{sustantivo}$
- $R_4: \text{predicado} \to \text{verbo}$
- $R_5: \text{predicado} \to \text{verbo} + \text{adverbio}$
- $R_6: \text{adverbio} \to \text{frecuentemente}$
- $R_7: \text{artículo} \to \text{el}$
- $R_8: \text{artículo} \to \text{la}$
- $R_9: \text{sustantivo} \to \text{libro}$
- $R_{10}: \text{sustantivo} \to \text{película}$
- $R_{11}: \text{adjetivo} \to \text{nuevo}$
- $R_{12}: \text{verbo} \to \text{aburre}$
- $R_{13}: \text{verbo} \to \text{entretiene}$

#### Derivación 1 (Diapositiva 3):
$$\text{frase} \xrightarrow{R_1} \text{sujeto} + \text{predicado} \xrightarrow{R_3} \text{artículo} + \text{sustantivo} + \text{predicado} \xrightarrow{R_4} \text{artículo} + \text{sustantivo} + \text{verbo} \xrightarrow{R_7, R_9, R_{13}} \text{el} + \text{libro} + \text{entretiene}$$

#### Derivación 2 (Diapositiva 4):
$$\text{frase} \xrightarrow{R_1} \text{sujeto} + \text{predicado} \xrightarrow{R_2} \text{artículo} + \text{sustantivo} + \text{adjetivo} + \text{predicado} \xrightarrow{R_5} \text{artículo} + \text{sustantivo} + \text{adjetivo} + \text{verbo} + \text{adverbio} \xrightarrow{R_7, R_9, R_{11}, R_{12}, R_6} \text{el} + \text{libro} + \text{nuevo} + \text{aburre} + \text{frecuentemente}$$

---

## 2. Definición Formal de una Gramática (Diapositivas 5 - 8)

Una gramática es una 4-tupla:
$$G = (V, \Sigma, S, P)$$
con $V \cap \Sigma = \emptyset$, donde:
- **$V$:** Conjunto finito de símbolos no terminales o variables sintácticas.
- **$\Sigma$:** Conjunto finito de símbolos terminales o constantes.
- **$S \in V$:** Variable inicial o axioma.
- **$P$:** Conjunto finito de producciones (reglas) de la forma $\alpha \to \beta$ tal que $\alpha, \beta \in (V \cup \Sigma)^*$ y $\alpha \neq \lambda$.

### Derivación y Lenguaje Generado:
- Se dice que $u\alpha v$ deriva en $u\beta v$ (denotado $u\alpha v \Rightarrow u\beta v$) si existe $\alpha \to \beta \in P$.
- Una cadena $w \in \Sigma^*$ es derivable a partir de $G$ si:
  $$S \Rightarrow a_1 \Rightarrow a_2 \Rightarrow \dots \Rightarrow a_n \Rightarrow w \quad (\text{denotado } S \Rightarrow^* w \text{ o } S \Rightarrow^n w)$$
- **Lenguaje generado:** $L(G) = \{w \in \Sigma^* : S \Rightarrow^* w\}$.

### Ejemplo de Diapositiva 7:
- $V = \{S\}$, $\Sigma = \{0, 1\}$, Axioma: $S$.
- Reglas: $1: S \to 0S1$; $2: S \to \lambda$.
- Genera el lenguaje no regular $L(G) = \{0^n 1^n : n \ge 0\}$.

### Ejemplo de Diapositiva 8: Identificadores en Lenguajes de Programación
- $V = \{\text{ID}, \text{LETRA}, \text{DIGITO}\}$
- $\Sigma = \{a, b, \dots, z, 0, 1, \dots, 9\}$
- $S = \text{ID}$
- $P = \{\text{ID} \to \text{LETRA}; \; \text{ID} \to \text{ID } \text{DIGITO}; \; \text{ID} \to \text{ID } \text{LETRA}; \; \text{LETRA} \to a|b|\dots|z; \; \text{DIGITO} \to 0|1|\dots|9\}$

#### Derivación de la cadena `punto0`:
$$\text{ID} \Rightarrow \text{ID } \text{DIGITO} \Rightarrow \text{ID } 0 \Rightarrow \text{ID } \text{LETRA } 0 \Rightarrow \text{ID } o0 \Rightarrow \text{ID } \text{LETRA } o0 \Rightarrow \text{ID } to0 \Rightarrow \text{ID } \text{LETRA } to0 \Rightarrow \text{ID } nto0 \Rightarrow \text{ID } \text{LETRA } nto0 \Rightarrow \text{ID } unto0 \Rightarrow \text{LETRA } unto0 \Rightarrow punto0$$

---

## 3. Gramáticas Regulares (Diapositivas 9 - 11)

- **Lineal por la derecha:** Todas las producciones son de la forma:
  $$A \to aB \quad \mid \quad A \to B \quad \mid \quad A \to a \quad \mid \quad A \to \lambda$$
- **Lineal por la izquierda:** Todas las producciones son de la forma:
  $$A \to Ba \quad \mid \quad A \to B \quad \mid \quad A \to a \quad \mid \quad A \to \lambda$$
- Una gramática es **regular** si es lineal por la derecha o lineal por la izquierda (sin mezclarlas).

### Ejemplo 1 de Gramática Regular (Diapositiva 10):
$V = \{S, A\}$, $\Sigma = \{0, 1\}$, Producciones:
$$1: S \to 0S, \quad 2: S \to 1A, \quad 3: S \to \lambda, \quad 4: A \to 1A, \quad 5: A \to 1$$

### Ejemplo 2 de Gramática Regular (Diapositiva 11):
$V = \{S, A, B\}$, $\Sigma = \{0, 1\}$, Producciones:
$$S \to 0A \mid 1B \mid 1$$
$$A \to 0A \mid 1B$$
$$B \to 0B \mid 1B \mid 0 \mid 1$$

---

## 4. Árboles de Derivación Sintáctica (Diapositivas 12 - 16)

Un **árbol con raíz** es un grafo dirigido con un nodo raíz (grado de entrada 0) y nodos interiores (grado de entrada 1).
- **Raíz:** Etiquetada con el símbolo inicial $S$.
- **Nodos interiores:** Etiquetados con no terminales ($V$).
- **Hojas:** Etiquetadas con terminales ($\Sigma$) o $\lambda$.
- **Rendimiento:** Las hojas leídas de izquierda a derecha forman la cadena derivada $w$.

### Ejemplo 1 (Diapositiva 15):
Gramática:
$$S \to AB \mid AaB, \quad A \to aA \mid a, \quad B \to bBa \mid b$$

### Ejemplo 2 (Diapositiva 16):
Gramática:
$$S \to BAa, \quad A \to bBC \mid a, \quad B \to bB \mid b \mid \lambda, \quad C \to aB \mid aa$$

---

## 5. Equivalencia entre Gramáticas Regulares y Autómatas Finitos (Diapositivas 17 - 26)

### 5.1 De Gramática Regular a Autómata Finito (Diapositivas 18 - 23)
Dada $G = (V, \Sigma, S, P)$ lineal por derecha, construimos $M = (\Sigma, Q, q_0, F, \Delta)$:
- $Q = V \cup \{Z\}$ ($Z$ es el estado asociado a las reglas $A \to a$)
- $q_0 = S$
- $F = \{A \in V : A \to \lambda \in P\} \cup \{Z\}$
- Transiciones:
  - $\Delta(A, a) = \{B : A \to aB \in P\}$
  - $\Delta(A, a) = \{Z : A \to a \in P\}$
  - $\Delta(A, \lambda) = \{B : A \to B \in P\}$

#### Ejemplo de Diapositiva 23 (Caso con producciones-$\lambda$ sin necesidad de $Z$):
Gramática:
$$S \to aS \mid B \mid \lambda$$
$$B \to bB \mid C \mid \lambda$$
$$C \to cC \mid \lambda$$
Autómata equivalente: $Q = \{S, B, C\}$, $q_0 = S$, $F = \{S, B, C\}$.

### 5.2 De Autómata Finito a Gramática Regular (Diapositivas 24 - 26)
Dado $M = (\Sigma, Q, q_0, F, \Delta)$, construimos $G = (V, \Sigma, S, P)$:
- $V = Q$
- $S = q_0$
- Reglas $P$:
  - $q_i \to a q_k$ si $q_k \in \Delta(q_i, a)$
  - $q_i \to q_k$ si $q_k \in \Delta(q_i, \lambda)$
  - $q_i \to \lambda$ si $q_i \in F$

#### Ejemplo 1 (Diapositiva 25):
- $V = \{S, X, Y\}$, $\Sigma = \{0, 1, 2\}$, Axioma: $S$
- Reglas:
  $$S \to 0S \mid 1S \mid 2X$$
  $$X \to 0S \mid 1S \mid 2Y$$
  $$Y \to 0Y \mid 1Y \mid 2Y \mid \lambda$$

#### Ejemplo 2 (Diapositiva 26):
- $V = \{q_0, q_1\}$, $\Sigma = \{a, b\}$, Axioma: $q_0$
- Reglas:
  $$q_0 \to a q_0 \mid b q_1$$
  $$q_1 \to a q_0 \mid b q_1 \mid \lambda$$

---

## 6. Bibliografía de la Cátedra (Diapositiva 27)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*. Capítulos 4.1, 4.2, 4.3, 4.7.
- **Peter Linz:** *An Introduction to Formal Languages and Automata*. Capítulo 3.3.
- **Lorena Bergamini:** *Autómatas, Lenguajes y Gramáticas*.
