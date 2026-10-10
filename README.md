# MiniHTML Parser - Proyecto Integrador 2026

**Materia:** Lenguajes Formales y Autómatas  
**Carrera:** Ingeniería en Informática  
**Institución:** Universidad Católica de Córdoba (UCC)  
**Autor:** Pedro Gatti ([@PedroGattiUCC](https://github.com/PedroGattiUCC))

---

## 📌 Descripción del Proyecto

En el desarrollo de software moderno, la validación de estructuras de datos y lenguajes de marcado (como HTML, XML o JSON) es una tarea fundamental. Un error común en documentos HTML es el mal anidamiento de etiquetas (por ejemplo, `<p><b>Texto</p></b>`), el cual viola la estructura jerárquica del lenguaje.

El objetivo de este proyecto es aplicar los conceptos formales de la materia para diseñar, modelar e implementar un analizador sintáctico (*parser*) capaz de validar documentos en **MiniHTML**: un subconjunto de HTML que requiere memoria LIFO (pila) para verificar el balanceo y anidamiento estricto de sus etiquetas.

### Alfabeto del Lenguaje ($\Sigma$)
MiniHTML opera sobre un alfabeto de 7 símbolos terminales:
$$\Sigma = \{ \lt\text{b}\gt, \lt\text{i}\gt, \lt\text{p}\gt, \lt/\text{b}\gt, \lt/\text{i}\gt, \lt/\text{p}\gt, \text{TEXTO} \}$$

* **Apertura:** `<b>`, `<i>`, `<p>`
* **Cierre:** `</b>`, `</i>`, `</p>`
* **Texto plano:** `TEXTO`

---

## 🚀 Fases del Proyecto

El proyecto se divide en tres fases correlativas que conectan la teoría matemática con la implementación en código:

| Fase | Descripción | Estado | Documentación / Código |
|:---:|:---|:---:|:---|
| **Fase 1** | **Especificación formal de una Gramática Libre de Contexto ($G$)**<br>Definición formal de la 4-tupla $G = (V, \Sigma, S, P)$, justificación teórica y árboles de derivación sintáctica para cadenas de prueba. | ✅ Completada | [docs/Fase1_Gramatica.md](docs/Fase1_Gramatica.md) |
| **Fase 2** | **Diseño formal del Autómata a Pila ($M$)**<br>Análisis comparativo de enfoques, definición formal del APD $M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$, tabla y diagrama de transiciones, y trazas instantáneas exhaustivas de $\alpha$, $\beta$ y $\gamma$. | ✅ Completada | [docs/Fase2_AutomataPila.md](docs/Fase2_AutomataPila.md)<br>[scripts/simulador_ap.py](scripts/simulador_ap.py) |
| **Fase 3** | **Implementación del Analizador Sintáctico (Parser)**<br>Reconocedor ejecutable en Python con manejo descriptivo de errores sintácticos y correspondencia formal. | ⏳ Próximamente | `src/` |

---

## 📂 Estructura del Repositorio

```text
├── docs/
│   ├── Fase1_Gramatica.md       # Especificación formal de la GLC y árboles de derivación
│   └── Fase2_AutomataPila.md    # Especificación formal del APD M, tabla delta y trazas
├── src/                         # Código fuente del parser (Fase 3)
├── tests/                       # Casos de prueba y test suite
├── scripts/
│   └── simulador_ap.py          # Simulador verificador formal del APD M en Python
├── Proyecto Integrador Lenguajes.pdf # Consigna general de la cátedra
└── README.md                    # Documentación general del repositorio
```
