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
        """Apertura sin cierre: <p> <b> TEXTO </b>"""
        tokens = tokenizar("<p> <b> TEXTO </b>")
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertFalse(valida_ap)
        self.assertFalse(valida_g)

    def test_etiquetas_mal_formadas(self):
        """Etiquetas mal escritas deben rechazarse como error léxico, no como TEXTO"""
        for cadena in ["TEXTO <b", "<p> < b > TEXTO </p>", "<p class=x> TEXTO </p>", "<b TEXTO </b>"]:
            tokens = tokenizar(cadena)
            valida_ap, mensaje_ap, _ = self.ap.simular(tokens, imprimir_traza=False)
            valida_g, mensaje_g = self.g.validar(tokens)
            self.assertFalse(valida_ap, cadena)
            self.assertFalse(valida_g, cadena)
            self.assertIn("léxico", mensaje_ap)
            self.assertIn("léxico", mensaje_g)

    def test_etiqueta_desconocida(self):
        """</u> no pertenece a Σ: ambos modelos lo reportan como error léxico"""
        tokens = tokenizar("<p> </u> </p>")
        _, mensaje_ap, _ = self.ap.simular(tokens, imprimir_traza=False)
        _, mensaje_g = self.g.validar(tokens)
        self.assertIn("léxico", mensaje_ap)
        self.assertIn("léxico", mensaje_g)

    def test_mensaje_etiquetas_pendientes(self):
        """Al final de la entrada se informan las etiquetas abiertas, no Z0"""
        tokens = tokenizar("<p> <i> <b> TEXTO </b>")
        valida_ap, mensaje_ap, _ = self.ap.simular(tokens, imprimir_traza=False)
        self.assertFalse(valida_ap)
        self.assertIn("<i>, <p>", mensaje_ap)
        self.assertNotIn("Z0", mensaje_ap)

    def test_traza_configuraciones(self):
        """Cada configuración (q, ω, γ) muestra la entrada restante luego de leer el símbolo"""
        tokens = tokenizar("<p> TEXTO </p>")
        _, _, traza = self.ap.simular(tokens, imprimir_traza=False)
        self.assertIn("(q0, <p> TEXTO </p>, Z0)", traza[0])
        self.assertIn("(q0, TEXTO </p>, P Z0)", traza[1])
        self.assertIn("(q0, λ, Z0)", traza[3])
        self.assertIn("(qf, λ, Z0)", traza[4])

    def test_anidamiento_profundo(self):
        """Un anidamiento muy profundo no debe romper el programa"""
        tokens = ["<b>"] * 3000 + ["</b>"] * 3000
        valida_ap, _, _ = self.ap.simular(tokens, imprimir_traza=False)
        valida_g, _ = self.g.validar(tokens)
        self.assertTrue(valida_ap)
        self.assertIsInstance(valida_g, bool)

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
