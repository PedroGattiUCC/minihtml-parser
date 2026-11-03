# MiniHTML Parser - Proyecto Integrador 2026

**Materia:** Lenguajes Formales y Autómatas  
**Carrera:** Ingeniería en Informática  
**Institución:** Universidad Católica de Córdoba (UCC)  
**Integrantes:** Delfina Artigau, Facundo Grillo, Pedro Gatti y Maria Emilia Lasa

---

## 📌 Descripción del Proyecto

El objetivo de este proyecto es aplicar los conceptos formales de la materia (Gramáticas Libres de Contexto y Autómatas a Pila) para diseñar, modelar e implementar un analizador sintáctico (*parser*) ejecutable capaz de validar documentos en **MiniHTML**: un subconjunto de HTML que requiere memoria LIFO (pila) para verificar el balanceo y anidamiento estricto de sus etiquetas.

### Alfabeto del Lenguaje ($\Sigma$)
$$\Sigma = \{ \lt\text{b}\gt, \lt\text{i}\gt, \lt\text{p}\gt, \lt/\text{b}\gt, \lt/\text{i}\gt, \lt/\text{p}\gt, \text{TEXTO} \}$$

* **Etiquetas de apertura:** `<b>`, `<i>`, `<p>`
* **Etiquetas de cierre:** `</b>`, `</i>`, `</p>`
* **Texto plano:** `TEXTO`

---

## 🚀 Fases del Proyecto

| Fase | Descripción | Estado | Documentación / Código |
|:---:|:---|:---:|:---|
| **Fase 1** | **Especificación formal de una Gramática Libre de Contexto ($G$)**<br>Definición de $G = (V, \Sigma, S, P)$, justificación teórica y árboles de derivación sintáctica (Clase 7). | ✅ Completada | [Informe técnico](entregables/Informe%20miniparser-html.pdf) |
| **Fase 2** | **Diseño formal del Autómata a Pila ($M$)**<br>7-upla del autómata $M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$, tabla y diagrama de transiciones, y trazas de configuración instantánea (Clase 8). | ✅ Completada | [Informe técnico](entregables/Informe%20miniparser-html.pdf) |
| **Fase 3** | **Implementación del Analizador Sintáctico en Python**<br>Simulador del autómata a pila (opción B), con reporte de errores y modo interactivo. | ✅ Completada | [Informe técnico](entregables/Informe%20miniparser-html.pdf)<br>[src/parser.py](src/parser.py) |

---

## 💻 Guía Rápida de Uso

El proyecto utiliza únicamente la **librería estándar de Python 3** (sin dependencias externas).

### 1. Modo Interactivo en Vivo (Para la Defensa Oral)
```bash
python src/parser.py
```

### 2. Probar una Cadena Específica con su Traza de Pila
```bash
python src/parser.py "<p> TEXTO <b> TEXTO </b> </p>"
```

### 3. Ejecutar las Pruebas Automatizadas
```bash
python -m unittest tests/test_parser.py
```

---

## 📂 Estructura del Repositorio

```text
├── entregables/
│   └── Informe miniparser-html.pdf  # Informe técnico (Fases 1 y 2, y por qué se necesita una pila)
├── src/
│   └── parser.py                    # Simulador del autómata a pila (programa de la demo)
├── tests/
│   └── test_parser.py               # Suite de pruebas unitarias
├── interno/                         # Material de trabajo del grupo (no forma parte de la entrega)
└── README.md                        # Documentación general del repositorio
```
