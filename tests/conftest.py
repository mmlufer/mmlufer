"""
Configuración compartida para los tests del servidor MCP filesystem.
Este archivo permite definir fixtures y configuraciones que serán
compartidas entre todos los tests.
"""

import pytest
from mcp.sdk import MCPClient

@pytest.fixture(scope="session")
def mcp_client():
    """
    Fixture que proporciona un cliente MCP conectado al servidor filesystem.

    Esta fixture tiene alcance de sesión, por lo que se crea una única vez
    para todos los tests y se reutiliza.
    """
    client = MCPClient("filesystem")
    yield client
    # Aquí se podría realizar limpieza si fuera necesario
