"""
Estrategia B: Analizador Sintáctico basado en el Autómata a Pila (M)
Implementa el motor del Autómata a Pila Determinista (APD):
  M = (Q, Σ, Γ, δ, q0, Z0, F)
gestionando explícitamente una estructura de datos tipo Pila (Stack)
y registrando las trazas de configuraciones instantáneas paso a paso.
"""

from typing import List, Tuple
from dataclasses import dataclass
from .tokens import Token, TokenType
from .config import LanguageConfig, default_config


@dataclass
class ConfigurationStep:
    """Representa una configuración instantánea (q, w, γ) en un paso de computación."""
    step_number: int
    state: str
    remaining_input: str
    stack_content: str  # El primer símbolo a la izquierda representa el tope
    action_description: str

    def __str__(self) -> str:
        return f"({self.state}, {self.remaining_input:<35}, {self.stack_content:>12}) |- {self.action_description}"


class PushdownAutomatonParser:
    """
    Simulador formal del APD M diseñado en la Fase 2.
    Procesa secuencialmente los tokens de entrada y gestiona el anidamiento LIFO.
    """

    def __init__(self, config: LanguageConfig = None):
        self.config = config if config else default_config
        self.q0 = "q0"
        self.qf = "qf"
        self.Z0 = "Z0"

    def parse(self, tokens: List[Token]) -> Tuple[bool, str, List[ConfigurationStep]]:
        """
        Ejecuta el reconocimiento secuencial de la cadena de tokens.
        Devuelve: (es_valida, mensaje_diagnostico, traza_de_configuraciones).
        """
        estado = self.q0
        pila: List[Tuple[str, Token]] = [(self.Z0, None)]  # (símbolo_pila, token_origen)
        traza: List[ConfigurationStep] = []
        step_counter = 1

        def format_remaining(idx: int) -> str:
            if idx >= len(tokens) or tokens[idx].type == TokenType.EOF:
                return "λ"
            return " ".join(t.raw for t in tokens[idx:] if t.type != TokenType.EOF)

        def format_stack() -> str:
            # Tope a la izquierda
            return " ".join(sym for sym, _ in reversed(pila))

        # Registrar configuración inicial
        traza.append(ConfigurationStep(
            step_number=step_counter,
            state=estado,
            remaining_input=format_remaining(0),
            stack_content=format_stack(),
            action_description="Configuración Inicial del Autómata"
        ))

        # Procesar cada token hasta llegar a EOF
        for idx, token in enumerate(tokens):
            if token.type == TokenType.EOF:
                break

            step_counter += 1
            tope_sym, tope_token = pila[-1]

            # 1. Token de Texto Plano (Operación NO-OP: conserva el tope)
            if token.type == TokenType.TEXT:
                traza.append(ConfigurationStep(
                    step_number=step_counter,
                    state=estado,
                    remaining_input=format_remaining(idx + 1),
                    stack_content=format_stack(),
                    action_description=f"Regla 1: Lee TEXTO, conserva tope '{tope_sym}'"
                ))

            # 2. Token de Apertura (Operación PUSH)
            elif token.type == TokenType.OPEN_TAG:
                stack_sym = self.config.get_stack_symbol(token.value)
                pila.append((stack_sym, token))
                traza.append(ConfigurationStep(
                    step_number=step_counter,
                    state=estado,
                    remaining_input=format_remaining(idx + 1),
                    stack_content=format_stack(),
                    action_description=f"Regla 2-4: Lee <{token.value}>, PUSH '{stack_sym}' sobre '{tope_sym}'"
                ))

            # 3. Token de Cierre (Operación POP con validación de tope)
            elif token.type == TokenType.CLOSE_TAG:
                esperado_sym = self.config.get_stack_symbol(token.value)

                if tope_sym == esperado_sym:
                    # Desapilar el marcador coincidente
                    desapilado_sym, _ = pila.pop()
                    traza.append(ConfigurationStep(
                        step_number=step_counter,
                        state=estado,
                        remaining_input=format_remaining(idx + 1),
                        stack_content=format_stack(),
                        action_description=f"Regla 5-7: Lee </{token.value}>, POP '{desapilado_sym}' (emparejamiento exitoso)"
                    ))
                else:
                    # Diagnóstico preciso del bloqueo formal
                    if tope_sym == self.Z0:
                        error_msg = (
                            f"[Línea {token.line}, Columna {token.column}] Error sintáctico: "
                            f"Se intentó cerrar '</{token.value}>' pero no hay etiquetas abiertas pendientes (tope Z0)."
                        )
                    else:
                        error_msg = (
                            f"[Línea {token.line}, Columna {token.column}] Error de anidamiento LIFO: "
                            f"Se leyó '</{token.value}>' (esperaba desapilar '{esperado_sym}'), "
                            f"pero en el tope de la pila está '{tope_sym}' (abierto por <{tope_token.value}> en línea {tope_token.line})."
                        )
                    
                    traza.append(ConfigurationStep(
                        step_number=step_counter,
                        state=estado,
                        remaining_input=format_remaining(idx),
                        stack_content=format_stack(),
                        action_description=f"BLOQUEO: delta({estado}, </{token.value}>, {tope_sym}) INDEFINIDA. {error_msg}"
                    ))
                    return False, error_msg, traza

        # Fin de la lectura: transición λ a estado final si el fondo Z0 está intacto
        step_counter += 1
        if len(pila) == 1 and pila[0][0] == self.Z0:
            estado = self.qf
            traza.append(ConfigurationStep(
                step_number=step_counter,
                state=estado,
                remaining_input="λ",
                stack_content=format_stack(),
                action_description="Regla 8: Fin de entrada con pila en Z0 -> Transición λ a estado de aceptación qf"
            ))
            return True, "Cadena válida en MiniHTML: pertenece a L(M).", traza
        else:
            # Etiquetas pendientes sin cerrar
            etiquetas_abiertas = [t.display_name() for _, t in pila[1:]]
            error_msg = (
                f"Error sintáctico: Fin de documento inesperado. Quedaron etiquetas abiertas sin cerrar en la pila: "
                f"{', '.join(etiquetas_abiertas)}."
            )
            traza.append(ConfigurationStep(
                step_number=step_counter,
                state=estado,
                remaining_input="λ",
                stack_content=format_stack(),
                action_description=f"BLOQUEO: Pila con marcadores residuales sin cerrar. {error_msg}"
            ))
            return False, error_msg, traza
