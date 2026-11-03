# Clase 4: Autómatas y Expresiones Regulares (Combinación y Teorema de Kleene)

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase 4 2026.pdf` (Clase 4)

---

## 1. Equivalencia entre Expresiones Regulares y Autómatas Finitos (Diapositivas 2 - 7)

### 1.1 De ER a AF (Gráficos de Conversión)
- **Gráficos de conversión:** Son AFN generalizados que admiten expresiones regulares completas como etiquetas en sus arcos de transición.
- **Procedimiento:** Consiste en una serie de expansiones sucesivas que transforman gradualmente la ER en un AFN canónico:
  1. **Paso inicial:** Crear un estado inicial y un estado final conectados por una única arista rotulada con la ER completa.
  2. **Regla de Unión ($R_1 + R_2$):** Se reemplaza la arista por dos aristas en paralelo rotuladas con $R_1$ y $R_2$ respectivamente.
  3. **Regla de Concatenación ($R_1 R_2$):** Se inserta un nodo intermedio, conectando el origen con $R_1$ al nodo intermedio y este al destino con $R_2$.
  4. **Regla de Clausura de Kleene ($R^*$):** Se agrega un lazo sobre un nodo intermedio con $R$, o bien la estructura canónica de Thompson con bifurcaciones $\lambda$.

### 1.2 Ejemplos Desarrollados de Cátedra:
- **Ejemplo 1 (Diapositiva 6):** Construcción del AFN para:
  $$E_1 = ab + ba^*$$
  - Bifurcación inicial para la suma ($+$) entre las ramas $ab$ y $ba^*$.
  - Descomposición de $ab$ en serie: estado inicial $\xrightarrow{a}$ estado intermedio $\xrightarrow{b}$ estado final.
  - Descomposición de $ba^*$: estado inicial $\xrightarrow{b}$ estado con lazo $\xrightarrow{a}$ estado final.

- **Ejemplo 2 (Diapositiva 7):** Construcción del AFN para:
  $$E_2 = (\lambda + b) ab + b^*(\lambda + a)$$
  - Bifurcación entre $(\lambda + b)ab$ y $b^*(\lambda + a)$.
  - Rama izquierda: alternancia inicial entre $\lambda$ y $b$, seguida por la secuencia $a$ y $b$.
  - Rama derecha: lazo inicial para $b^*$, seguido de bifurcación terminal hacia $\lambda$ o $a$.

---

## 2. De Autómata Finito a Expresión Regular: Método de Eliminación de Estados (Diapositivas 8 - 10)

Dado un autómata finito $M = (\Sigma, Q, q_0, F, \Delta)$, el procedimiento para obtener la ER equivalente para $L(M)$ es:

### Algoritmo Paso a Paso:
1. **Paso 1 (Normalización de Estados):**
   - Añadir un nuevo estado inicial $q_{\text{ini}}$ ($q_0$ deja de ser inicial).
   - Añadir un nuevo estado final $q_{\text{fin}}$ (los estados de $F$ dejan de ser finales).
   - Añadir transiciones espontáneas:
     $$\Delta(q_{\text{ini}}, \lambda) = \{q_0\}, \quad \Delta(q, \lambda) = \{q_{\text{fin}}\} \quad \forall q \in F$$
2. **Paso 2 (Eliminación de Transiciones Paralelas):**
   - Si entre dos nodos existen múltiples arcos con etiquetas $R_1, R_2, \dots$, se consolidan en una única arista rotulada con la suma:
     $$R_1 + R_2 + \dots$$
3. **Paso 3 (Eliminación de Nodos Muertos):**
   - Si desde algún nodo no existe ningún camino hacia otro estado o hacia el estado final, ese nodo se elimina directamente (no aporta cadenas aceptadas).
4. **Paso 4 (Eliminación de Nodos Intermedios):**
   - Para cada nodo intermedio $q$ a eliminar:
     - Sean $p$ cualquier predecesor de $q$, $r$ cualquier sucesor de $q$, y $R_{qq}$ el lazo sobre $q$ (si no hay lazo, $R_{qq} = \emptyset \implies R_{qq}^* = \lambda$).
     - La nueva etiqueta directa entre $p$ y $r$ se actualiza como:
       $$R_{\text{nuevo}} = R_{pr} + R_{pq} (R_{qq})^* R_{qr}$$
     - Se elimina el estado $q$.

### Secuencia del Ejemplo de Diapositiva 10:
El ejemplo muestra la reducción en 5 pasos progresivos:
- Paso 1: Incorporación de $q_{\text{ini}}$ y $q_{\text{fin}}$.
- Paso 2: Fusión de aristas paralelas en sumas.
- Paso 3: Eliminación del primer nodo intermedio (nodo 1).
- Paso 4: Eliminación del segundo nodo intermedio (nodo 2) actualizando expresiones con lazos $(R^*)$.
- Paso 5: Quedan únicamente $q_{\text{ini}}$ y $q_{\text{fin}}$ conectados por la expresión regular definitiva.

---

## 3. Combinación Modular de Autómatas (Diapositivas 11 - 13)

Permite construir de forma formal y directa los autómatas para las operaciones regulares a partir de dos AFN-$\lambda$ dados, $M_1 = (\Sigma, Q_1, q_1, F_1, \Delta_1)$ y $M_2 = (\Sigma, Q_2, q_2, F_2, \Delta_2)$:

### 3.1 Unión de Autómatas ($L(M_1) \cup L(M_2)$) (Diapositiva 11)
El AFN-$\lambda$ $M = (\Sigma, Q, q_0, F, \Delta)$ se define con:
- $Q = Q_1 \cup Q_2 \cup \{q_0\}$ (nuevo estado inicial)
- $F = F_1 \cup F_2$
- $\Delta = \Delta_1 \cup \Delta_2 \cup \{((q_0, \lambda), \{q_1, q_2\})\}$
Reconoce exactamente el lenguaje $L(M_1) \cup L(M_2)$.

### 3.2 Concatenación de Autómatas ($L(M_1) L(M_2)$) (Diapositiva 12)
El AFN-$\lambda$ $M = (\Sigma, Q, q_1, F, \Delta)$ se define con:
- $Q = Q_1 \cup Q_2$
- Estado inicial: $q_1$
- $F = F_2$
- $\Delta = \Delta_1 \cup \Delta_2 \cup \{((q, \lambda), \{q_2\}) : q \in F_1\}$
Reconoce exactamente el lenguaje $L(M_1) L(M_2)$.

### 3.3 Clausura de un Autómata ($L(M_1)^*$) (Diapositiva 13)
El AFN-$\lambda$ $M = (\Sigma, Q, q_0, F, \Delta)$ se define con:
- $Q = Q_1 \cup \{q_0\}$ (nuevo estado inicial)
- $F = F_1 \cup \{q_0\}$
- $\Delta = \Delta_1 \cup \{((q, \lambda), \{q_0\}) : q \in F_1\} \cup \{((q_0, \lambda), \{q_1\})\}$
Reconoce exactamente el lenguaje $L(M_1)^*$.

---

## 4. Bibliografía de la Cátedra (Diapositiva 14)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*. Capítulo 1: Alfabetos, cadenas y lenguajes. Secciones 2.4 a 2.12.
- **Peter Linz:** *An Introduction to Formal Languages and Automata*. Capítulo 2.2.
- **Lorena Bergamini:** *Autómatas, Lenguajes y Gramáticas*.
