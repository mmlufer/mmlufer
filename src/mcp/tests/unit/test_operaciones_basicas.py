import unittest
import pytest
from mcp.sdk import MCPClient

@pytest.mark.unit
class TestOperacionesBasicas(unittest.TestCase):
    """Test unitarios para las operaciones básicas de la calculadora."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Conectar al servidor MCP
        self.client = MCPClient("Calculadora")

    def test_suma(self):
        """Verificar que la función de suma funciona correctamente."""
        casos_prueba = [
            {"a": 5, "b": 3, "esperado": 8},
            {"a": -2, "b": 7, "esperado": 5},
            {"a": 0, "b": 0, "esperado": 0},
            {"a": 1000, "b": 1000, "esperado": 2000}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.sumar(a=caso["a"], b=caso["b"])
                self.assertEqual(resultado, caso["esperado"],
                                f"La suma de {caso['a']} y {caso['b']} debería ser {caso['esperado']}")

    def test_resta(self):
        """Verificar que la función de resta funciona correctamente."""
        casos_prueba = [
            {"a": 10, "b": 5, "esperado": 5},
            {"a": -2, "b": 7, "esperado": -9},
            {"a": 0, "b": 0, "esperado": 0},
            {"a": 1000, "b": 500, "esperado": 500}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.restar(a=caso["a"], b=caso["b"])
                self.assertEqual(resultado, caso["esperado"],
                                f"La resta de {caso['a']} y {caso['b']} debería ser {caso['esperado']}")

    def test_multiplicacion(self):
        """Verificar que la función de multiplicación funciona correctamente."""
        casos_prueba = [
            {"a": 3, "b": 4, "esperado": 12},
            {"a": -5, "b": 2, "esperado": -10},
            {"a": 0, "b": 10, "esperado": 0},
            {"a": 2.5, "b": 2, "esperado": 5.0}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.multiplicar(a=caso["a"], b=caso["b"])
                self.assertEqual(resultado, caso["esperado"],
                                f"La multiplicación de {caso['a']} y {caso['b']} debería ser {caso['esperado']}")

    def test_division(self):
        """Verificar que la función de división funciona correctamente."""
        casos_prueba = [
            {"a": 10, "b": 2, "esperado": 5},
            {"a": 7, "b": 2, "esperado": 3.5},
            {"a": 0, "b": 5, "esperado": 0},
            {"a": 10, "b": 4, "esperado": 2.5}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.dividir(a=caso["a"], b=caso["b"])
                self.assertEqual(resultado, caso["esperado"],
                                f"La división de {caso['a']} y {caso['b']} debería ser {caso['esperado']}")

    def test_division_por_cero(self):
        """Verificar que la división por cero lanza una excepción."""
        with self.assertRaises(Exception):
            self.client.tools.dividir(a=10, b=0)

if __name__ == "__main__":
    unittest.main()
