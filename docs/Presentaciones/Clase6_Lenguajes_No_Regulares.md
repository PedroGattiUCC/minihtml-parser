# Clase 6: Lenguajes No Regulares y el Lema de Bombeo

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase 6 2026.pdf` (Clase 6)

---

## 1. Ejemplos de Lenguajes No Regulares y Necesidad de Memoria (Diapositivas 2 - 4)

¿Existe una gramática regular o un autómata finito para reconocer los siguientes lenguajes?
1. $L = \{a^n b^n : n \ge 0\}$
2. $L = \{\alpha \in \Sigma^* : \alpha = \alpha^R\}$ (cadenas capicúas / palíndromas)
3. $L = \{\alpha \in \Sigma^* : \alpha = \beta \beta, \; \beta \in \Sigma^*\}$ (duplicación exacta)

### La Respuesta Teórica:
**NO.** Ninguno de ellos puede ser generado por una gramática regular ni reconocido por un autómata finito:
- Estos lenguajes son **independientes de contexto** o **sensibles al contexto**.
- Un autómata necesita **memoria auxiliar** para reconocer sus cadenas: recordar todos los caracteres leídos al principio para compararlos con los que se leen después.
- **Eso no se puede hacer con un conjunto finito de estados.**

---

## 2. El Lema de Bombeo para Lenguajes Regulares (Diapositivas 5 - 8)

Esta propiedad establece que toda cadena suficientemente larga de un lenguaje regular contiene una subcadena que puede repetirse una cantidad arbitraria de veces (*bombeo*) de modo que la nueva cadena resultante continúe perteneciendo al lenguaje.

### Enunciado Formal:
> Para todo lenguaje regular $L$ (sobre un alfabeto dado $\Sigma$), existe una constante $n \in \mathbb{N}$, llamada **constante de bombeo para $L$**, tal que toda cadena $\omega \in L$ con $|\omega| \ge n$ satisface la siguiente propiedad:  
> $\omega$ se puede descomponer como:
> $$\omega = \alpha \beta \gamma$$
> cumpliendo:
> 1. $|\alpha \beta| \le n$
> 2. $\beta \neq \lambda \quad (|\beta| \ge 1)$
> 3. $\forall i \ge 0, \quad \alpha \beta^i \gamma \in L$

---

### 2.1 Ejemplo 1: $L = \{\text{cadenas con cantidad par de } a\}$ (Diapositiva 7)
- **Constante de bombeo:** $n = 2$.
- Toda cadena $\omega \in L$ con $|\omega| \ge 2$ admite una descomposición $\omega = \alpha \beta \gamma$ con $|\alpha \beta| \le 2$:
  - Si $\omega$ comienza con $b$: elegimos $\alpha = \lambda$ y $\beta = b$. Por lo tanto, $\gamma$ conserva cantidad par de 'a'. Luego $\alpha \beta^i \gamma = b^i \gamma$ tiene cantidad par de 'a' $\implies \alpha \beta^i \gamma \in L$.
  - Si $\omega$ comienza con $ab$: elegimos $\alpha = a$ y $\beta = b$. $\gamma$ tiene cantidad impar de 'a'. Luego $\alpha \beta^i \gamma = a b^i \gamma$ tiene cantidad par de 'a' $\implies \alpha \beta^i \gamma \in L$.
  - Si $\omega$ comienza con $aa$: elegimos $\alpha = \lambda$ y $\beta = aa$. Luego $\alpha \beta^i \gamma = (aa)^i \gamma = a^{2i} \gamma$ tiene cantidad par de 'a' $\implies \alpha \beta^i \gamma \in L$.

---

### 2.2 Ejemplo 2: $L = \{\text{cadenas que comienzan y terminan con } bb\}$ (Diapositiva 8)
- **Constante de bombeo:** $n = 4$.
- Toda cadena $\omega \in L$ con $|\omega| \ge 4$ es de la forma $\omega = bb \omega' bb$.
- Descomposición: $\alpha = \lambda$, $\beta = bb$, $\gamma = \omega' bb$.
- Claramente $|\alpha \beta| = |bb| = 2 \le 4$ y $\beta \neq \lambda$.
- Bombeo: $\alpha \beta^i \gamma = (bb)^i \omega' bb$ comienza y termina con $bb$ para todo $i \ge 1$ (e incluso para $i=0$ si $\omega'$ mantiene el formato) $\implies \alpha \beta^i \gamma \in L$.

---

## 3. Demostración de No-Regularidad usando el Lema de Bombeo (Diapositivas 9 - 12)

### ¿Cómo probar que un lenguaje NO es regular?
Se demuestra por contradicción mostrando que para cualquier constante $n$, **existe al menos una cadena adecuada y larga $\omega \in L$ con $|\omega| \ge n$ para la cual NO se cumple la propiedad de bombeo**:
Cualquiera sea la descomposición $\omega = \alpha \beta \gamma$ con $|\alpha \beta| \le n$ y $\beta \neq \lambda$, **existe un $i$ para el cual $\alpha \beta^i \gamma \notin L$**.

---

### 3.1 Demostración 1: $L = \{a^k b^k : k \ge 1\}$ (Diapositiva 10)
1. Sea $n$ cualquier número natural.
2. Tomamos la cadena estratégica: $\omega = a^n b^n \in L$, con $|\omega| = 2n \ge n$.
3. Si $\omega = \alpha \beta \gamma$ es cualquier descomposición válida con $|\alpha \beta| \le n$ y $\beta \neq \lambda$:  
   Dado que los primeros $n$ caracteres son exclusivamente 'a', tanto $\alpha$ como $\beta$ están formadas puramente por 'a':
   $$\alpha = a^r, \quad \beta = a^s \quad (\text{con } s \ge 1), \quad \gamma = a^{n-r-s} b^n$$
4. Evaluamos con $i = 0$ (*bombeo hacia abajo*):
   $$\alpha \beta^0 \gamma = \alpha \gamma = a^r a^{n-r-s} b^n = a^{n-s} b^n$$
5. Como $s \ge 1$, el número de 'a' es $n - s < n$, mientras que hay $n$ símbolos 'b'. Por lo tanto, $a^{n-s} b^n \notin L$.
6. **Conclusión:** $L = \{a^k b^k : k \ge 1\}$ **no es un lenguaje regular**. $\blacksquare$

---

### 3.2 Demostración 2: $L = \{\text{paréntesis balanceados}\}$ (Diapositiva 11)
1. Sea $n$ cualquier número natural.
2. Tomamos la cadena: $\omega = (^n )^n \in L$, con $|\omega| = 2n \ge n$.
3. Dado que $|\alpha \beta| \le n$ y $\beta \neq \lambda$, $\beta$ se compone enteramente de paréntesis de apertura: $\beta = (^s$ con $s \ge 1$.
4. Bombeando hacia abajo con $i = 0$:
   $$\alpha \beta^0 \gamma = (^{n-s} )^n \notin L$$
   pues posee menos paréntesis de apertura que de cierre.
5. **Conclusión:** El lenguaje de paréntesis balanceados **no es regular**. $\blacksquare$

---

### 3.3 Demostración 3: $L = \{\alpha \in \{a, b\}^* : \alpha = \alpha^R\}$ (Palíndromos) (Diapositiva 12)
1. Sea $n$ cualquier número natural.
2. Tomamos la cadena estratégica: $\omega = a^n b a^n \in L$, con $|\omega| = 2n + 1 \ge n$.
3. Dado que $|\alpha \beta| \le n$ y $\beta \neq \lambda$, $\alpha$ y $\beta$ son puramente 'a':
   $$\alpha = a^r, \quad \beta = a^s \quad (\text{con } s \ge 1), \quad \gamma = a^{n-r-s} b a^n$$
4. Evaluamos con $i = 2$ (*bombeo hacia arriba*):
   $$\alpha \beta^2 \gamma = a^r a^{2s} a^{n-r-s} b a^n = a^{n+s} b a^n$$
5. Como $s \ge 1$, la cadena resultante posee $n+s$ símbolos 'a' a la izquierda y solo $n$ a la derecha. Ya no es simétrica:
   $$a^{n+s} b a^n \notin L$$
6. **Conclusión:** El lenguaje de palíndromos **no es regular**. $\blacksquare$

---

## 4. Sustentación Teórica para el Proyecto Integrador MiniHTML

> [!IMPORTANT]
> **Pregunta del Proyecto Integrador:**  
> *"¿Por qué un Autómata Finito no es capaz de validar este lenguaje de anidamiento y por qué se requiere la pila?"*
> 
> **Respuesta Formal con base en la Clase 6:**  
> Un documento MiniHTML permite anidamiento arbitrario de etiquetas:
> $$\omega = \text{<p>}^n \text{TEXTO} \text{</p>}^n$$
> Este lenguaje contiene como sublenguaje isomórfico a $L = \{a^n b^n : n \ge 0\}$ y al lenguaje de paréntesis balanceados.  
> Por el Lema de Bombeo, un Autómata Finito posee un número fijo de estados $|Q| = k$. Si un documento presenta una profundidad de anidamiento $n > k$, por el Principio del Palomar la máquina se verá forzada a ciclar sobre sus estados internos dentro de las etiquetas de apertura, perdiendo la cuenta exacta de cuántas etiquetas fueron abiertas y en qué orden deben cerrarse.  
> Por lo tanto, MiniHTML **no es regular** y requiere inexorablemente un **Autómata a Pila con memoria LIFO** para emparejar etiquetas en orden inverso.

---

## 5. Bibliografía de la Cátedra (Diapositiva 13)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*. Capítulo 1: Alfabetos, cadenas y lenguajes. Sección 3.1.
