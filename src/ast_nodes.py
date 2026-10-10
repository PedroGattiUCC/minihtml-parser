"""
Nodos del Árbol Sintáctico (AST / Parse Tree)
Representan la jerarquía gramatical de las producciones de MiniHTML.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .tokens import Token


class ASTNode(ABC):
    """Clase base para todos los nodos del árbol sintáctico."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Representación estructurada como diccionario para serialización."""
        pass

    @abstractmethod
    def to_ascii_tree(self, prefix: str = "", is_tail: bool = True) -> str:
        """Genera una vista en árbol en texto plano ASCII."""
        pass


class TextNode(ASTNode):
    """Nodo hoja que representa un bloque de texto plano (E -> TEXTO)."""

    def __init__(self, text: str, token: Token):
        self.text = text
        self.token = token

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "TextNode",
            "content": self.text,
            "line": self.token.line,
            "column": self.token.column
        }

    def to_ascii_tree(self, prefix: str = "", is_tail: bool = True) -> str:
        connector = "└── " if is_tail else "├── "
        return f"{prefix}{connector}TEXTO: \"{self.text}\"\n"


class ElementNode(ASTNode):
    """Nodo interno que representa una etiqueta balanceada (E -> <tag> S </tag>)."""

    def __init__(self, tag: str, open_token: Token, children: List[ASTNode], close_token: Optional[Token] = None):
        self.tag = tag
        self.open_token = open_token
        self.children = children
        self.close_token = close_token

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "ElementNode",
            "tag": self.tag,
            "open_line": self.open_token.line,
            "close_line": self.close_token.line if self.close_token else None,
            "children": [child.to_dict() for child in self.children]
        }

    def to_ascii_tree(self, prefix: str = "", is_tail: bool = True) -> str:
        connector = "└── " if is_tail else "├── "
        result = f"{prefix}{connector}Elemento <{self.tag}>\n"
        child_prefix = prefix + ("    " if is_tail else "│   ")
        for i, child in enumerate(self.children):
            child_tail = (i == len(self.children) - 1)
            result += child.to_ascii_tree(child_prefix, child_tail)
        return result


class DocumentNode(ASTNode):
    """Nodo raíz del documento (Símbolo inicial S)."""

    def __init__(self, children: List[ASTNode]):
        self.children = children

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "DocumentNode",
            "children": [child.to_dict() for child in self.children]
        }

    def to_ascii_tree(self, prefix: str = "", is_tail: bool = True) -> str:
        result = "Documento MiniHTML (Raíz S)\n"
        for i, child in enumerate(self.children):
            child_tail = (i == len(self.children) - 1)
            result += child.to_ascii_tree("", child_tail)
        return result
