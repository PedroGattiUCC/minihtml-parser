"""
Analizador Léxico (Lexer / Tokenizer) para MiniHTML
Transforma una secuencia de caracteres en una lista ordenada de tokens
reconociendo etiquetas de apertura, cierre y texto plano.
"""

from typing import List
from .tokens import Token, TokenType
from .config import LanguageConfig, default_config


class LexicalError(Exception):
    """Error emitido ante caracteres o etiquetas malformadas en el análisis léxico."""
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"[Línea {line}, Columna {column}] {message}")
        self.message = message
        self.line = line
        self.column = column


class Lexer:
    """Escáner léxico para MiniHTML."""

    def __init__(self, source_code: str, config: LanguageConfig = None):
        self.source = source_code
        self.config = config if config else default_config
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def _peek(self, offset: int = 0) -> str:
        target = self.pos + offset
        if target < self.length:
            return self.source[target]
        return ""

    def _advance(self) -> str:
        if self.pos < self.length:
            char = self.source[self.pos]
            self.pos += 1
            if char == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return ""

    def tokenize(self) -> List[Token]:
        """Convierte todo el código fuente en una lista de tokens finalizada en EOF."""
        tokens: List[Token] = []

        while self.pos < self.length:
            char = self._peek()

            # 1. Ignorar saltos de línea y espacios en blanco que estén entre etiquetas si no forman texto
            if char.isspace():
                self._advance()
                continue

            # 2. Apertura o Cierre de Etiqueta
            if char == "<":
                start_line = self.line
                start_col = self.column
                raw_buffer = self._advance()  # consume '<'

                is_closing = False
                if self._peek() == "/":
                    is_closing = True
                    raw_buffer += self._advance()  # consume '/'

                # Leer nombre de la etiqueta
                tag_name_chars = []
                while self.pos < self.length and self._peek() not in (">", " ", "\t", "\n", "\r"):
                    c = self._advance()
                    raw_buffer += c
                    tag_name_chars.append(c)

                # Consumir espacios opcionales antes de '>'
                while self._peek().isspace():
                    raw_buffer += self._advance()

                if self._peek() != ">":
                    raise LexicalError(
                        f"Etiqueta sin cerrar: se esperaba '>' después de '{''.join(tag_name_chars)}'.",
                        start_line,
                        start_col
                    )

                raw_buffer += self._advance()  # consume '>'
                tag_name = "".join(tag_name_chars).lower()

                if not tag_name:
                    raise LexicalError(
                        "Etiqueta vacía '<>' o '</>' no permitida.",
                        start_line,
                        start_col
                    )

                # Validar que la etiqueta esté dentro de las permitidas por la gramática
                if not self.config.is_allowed_tag(tag_name):
                    tipo_desc = "cierre" if is_closing else "apertura"
                    permitidas = ", ".join(sorted(f"<{t}>" for t in self.config.allowed_tags))
                    raise LexicalError(
                        f"Etiqueta de {tipo_desc} no reconocida '{raw_buffer}'. "
                        f"Etiquetas permitidas en MiniHTML: {permitidas}.",
                        start_line,
                        start_col
                    )

                token_type = TokenType.CLOSE_TAG if is_closing else TokenType.OPEN_TAG
                tokens.append(Token(
                    type=token_type,
                    value=tag_name,
                    raw=raw_buffer,
                    line=start_line,
                    column=start_col
                ))

            # 3. Contenido de Texto Plano (hasta encontrar el próximo '<')
            else:
                start_line = self.line
                start_col = self.column
                text_chars = []

                while self.pos < self.length and self._peek() != "<":
                    text_chars.append(self._advance())

                text_content = "".join(text_chars).strip()
                if text_content:
                    tokens.append(Token(
                        type=TokenType.TEXT,
                        value=text_content,
                        raw="".join(text_chars),
                        line=start_line,
                        column=start_col
                    ))

        # Añadir token EOF al final
        tokens.append(Token(
            type=TokenType.EOF,
            value="",
            raw="",
            line=self.line,
            column=self.column
        ))

        return tokens
