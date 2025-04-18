"""
Pruebas básicas para el servidor MCP Filesystem.
"""

import os
import tempfile
import unittest
from pathlib import Path

from .filesystem import FilesystemServer

class TestFilesystemServer(unittest.TestCase):
    """Pruebas para el servidor FilesystemServer."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear un directorio temporal para las pruebas
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

        # Crear algunos archivos y directorios de prueba
        self.test_file = self.test_path / "test_file.txt"
        self.test_file.write_text("Contenido de prueba")

        # Crear archivos para búsqueda
        self.test_file2 = self.test_path / "otro_archivo.txt"
        self.test_file2.write_text("Otro contenido")

        self.test_file3 = self.test_path / "archivo_python.py"
        self.test_file3.write_text("print('Hola mundo')")

        # Crear subdirectorio con archivos
        self.test_subdir = self.test_path / "test_subdir"
        self.test_subdir.mkdir()

        self.test_subfile = self.test_subdir / "subdir_file.txt"
        self.test_subfile.write_text("Archivo en subdirectorio")

        # Inicializar el servidor con el directorio temporal
        self.server = FilesystemServer(allowed_directories=[str(self.test_path)])

    def tearDown(self):
        """Limpieza después de las pruebas."""
        self.test_dir.cleanup()

    def test_read_file(self):
        """Probar la lectura de archivos."""
        content = self.server.read_file(str(self.test_file))
        self.assertEqual(content, "Contenido de prueba")

    def test_write_file(self):
        """Probar la escritura de archivos."""
        new_file = self.test_path / "nuevo_archivo.txt"
        result = self.server.write_file(str(new_file), "Nuevo contenido")
        self.assertTrue(result)
        self.assertTrue(new_file.exists())
        self.assertEqual(new_file.read_text(), "Nuevo contenido")

    def test_list_directory(self):
        """Probar el listado de directorios."""
        result = self.server.list_directory(str(self.test_path))

        # Verificar que hay al menos dos elementos
        self.assertGreaterEqual(len(result), 2)

        # Verificar que test_file.txt y test_subdir están en el listado
        file_names = [item['name'] for item in result]
        self.assertIn("test_file.txt", file_names)
        self.assertIn("test_subdir", file_names)

    def test_create_directory(self):
        """Probar la creación de directorios."""
        new_dir = self.test_path / "nuevo_directorio"
        result = self.server.create_directory(str(new_dir))
        self.assertTrue(result)
        self.assertTrue(new_dir.is_dir())

    def test_get_file_info(self):
        """Probar la obtención de información de archivos."""
        info = self.server.get_file_info(str(self.test_file))

        # Verificar que la información contiene los campos esperados
        self.assertEqual(info['name'], "test_file.txt")
        self.assertEqual(info['is_directory'], False)
        self.assertEqual(info['extension'], "txt")
        self.assertGreater(info['size'], 0)

    def test_search_files_glob(self):
        """Probar la búsqueda de archivos usando patrones glob."""
        # Buscar archivos .txt
        result = self.server.search_files(str(self.test_path), "*.txt")

        # Debe encontrar al menos 3 archivos .txt (incluyendo el del subdirectorio)
        self.assertGreaterEqual(len(result), 3)

        # Verificar que los archivos .txt están en los resultados
        file_names = [item['name'] for item in result]
        self.assertIn("test_file.txt", file_names)
        self.assertIn("otro_archivo.txt", file_names)

        # Buscar archivos que comienzan con "test"
        result = self.server.search_files(str(self.test_path), "test*")
        file_names = [item['name'] for item in result]
        self.assertIn("test_file.txt", file_names)
        self.assertIn("test_subdir", file_names)

    def test_search_files_regex(self):
        """Probar la búsqueda de archivos usando expresiones regulares."""
        # Buscar archivos que terminan en .py
        result = self.server.search_files(str(self.test_path), r"\.py$", use_regex=True)

        # Debe encontrar al menos 1 archivo .py
        self.assertGreaterEqual(len(result), 1)

        # Verificar que el archivo Python está en los resultados
        file_names = [item['name'] for item in result]
        self.assertIn("archivo_python.py", file_names)

    def test_search_files_no_recursive(self):
        """Probar la búsqueda de archivos sin recursión."""
        # Buscar archivos .txt sin recursión
        result = self.server.search_files(str(self.test_path), "*.txt", recursive=False)

        # No debe incluir el archivo en el subdirectorio
        paths = [item['path'] for item in result]
        subdir_files = [p for p in paths if str(self.test_subdir) in p]
        self.assertEqual(len(subdir_files), 0)

    def test_security_prevention(self):
        """Probar que se previenen accesos fuera de directorios permitidos."""
        with self.assertRaises(ValueError):
            self.server.read_file("/etc/passwd")

        with self.assertRaises(ValueError):
            self.server.write_file("/tmp/test.txt", "Test")

    def test_delete_file(self):
        """Probar la eliminación de archivos."""
        # Crear un archivo para eliminar
        file_to_delete = self.test_path / "archivo_para_eliminar.txt"
        file_to_delete.write_text("Este archivo será eliminado")

        # Verificar que el archivo existe
        self.assertTrue(file_to_delete.exists())

        # Eliminar el archivo
        result = self.server.delete_file(str(file_to_delete))

        # Verificar que la operación fue exitosa y el archivo ya no existe
        self.assertTrue(result)
        self.assertFalse(file_to_delete.exists())

        # Probar eliminación de un directorio vacío
        empty_dir = self.test_path / "directorio_vacio"
        empty_dir.mkdir()

        result = self.server.delete_file(str(empty_dir))
        self.assertTrue(result)
        self.assertFalse(empty_dir.exists())

        # Probar que se lanza error al eliminar un directorio no vacío
        with self.assertRaises(IsADirectoryError):
            self.server.delete_file(str(self.test_subdir))

    def test_delete_directory_recursive(self):
        """Probar la eliminación recursiva de directorios."""
        # Crear estructura de directorios y archivos para eliminar
        test_recursive_dir = self.test_path / "directorio_recursivo"
        test_recursive_dir.mkdir()

        # Crear subdirectorio
        subdir = test_recursive_dir / "subdirectorio"
        subdir.mkdir()

        # Crear archivos
        (test_recursive_dir / "archivo1.txt").write_text("Contenido 1")
        (subdir / "archivo2.txt").write_text("Contenido 2")

        # Verificar que todo existe
        self.assertTrue(test_recursive_dir.exists())
        self.assertTrue(subdir.exists())
        self.assertTrue((test_recursive_dir / "archivo1.txt").exists())
        self.assertTrue((subdir / "archivo2.txt").exists())

        # Eliminar recursivamente
        result = self.server.delete_directory_recursive(str(test_recursive_dir), confirm=True)

        # Verificar que la operación fue exitosa y el directorio no existe
        self.assertTrue(result)
        self.assertFalse(test_recursive_dir.exists())

        # Probar que se lanza error al intentar eliminar un directorio base permitido
        with self.assertRaises(PermissionError):
            self.server.delete_directory_recursive(str(self.test_path), confirm=True)

    def test_copy_file(self):
        """Probar la copia de archivos y directorios."""
        # Copiar un archivo
        source_file = self.test_file
        dest_file = self.test_path / "archivo_copiado.txt"

        result = self.server.copy_file(str(source_file), str(dest_file))

        # Verificar que la operación fue exitosa y el archivo existe
        self.assertTrue(result)
        self.assertTrue(dest_file.exists())
        self.assertEqual(dest_file.read_text(), source_file.read_text())

        # Copiar un directorio
        source_dir = self.test_subdir
        dest_dir = self.test_path / "directorio_copiado"

        result = self.server.copy_file(str(source_dir), str(dest_dir))

        # Verificar que la operación fue exitosa
        self.assertTrue(result)
        self.assertTrue(dest_dir.exists())
        self.assertTrue((dest_dir / "subdir_file.txt").exists())
        self.assertEqual(
            (dest_dir / "subdir_file.txt").read_text(),
            self.test_subfile.read_text()
        )

        # Probar que se lanza error si el destino existe y overwrite=False
        with self.assertRaises(FileExistsError):
            self.server.copy_file(str(source_file), str(dest_file), overwrite=False)

        # Probar sobrescritura
        original_content = source_file.read_text()
        dest_file.write_text("Contenido diferente")

        result = self.server.copy_file(str(source_file), str(dest_file), overwrite=True)

        self.assertTrue(result)
        self.assertEqual(dest_file.read_text(), original_content)

if __name__ == "__main__":
    unittest.main()
