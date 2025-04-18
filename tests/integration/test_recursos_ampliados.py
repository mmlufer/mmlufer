import unittest
import pytest
import math
from mcp.sdk import MCPClient
from typing import Dict, List, Any

@pytest.mark.integration
class TestRecursosAmpliados(unittest.TestCase):
    """Tests de integración para los recursos ampliados del servidor MCP."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Conectar al servidor MCP
        self.client = MCPClient("Calculadora")

    def test_saludo(self):
        """Verificar que el recurso de saludo funciona correctamente."""
        casos_prueba = [
            {"nombre": "Juan", "esperado": "¡Hola, Juan!"},
            {"nombre": "Maria", "esperado": "¡Hola, Maria!"},
            {"nombre": "Carlos", "esperado": "¡Hola, Carlos!"}
        ]

        for caso in casos_prueba:
            with self.subTest(caso=caso):
                saludo = self.client.resource(f"saludo://{caso['nombre']}")
                self.assertEqual(saludo, caso["esperado"],
                                f"El saludo para {caso['nombre']} debería ser {caso['esperado']}")

    def test_historial(self):
        """Verificar que el recurso de historial devuelve la estructura esperada."""
        historial = self.client.resource("historial")

        # Verificar que es una lista
        self.assertIsInstance(historial, list, "El historial debe ser una lista")

        # Verificar que tiene elementos
        self.assertTrue(len(historial) > 0, "El historial no debe estar vacío")

        # Verificar la estructura de cada elemento
        for operacion in historial:
            self.assertIsInstance(operacion, dict, "Cada operación debe ser un diccionario")
            self.assertIn("operacion", operacion, "Cada operación debe tener un campo 'operacion'")
            self.assertIn("valores", operacion, "Cada operación debe tener un campo 'valores'")
            self.assertIn("resultado", operacion, "Cada operación debe tener un campo 'resultado'")

            # Verificar los tipos
            self.assertIsInstance(operacion["operacion"], str)
            self.assertIsInstance(operacion["valores"], list)
            self.assertIsInstance(operacion["resultado"], (int, float))

    def test_constantes_existentes(self):
        """Verificar que se pueden obtener las constantes matemáticas existentes."""
        constantes = ["pi", "e", "phi"]

        for constante in constantes:
            with self.subTest(constante=constante):
                info = self.client.resource(f"constantes/{constante}")

                # Verificar estructura
                self.assertIsInstance(info, dict)
                self.assertIn("valor", info)
                self.assertIn("descripcion", info)

                # Verificar tipos
                self.assertIsInstance(info["valor"], float)
                self.assertIsInstance(info["descripcion"], str)

                # Verificar valores específicos
                if constante == "pi":
                    self.assertAlmostEqual(info["valor"], math.pi)
                elif constante == "e":
                    self.assertAlmostEqual(info["valor"], math.e)
                elif constante == "phi":
                    self.assertAlmostEqual(info["valor"], 1.618033988749895)

    def test_constante_inexistente(self):
        """Verificar que se lanza una excepción al solicitar una constante inexistente."""
        with self.assertRaises(Exception):
            self.client.resource("constantes/inexistente")

    def test_integracion_completa(self):
        """Realizar una prueba de integración completa utilizando múltiples recursos y herramientas."""
        # Obtener una constante
        constante_pi = self.client.resource("constantes/pi")

        # Usar el valor de pi en un cálculo
        area = self.client.tools.multiplicar(
            a=constante_pi["valor"],
            b=self.client.tools.potencia(base=5, exponente=2)
        )

        # Verificar el resultado (π × r²)
        self.assertAlmostEqual(area, math.pi * 25)

        # Obtener un saludo personalizado
        saludo = self.client.resource("saludo://Matemático")
        self.assertEqual(saludo, "¡Hola, Matemático!")

        # Verificar el historial
        historial = self.client.resource("historial")
        self.assertIsInstance(historial, list)

if __name__ == "__main__":
    unittest.main()
