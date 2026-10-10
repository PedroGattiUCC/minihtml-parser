"""
Módulo de Configuración del Lenguaje MiniHTML
Permite registrar dinámicamente nuevas etiquetas en tiempo de ejecución,
satisfaciendo el requisito de extensibilidad en vivo durante la defensa oral.
"""

from dataclasses import dataclass, field
from typing import Set, Dict


@dataclass
class LanguageConfig:
    """Configuración del alfabeto y etiquetas de MiniHTML."""
    
    # Conjunto de etiquetas de apertura soportadas (sin los corchetes angulares)
    allowed_tags: Set[str] = field(default_factory=lambda: {"b", "i", "p"})
    
    # Mapeo de etiqueta a símbolo de pila en el autómata (Γ)
    tag_stack_symbols: Dict[str, str] = field(default_factory=lambda: {
        "b": "B",
        "i": "I",
        "p": "P"
    })

    def register_tag(self, tag_name: str, stack_symbol: str = None) -> None:
        """
        Registra una nueva etiqueta en el lenguaje.
        Ejemplo: config.register_tag("u", "U") para añadir soporte a <u> y </u>.
        """
        tag_clean = tag_name.lower().strip("<>/ ")
        if not tag_clean:
            raise ValueError("El nombre de la etiqueta no puede estar vacío.")
        
        self.allowed_tags.add(tag_clean)
        self.tag_stack_symbols[tag_clean] = stack_symbol if stack_symbol else tag_clean.upper()

    def is_allowed_tag(self, tag_name: str) -> bool:
        """Verifica si una etiqueta pertenece al lenguaje."""
        return tag_name.lower().strip("<>/ ") in self.allowed_tags

    def get_stack_symbol(self, tag_name: str) -> str:
        """Devuelve el símbolo de la pila asignado a la etiqueta."""
        tag_clean = tag_name.lower().strip("<>/ ")
        return self.tag_stack_symbols.get(tag_clean, tag_clean.upper())


# Instancia por defecto del lenguaje según la consigna oficial
default_config = LanguageConfig()
