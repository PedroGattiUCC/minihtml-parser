"""
Suite de Pruebas Unitarias para el Analizador Sintáctico de MiniHTML
Materia: Lenguajes Formales y Autómatas (2026) - UCC
Autor: Pedro Gatti (@PedroGattiUCC)

Ejecutar con: python -m unittest tests/test_parser.py
"""

import unittest
from src.engine import MiniHTMLParser
from src.config import LanguageConfig
from src.tokens import TokenType


class TestMiniHTMLParser(unittest.TestCase):
    """Test suite para validar la corrección formal de las Estrategias A y B."""

    def setUp(self):
        self.config = LanguageConfig()
        self.parser = MiniHTMLParser(self.config)

    # -------------------------------------------------------------
    # 1. Cadenas Válidas Oficiales de la Cátedra
    # -------------------------------------------------------------
    def test_cadena_alfa(self):
        """Cadena α = <p> TEXTO <b> TEXTO </b> </p>"""
        code = "<p> TEXTO <b> TEXTO </b> </p>"
        res = self.parser.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)
        self.assertIsNotNone(res.ast)
        self.assertEqual(len(res.ast.children), 1)

    def test_cadena_beta(self):
        """Cadena β = <p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>"""
        code = "<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>"
        res = self.parser.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    def test_cadena_gamma(self):
        """Cadena γ = <p> TEXTO TEXTO </p> <i> TEXTO </i>"""
        code = "<p> TEXTO TEXTO </p> <i> TEXTO </i>"
        res = self.parser.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    # -------------------------------------------------------------
    # 2. Casos Borde y Extensiones Válidas
    # -------------------------------------------------------------
    def test_cadena_vacia(self):
        """Cadena vacía λ (válida según consigna y regla S -> λ)."""
        res = self.parser.parse("", strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    def test_solo_texto_plano(self):
        """Documento consistente únicamente de texto plano."""
        code = "Este es un texto plano sin etiquetas"
        res = self.parser.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    def test_anidamiento_profundo(self):
        """Múltiples niveles de anidamiento jerárquico LIFO."""
        code = "<p><b><i>TEXTO PROFUNDO</i></b></p>"
        res = self.parser.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    def test_hermanos_multiples(self):
        """Múltiples etiquetas hermanas contiguas."""
        code = "<b>uno</b> <i>dos</i> <p>tres</p>"
        res = self.parser.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    # -------------------------------------------------------------
    # 3. Casos Inválidos (Violaciones Sintácticas y Léxicas)
    # -------------------------------------------------------------
    def test_anidamiento_cruzado(self):
        """Violación del orden LIFO: <p> <b> TEXTO </p> </b>"""
        code = "<p> <b> TEXTO </p> </b>"
        res = self.parser.parse(code, strategy="both")
        self.assertFalse(res.is_valid)
        self.assertTrue(res.equivalent_verified)
        self.assertIn("anidamiento", res.error.message.lower())

    def test_etiqueta_de_cierre_huerfana(self):
        """Etiqueta de cierre sin apertura previa: </b>"""
        code = "<p> TEXTO </p> </b>"
        res = self.parser.parse(code, strategy="both")
        self.assertFalse(res.is_valid)
        self.assertTrue(res.equivalent_verified)
        self.assertIn("huérfana", res.error.message.lower())

    def test_etiqueta_sin_cerrar_al_final(self):
        """Etiqueta abierta que nunca se cierra antes de EOF: <p> <b> TEXTO"""
        code = "<p> <b> TEXTO"
        res = self.parser.parse(code, strategy="both")
        self.assertFalse(res.is_valid)
        self.assertTrue(res.equivalent_verified)

    def test_etiqueta_no_reconocida(self):
        """Etiqueta fuera del alfabeto Σ: <div>Texto</div>"""
        code = "<div>Texto</div>"
        res = self.parser.parse(code, strategy="both")
        self.assertFalse(res.is_valid)
        self.assertIn("no reconocida", res.error.message.lower())

    def test_sintaxis_malformada_sin_mayor(self):
        """Error léxico de etiqueta malformada: <p texto"""
        code = "<p texto"
        res = self.parser.parse(code, strategy="both")
        self.assertFalse(res.is_valid)
        self.assertIn("sin cerrar", res.error.message.lower())

    # -------------------------------------------------------------
    # 4. Prueba de Extensibilidad Dinámica (Defensa Oral)
    # -------------------------------------------------------------
    def test_extension_dinamica_de_etiqueta(self):
        """Demuestra que incorporar una nueva etiqueta funciona al instante en ambas estrategias."""
        config_extendida = LanguageConfig()
        config_extendida.register_tag("u", "U")  # Añadir <u>
        parser_extendido = MiniHTMLParser(config_extendida)

        code = "<p>Texto <u>subrayado</u></p>"
        res = parser_extendido.parse(code, strategy="both")
        self.assertTrue(res.is_valid)
        self.assertTrue(res.equivalent_verified)
        # Comprobar que en el autómata a pila se usó el símbolo 'U'
        stack_symbols_used = [step.stack_content for step in res.pda_trace]
        self.assertTrue(any("U" in s for s in stack_symbols_used))


if __name__ == "__main__":
    unittest.main()
