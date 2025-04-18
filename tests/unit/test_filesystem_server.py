"""
Tests unitarios para el servidor MCP filesystem.

Este módulo contiene pruebas para las operaciones básicas
del servidor MCP filesystem, siguiendo las mejores prácticas.
"""

import os
import pytest
import tempfile
from pathlib import Path

# Importar el módulo a probar
from mcp.servers.filesystem import FilesystemServer

# Test Fixtures
@pytest.fixture
def temp_test_dir():
    """Proporciona un directorio temporal para las pruebas."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def filesystem_server(temp_test_dir):
    """Proporciona una instancia del servidor filesystem configurada para pruebas."""
    server = FilesystemServer(allowed_directories=[str(temp_test_dir)])
    return server

@pytest.fixture
def sample_file(temp_test_dir):
    """Crea un archivo de muestra en el directorio temporal."""
    test_file = temp_test_dir / "test_file.txt"
    test_file.write_text("Contenido de prueba")
    return test_file

@pytest.fixture
def multiple_files(temp_test_dir):
    """Crea múltiples archivos de prueba en el directorio temporal."""
    files = {
        "file1.txt": "Contenido del archivo 1",
        "file2.txt": "Contenido del archivo 2",
        "subdir/file3.txt": "Contenido del archivo en subdirectorio"
    }

    # Crear los archivos
    for path, content in files.items():
        full_path = temp_test_dir / path
        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)
        full_path.write_text(content)

    # Devolver un diccionario con las rutas completas
    result = {
        name: temp_test_dir / name for name in files.keys()
    }

    return result

# Tests básicos para funcionalidades existentes
@pytest.mark.unit
def test_read_file_exists_returns_content(filesystem_server, sample_file):
    """Verificar que read_file devuelve el contenido correcto cuando el archivo existe."""
    # Arrange - La configuración se realiza en los fixtures

    # Act
    content = filesystem_server.read_file(str(sample_file))

    # Assert
    assert content == "Contenido de prueba"

@pytest.mark.unit
def test_write_file_creates_new_file(filesystem_server, temp_test_dir):
    """Verificar que write_file crea un nuevo archivo con el contenido correcto."""
    # Arrange
    new_file = temp_test_dir / "new_file.txt"
    test_content = "Nuevo contenido de prueba"

    # Act
    result = filesystem_server.write_file(str(new_file), test_content)

    # Assert
    assert result is True
    assert new_file.exists()
    assert new_file.read_text() == test_content

@pytest.mark.unit
def test_read_file_nonexistent_raises_error(filesystem_server, temp_test_dir):
    """Verificar que read_file lanza error cuando el archivo no existe."""
    # Arrange
    nonexistent_file = temp_test_dir / "nonexistent.txt"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        filesystem_server.read_file(str(nonexistent_file))

@pytest.mark.unit
@pytest.mark.parametrize("file_extension,expected_extension", [
    ("txt", "txt"),
    ("py", "py"),
    ("", None),
])
def test_get_file_info_returns_correct_extension(filesystem_server, temp_test_dir, file_extension, expected_extension):
    """Verificar que get_file_info devuelve la extensión correcta para diferentes tipos de archivos."""
    # Arrange
    filename = f"test_file.{file_extension}" if file_extension else "test_file"
    test_file = temp_test_dir / filename
    test_file.write_text("Contenido")

    # Act
    info = filesystem_server.get_file_info(str(test_file))

    # Assert
    assert info["extension"] == expected_extension
    assert info["is_directory"] is False
    assert info["name"] == filename

@pytest.mark.unit
def test_read_multiple_files_returns_all_contents(filesystem_server, multiple_files):
    """Verificar que read_multiple_files devuelve el contenido de todos los archivos."""
    # Arrange
    paths = [str(path) for path in multiple_files.values()]

    # Act
    result = filesystem_server.read_multiple_files(paths)

    # Assert
    assert len(result) == 3
    assert result[str(multiple_files["file1.txt"])] == "Contenido del archivo 1"
    assert result[str(multiple_files["file2.txt"])] == "Contenido del archivo 2"
    assert result[str(multiple_files["subdir/file3.txt"])] == "Contenido del archivo en subdirectorio"

@pytest.mark.unit
def test_read_multiple_files_with_size_limit_raises_error(filesystem_server, multiple_files):
    """Verificar que read_multiple_files lanza error cuando se excede el límite de tamaño."""
    # Arrange
    paths = [str(path) for path in multiple_files.values()]

    # Act & Assert - Límite por archivo
    with pytest.raises(RuntimeError) as excinfo:
        filesystem_server.read_multiple_files(paths, max_size_per_file=10)

    assert "excede el tamaño máximo permitido" in str(excinfo.value)

    # Act & Assert - Límite total
    with pytest.raises(RuntimeError) as excinfo:
        filesystem_server.read_multiple_files(paths, max_total_size=50)

    assert "El tamaño total de los archivos" in str(excinfo.value)

@pytest.mark.unit
def test_move_file_relocates_file(filesystem_server, sample_file, temp_test_dir):
    """Verificar que move_file mueve correctamente un archivo."""
    # Arrange
    target_path = temp_test_dir / "subdir" / "moved_file.txt"

    # Act
    result = filesystem_server.move_file(str(sample_file), str(target_path))

    # Assert
    assert result is True
    assert not sample_file.exists()
    assert target_path.exists()
    assert target_path.read_text() == "Contenido de prueba"

@pytest.mark.unit
def test_move_file_with_existing_destination_no_overwrite_raises_error(filesystem_server, multiple_files):
    """Verificar que move_file lanza error cuando el destino existe y no se permite sobrescritura."""
    # Arrange
    source = multiple_files["file1.txt"]
    destination = multiple_files["file2.txt"]

    # Act & Assert
    with pytest.raises(FileExistsError):
        filesystem_server.move_file(str(source), str(destination), overwrite=False)

@pytest.mark.unit
def test_move_file_with_existing_destination_overwrite(filesystem_server, multiple_files):
    """Verificar que move_file sobrescribe el destino cuando se permite."""
    # Arrange
    source = multiple_files["file1.txt"]
    destination = multiple_files["file2.txt"]
    original_content = source.read_text()

    # Act
    result = filesystem_server.move_file(str(source), str(destination), overwrite=True)

    # Assert
    assert result is True
    assert not source.exists()
    assert destination.exists()
    assert destination.read_text() == original_content

@pytest.mark.unit
def test_edit_file_replace_operation(filesystem_server, temp_test_dir):
    """Verificar que edit_file realiza correctamente la operación de reemplazo."""
    # Arrange
    test_file = temp_test_dir / "edit_test.txt"
    test_file.write_text("Línea 1\nLínea 2\nLínea 3\nLínea 4\n")

    operations = [
        {
            "type": "replace",
            "line_start": 1,  # Línea 2
            "line_end": 2,    # Línea 3
            "content": "Línea 2 modificada\nLínea 3 modificada\n"
        }
    ]

    # Act
    result = filesystem_server.edit_file(str(test_file), operations)

    # Assert
    assert result is True
    expected_content = "Línea 1\nLínea 2 modificada\nLínea 3 modificada\nLínea 4\n"
    assert test_file.read_text() == expected_content

@pytest.mark.unit
def test_edit_file_delete_operation(filesystem_server, temp_test_dir):
    """Verificar que edit_file realiza correctamente la operación de eliminación."""
    # Arrange
    test_file = temp_test_dir / "edit_test.txt"
    test_file.write_text("Línea 1\nLínea 2\nLínea 3\nLínea 4\n")

    operations = [
        {
            "type": "delete",
            "line_start": 1,  # Línea 2
            "line_end": 2,    # Línea 3
        }
    ]

    # Act
    result = filesystem_server.edit_file(str(test_file), operations)

    # Assert
    assert result is True
    expected_content = "Línea 1\nLínea 4\n"
    assert test_file.read_text() == expected_content

@pytest.mark.unit
def test_edit_file_insert_operation(filesystem_server, temp_test_dir):
    """Verificar que edit_file realiza correctamente la operación de inserción."""
    # Arrange
    test_file = temp_test_dir / "edit_test.txt"
    test_file.write_text("Línea 1\nLínea 4\n")

    operations = [
        {
            "type": "insert",
            "line_start": 1,  # Después de "Línea 1"
            "content": "Línea 2\nLínea 3\n"
        }
    ]

    # Act
    result = filesystem_server.edit_file(str(test_file), operations)

    # Assert
    assert result is True
    expected_content = "Línea 1\nLínea 2\nLínea 3\nLínea 4\n"
    assert test_file.read_text() == expected_content

@pytest.mark.unit
def test_edit_file_multiple_operations(filesystem_server, temp_test_dir):
    """Verificar que edit_file puede aplicar múltiples operaciones en una sola llamada."""
    # Arrange
    test_file = temp_test_dir / "edit_test.txt"
    test_file.write_text("Línea 1\nLínea 2\nLínea 3\nLínea 4\n")

    operations = [
        {
            "type": "replace",
            "line_start": 0,
            "line_end": 0,
            "content": "Primera línea modificada\n"
        },
        {
            "type": "delete",
            "line_start": 2,
            "line_end": 2,
        },
        {
            "type": "insert",
            "line_start": 3,
            "content": "Línea adicional\n"
        }
    ]

    # Act
    result = filesystem_server.edit_file(str(test_file), operations)

    # Assert
    assert result is True
    expected_content = "Primera línea modificada\nLínea 2\nLínea 4\nLínea adicional\n"
    assert test_file.read_text() == expected_content

@pytest.mark.unit
def test_edit_file_invalid_operations(filesystem_server, sample_file):
    """Verificar que edit_file valida correctamente las operaciones antes de aplicarlas."""
    # Arrange - Operación sin tipo
    with pytest.raises(ValueError) as excinfo:
        filesystem_server.edit_file(str(sample_file), [{"line_start": 0}])
    assert "debe tener un tipo" in str(excinfo.value)

    # Arrange - Tipo de operación desconocido
    with pytest.raises(ValueError) as excinfo:
        filesystem_server.edit_file(str(sample_file), [{"type": "unknown", "line_start": 0}])
    assert "Tipo de operación desconocido" in str(excinfo.value)

    # Arrange - Sin línea inicial
    with pytest.raises(ValueError) as excinfo:
        filesystem_server.edit_file(str(sample_file), [{"type": "replace", "line_end": 1, "content": ""}])
    assert "debe tener una línea inicial" in str(excinfo.value)

    # Arrange - Replace sin línea final
    with pytest.raises(ValueError) as excinfo:
        filesystem_server.edit_file(str(sample_file), [{"type": "replace", "line_start": 0, "content": ""}])
    assert "debe tener una línea final" in str(excinfo.value)
