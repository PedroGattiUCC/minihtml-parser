# Clase 0: Introducción a Lenguajes Formales y Autómatas

> **Materia:** Lenguajes Formales y Autómatas  
> **Institución:** Universidad Católica de Córdoba (UCC)  
> **Año:** 2026  
> **Documento base:** `clase0 2026.pdf` (Clase 1a)

---

## 1. Motivación y Preguntas Fundamentales

La teoría de la computación busca responder preguntas esenciales sobre los límites y costos del procesamiento de información:
- **¿Qué es computable?** ¿Qué problemas puede resolver una computadora y cuáles están más allá de sus capacidades teóricas? (Teoría de la Decidibilidad).
- **¿Qué problemas puede resolver en la práctica una máquina?** ¿Cuáles pueden resolverse con una cantidad razonable y finita de recursos de tiempo y memoria? (Teoría de la Complejidad Computacional y Tratabilidad).

### Dos Enfoques Complementarios:
1. **Lenguajes Formales:** Estudia los problemas desde su **dificultad estructural** y los respectivos **modelos computacionales** (reconocedores y generativos) necesarios para procesarlos.
   - *Lenguaje formal:* Conjunto de símbolos y reglas de formación que determinan cómo dichos símbolos pueden combinarse para constituir cadenas válidas del lenguaje.
2. **Complejidad Computacional:** Estudia los lenguajes desde su **dificultad computacional**, evaluando cuánto recurso de tiempo (pasos de ejecución) y espacio (memoria) se requiere para computarlos.

---

## 2. Relevancia y Aplicaciones Prácticas

La teoría de la computación proporciona un marco común mediante la **abstracción**, simplificando la realidad física y capturando las leyes esenciales compartidas por el hardware y el software:
- **Diseño de circuitos digitales:** Circuitos secuenciales modelados como máquinas de estados finitos.
- **Compiladores y analizadores sintácticos (*parsers*):**
  - Análisis léxico mediante autómatas finitos y expresiones regulares (Lenguajes Regulares).
  - Análisis sintáctico mediante gramáticas libres de contexto y memoria tipo pila (Lenguajes Libres de Contexto).
- **Sistemas operativos y protocolos de comunicación:** Modelado de estados de procesos, sincronización y transiciones de red.
- **Procesamiento de texto y reconocimiento de patrones:** Búsqueda mediante expresiones regulares y motores léxicos.

---

## 3. La Jerarquía de Chomsky

Propuesta por Noam Chomsky en la década de 1950, clasifica los lenguajes formales en cuatro niveles jerárquicos según la complejidad de las reglas gramaticales que los generan y el poder de los modelos computacionales requeridos para reconocerlos:

```
  +-----------------------------------------------------------+
  | Tipo 0: Recursivamente Enumerables (Máquinas de Turing)   |
  |   +-----------------------------------------------------+ |
  |   | Tipo 1: Sensibles al Contexto (Autómata con n-Pilas)| |
  |   |   +-----------------------------------------------+ | |
  |   |   | Tipo 2: Libres de Contexto (Autómata a Pila)  | | |
  |   |   |   +-----------------------------------------+ | | |
  |   |   |   | Tipo 3: Regulares (Autómatas Finitos)   | | | |
  |   |   |   +-----------------------------------------+ | | |
  |   |   +-----------------------------------------------+ | |
  |   +-----------------------------------------------------+ |
  +-----------------------------------------------------------+
```

### Relación entre Lenguajes y Modelos Computacionales

| Tipo | Clase de Lenguaje | Modelo Generativo (Gramática) | Modelo Reconocedor (Autómata) | Tipo de Memoria |
|:---:|:---|:---|:---|:---|
| **Tipo 3** | **Lenguajes Regulares** | Gramática Regular (Lineal por derecha / izquierda) | Autómata Finito (AFD / AFN) | Memoria interna finita (solo estados) |
| **Tipo 2** | **Lenguajes Independientes de Contexto** | Gramática Libre de Contexto (GLC / GIC) | Autómata Finito con Pila (AP / PDA) | Memoria auxiliar LIFO no acotada (Pila) |
| **Tipo 1** | **Lenguajes Sensibles de Contexto** | Gramática Sensible de Contexto | Autómata Linealmente Acotado / $n$ Pilas | Cinta acotada por longitud de entrada |
| **Tipo 0** | **Lenguajes Recursivamente Enumerables** | Gramática Sin Restricciones | Máquina de Turing (MT) | Memoria infinita de acceso aleatorio (Cinta bidireccional) |

> [!NOTE]
> En este curso se estudian en profundidad los **Lenguajes Regulares (Tipo 3)** y los **Lenguajes Independientes de Contexto (Tipo 2)**, pilares fundamentales de la computación y la construcción de analizadores léxicos y sintácticos.

---

## 4. Modelos Computacionales: Reconocedores vs. Generativos

Existen dos aproximaciones duales para caracterizar un lenguaje formal:

1. **Modelos Generativos (Gramáticas):**
   - Sistema axiomático de reglas de derivación o producción ($P$) que permite producir o derivar todas las cadenas válidas del lenguaje a partir de un símbolo inicial ($S$).
2. **Modelos Reconocedores (Autómatas / Máquinas de Estados):**
   - Máquinas abstractas y sistemas reactivos que consumen una cadena de entrada símbolo a símbolo.
   - Pasan por una secuencia de estados internos en respuesta a los estímulos y determinan si la cadena es aceptada o rechazada.

---

## 5. Hitos Históricos en la Teoría de la Computación

- **Alan Turing (1936):** Introduce la *Máquina de Turing*, demostrando formalmente qué es computable y definiendo los límites de la computación (Problema de la Parada / *Halting Problem*).
- **Tesis de Church-Turing:** Todo algoritmo realizable físicamente por un procedimiento computacional puede ser simulado por una Máquina de Turing equivalente.
- **George Mealy y Edward Moore (1950s):** Formalizan los autómatas de estados finitos (máquinas con salida).
- **Noam Chomsky (1956):** Establece las gramáticas formales y su jerarquía de cuatro niveles.
- **Stephen Cook (1971):** Formaliza la teoría de NP-Completitud (Teorema de Cook-Levin), separando problemas eficientemente tratables ($P$) de problemas intratables ($NP$).

---

## 6. Introducción a la Complejidad Computacional

- **Decidibilidad:** ¿Existe un algoritmo que termine en tiempo finito con respuesta SI/NO para cualquier entrada?
- **Tratabilidad:** ¿El problema puede resolverse en tiempo polinomial $\mathcal{O}(n^k)$ respecto al tamaño de la entrada?
  - **Clase P:** Problemas resolubles en tiempo polinomial determinista.
  - **Clase NP:** Problemas cuyas soluciones pueden verificarse en tiempo polinomial determinista.
  - **NP-Completitud:** Los problemas más difíciles dentro de NP; si alguno de ellos se resolviera en tiempo polinomial, entonces $P = NP$.

---

## 7. Conexión con el Proyecto Integrador (MiniHTML)

El analizador sintáctico para **MiniHTML** aborda un problema que trasciende las capacidades de los Autómatas Finitos (Tipo 3) debido a la necesidad de verificar etiquetas anidadas arbitrariamente (como `<p><b>...</b></p>`). Dicha validación requiere:
1. Una **Gramática Libre de Contexto (Tipo 2)** para especificar la jerarquía sintáctica.
2. Un **Autómata a Pila (Tipo 2)** con memoria LIFO para emparejar etiquetas de apertura y cierre en estricto orden inverso a su aparición.
