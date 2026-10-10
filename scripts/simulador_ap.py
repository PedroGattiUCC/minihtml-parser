"""
Simulador Formal del Autómata a Pila (M) para MiniHTML
Materia: Lenguajes Formales y Autómatas (2026) - UCC
Autor: Pedro Gatti (@PedroGattiUCC)

Este script implementa rigurosamente el Autómata a Pila Determinista (APD):
M = (Q, Σ, Γ, δ, q0, Z0, F)
diseñado en la Fase 2, y valida las cadenas de prueba generando la traza de
configuración instantánea paso a paso.
"""

import sys
from typing import List, Tuple

# Asegurar soporte de caracteres UTF-8 en terminales Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class AutomataPilaMiniHTML:
    """Implementación del APD M = (Q, Σ, Γ, δ, q0, Z0, F)"""

    def __init__(self):
        # Q = { 'q0', 'qf' }
        self.q0 = "q0"
        self.qf = "qf"
        self.F = {"qf"}
        
        # Alfabeto de pila Γ = { 'Z0', 'B', 'I', 'P' }
        self.Z0 = "Z0"
        self.tag_to_stack = {
            "<b>": "B",
            "<i>": "I",
            "<p>": "P"
        }
        self.close_to_stack = {
            "</b>": "B",
            "</i>": "I",
            "</p>": "P"
        }

    def simular(self, tokens: List[str]) -> Tuple[bool, str, List[str]]:
        """
        Ejecuta la simulación de la secuencia de tokens en el APD M.
        Devuelve (es_valida, mensaje_diagnostico, traza_pasos).
        """
        estado = self.q0
        pila: List[str] = [self.Z0]  # El final de la lista representa el tope de la pila
        traza: List[str] = []
        
        def snapshot(idx: int, transicion: str) -> str:
            remanente = " ".join(tokens[idx:]) if idx < len(tokens) else "λ"
            # Representar la pila con el tope a la izquierda:
            pila_str = " ".join(reversed(pila))
            return f"({estado},  {remanente:<40},  {pila_str:>10})   |- {transicion}"

        traza.append(f"Configuración Inicial: ({estado}, {' '.join(tokens) if tokens else 'λ'}, {pila[0]})")

        for idx, token in enumerate(tokens):
            tope = pila[-1]

            # 1. Caso TEXTO (No-Op sobre la pila)
            if token == "TEXTO":
                traza.append(snapshot(idx, f"Lee TEXTO, conserva tope '{tope}'"))

            # 2. Caso Apertura (Push)
            elif token in self.tag_to_stack:
                marcador = self.tag_to_stack[token]
                pila.append(marcador)
                traza.append(snapshot(idx, f"Lee {token}, PUSH '{marcador}'"))

            # 3. Caso Cierre (Pop)
            elif token in self.close_to_stack:
                esperado = self.close_to_stack[token]
                if tope == esperado:
                    pila.pop()
                    traza.append(snapshot(idx, f"Lee {token}, POP '{esperado}'"))
                else:
                    if tope == self.Z0:
                        msg = f"Error sintáctico: Se intentó cerrar '{token}' sin etiqueta de apertura previa (pila vacía)."
                    else:
                        msg = f"Error de anidamiento LIFO: Se intentó cerrar '{token}', pero en el tope de la pila está '{tope}'."
                    traza.append(snapshot(idx, f"BLOQUEO: {msg}"))
                    return False, msg, traza
            else:
                msg = f"Error léxico: Token '{token}' no pertenece al alfabeto Σ."
                traza.append(snapshot(idx, f"BLOQUEO: {msg}"))
                return False, msg, traza

        # Fin de la entrada: verificar si se puede transicionar a qf
        if pila == [self.Z0]:
            estado = self.qf
            traza.append(snapshot(len(tokens), "Fin de entrada con fondo Z0 intacto -> Transición λ a estado final qf"))
            return True, "Cadena válida perteneciente a L(M).", traza
        else:
            pendientes = list(reversed(pila[:-1]))
            msg = f"Error sintáctico: Fin de archivo alcanzado con etiquetas sin cerrar pendientes en la pila: {pendientes}."
            traza.append(snapshot(len(tokens), f"BLOQUEO: {msg}"))
            return False, msg, traza


def main():
    automata = AutomataPilaMiniHTML()
    
    cadenas_prueba = {
        "Cadena alfa (α)": ["<p>", "TEXTO", "<b>", "TEXTO", "</b>", "</p>"],
        "Cadena beta (β)": ["<p>", "TEXTO", "<b>", "TEXTO", "</b>", "<i>", "TEXTO", "</i>", "</p>"],
        "Cadena gamma (γ)": ["<p>", "TEXTO", "TEXTO", "</p>", "<i>", "TEXTO", "</i>"],
        "Cadena Inválida 1 (Anidamiento cruzado)": ["<p>", "<b>", "TEXTO", "</p>", "</b>"],
        "Cadena Inválida 2 (Etiqueta huérfana)": ["<p>", "TEXTO", "</b>"],
        "Cadena Inválida 3 (Sin cerrar)": ["<p>", "<b>", "TEXTO"]
    }

    print("=" * 80)
    print("EJECUCIÓN DEL SIMULADOR DEL AUTÓMATA A PILA (M)")
    print("=" * 80)

    for nombre, tokens in cadenas_prueba.items():
        print(f"\n>>> Probando: {nombre}")
        print(f"Tokens: {' '.join(tokens)}")
        valida, mensaje, traza = automata.simular(tokens)
        print(f"Resultado: {'ACEPTADA (w ∈ L(M))' if valida else 'RECHAZADA (w ∉ L(M))'}")
        print(f"Diagnóstico: {mensaje}\n")
        print("Traza de configuración instantánea:")
        for paso in traza:
            print(f"  {paso}")
        print("-" * 80)


if __name__ == "__main__":
    main()
