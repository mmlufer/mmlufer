"""
Tests de integración para el servidor MCP filesystem.

Este módulo verifica la integración del servidor filesystem con otros componentes,
como el cliente MCP y el sistema de archivos real.
"""

import os
import pytest
import tempfile
from pathlib import Path

# Importar los módulos necesarios
from mcp.servers.filesystem import FilesystemServer
from mcp.sdk import MCPClient  # Cliente MCP para integración

# Fixtures compartidas
@pytest.fixture(scope="module")
def temp_test_dir():
    """Proporciona un directorio temporal que persiste durante el módulo de tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)

        # Crear estructura de prueba
        (test_dir / "subdir").mkdir()
        (test_dir / "test_file.txt").write_text("Contenido inicial")
        (test_dir / "subdir" / "nested_file.txt").write_text("Contenido anidado")

        yield test_dir

@pytest.fixture(scope="module")
def filesystem_server(temp_test_dir):
    """Crea una instancia del servidor filesystem que se mantiene durante todo el módulo."""
    server = FilesystemServer(allowed_directories=[str(temp_test_dir)])
    return server

@pytest.fixture
def mcp_client(filesystem_server, monkeypatch):
    """Configura un cliente MCP que utiliza directamente el servidor filesystem."""
    # En un entorno real, esto se conectaría a un servidor en ejecución
    # Para pruebas, hacemos que el cliente llame directamente a los métodos del servidor
    client = MCPClient("filesystem")

    # Mockear los métodos del cliente para que llamen directamente al servidor
    def mock_call_method(self, method_name, *args, **kwargs):
        server_method = getattr(filesystem_server, method_name, None)
        if server_method:
            return server_method(*args, **kwargs)
        raise AttributeError(f"Método '{method_name}' no encontrado en el servidor")

    # Aplicar el mock
    monkeypatch.setattr(MCPClient, "call_method", mock_call_method)

    return client

# Tests de integración
@pytest.mark.integration
def test_list_and_read_operations(mcp_client, temp_test_dir):
    """Verificar que se pueden listar directorios y leer archivos a través del cliente."""
    # Listar el directorio principal
    result = mcp_client.call_method("list_directory", str(temp_test_dir))

    # Verificar que contiene los elementos esperados
    file_names = [item["name"] for item in result]
    assert "test_file.txt" in file_names
    assert "subdir" in file_names

    # Leer el archivo principal
    content = mcp_client.call_method("read_file", str(temp_test_dir / "test_file.txt"))
    assert content == "Contenido inicial"

    # Leer el archivo anidado
    nested_content = mcp_client.call_method("read_file", str(temp_test_dir / "subdir" / "nested_file.txt"))
    assert nested_content == "Contenido anidado"

@pytest.mark.integration
def test_write_and_verify_cycle(mcp_client, temp_test_dir):
    """Verificar el ciclo completo de escribir un archivo y luego verificar su contenido."""
    # Crear un nuevo archivo
    new_file_path = str(temp_test_dir / "integration_test.txt")
    content = "Contenido creado durante test de integración"

    # Escribir archivo
    result = mcp_client.call_method("write_file", new_file_path, content)
    assert result is True

    # Verificar que el archivo existe físicamente
    assert Path(new_file_path).exists()

    # Verificar el contenido a través del cliente
    read_content = mcp_client.call_method("read_file", new_file_path)
    assert read_content == content

    # Obtener información del archivo
    file_info = mcp_client.call_method("get_file_info", new_file_path)
    assert file_info["name"] == "integration_test.txt"
    assert file_info["extension"] == "txt"

@pytest.mark.integration
def test_search_files(mcp_client, temp_test_dir):
    """Verificar la búsqueda de archivos con diferentes patrones."""
    # Crear algunos archivos adicionales para la búsqueda
    (temp_test_dir / "test_python.py").write_text("print('Hola')")
    (temp_test_dir / "test_markdown.md").write_text("# Título")

    # Buscar archivos .txt
    txt_files = mcp_client.call_method("search_files", str(temp_test_dir), "*.txt")
    txt_names = [item["name"] for item in txt_files]
    assert "test_file.txt" in txt_names
    assert "nested_file.txt" in txt_names

    # Buscar archivos Python
    py_files = mcp_client.call_method("search_files", str(temp_test_dir), "*.py")
    py_names = [item["name"] for item in py_files]
    assert "test_python.py" in py_names

    # Buscar usando regex
    md_files = mcp_client.call_method("search_files", str(temp_test_dir), r"\.md$", use_regex=True)
    md_names = [item["name"] for item in md_files]
    assert "test_markdown.md" in md_names
