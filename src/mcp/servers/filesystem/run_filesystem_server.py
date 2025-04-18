#!/usr/bin/env python3
"""
Script para ejecutar el servidor MCP Filesystem.

Este script lanza un servidor FastMCP que proporciona acceso
al sistema de archivos de manera segura.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from mcp.servers.filesystem import FilesystemServer

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("filesystem_server")

def main():
    """Función principal para ejecutar el servidor."""
    try:
        # Determinar los directorios permitidos
        default_allowed_dirs = [os.getcwd()]

        # Comprobar si hay un archivo de configuración
        config_path = Path(os.getcwd()) / "filesystem_config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                allowed_dirs = config.get("allowed_directories", default_allowed_dirs)
                logger.info(f"Cargada configuración desde {config_path}")
        else:
            allowed_dirs = default_allowed_dirs
            logger.info("Usando configuración por defecto")

        # Inicializar el servidor
        server = FilesystemServer(allowed_directories=allowed_dirs)
        logger.info(f"Servidor iniciado con directorios permitidos: {server.list_allowed_directories()}")

        # Demostrar algunas funcionalidades básicas
        print("\n=== Demostración del servidor MCP Filesystem ===")
        print(f"Directorios permitidos: {server.list_allowed_directories()}")

        # Listar el directorio actual
        current_dir = os.getcwd()
        print(f"\nContenido del directorio actual ({current_dir}):")
        for item in server.list_directory(current_dir):
            type_marker = "[DIR]" if item['is_directory'] else "[FILE]"
            print(f"{type_marker} {item['name']}")

        # Crear un archivo de prueba
        test_file = os.path.join(current_dir, "filesystem_test.txt")
        server.write_file(test_file, "Este es un archivo de prueba creado por el servidor MCP Filesystem.")
        print(f"\nArchivo creado: {test_file}")

        # Leer el archivo
        content = server.read_file(test_file)
        print(f"Contenido del archivo: {content}")

        # Obtener información del archivo
        info = server.get_file_info(test_file)
        print("\nInformación del archivo:")
        for key, value in info.items():
            print(f"  - {key}: {value}")

        # Demostrar la búsqueda de archivos
        print("\n=== Demostración de búsqueda de archivos ===")

        # Buscar archivos Python
        print("\nBuscando archivos Python (*.py):")
        py_files = server.search_files(current_dir, "*.py")
        if py_files:
            for file in py_files[:5]:  # Mostrar solo los primeros 5 resultados
                print(f"  - {file['path']}")
            if len(py_files) > 5:
                print(f"  ... y {len(py_files) - 5} más")
        else:
            print("  No se encontraron archivos Python")

        # Buscar archivos Markdown
        print("\nBuscando archivos Markdown (*.md):")
        md_files = server.search_files(current_dir, "*.md")
        if md_files:
            for file in md_files[:5]:  # Mostrar solo los primeros 5 resultados
                print(f"  - {file['path']}")
            if len(md_files) > 5:
                print(f"  ... y {len(md_files) - 5} más")
        else:
            print("  No se encontraron archivos Markdown")

        # Buscar con expresión regular
        print("\nBuscando archivos con expresión regular (README.*):")
        readme_files = server.search_files(current_dir, "README.*", use_regex=True)
        if readme_files:
            for file in readme_files:
                print(f"  - {file['path']}")
        else:
            print("  No se encontraron archivos README")

        print("\nEl servidor MCP Filesystem está listo para ser integrado con FastMCP.")
        print("Para usar en una aplicación, importa la clase FilesystemServer.")

        # Demostración de operaciones avanzadas
        print("\n=== Demostración de operaciones avanzadas ===")

        # Crear directorio para pruebas
        advanced_dir = os.path.join(current_dir, "prueba_avanzada")
        if os.path.exists(advanced_dir):
            server.delete_directory_recursive(advanced_dir, confirm=True)
            print(f"Se eliminó el directorio existente: {advanced_dir}")

        server.create_directory(advanced_dir)
        print(f"Directorio creado: {advanced_dir}")

        # Crear algunos archivos
        for i in range(1, 4):
            file_path = os.path.join(advanced_dir, f"archivo_{i}.txt")
            server.write_file(file_path, f"Contenido del archivo {i}")
            print(f"Archivo creado: {file_path}")

        # Copiar un archivo
        source_file = os.path.join(advanced_dir, "archivo_1.txt")
        dest_file = os.path.join(advanced_dir, "archivo_copia.txt")
        server.copy_file(source_file, dest_file)
        print(f"Archivo copiado: {source_file} -> {dest_file}")

        # Mostrar listado del directorio
        print(f"\nContenido del directorio de prueba ({advanced_dir}):")
        for item in server.list_directory(advanced_dir):
            type_marker = "[DIR]" if item['is_directory'] else "[FILE]"
            print(f"{type_marker} {item['name']}")

        # Eliminar un archivo
        file_to_delete = os.path.join(advanced_dir, "archivo_2.txt")
        server.delete_file(file_to_delete)
        print(f"Archivo eliminado: {file_to_delete}")

        # Crear subdirectorio para probar copia de directorios
        subdir = os.path.join(advanced_dir, "subdirectorio")
        server.create_directory(subdir)
        server.write_file(os.path.join(subdir, "subarchivo.txt"), "Contenido en subdirectorio")
        print(f"Subdirectorio creado con archivo: {subdir}")

        # Copiar directorio
        dest_dir = os.path.join(advanced_dir, "subdirectorio_copia")
        server.copy_file(subdir, dest_dir)
        print(f"Directorio copiado: {subdir} -> {dest_dir}")

        # Listado final
        print(f"\nContenido final del directorio de prueba ({advanced_dir}):")
        dirs = []

        def print_dir_tree(directory, indent=""):
            items = server.list_directory(directory)
            for item in items:
                type_marker = "[DIR]" if item['is_directory'] else "[FILE]"
                print(f"{indent}{type_marker} {item['name']}")
                if item['is_directory']:
                    print_dir_tree(os.path.join(directory, item['name']), indent + "  ")

        print_dir_tree(advanced_dir)

    except Exception as e:
        logger.error(f"Error al ejecutar el servidor: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
