"""
Pruebas Unitarias para el Analizador Sintáctico de MiniHTML
Materia: Lenguajes Formales y Autómatas (2026) - UCC
Autor: Pedro Gatti (@PedroGattiUCC)

Ejecución: python -m unittest tests/test_parser.py
"""

import unittest
from src.parser import AutomataPilaMiniHTML, AnalizadorRecursivoMiniHTML, tokenizar


class TestMiniHTML(unittest.TestCase):
    """Test suite que valida los modelos de la Clase 7 (G) y Clase 8 (M)."""

    def setUp(self):
        self.ap = AutomataPilaMiniHTML()
        self.g = AnalizadorRecursivoMiniHTML()

    # 1. Cadenas Oficiales de la Cátedra
    def test_cadena_alfa(self):
        """Cadena α = <p> TEXTO <b> TEXTO </b> </p>"""
        tokens = tokenizar("<p> TEXTO <b> TEXTO </b> </p>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertTrue(valida_g)

    def test_cadena_beta(self):
        """Cadena β = <p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>"""
        tokens = tokenizar("<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertTrue(valida_g)

    def test_cadena_gamma(self):
        """Cadena γ = <p> TEXTO TEXTO </p> <i> TEXTO </i>"""
        tokens = tokenizar("<p> TEXTO TEXTO </p> <i> TEXTO </i>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertTrue(valida_g)

    # 2. Casos Borde
    def test_cadena_vacia(self):
        """Cadena vacía λ (w ∈ L según regla S -> λ)"""
        tokens = tokenizar("")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertTrue(valida_g)

    def test_texto_plano(self):
        """Documento solo con texto"""
        tokens = tokenizar("TEXTO")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertTrue(valida_g)

    # 3. Casos Inválidos
    def test_anidamiento_cruzado(self):
        """Violación LIFO: <p> <b> TEXTO </p> </b>"""
        tokens = tokenizar("<p> <b> TEXTO </p> </b>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertFalse(valida_ap)
        self.assertFalse(valida_g)

    def test_etiqueta_huerfana(self):
        """Cierre sin apertura previa: </p>"""
        tokens = tokenizar("<p> TEXTO </p> </b>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertFalse(valida_ap)
        self.assertFalse(valida_g)

    def test_etiqueta_sin_cerrar(self):
        """Apertura sin cierre: <p> <b> TEXTO"""
        tokens = tokenizar("<p> <b> TEXTO")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertFalse(valida_ap)
        self.assertFalse(valida_g)

    # 4. Modificación en Vivo (Defensa Oral)
    def test_incorporar_nueva_etiqueta(self):
        """Incorporar la etiqueta <u> dinámicamente"""
        self.ap.agregar_etiqueta("u", "U")
        self.g.tags.add("u")
        tokens = tokenizar("<p> TEXTO <u> TEXTO </u> </p>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertTrue(valida_g)


if __name__ == "__main__":
    unittest.main()
