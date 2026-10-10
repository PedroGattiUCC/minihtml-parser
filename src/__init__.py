"""
MiniHTML Parser - Paquete de Análisis Sintáctico
Materia: Lenguajes Formales y Autómatas (2026) - UCC
Autor: Pedro Gatti (@PedroGattiUCC)
"""

from .engine import MiniHTMLParser, ParseResult, ParseError
from .tokens import Token, TokenType
from .lexer import Lexer
from .recursive_parser import RecursiveDescentParser
from .pda_parser import PushdownAutomatonParser
from .config import LanguageConfig, default_config

__all__ = [
    "MiniHTMLParser",
    "ParseResult",
    "ParseError",
    "Token",
    "TokenType",
    "Lexer",
    "RecursiveDescentParser",
    "PushdownAutomatonParser",
    "LanguageConfig",
    "default_config",
]
