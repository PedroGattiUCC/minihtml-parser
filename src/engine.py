"""
Motor Unificado de Análisis Sintáctico (Facade Pattern)
Integra el Analizador Léxico, el Parser Recursivo (Fase 1/G) y el Autómata a Pila (Fase 2/M).
Permite verificar y demostrar la equivalencia formal L(G) = L(M).
"""

from typing import List, Optional, Literal
from dataclasses import dataclass
from .config import LanguageConfig, default_config
from .tokens import Token
from .lexer import Lexer, LexicalError
from .ast_nodes import DocumentNode
from .recursive_parser import RecursiveDescentParser, SyntaxErrorMiniHTML
from .pda_parser import PushdownAutomatonParser, ConfigurationStep


@dataclass
class ParseError:
    """Error unificado con renderizado visual de puntero (caret indicator)."""
    message: str
    line: int
    column: int
    source_line: str = ""
    hint: str = ""

    def format_visual_error(self) -> str:
        """Genera un reporte gráfico de error con puntero '^' similar a compiladores modernos."""
        lines = [f"Error [Línea {self.line}, Columna {self.column}]: {self.message}"]
        if self.source_line:
            lines.append("    " + self.source_line)
            # Dibujar flecha apuntando a la columna exacta
            pointer = " " * (self.column - 1) + "^"
            lines.append("    " + pointer)
        if self.hint:
            lines.append(f"Ayuda: {self.hint}")
        return "\n".join(lines)


@dataclass
class ParseResult:
    """Resultado integral del análisis sintáctico."""
    is_valid: bool
    source_text: str
    tokens: List[Token]
    strategy_used: str
    ast: Optional[DocumentNode] = None
    pda_trace: Optional[List[ConfigurationStep]] = None
    error: Optional[ParseError] = None
    equivalent_verified: Optional[bool] = None  # True si ambas estrategias coincidieron


class MiniHTMLParser:
    """Fachada de análisis sintáctico para MiniHTML."""

    def __init__(self, config: LanguageConfig = None):
        self.config = config if config else default_config

    def parse(
        self,
        source_code: str,
        strategy: Literal["both", "recursive", "pda"] = "both"
    ) -> ParseResult:
        """
        Ejecuta el análisis sintáctico sobre el código fuente de entrada.
        
        Parámetros:
            source_code: Cadena de texto a analizar.
            strategy: 'both' (ambas estrategias y verificación de equivalencia),
                      'recursive' (Estrategia A basada en GLC),
                      'pda' (Estrategia B basada en Autómata a Pila).
        """
        # 1. Fase de Análisis Léxico
        try:
            lexer = Lexer(source_code, self.config)
            tokens = lexer.tokenize()
        except LexicalError as le:
            source_lines = source_code.splitlines()
            err_line = source_lines[le.line - 1] if 0 <= le.line - 1 < len(source_lines) else ""
            return ParseResult(
                is_valid=False,
                source_text=source_code,
                tokens=[],
                strategy_used=strategy,
                error=ParseError(
                    message=le.message,
                    line=le.line,
                    column=le.column,
                    source_line=err_line,
                    hint="Asegúrese de escribir etiquetas válidas y cerradas con '>'."
                )
            )

        # Variables para acumular resultados
        rec_valid = True
        rec_ast: Optional[DocumentNode] = None
        rec_err: Optional[ParseError] = None

        pda_valid = True
        pda_trace: Optional[List[ConfigurationStep]] = None
        pda_err: Optional[ParseError] = None

        source_lines = source_code.splitlines()

        # 2. Estrategia A: Parser Recursivo (GLC)
        if strategy in ("both", "recursive"):
            rec_parser = RecursiveDescentParser(tokens)
            try:
                rec_ast = rec_parser.parse()
                rec_valid = True
            except SyntaxErrorMiniHTML as se:
                rec_valid = False
                line_idx = (se.token.line - 1) if se.token else 0
                err_line = source_lines[line_idx] if 0 <= line_idx < len(source_lines) else ""
                rec_err = ParseError(
                    message=se.message,
                    line=se.token.line if se.token else 1,
                    column=se.token.column if se.token else 1,
                    source_line=err_line,
                    hint=se.hint
                )

        # 3. Estrategia B: Autómata a Pila (APD)
        if strategy in ("both", "pda"):
            pda_engine = PushdownAutomatonParser(self.config)
            pda_valid, pda_msg, pda_trace = pda_engine.parse(tokens)
            if not pda_valid:
                # Localizar el token causante del bloqueo en la traza si es posible
                last_step = pda_trace[-1]
                pda_err = ParseError(
                    message=pda_msg,
                    line=1,
                    column=1,
                    hint="Verifique el balanceo LIFO de las etiquetas."
                )

        # 4. Consolidar veredicto y verificar equivalencia
        if strategy == "both":
            equivalent = (rec_valid == pda_valid)
            main_error = rec_err if not rec_valid else None
            return ParseResult(
                is_valid=rec_valid,
                source_text=source_code,
                tokens=tokens,
                strategy_used="both (GLC + APD)",
                ast=rec_ast,
                pda_trace=pda_trace,
                error=main_error,
                equivalent_verified=equivalent
            )
        elif strategy == "recursive":
            return ParseResult(
                is_valid=rec_valid,
                source_text=source_code,
                tokens=tokens,
                strategy_used="Estrategia A (Parser Recursivo G)",
                ast=rec_ast,
                error=rec_err
            )
        else:
            return ParseResult(
                is_valid=pda_valid,
                source_text=source_code,
                tokens=tokens,
                strategy_used="Estrategia B (Simulador de APD M)",
                pda_trace=pda_trace,
                error=pda_err
            )
