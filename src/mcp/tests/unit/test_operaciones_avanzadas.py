import unittest
import pytest
import math
from mcp.sdk import MCPClient

@pytest.mark.unit
class TestOperacionesAvanzadas(unittest.TestCase):
    """Test unitarios para las operaciones matemáticas avanzadas de la calculadora."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Conectar al servidor MCP
        self.client = MCPClient("Calculadora")

    def test_raiz_cuadrada(self):
        """Verificar que la función de raíz cuadrada funciona correctamente."""
        casos_prueba = [
            {"numero": 4, "esperado": 2.0},
            {"numero": 9, "esperado": 3.0},
            {"numero": 2, "esperado": 1.4142135623730951},
            {"numero": 0, "esperado": 0.0}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.raiz_cuadrada(numero=caso["numero"])
                self.assertAlmostEqual(resultado, caso["esperado"], places=10,
                                      msg=f"La raíz cuadrada de {caso['numero']} debería ser {caso['esperado']}")

    def test_raiz_cuadrada_numero_negativo(self):
        """Verificar que la raíz cuadrada de un número negativo lanza una excepción."""
        with self.assertRaises(Exception):
            self.client.tools.raiz_cuadrada(numero=-1)

    def test_potencia(self):
        """Verificar que la función de potencia funciona correctamente."""
        casos_prueba = [
            {"base": 2, "exponente": 3, "esperado": 8.0},
            {"base": 5, "exponente": 2, "esperado": 25.0},
            {"base": 10, "exponente": 0, "esperado": 1.0},
            {"base": 2, "exponente": -1, "esperado": 0.5}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.potencia(base=caso["base"], exponente=caso["exponente"])
                self.assertAlmostEqual(resultado, caso["esperado"], places=10,
                                      msg=f"{caso['base']} elevado a {caso['exponente']} debería ser {caso['esperado']}")

    def test_logaritmo(self):
        """Verificar que la función de logaritmo funciona correctamente."""
        casos_prueba = [
            {"numero": 100, "base": 10, "esperado": 2.0},
            {"numero": 8, "base": 2, "esperado": 3.0},
            {"numero": math.e, "base": math.e, "esperado": 1.0},
            {"numero": 10, "base": 10, "esperado": 1.0}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                resultado = self.client.tools.logaritmo(numero=caso["numero"], base=caso["base"])
                self.assertAlmostEqual(resultado, caso["esperado"], places=10,
                                      msg=f"El logaritmo en base {caso['base']} de {caso['numero']} debería ser {caso['esperado']}")

    def test_logaritmo_parametros_invalidos(self):
        """Verificar que el logaritmo con parámetros inválidos lanza una excepción."""
        parametros_invalidos = [
            {"numero": 0, "base": 10},
            {"numero": -1, "base": 10},
            {"numero": 10, "base": 0},
            {"numero": 10, "base": 1},
            {"numero": 10, "base": -1}
        ]

        for params in parametros_invalidos:
            with self.subTest(params=params), self.assertRaises(Exception):
                self.client.tools.logaritmo(**params)

    def test_operaciones_listas(self):
        """Verificar que las operaciones con listas funcionan correctamente."""
        # Probar promedio
        numeros = [1, 2, 3, 4, 5]
        resultado = self.client.tools.promedio(numeros=numeros)
        self.assertEqual(resultado, 3.0, f"El promedio de {numeros} debería ser 3.0")

        # Probar suma_lista
        resultado = self.client.tools.suma_lista(numeros=numeros)
        self.assertEqual(resultado, 15.0, f"La suma de {numeros} debería ser 15.0")

        # Probar lista vacía
        with self.assertRaises(Exception):
            self.client.tools.promedio(numeros=[])

if __name__ == "__main__":
    unittest.main()
