import unittest
from mcp.sdk import MCPClient

class TestRecursos(unittest.TestCase):
    """Tests de integración para los recursos del servidor MCP."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Conectar al servidor MCP
        self.client = MCPClient("Calculadora")

    def test_saludo(self):
        """Verificar que el recurso de saludo funciona correctamente."""
        # Casos de prueba para el recurso de saludo
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

if __name__ == "__main__":
    unittest.main()
