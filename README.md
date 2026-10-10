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
| **Fase 3** | **Implementación del Analizador Sintáctico (Parser)**<br>Arquitectura dual híbrida en Python con Parser Recursivo (GLC) y Simulador de APD ($M$), verificación de equivalencia $L(G) = L(M)$, CLI enriquecida con `rich`, soporte de pruebas en vivo y suite de tests. | ✅ Completada | [docs/Fase3_Implementacion.md](docs/Fase3_Implementacion.md)<br>[src/](src/) |

---

## 💻 Guía Rápida de Uso

### 1. Ejecutar la Batería Oficial de Pruebas de la Cátedra
Valida las cadenas oficiales ($\alpha, \beta, \gamma$), casos borde y casos inválidos:
```bash
python -m src.cli --test
```

### 2. Analizar una Cadena Específica
Muestra el veredicto, el árbol de análisis sintáctico y la traza de la pila:
```bash
python -m src.cli -t "<p>TEXTO <b>TEXTO</b></p>"
```

### 3. Modo Interactivo REPL (Para la Entrevista Oral)
Inicia la consola interactiva para ingresar cadenas en vivo:
```bash
python -m src.cli
```

### 4. Extensión Dinámica de Etiquetas en Vivo
Para incorporar una nueva etiqueta (por ejemplo, `<u>`) en el momento ante el docente:
```bash
python -m src.cli -t "<p>Texto <u>subrayado</u></p>" --add-tag u
```

### 5. Ejecutar la Suite de Pruebas Automatizadas
```bash
python -m unittest tests/test_parser.py
```

---

## 📂 Estructura del Repositorio

```text
├── docs/
│   ├── Fase1_Gramatica.md       # Especificación formal de la GLC y árboles de derivación
│   ├── Fase2_AutomataPila.md    # Especificación formal del APD M, tabla delta y trazas
│   └── Fase3_Implementacion.md  # Manual técnico de arquitectura, diseño dual y CLI
├── src/                         # Código fuente del parser (Fase 3)
│   ├── __init__.py
│   ├── config.py                # Configuración extensible de etiquetas (Open-Closed)
│   ├── tokens.py                # Definición de tokens con línea y columna
│   ├── lexer.py                 # Analizador léxico robusto
│   ├── ast_nodes.py             # Nodos del árbol sintáctico (AST)
│   ├── recursive_parser.py      # Estrategia A: Parser descendente recursivo (GLC)
│   ├── pda_parser.py            # Estrategia B: Simulador del Autómata a Pila (APD)
│   ├── engine.py                # Fachada unificada y verificación de L(G) = L(M)
│   └── cli.py                   # Interfaz interactiva CLI con librería Rich
├── tests/
│   └── test_parser.py           # Suite de 13 pruebas unitarias exhaustivas
├── scripts/
│   └── simulador_ap.py          # Simulador verificador formal del APD M en Python
├── Proyecto Integrador Lenguajes.pdf # Consigna general de la cátedra
└── README.md                    # Documentación general del repositorio
```
