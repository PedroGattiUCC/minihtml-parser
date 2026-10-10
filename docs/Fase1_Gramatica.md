# Fase 1: Especificación formal de una gramática libre de contexto (G)

Para diseñar el analizador sintáctico de MiniHTML, primero formalizamos su estructura mediante una Gramática Libre de Contexto (GLC).

## 1. Definición de la Gramática

Formalmente, definimos la gramática $G = (V, \Sigma, S, P)$ como una 4-tupla, donde:

*   **Símbolos Terminales ($\Sigma$):** Son los caracteres y tokens indivisibles del lenguaje.
    $$\Sigma = \{ \text{<b>}, \text{<i>}, \text{<p>}, \text{</b>}, \text{</i>}, \text{</p>}, \text{TEXTO} \}$$

*   **Variables No Terminales ($V$):** Son las variables sintácticas que generan el lenguaje. 
    Definimos dos variables para mantener la gramática simple y no ambigua:
    $$V = \{ S, E \}$$
    *Donde $S$ representa una secuencia de elementos (el documento o el contenido de una etiqueta) y $E$ representa un único elemento (texto plano o un bloque de etiquetas).*

*   **Símbolo Inicial ($S$):** El punto de partida de la gramática.

*   **Reglas de Producción ($P$):**
    1.  $S \rightarrow E \ S$
    2.  $S \rightarrow \lambda$
    3.  $E \rightarrow \text{TEXTO}$
    4.  $E \rightarrow \text{<b>} \ S \ \text{</b>}$
    5.  $E \rightarrow \text{<i>} \ S \ \text{</i>}$
    6.  $E \rightarrow \text{<p>} \ S \ \text{</p>}$

**Justificación del diseño:** 
La regla $S \rightarrow E \ S \ | \ \lambda$ permite generar una lista de cero o más elementos consecutivos (texto seguido de etiqueta, o múltiples etiquetas anidadas). Las reglas de $E$ aseguran el anidamiento LIFO de las etiquetas, ya que cada apertura (ej. `<b>`) obliga a que se genere su cierre correspondiente (`</b>`), conteniendo una nueva secuencia $S$ en su interior.

---

## 2. Análisis de la gramática (Árboles de derivación sintáctica)

A continuación, mostramos los árboles de derivación para las dos cadenas de prueba solicitadas.

### Cadena $\alpha = \text{<p> TEXTO <b> TEXTO </b> </p>}$

```mermaid
graph TD
    S0((S)) --> E1((E))
    S0 --> S1((S))
    S1 --> lam1((λ))
    
    E1 --> tagP_o(["&lt;p&gt;"])
    E1 --> S2((S))
    E1 --> tagP_c(["&lt;/p&gt;"])
    
    S2 --> E2((E))
    S2 --> S3((S))
    
    E2 --> T1(["TEXTO"])
    
    S3 --> E3((E))
    S3 --> S4((S))
    
    E3 --> tagB_o(["&lt;b&gt;"])
    E3 --> S5((S))
    E3 --> tagB_c(["&lt;/b&gt;"])
    
    S5 --> E4((E))
    S5 --> S6((S))
    E4 --> T2(["TEXTO"])
    S6 --> lam2((λ))
    
    S4 --> lam3((λ))
```

**Derivación por la izquierda para $\alpha$:**
$S \Rightarrow E \ S \Rightarrow \text{<p>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ E \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ E \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ S \ \text{</b>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ E \ S \ \text{</b>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ S \ \text{</b>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \lambda \ \text{</b>} \ \lambda \ \text{</p>} \ \lambda \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ \text{</p>}$

---

### Cadena $\beta = \text{<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>}$

```mermaid
graph TD
    S0((S)) --> E1((E))
    S0 --> S1((S))
    S1 --> lam1((λ))
    
    E1 --> tagP_o(["&lt;p&gt;"])
    E1 --> S2((S))
    E1 --> tagP_c(["&lt;/p&gt;"])
    
    S2 --> E2((E))
    S2 --> S3((S))
    E2 --> T1(["TEXTO"])
    
    S3 --> E3((E))
    S3 --> S4((S))
    E3 --> tagB_o(["&lt;b&gt;"])
    E3 --> S5((S))
    E3 --> tagB_c(["&lt;/b&gt;"])
    S5 --> E4((E))
    S5 --> S6((S))
    E4 --> T2(["TEXTO"])
    S6 --> lam2((λ))
    
    S4 --> E5((E))
    S4 --> S7((S))
    E5 --> tagI_o(["&lt;i&gt;"])
    E5 --> S8((S))
    E5 --> tagI_c(["&lt;/i&gt;"])
    S8 --> E6((E))
    S8 --> S9((S))
    E6 --> T3(["TEXTO"])
    S9 --> lam3((λ))
    
    S7 --> lam4((λ))
```

**Derivación por la izquierda para $\beta$:**
El procedimiento es idéntico a $\alpha$ hasta procesar `</b>`. En vez de que $S$ evalúe a $\lambda$, se expande a $E \ S$ nuevamente para generar la etiqueta `<i>`:
$... \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ E \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ \text{<i>} \ S \ \text{</i>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ \text{<i>} \ E \ S \ \text{</i>} \ S \ \text{</p>} \ S \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ \text{<i>} \ \text{TEXTO} \ \lambda \ \text{</i>} \ \lambda \ \text{</p>} \ \lambda \Rightarrow \text{<p>} \ \text{TEXTO} \ \text{<b>} \ \text{TEXTO} \ \text{</b>} \ \text{<i>} \ \text{TEXTO} \ \text{</i>} \ \text{</p>}$
