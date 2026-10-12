"""
Genera las imágenes del informe (árboles de derivación y diagrama del autómata a pila).

Uso:
    pip install matplotlib
    python docs/diagramas/generar_diagramas.py

Crea en esta misma carpeta:
    arbol_alfa.png   árbol de derivación de α = <p> TEXTO <b> TEXTO </b> </p>
    arbol_beta.png   árbol de derivación de β = <p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>
    automata.png     diagrama de transiciones del AFPN-λ M
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

CARPETA = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"

AZUL = "#1f4e79"
AZUL_CLARO = "#dbe7f3"
VERDE_CLARO = "#e3f1df"
VERDE = "#2e6b2a"
GRIS = "#8a8a8a"


# ==============================================================================
# ÁRBOLES DE DERIVACIÓN (gramática G de la Fase 1)
#   S -> E S | λ
#   E -> TEXTO | <b> S </b> | <i> S </i> | <p> S </p>
# ==============================================================================

class Nodo:
    def __init__(self, etiqueta, tipo, hijos=None):
        self.etiqueta = etiqueta
        self.tipo = tipo  # "variable", "terminal" o "lambda"
        self.hijos = hijos or []
        self.x = 0.0
        self.y = 0.0


def derivar(tokens):
    """Construye el árbol de derivación de la cadena aplicando las producciones de G."""
    pos = 0

    def S():
        nonlocal pos
        if pos < len(tokens) and not tokens[pos].startswith("</"):
            e = E()
            return Nodo("S", "variable", [e, S()])
        return Nodo("S", "variable", [Nodo("λ", "lambda")])

    def E():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok == "TEXTO":
            return Nodo("E", "variable", [Nodo("TEXTO", "terminal")])
        apertura = Nodo(tok, "terminal")
        contenido = S()
        cierre = Nodo(tokens[pos], "terminal")
        pos += 1
        return Nodo("E", "variable", [apertura, contenido, cierre])

    arbol = S()
    assert pos == len(tokens), "la cadena no pertenece a L(G)"
    return arbol


def ubicar(nodo, profundidad, siguiente_hoja):
    """Hojas equiespaciadas de izquierda a derecha; cada padre centrado sobre sus hijos."""
    nodo.y = -profundidad
    if not nodo.hijos:
        nodo.x = siguiente_hoja[0]
        siguiente_hoja[0] += 1
        return
    for h in nodo.hijos:
        ubicar(h, profundidad + 1, siguiente_hoja)
    nodo.x = (nodo.hijos[0].x + nodo.hijos[-1].x) / 2


def nodos(n):
    yield n
    for h in n.hijos:
        yield from nodos(h)


def dibujar_arbol(cadena, titulo, archivo):
    arbol = derivar(cadena.split())
    ubicar(arbol, 0, [0])
    todos = list(nodos(arbol))
    ancho = max(n.x for n in todos) + 1
    alto = -min(n.y for n in todos) + 1

    sx, sy = 1.15, 1.0  # escala horizontal / vertical
    fig, ax = plt.subplots(figsize=(ancho * sx * 0.95, alto * sy * 0.95 + 0.8))
    ax.set_xlim(-0.8, (ancho - 1) * sx + 0.8)
    ax.set_ylim(-(alto - 1) * sy - 0.6, 0.9)
    ax.axis("off")
    ax.set_aspect("equal")

    for n in todos:
        for h in n.hijos:
            fin = h.y * sy + (0.2 if h.tipo == "lambda" else 0)  # la línea no tapa la λ
            ax.plot([n.x * sx, h.x * sx], [n.y * sy, fin], color=GRIS, lw=1.2, zorder=1)

    for n in todos:
        x, y = n.x * sx, n.y * sy
        if n.tipo == "variable":
            ax.add_patch(Circle((x, y), 0.3, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=1.6, zorder=2))
            ax.text(x, y, n.etiqueta, ha="center", va="center", fontsize=15, fontweight="bold", color=AZUL, zorder=3)
        elif n.tipo == "terminal":
            w = 0.16 * len(n.etiqueta) + 0.2
            ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.22), w, 0.44, boxstyle="round,pad=0.04,rounding_size=0.1",
                                        facecolor=VERDE_CLARO, edgecolor=VERDE, lw=1.4, zorder=2))
            ax.text(x, y, n.etiqueta, ha="center", va="center", fontsize=13, color=VERDE, zorder=3)
        else:
            ax.text(x, y, "λ", ha="center", va="center", fontsize=17, color=GRIS, zorder=3)

    ax.text((ancho - 1) * sx / 2, 0.7, titulo, ha="center", va="center", fontsize=15)
    fig.savefig(CARPETA / archivo, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ==============================================================================
# DIAGRAMA DEL AUTÓMATA A PILA M (Fase 2)
# ==============================================================================

def dibujar_automata(archivo):
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_aspect("equal")

    q0 = (2.6, 1.6)
    qf = (6.8, 1.6)
    r = 0.55

    # Estados
    ax.add_patch(Circle(q0, r, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2))
    ax.text(*q0, r"$q_0$", ha="center", va="center", fontsize=22, color=AZUL)
    ax.add_patch(Circle(qf, r, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2))
    ax.add_patch(Circle(qf, r - 0.1, facecolor="none", edgecolor=AZUL, lw=2))
    ax.text(*qf, r"$q_f$", ha="center", va="center", fontsize=22, color=AZUL)

    # Flecha de inicio
    ax.add_patch(FancyArrowPatch((0.6, q0[1]), (q0[0] - r, q0[1]), arrowstyle="-|>", mutation_scale=20, lw=2, color="black"))
    ax.text(0.6, q0[1] + 0.25, "inicio", fontsize=13)

    # Transición λ de q0 a qf
    ax.add_patch(FancyArrowPatch((q0[0] + r, q0[1]), (qf[0] - r, qf[1]), arrowstyle="-|>", mutation_scale=20, lw=2, color="black"))
    ax.text((q0[0] + qf[0]) / 2, q0[1] + 0.22, r"λ, $Z_0$ / $Z_0$", ha="center", fontsize=15)

    # Lazo sobre q0 con todas las lecturas
    ax.add_patch(FancyArrowPatch((q0[0] - 0.35, q0[1] + 0.43), (q0[0] + 0.35, q0[1] + 0.43),
                                 connectionstyle="arc3,rad=-2.2", arrowstyle="-|>", mutation_scale=20, lw=2, color="black"))
    lineas = [
        "TEXTO, X / X",
        "<b>, X / BX       </b>, B / λ",
        "<i>, X / IX        </i>, I / λ",
        "<p>, X / PX       </p>, P / λ",
    ]
    ax.add_patch(FancyBboxPatch((0.9, 3.25), 3.4, 1.65, boxstyle="round,pad=0.08,rounding_size=0.15",
                                facecolor="white", edgecolor=GRIS, lw=1))
    for i, linea in enumerate(lineas):
        ax.text(2.6, 4.6 - i * 0.4, linea, ha="center", va="center", fontsize=14)

    ax.text(6.0, 4.3, r"X $\in$ Γ = { $Z_0$, B, I, P }", fontsize=14, color=GRIS)
    ax.text(6.0, 3.85, "rótulo: entrada, tope / reemplazo", fontsize=14, color=GRIS)

    fig.savefig(CARPETA / archivo, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    dibujar_arbol("<p> TEXTO <b> TEXTO </b> </p>", "α = <p> TEXTO <b> TEXTO </b> </p>", "arbol_alfa.png")
    dibujar_arbol("<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>",
                  "β = <p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>", "arbol_beta.png")
    dibujar_automata("automata.png")
    print("Imágenes generadas en", CARPETA)
