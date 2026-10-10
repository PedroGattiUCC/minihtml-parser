# Índice Teórico: Presentaciones de Lenguajes Formales y Autómatas

Este directorio contiene la digitalización y sistematización teórica de las presentaciones de cátedra (2026) de la materia **Lenguajes Formales y Autómatas** (Universidad Católica de Córdoba), formateadas en Markdown con rigor matemático para servir de sustentación teórica tanto a los desarrolladores como a los agentes de IA que asisten en el **Proyecto Integrador MiniHTML**.

---

## 📚 Mapa de Clases Teóricas

| Clase | Archivo Markdown | Archivo PDF Original | Temáticas Clave |
|:---:|:---|:---|:---|
| **0** | [Clase 0: Introducción](Clase0_Introduccion.md) | `clase0 2026.pdf` | Computabilidad, Jerarquía de Chomsky, Modelos generativos vs. reconocedores, P vs NP. |
| **1** | [Clase 1: Alfabetos y Lenguajes](Clase1_Alfabetos_Lenguajes.md) | `clase1 2026.pdf` | Conjuntos, funciones, alfabetos ($\Sigma$), cadenas, operaciones ($\cdot, ^n, |\cdot|, ^R$), clausuras ($\Sigma^*, \Sigma^+$), lenguajes. |
| **2** | [Clase 2: Lenguajes y Expresiones Regulares](Clase2_Lenguajes_Expresiones_Regulares.md) | `clase2 2026.pdf` | Definición inductiva de LR, Expresiones Regulares (ER), propiedades de clausura, álgebra de ER, Lema de Arden. |
| **3** | [Clase 3: Autómatas Finitos Deterministas (AFD)](Clase3_Automatas_Finitos_Deterministas.md) | `clase3 2026.pdf` | Definición formal (5-tupla), función extendida $\delta^*$, $L(M)$, estados pozo/trampa, funciones parciales vs totales, complemento $L^c$. |
| **3b** | [Clase 3b: Autómatas Finitos No Deterministas (AFN)](Clase3b_Automatas_Finitos_No_Deterministas.md) | `clase 3b 2026.pdf` | No determinismo, $\Delta: Q \times \Sigma \to \mathcal{P}(Q)$, construcción de subconjuntos (determinización), transiciones-$\lambda$, $\lambda$-clausura, equivalencia $\text{AFD} \equiv \text{AFN} \equiv \text{AFN-}\lambda$. |
| **4** | [Clase 4: Autómatas y Expresiones Regulares](Clase4_Automatas_Expresiones_Regulares.md) | `clase 4 2026.pdf` | Teorema de Kleene, construcción de Thompson (ER $\implies$ AFN-$\lambda$), método de eliminación de estados (AF $\implies$ ER), combinación de autómatas. |
| **5** | [Clase 5: Gramáticas Regulares](Clase5_Gramaticas_Regulares.md) | `clase 5 2026.pdf` | Gramáticas formales (4-tupla $G = (V, \Sigma, S, P)$), derivaciones ($\Rightarrow, \Rightarrow^*$), árboles sintácticos, gramáticas regulares (lineales a derecha/izquierda), equivalencia GR $\equiv$ AF. |
| **6** | [Clase 6: Lenguajes No Regulares](Clase6_Lenguajes_No_Regulares.md) | `clase 6 2026.pdf` | Límites de los autómatas finitos, **Lema de Bombeo (Pumping Lemma)**, pruebas de no regularidad ($a^n b^n$, palíndromos, paréntesis balanceados / MiniHTML). |
| **7** | [Clase 7: Lenguajes Libres de Contexto (GLC)](Clase7_Lenguajes_Independientes_Contexto.md) | `clase 7 2026.pdf` | Gramáticas Libres de Contexto ($A \to \alpha$), BNF en compiladores, propiedades de clausura, ambigüedad sintáctica y desambiguación, problemas de decisión (CYK, indecidibilidad). |
| **8** | [Clase 8: Autómatas a Pila (AP / PDA)](Clase8_Automatas_a_Pila.md) | `clase 8 2026.pdf` | Memoria LIFO, 7-tupla formal, configuraciones instantáneas $(q, w, \gamma) \vdash (p, w', \gamma')$, aceptación por estado final $L(M)$ vs vaciado $N(M)$, AFPD $\subset$ AFPN-$\lambda$, Teorema GLC $\equiv$ AP. |

---

## 🎯 Correspondencia con el Proyecto Integrador (MiniHTML)

Para los agentes de IA y colaboradores del proyecto, consultar las siguientes clases según la fase:

```
+-----------------------------------------------------------------------------------------+
|                               PROYECTO INTEGRADOR MiniHTML                              |
+-----------------------------------------------------------------------------------------+
       |                                       |                                    |
       v                                       v                                    v
   [ FASE 1 ]                             [ FASE 2 ]                           [ FASE 3 ]
Gramática Libre de                   Autómata a Pila (AP)                 Implementación Parser
  Contexto (GLC)                               |                                    |
       |                                       +---------------+                    |
       v                                       |               v                    v
• Clase 5 (Gramáticas)                   • Clase 6       • Clase 8            • Opción A (GLC):
• Clase 7 (GLC y Derivaciones)             (Justificación  (7-tupla, tabla      Clase 7 (Descenso recursivo)
• Árboles sintácticos                      de Pila /       delta, trazas      • Opción B (AP):
                                           No-regular)     instantáneas)        Clase 8 (Simulador con Stack)
```

1. **Justificación del Uso de la Pila (Informe Técnico):**
   - Consultar [Clase 6: Lenguajes No Regulares](Clase6_Lenguajes_No_Regulares.md#5-justificación-teórica-para-el-proyecto-integrador-minihtml).
2. **Modelado de la Gramática (Fase 1):**
   - Consultar [Clase 5: Gramáticas Regulares](Clase5_Gramaticas_Regulares.md) y [Clase 7: Lenguajes Libres de Contexto](Clase7_Lenguajes_Independientes_Contexto.md).
3. **Modelado del Autómata a Pila (Fase 2):**
   - Consultar [Clase 8: Autómatas a Pila](Clase8_Automatas_a_Pila.md).
4. **Estrategia de Código del Parser (Fase 3):**
   - **Opción A (Analizador recursivo por GLC):** Sigue la estructura de derivaciones de [Clase 7](Clase7_Lenguajes_Independientes_Contexto.md).
   - **Opción B (Simulador de AP con Pila LIFO):** Sigue la función de transición y configuraciones instantáneas de [Clase 8](Clase8_Automatas_a_Pila.md).
