"""
Módulo de Tokens para MiniHTML
Define los tipos de tokens y la estructura de datos para representar
unidades léxicas con metadatos de ubicación (línea, columna).
"""

from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    """Categorías léxicas de MiniHTML."""
    OPEN_TAG = auto()   # <b>, <i>, <p>, etc.
    CLOSE_TAG = auto()  # </b>, </i>, </p>, etc.
    TEXT = auto()       # TEXTO o contenido textual plano
    EOF = auto()        # Fin de entrada (End of File)


@dataclass
class Token:
    """Representación de un token léxico con trazabilidad espacial."""
    type: TokenType
    value: str       # Nombre de etiqueta normalizado ("p", "b") o texto contenido
    raw: str         # Texto exacto original (ej: "<p>", "</p>", "TEXTO")
    line: int        # Número de línea (1-indexed)
    column: int      # Número de columna (1-indexed)

    def __str__(self) -> str:
        if self.type == TokenType.OPEN_TAG:
            return f"<{self.value}>"
        elif self.type == TokenType.CLOSE_TAG:
            return f"</{self.value}>"
        elif self.type == TokenType.TEXT:
            return f"TEXTO({self.value})"
        elif self.type == TokenType.EOF:
            return "EOF"
        return f"{self.type.name}({self.value})"

    def display_name(self) -> str:
        """Nombre amigable para reportes de error."""
        if self.type == TokenType.OPEN_TAG:
            return f"<{self.value}>"
        elif self.type == TokenType.CLOSE_TAG:
            return f"</{self.value}>"
        elif self.type == TokenType.TEXT:
            return f"'{self.value}'"
        elif self.type == TokenType.EOF:
            return "Fin de Documento (EOF)"
        return self.value
