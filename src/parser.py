"""MiniHTML: simulador del autómata a pila M (opción B).
Proyecto Integrador 2026 - Lenguajes Formales y Autómatas - UCC
"""

import re
import sys

# Para que δ y λ se vean bien también en la consola de Windows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Etiqueta -> símbolo de pila. Para agregar una etiqueta alcanza con sumarla acá.
ETIQUETAS = {"b": "B", "i": "I", "p": "P"}

APERTURAS = {f"<{e}>": s for e, s in ETIQUETAS.items()}
CIERRES = {f"</{e}>": s for e, s in ETIQUETAS.items()}


def tokenizar(cadena):
    """Convierte el texto en tokens de Σ. Lo mal escrito queda igual para rechazarlo después."""
    tokens = []
    for trozo in re.findall(r"<[^<>]*>?|[^<\s]+", cadena):
        if trozo.startswith("<"):
            tokens.append(trozo.strip().lower().replace("\\", "/"))
        else:
            tokens.append("TEXTO")
    return tokens


def configuracion(estado, resto, pila):
    """Arma el texto (q, ω, γ), con el tope de la pila a la izquierda."""
    return f"({estado}, {' '.join(resto) or 'λ'}, {' '.join(reversed(pila))})"


def simular(tokens):
    """Aplica δ token por token. Devuelve (es_valida, mensaje, traza)."""
    pila = ["Z0"]  # el tope es el último elemento
    traza = [configuracion("q0", tokens, pila)]

    for i, token in enumerate(tokens):
        tope = pila[-1]
        if token == "TEXTO":                  # regla 1: la pila no cambia
            pass
        elif token in APERTURAS:              # reglas 2 a 4: apila
            pila.append(APERTURAS[token])
        elif token not in CIERRES:
            return False, f"Error léxico: '{token}' no pertenece a Σ.", traza
        elif tope == CIERRES[token]:          # reglas 5 a 7: desapila
            pila.pop()
        elif tope == "Z0":
            return False, f"Error sintáctico: se cerró '{token}' sin apertura previa.", traza
        else:
            return False, f"Error de anidamiento: se leyó '{token}' con {tope} en el tope.", traza
        traza.append(configuracion("q0", tokens[i + 1:], pila))

    if pila != ["Z0"]:
        abiertas = [f"<{s.lower()}>" for s in reversed(pila[1:])]
        return False, f"Error sintáctico: etiquetas sin cerrar: {', '.join(abiertas)}.", traza
    traza.append(configuracion("qf", [], pila))  # regla 8: δ(q0, λ, Z0) = (qf, Z0)
    return True, "Cadena válida (w ∈ L(M)).", traza


def analizar_cadena(cadena):
    tokens = tokenizar(cadena)
    valida, mensaje, traza = simular(tokens)
    print(f"Tokens: {tokens or 'λ'}")
    print("\n⊢ ".join(traza))
    print(f"{'ACEPTADA' if valida else 'RECHAZADA (w ∉ L(M))'}. {mensaje}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        analizar_cadena(sys.argv[1])
    else:
        print("Escribí una cadena (Enter solo = cadena vacía) o 'salir' para terminar.")
        try:
            while (entrada := input("\nCadena MiniHTML > ").strip()).lower() != "salir":
                analizar_cadena(entrada)
        except (KeyboardInterrupt, EOFError):
            pass
