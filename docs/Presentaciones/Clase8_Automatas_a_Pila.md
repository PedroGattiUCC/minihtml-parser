# Clase 8: Autómatas a Pila (AP / PDA) y Lenguajes Libres de Contexto

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase 8 2026.pdf` (Clase 8)

---

## 1. Autómatas para Lenguajes Independientes de Contexto (Diapositiva 2)

- El Autómata Finito es la máquina secuencial que caracteriza a los Lenguajes Regulares (LR).
- Para reconocer Lenguajes Independientes de Contexto (LIC), el autómata debe superar la debilidad de los AF: la **carencia de un mecanismo de memoria**.
- Se equipa al autómata con una segunda cinta de memoria auxiliar cuyo modo de acceso es de tipo **Pila / Memoria LIFO** (*Last-In, First-Out*).

---

## 2. Autómata a Pila Determinista (AFPD) (Diapositivas 3 - 6)

Un autómata a pila opera con dos cintas:
1. Una **cinta de entrada**, de donde lee la cadena de entrada hacia la derecha.
2. Una **cinta de memoria (pila LIFO)** donde puede leer el tope y escribir / reemplazar símbolos.

### Definición Formal (7-tupla de Cátedra):
$$M = (\Sigma, \Gamma, Q, q_0, Z_0, F, \delta)$$
Donde:
- $\Sigma$: Alfabeto de entrada.
- $\Gamma$: Alfabeto de pila.
- $Q$: Conjunto finito y no vacío de estados.
- $q_0 \in Q$: Estado inicial.
- $Z_0 \in \Gamma$: Símbolo inicial de la pila (**marcador de fondo de pila**).
- $F \subseteq Q$: Conjunto de estados de aceptación o finales.
- $\delta: Q \times \Sigma \times \Gamma \to Q \times \Gamma^*$: Función de transición determinista.

### Semántica de la Transición (Diapositiva 4):
$$\delta(q, a, z) = (q', \gamma)$$
Significa: Si el autómata se encuentra en el estado $q$, el cabezal lee el símbolo $a$ en la cinta de entrada y en el tope de la pila se encuentra el símbolo $z$, entonces:
1. Pasa al estado $q'$.
2. Reemplaza el tope $z$ por la cadena de pila $\gamma \in \Gamma^*$.
   - Si $\gamma = \lambda \implies$ **desapila** $z$ (*pop*).
   - Si $\gamma = z \implies$ **conserva** el tope sin modificaciones.
   - Si $\gamma = yz \implies$ **apila** $y$ sobre $z$ (*push*).

### Criterio de Aceptación por Estado Final:
Una cadena $\alpha \in \Sigma^*$ es aceptada por $M$ si al terminar de procesar toda la cadena partiendo desde $q_0$, el estado alcanzado pertenece a $F$:
$$L(M) = \{\alpha \in \Sigma^* : \alpha \text{ es aceptada por } M \text{ alcanzando un estado final}\}$$

---

## 3. Autómata a Pila No Determinista con Transiciones Espontáneas (AFPN-$\lambda$) (Diapositivas 7 - 10)

Un **AFPN-$\lambda$** es una 7-tupla:
$$M = (\Sigma, \Gamma, Q, q_0, Z_0, F, \Delta)$$
con función de transición:
$$\Delta: Q \times (\Sigma \cup \{\lambda\}) \times \Gamma \to \mathcal{P}(Q \times \Gamma^*)$$

Donde:
$$\Delta(q, x, z) = \{(q_1, \gamma_1), \dots, (q_k, \gamma_k)\}$$
significa que estando en el estado $q$, leyendo el símbolo $x$ (o sin consumir entrada si $x = \lambda$) y con el símbolo $z$ en el tope de la pila, la máquina puede transicionar de forma no determinista a cualquiera de los estados $q_i$, reemplazando $z$ por $\gamma_i$.

---

## 4. Configuraciones Instantáneas de un Autómata a Pila (Diapositiva 11)

En cada paso de procesamiento, la configuración del sistema comprende:
1. El estado actual $q \in Q$.
2. La cadena de caracteres de entrada restante por leer $\omega \in \Sigma^*$.
3. El contenido completo de la pila $\gamma \in \Gamma^*$ (donde el primer carácter es el tope).

Se denota como la tripla:
$$(q, \omega, \gamma)$$

### Paso Computacional ($\vdash$):
$$(q, \omega, \gamma) \vdash (p, \omega', \gamma')$$
si el autómata realizó la transición $\delta(q, a, X) = (p, \eta)$, siendo:
- $\omega = a \omega'$ (consume el símbolo $a$).
- $\gamma = X \zeta$ (el tope era $X$).
- $\gamma' = \eta \zeta$ (el tope $X$ es reemplazado por la secuencia $\eta$).

La relación $\vdash^*$ representa una secuencia de cero o más pasos computacionales.

---

## 5. Lenguaje por Vaciado de Pila vs. Estado Final (Diapositivas 12 - 14)

Dado un autómata a pila $M$, existen dos formas formales de definir las cadenas que acepta:
1. **$L(M)$ (Alcance de Estado Final):**
   $$L(M) = \{w \in \Sigma^* : (q_0, w, Z_0) \vdash^* (q_f, \lambda, \gamma) \text{ con } q_f \in F\}$$
2. **$N(M)$ (Vaciamiento de Pila):**
   $$N(M) = \{w \in \Sigma^* : (q_0, w, Z_0) \vdash^* (q, \lambda, \lambda) \text{ para cualquier } q \in Q\}$$
   *(La pila se vacía por completo exactamente al procesar el último símbolo de $w$, sin importar en qué estado quede la máquina).*

### Ejemplo de Discrepancia (Diapositiva 13):
Dado un autómata $M$ concreto:
- $L(M) = \{a\alpha : \alpha \in \Sigma^*\}$ (cadenas que comienzan con 'a').
- $N(M) = \{\alpha : |\alpha| \ge 2\}$ (cadenas de longitud mayor o igual a 2).
- **Conclusión:** Para un autómata $M$ arbitrario, en general $L(M) \neq N(M)$.

---

## 6. Teorema de Equivalencia entre $L(M)$ y $N(M)$ para AFPN-$\lambda$ (Diapositivas 14 - 19)

> **Teorema:**
> 1. Para todo AFPN-$\lambda$ $M$, existe un AFPN-$\lambda$ $M'$ tal que $N(M') = L(M)$.
> 2. Para todo AFPN-$\lambda$ $M$, existe un AFPN-$\lambda$ $M''$ tal que $L(M'') = N(M)$.

---

### 6.1 Conversión: De Estado Final a Vaciado de Pila ($N(M') = L(M)$) (Diapositivas 15 - 17)
Para lograr que $M'$ vacíe su pila si y solo si $M$ llega a un estado de aceptación:
1. Se añade un **nuevo estado inicial $q_0'$** y un **nuevo marcador de fondo $Z_0'$** a la pila ($\Gamma' = \Gamma \cup \{Z_0'\}$).  
   Al arrancar, $q_0'$ coloca $Z_0 Z_0'$ en la pila y salta a $q_0$:
   $$((q_0', \lambda, Z_0'), (q_0, Z_0 Z_0'))$$
2. Se añade un **estado vaciador $q_v$**. Desde cualquier estado de aceptación $q \in F$, se agregan transiciones-$\lambda$ hacia $q_v$:
   $$((q, \lambda, X), (q_v, \lambda)) \quad \forall X \in \Gamma \cup \{Z_0'\}$$
3. En $q_v$, se desapila sistemáticamente todo lo que quede en la pila mediante lazos-$\lambda$:
   $$((q_v, \lambda, X), (q_v, \lambda)) \quad \forall X \in \Gamma \cup \{Z_0'\}$$

> **¿Por qué es indispensable el nuevo marcador de fondo $Z_0'$? (Diapositiva 17):**  
> Si no se agregara $Z_0'$, el autómata original $M$ podría vaciar accidentalmente su pila durante cómputos intermedios no aceptados, aceptando erróneamente cadenas que no pertenecían a $L(M)$.

---

### 6.2 Conversión: De Vaciado de Pila a Estado Final ($L(M'') = N(M)$) (Diapositivas 18 y 19)
Para lograr que $M''$ alcance un estado final cuando $M$ vacía su pila:
1. Se añade un nuevo estado inicial $q_0'$ que apila un marcador de fondo protegido $Z_0'$ debajo de $Z_0$:
   $$((q_0', \lambda, Z_0'), (q_0, Z_0 Z_0'))$$
2. Se añade un **único nuevo estado final de aceptación $q_A$** ($F' = \{q_A\}$).
3. Si la pila de $M$ se vacía, en el tope **emerge $Z_0'$**. Se agregan transiciones-$\lambda$ desde cualquier estado que detecte $Z_0'$ hacia $q_A$:
   $$((q, \lambda, Z_0'), \{(q_A, Z_0')\}) \quad \forall q \in Q$$

---

## 7. Determinismo vs. No Determinismo en Autómatas a Pila (Diapositiva 20)

> [!IMPORTANT]
> **Diferencia Fundamental con los Autómatas Finitos:**
> $$\mathbf{AFPD \subset AFPN\text{-}\lambda} \quad (\text{NO son equivalentes})$$
> No todo lenguaje independiente de contexto puede ser reconocido por un autómata a pila determinista.

- **Intuición:** El lenguaje de palíndromos de longitud par $L = \{w w^R : w \in \{a, b\}^*\}$ no puede ser determinista porque no existe manera de determinar determinísticamente cuándo finaliza la primera mitad y cuándo comienza la segunda mitad para empezar a desapilar.
- Por convención, se denota $\text{AFP} = \text{AFPD} \cup \text{AFPN}_\lambda$.

---

## 8. Equivalencia Fundamental entre LIC y Autómatas a Pila (Diapositiva 21)

> **Teorema de Chomsky-Schützenberger:**
> - Si $G$ es una Gramática Libre de Contexto (GIC), entonces existe un AFPN-$\lambda$ $M$ tal que $N(M) = L(G)$.
> - Si $M$ es un AFPN-$\lambda$, entonces existe una GIC $G$ tal que $L(G) = N(M)$.
> 
> **Conclusión:** Un lenguaje $L$ es Independiente de Contexto si y solo si existe un autómata a pila $M$ tal que $L = N(M) = L(M)$.

---

## 9. Bibliografía de la Cátedra (Diapositiva 22)

- **Rodrigo De Castro Korgi:** *Teoría de la computación. Lenguajes, autómatas, gramáticas*.
