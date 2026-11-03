"""Pruebas del simulador de MiniHTML. Ejecución: python -m unittest tests/test_parser.py"""

import unittest
from src.parser import simular, tokenizar


def es_valida(cadena):
    return simular(tokenizar(cadena))[0]


def mensaje(cadena):
    return simular(tokenizar(cadena))[1]


class TestMiniHTML(unittest.TestCase):
    def test_cadena_alfa(self):
        self.assertTrue(es_valida("<p> TEXTO <b> TEXTO </b> </p>"))

    def test_cadena_beta(self):
        self.assertTrue(es_valida("<p> TEXTO <b> TEXTO </b> <i> TEXTO </i> </p>"))

    def test_cadena_gamma(self):
        self.assertTrue(es_valida("<p> TEXTO TEXTO </p> <i> TEXTO </i>"))

    def test_cadena_vacia(self):
        self.assertTrue(es_valida(""))

    def test_texto_plano(self):
        self.assertTrue(es_valida("TEXTO"))

    def test_html_real(self):
        self.assertTrue(es_valida("<P>Hola <b>mundo</b><\\p>"))

    def test_anidamiento_cruzado(self):
        self.assertIn("anidamiento", mensaje("<p> <b> TEXTO </p> </b>"))

    def test_cierre_sin_apertura(self):
        self.assertIn("sin apertura", mensaje("<p> TEXTO </p> </b>"))

    def test_etiquetas_sin_cerrar(self):
        self.assertIn("<i>, <p>", mensaje("<p> <i> <b> TEXTO </b>"))

    def test_etiquetas_mal_formadas(self):
        for cadena in ["TEXTO <b", "<p> < b > TEXTO </p>", "<p class=x> TEXTO </p>", "<b TEXTO </b>"]:
            self.assertIn("léxico", mensaje(cadena), cadena)

    def test_etiqueta_desconocida(self):
        self.assertIn("léxico", mensaje("<p> </x> </p>"))

    def test_traza(self):
        traza = simular(tokenizar("<p> TEXTO </p>"))[2]
        self.assertEqual(traza[0], "(q0, <p> TEXTO </p>, Z0)")
        self.assertEqual(traza[1], "(q0, TEXTO </p>, P Z0)")
        self.assertEqual(traza[3], "(q0, λ, Z0)")
        self.assertEqual(traza[4], "(qf, λ, Z0)")


if __name__ == "__main__":
    unittest.main()
