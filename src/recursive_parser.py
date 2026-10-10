"""
Estrategia A: Analizador Sintáctico Descendente Recursivo
Implementa un reconocedor directo a partir de las producciones de la
Gramática Libre de Contexto G = (V, Σ, S, P):
  S -> E S | λ
  E -> TEXTO | <tag> S </tag>
"""

from typing import List
from .tokens import Token, TokenType
from .ast_nodes import ASTNode, DocumentNode, ElementNode, TextNode


class SyntaxErrorMiniHTML(Exception):
    """Error sintáctico detallado con información de línea, columna y contexto."""
    def __init__(self, message: str, token: Token, hint: str = ""):
        prefix = f"[Línea {token.line}, Columna {token.column}]" if token else "[EOF]"
        full_message = f"{prefix} Error Sintáctico: {message}"
        if hint:
            full_message += f"\nSugerencia: {hint}"
        super().__init__(full_message)
        self.message = message
        self.token = token
        self.hint = hint


class RecursiveDescentParser:
    """
    Parser descendente recursivo basado en la gramática libre de contexto.
    Cada procedimiento corresponde a una variable no terminal de G:
      - parse_S(): Variable S (Secuencia de elementos)
      - parse_E(): Variable E (Elemento individual)
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # Devuelve EOF

    def _advance(self) -> Token:
        token = self._peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return token

    def parse(self) -> DocumentNode:
        """Punto de entrada principal. Valida que el documento derive de S y consuma toda la entrada."""
        self.pos = 0
        children = self.parse_S()

        # Verificar que no queden tokens sobrantes al final del documento
        current = self._peek()
        if current.type != TokenType.EOF:
            if current.type == TokenType.CLOSE_TAG:
                raise SyntaxErrorMiniHTML(
                    f"Etiqueta de cierre huérfana '</{current.value}>' encontrada sin etiqueta de apertura.",
                    current,
                    hint=f"Verifique que exista un '<{current.value}>' previo que encierre este bloque."
                )
            else:
                raise SyntaxErrorMiniHTML(
                    f"Contenido inesperado '{current.display_name()}' después del fin del documento.",
                    current
                )

        return DocumentNode(children)

    def parse_S(self) -> List[ASTNode]:
        """
        Regla de Producción:
          S -> E S
          S -> λ
        Lee recursivamente elementos E mientras el token actual pueda iniciar un elemento.
        Si encuentra una etiqueta de cierre o EOF, aplica S -> λ.
        """
        elements: List[ASTNode] = []

        while True:
            current = self._peek()

            # Caso base S -> λ: Se alcanza una etiqueta de cierre o fin de archivo
            if current.type in (TokenType.CLOSE_TAG, TokenType.EOF):
                break

            # Caso inductivo S -> E S: Se procesa un elemento E
            element_node = self.parse_E()
            elements.append(element_node)

        return elements

    def parse_E(self) -> ASTNode:
        """
        Reglas de Producción:
          E -> TEXTO
          E -> <tag> S </tag>
        """
        current = self._peek()

        # 1. Regla: E -> TEXTO
        if current.type == TokenType.TEXT:
            token = self._advance()
            return TextNode(text=token.value, token=token)

        # 2. Regla: E -> <tag> S </tag>
        elif current.type == TokenType.OPEN_TAG:
            open_token = self._advance()
            tag_name = open_token.value

            # Llamada recursiva a S para obtener el contenido interno
            inner_children = self.parse_S()

            # Exigir la etiqueta de cierre correspondiente
            closing_token = self._peek()

            if closing_token.type == TokenType.EOF:
                raise SyntaxErrorMiniHTML(
                    f"Etiqueta '<{tag_name}>' abierta en línea {open_token.line} nunca fue cerrada (Fin de archivo inesperado).",
                    closing_token,
                    hint=f"Asegúrese de añadir '</{tag_name}>' antes del final del documento."
                )

            if closing_token.type != TokenType.CLOSE_TAG:
                raise SyntaxErrorMiniHTML(
                    f"Se esperaba una etiqueta de cierre '</{tag_name}>', pero se encontró '{closing_token.display_name()}'.",
                    closing_token
                )

            # Verificar coincidencia estricta LIFO de la etiqueta
            if closing_token.value != tag_name:
                raise SyntaxErrorMiniHTML(
                    f"Error de anidamiento de etiquetas: Se abrió '<{tag_name}>' (línea {open_token.line}), "
                    f"pero se intentó cerrar con '</{closing_token.value}>'.",
                    closing_token,
                    hint=f"Cierre primero la etiqueta '<{tag_name}>' antes de cerrar '</{closing_token.value}>'."
                )

            # Consumir la etiqueta de cierre correcta
            self._advance()
            return ElementNode(
                tag=tag_name,
                open_token=open_token,
                children=inner_children,
                close_token=closing_token
            )

        else:
            raise SyntaxErrorMiniHTML(
                f"Elemento no reconocido o token inesperado '{current.display_name()}'.",
                current
            )
