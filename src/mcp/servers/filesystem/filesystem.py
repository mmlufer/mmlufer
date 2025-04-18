"""
Implementación del servidor MCP para operaciones seguras del sistema de archivos.

Este módulo proporciona acceso controlado al sistema de archivos, permitiendo
operaciones básicas como lectura, escritura y listado de directorios.
"""

import os
import json
import fnmatch
import re
import shutil
from pathlib import Path
from typing import Dict, List, Union, Optional, Any, Tuple

# Clase principal del servidor Filesystem MCP
class FilesystemServer:
    """
    Servidor MCP para operaciones seguras en el sistema de archivos.
    Proporciona herramientas para interactuar con archivos y directorios
    de manera controlada y segura.
    """

    def __init__(self, allowed_directories: List[str] = None):
        """
        Inicializa el servidor con los directorios permitidos.

        Args:
            allowed_directories: Lista de directorios a los que se permite acceso.
                                Si es None, solo se permite el directorio actual.
        """
        if allowed_directories is None:
            self.allowed_directories = [os.getcwd()]
        else:
            self.allowed_directories = [os.path.abspath(d) for d in allowed_directories]

    def _validate_path(self, path: str) -> str:
        """
        Valida que una ruta sea segura y esté dentro de los directorios permitidos.

        Args:
            path: Ruta a validar

        Returns:
            Ruta absoluta normalizada

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
        """
        abs_path = os.path.abspath(path)

        for allowed_dir in self.allowed_directories:
            if abs_path.startswith(allowed_dir):
                return abs_path

        raise ValueError(f"Acceso denegado: la ruta '{path}' no está en un directorio permitido")

    def _safe_relpath(self, path: str, start: str = None) -> str:
        """
        Versión segura de os.path.relpath que maneja diferentes unidades en Windows.

        Args:
            path: Ruta a convertir en relativa
            start: Directorio de inicio para la ruta relativa

        Returns:
            Ruta relativa o absoluta si están en diferentes unidades
        """
        if start is None:
            start = os.getcwd()

        try:
            return os.path.relpath(path, start=start)
        except ValueError:
            # Si están en diferentes unidades, devolver la ruta absoluta
            return path

    # Implementación de herramientas (tools)

    def read_file(self, path: str) -> str:
        """
        Lee el contenido de un archivo.

        Args:
            path: Ruta del archivo a leer

        Returns:
            Contenido del archivo como string

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
            FileNotFoundError: Si el archivo no existe
        """
        validated_path = self._validate_path(path)

        if not os.path.isfile(validated_path):
            raise FileNotFoundError(f"El archivo '{path}' no existe")

        with open(validated_path, 'r', encoding='utf-8') as f:
            return f.read()

    def read_multiple_files(self, paths: List[str], max_size_per_file: int = None, max_total_size: int = None) -> Dict[str, str]:
        """
        Lee el contenido de múltiples archivos en una sola operación.

        Args:
            paths: Lista de rutas de archivos a leer
            max_size_per_file: Tamaño máximo en bytes permitido por archivo (None = sin límite)
            max_total_size: Tamaño máximo en bytes para la suma de todos los archivos (None = sin límite)

        Returns:
            Diccionario con las rutas como claves y los contenidos como valores

        Raises:
            ValueError: Si alguna ruta no está en un directorio permitido
            FileNotFoundError: Si algún archivo no existe
            RuntimeError: Si se excede algún límite de tamaño
        """
        if not paths:
            return {}

        result = {}
        total_size = 0

        # Primero validamos todas las rutas
        validated_paths = {path: self._validate_path(path) for path in paths}

        # Verificamos que todos los archivos existan y calculamos el tamaño total
        for orig_path, val_path in validated_paths.items():
            if not os.path.isfile(val_path):
                raise FileNotFoundError(f"El archivo '{orig_path}' no existe")

            size = os.path.getsize(val_path)

            # Verificar límite por archivo
            if max_size_per_file is not None and size > max_size_per_file:
                raise RuntimeError(f"El archivo '{orig_path}' excede el tamaño máximo permitido ({size} > {max_size_per_file} bytes)")

            total_size += size

        # Verificar límite total
        if max_total_size is not None and total_size > max_total_size:
            raise RuntimeError(f"El tamaño total de los archivos ({total_size} bytes) excede el máximo permitido ({max_total_size} bytes)")

        # Leer los archivos
        for orig_path, val_path in validated_paths.items():
            with open(val_path, 'r', encoding='utf-8') as f:
                result[orig_path] = f.read()

        return result

    def write_file(self, path: str, content: str) -> bool:
        """
        Crea o sobrescribe un archivo con el contenido proporcionado.

        Args:
            path: Ruta del archivo a escribir
            content: Contenido a escribir en el archivo

        Returns:
            True si la escritura fue exitosa

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
        """
        validated_path = self._validate_path(path)

        # Crear directorios si no existen
        directory = os.path.dirname(validated_path)
        os.makedirs(directory, exist_ok=True)

        with open(validated_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """
        Lista el contenido de un directorio.

        Args:
            path: Ruta del directorio a listar

        Returns:
            Lista de archivos y subdirectorios con metadatos

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
            NotADirectoryError: Si la ruta no es un directorio
        """
        validated_path = self._validate_path(path)

        if not os.path.isdir(validated_path):
            raise NotADirectoryError(f"La ruta '{path}' no es un directorio")

        result = []

        for item in os.listdir(validated_path):
            item_path = os.path.join(validated_path, item)
            is_dir = os.path.isdir(item_path)

            item_info = {
                'name': item,
                'path': self._safe_relpath(item_path),
                'is_directory': is_dir,
            }

            if not is_dir:
                item_info['size'] = os.path.getsize(item_path)
                item_info['extension'] = os.path.splitext(item)[1][1:] or None

            result.append(item_info)

        return result

    def create_directory(self, path: str) -> bool:
        """
        Crea un nuevo directorio.

        Args:
            path: Ruta del directorio a crear

        Returns:
            True si la creación fue exitosa

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
            FileExistsError: Si el directorio ya existe
        """
        validated_path = self._validate_path(path)

        if os.path.exists(validated_path):
            raise FileExistsError(f"El directorio o archivo '{path}' ya existe")

        os.makedirs(validated_path)
        return True

    def get_file_info(self, path: str) -> Dict[str, Any]:
        """
        Obtiene metadatos de un archivo.

        Args:
            path: Ruta del archivo

        Returns:
            Diccionario con información del archivo

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
            FileNotFoundError: Si el archivo no existe
        """
        validated_path = self._validate_path(path)

        if not os.path.exists(validated_path):
            raise FileNotFoundError(f"El archivo o directorio '{path}' no existe")

        stats = os.stat(validated_path)
        is_dir = os.path.isdir(validated_path)

        result = {
            'name': os.path.basename(validated_path),
            'path': self._safe_relpath(validated_path),
            'is_directory': is_dir,
            'size': stats.st_size,
            'created_at': stats.st_ctime,
            'modified_at': stats.st_mtime,
            'accessed_at': stats.st_atime,
        }

        if not is_dir:
            result['extension'] = os.path.splitext(validated_path)[1][1:] or None

        return result

    def search_files(self, directory: str, pattern: str, recursive: bool = True, use_regex: bool = False) -> List[Dict[str, Any]]:
        """
        Busca archivos que coincidan con un patrón en un directorio.

        Args:
            directory: Directorio donde buscar
            pattern: Patrón de búsqueda (glob o regex según use_regex)
            recursive: Si es True, busca en subdirectorios
            use_regex: Si es True, interpreta pattern como expresión regular

        Returns:
            Lista de archivos y directorios que coinciden con el patrón

        Raises:
            ValueError: Si la ruta no está en un directorio permitido
            NotADirectoryError: Si la ruta no es un directorio
        """
        validated_path = self._validate_path(directory)

        if not os.path.isdir(validated_path):
            raise NotADirectoryError(f"La ruta '{directory}' no es un directorio")

        results = []

        # Preparar el patrón de regex si es necesario
        if use_regex:
            try:
                regex = re.compile(pattern)
            except re.error:
                raise ValueError(f"Patrón de expresión regular inválido: {pattern}")

        # Función para verificar si un archivo coincide con el patrón
        def matches_pattern(filename: str) -> bool:
            if use_regex:
                return bool(regex.search(filename))
            else:
                return fnmatch.fnmatch(filename, pattern)

        # Función para procesar un directorio
        def process_directory(current_dir: str) -> None:
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                is_dir = os.path.isdir(item_path)

                # Verificar si el elemento coincide con el patrón
                if matches_pattern(item):
                    item_info = {
                        'name': item,
                        'path': self._safe_relpath(item_path),
                        'is_directory': is_dir,
                    }

                    if not is_dir:
                        item_info['size'] = os.path.getsize(item_path)
                        item_info['extension'] = os.path.splitext(item)[1][1:] or None

                    results.append(item_info)

                # Si es un directorio y la búsqueda es recursiva, procesar subdirectorios
                if is_dir and recursive:
                    try:
                        process_directory(item_path)
                    except PermissionError:
                        # Ignorar directorios a los que no tenemos acceso
                        pass

        # Iniciar la búsqueda
        process_directory(validated_path)
        return results

    def move_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """
        Mueve o renombra un archivo o directorio.

        Args:
            source: Ruta del archivo o directorio origen
            destination: Ruta del archivo o directorio destino
            overwrite: Si es True, sobrescribe el destino si existe

        Returns:
            True si la operación fue exitosa

        Raises:
            ValueError: Si alguna ruta no está en un directorio permitido
            FileNotFoundError: Si el origen no existe
            FileExistsError: Si el destino existe y overwrite es False
        """
        source_path = self._validate_path(source)
        dest_path = self._validate_path(destination)

        # Verificar que el origen existe
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"El archivo o directorio origen '{source}' no existe")

        # Verificar si el destino existe
        if os.path.exists(dest_path) and not overwrite:
            raise FileExistsError(f"El destino '{destination}' ya existe y no se ha especificado sobrescritura")

        # Crear directorios padre del destino si no existen
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Mover el archivo o directorio
        shutil.move(source_path, dest_path)
        return True

    def edit_file(self, path: str, edit_operations: List[Dict[str, Any]]) -> bool:
        """
        Edita un archivo aplicando una serie de operaciones.

        Args:
            path: Ruta del archivo a editar
            edit_operations: Lista de operaciones de edición a aplicar.
                             Cada operación es un diccionario con las siguientes claves:
                             - 'type': Tipo de operación ('replace', 'insert', 'delete')
                             - 'line_start': Línea inicial (base 0) para la operación
                             - 'line_end': Línea final (base 0) para la operación (solo para 'replace' y 'delete')
                             - 'content': Nuevo contenido a insertar o reemplazar (no aplica para 'delete')

        Returns:
            True si la edición fue exitosa

        Raises:
            ValueError: Si la ruta no está en un directorio permitido o las operaciones son inválidas
            FileNotFoundError: Si el archivo no existe
        """
        validated_path = self._validate_path(path)

        # Verificar que el archivo existe
        if not os.path.isfile(validated_path):
            raise FileNotFoundError(f"El archivo '{path}' no existe")

        # Leer el contenido actual del archivo
        with open(validated_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Validar operaciones
        for op in edit_operations:
            if 'type' not in op:
                raise ValueError("La operación debe tener un tipo ('replace', 'insert', 'delete')")

            if op['type'] not in ['replace', 'insert', 'delete']:
                raise ValueError(f"Tipo de operación desconocido: {op['type']}")

            if 'line_start' not in op:
                raise ValueError("La operación debe tener una línea inicial (line_start)")

            if op['line_start'] < 0 or op['line_start'] > len(lines):
                raise ValueError(f"Línea inicial fuera de rango: {op['line_start']}")

            if op['type'] in ['replace', 'delete']:
                if 'line_end' not in op:
                    raise ValueError(f"La operación '{op['type']}' debe tener una línea final (line_end)")

                if op['line_end'] < op['line_start'] or op['line_end'] > len(lines):
                    raise ValueError(f"Línea final fuera de rango: {op['line_end']}")

            if op['type'] in ['replace', 'insert'] and 'content' not in op:
                raise ValueError(f"La operación '{op['type']}' debe tener contenido a insertar (content)")

        # Aplicar las operaciones en orden inverso para que las líneas no se desplacen
        # durante la edición
        edited_lines = lines.copy()

        for op in sorted(edit_operations, key=lambda x: x['line_start'], reverse=True):
            if op['type'] == 'replace':
                content = op['content']
                if not isinstance(content, list):
                    content = content.splitlines(True) if content else []

                edited_lines[op['line_start']:op['line_end'] + 1] = content

            elif op['type'] == 'delete':
                del edited_lines[op['line_start']:op['line_end'] + 1]

            elif op['type'] == 'insert':
                content = op['content']
                if not isinstance(content, list):
                    content = content.splitlines(True) if content else []

                edited_lines[op['line_start']:op['line_start']] = content

        # Escribir el contenido actualizado
        with open(validated_path, 'w', encoding='utf-8') as f:
            f.writelines(edited_lines)

        return True

    def list_allowed_directories(self) -> List[str]:
        """
        Obtiene la lista de directorios permitidos.

        Returns:
            Lista de directorios permitidos
        """
        return self.allowed_directories.copy()

    def delete_file(self, path: str) -> bool:
        """
        Elimina un archivo o directorio del sistema de archivos.

        Args:
            path: Ruta del archivo o directorio a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario

        Raises:
            ValueError: Si la ruta está fuera de los directorios permitidos
            FileNotFoundError: Si el archivo no existe
            PermissionError: Si no se tienen permisos para eliminar
            IsADirectoryError: Si se intenta eliminar un directorio no vacío
        """
        validated_path = self._validate_path(path)

        if not os.path.exists(validated_path):
            raise FileNotFoundError(f"La ruta no existe: {path}")

        try:
            if os.path.isfile(validated_path):
                os.remove(validated_path)
            elif os.path.isdir(validated_path):
                os.rmdir(validated_path)  # Solo elimina directorios vacíos
            else:
                return False
            return True
        except PermissionError:
            raise PermissionError(f"No tiene permisos para eliminar: {path}")
        except OSError as e:
            if os.path.isdir(validated_path):
                raise IsADirectoryError(f"El directorio no está vacío: {path}")
            raise e

    def delete_directory_recursive(self, path: str, confirm: bool = False) -> bool:
        """
        Elimina un directorio y todo su contenido recursivamente.

        Args:
            path: Ruta del directorio a eliminar
            confirm: Si es True, se realiza la eliminación. Si es False, solo se valida.

        Returns:
            True si se eliminó correctamente o si confirm=False y la operación es válida

        Raises:
            ValueError: Si la ruta está fuera de los directorios permitidos
            FileNotFoundError: Si el directorio no existe
            NotADirectoryError: Si la ruta no es un directorio
            PermissionError: Si no se tienen permisos para eliminar
        """
        validated_path = self._validate_path(path)

        if not os.path.exists(validated_path):
            raise FileNotFoundError(f"La ruta no existe: {path}")

        if not os.path.isdir(validated_path):
            raise NotADirectoryError(f"La ruta no es un directorio: {path}")

        # Comprobar si está intentando eliminar un directorio permitido
        for allowed_dir in self.allowed_directories:
            if os.path.abspath(allowed_dir) == os.path.abspath(validated_path):
                raise PermissionError(f"No se puede eliminar un directorio base permitido: {path}")

        if not confirm:
            return True  # Solo validación, no elimina

        try:
            # shutil.rmtree es peligroso, usamos nuestra propia implementación recursiva
            def remove_recursive(current_path):
                if os.path.isdir(current_path):
                    # Primero validamos que cada elemento a eliminar esté en directorios permitidos
                    entries = os.listdir(current_path)
                    for entry in entries:
                        entry_path = os.path.join(current_path, entry)
                        # Validar de nuevo cada ruta por seguridad
                        self._validate_path(entry_path)
                        remove_recursive(entry_path)
                    os.rmdir(current_path)
                else:
                    os.remove(current_path)

            remove_recursive(validated_path)
            return True

        except PermissionError:
            raise PermissionError(f"No tiene permisos para eliminar: {path}")
        except OSError as e:
            raise e

    def copy_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """
        Copia un archivo o directorio de una ubicación a otra.

        Args:
            source: Ruta del archivo o directorio origen
            destination: Ruta de destino
            overwrite: Si es True, sobrescribe archivos existentes

        Returns:
            True si se copió correctamente

        Raises:
            ValueError: Si alguna ruta está fuera de los directorios permitidos
            FileNotFoundError: Si el origen no existe
            FileExistsError: Si el destino existe y overwrite=False
            PermissionError: Si no se tienen permisos
        """
        # Validar ambas rutas
        validated_source = self._validate_path(source)
        validated_dest = self._validate_path(destination)

        if not os.path.exists(validated_source):
            raise FileNotFoundError(f"La ruta de origen no existe: {source}")

        # Verificar si el destino existe y manejar según overwrite
        if os.path.exists(validated_dest) and not overwrite:
            raise FileExistsError(f"La ruta de destino ya existe: {destination}")

        try:
            if os.path.isfile(validated_source):
                # Copiar archivo
                # Si el destino es un directorio, crear el archivo dentro del directorio
                if os.path.isdir(validated_dest):
                    dest_path = os.path.join(validated_dest, os.path.basename(validated_source))
                    validated_dest = self._validate_path(dest_path)

                # Crear el directorio de destino si no existe
                os.makedirs(os.path.dirname(validated_dest), exist_ok=True)

                # Copiar el contenido del archivo
                with open(validated_source, 'rb') as src_file:
                    with open(validated_dest, 'wb') as dest_file:
                        dest_file.write(src_file.read())

            elif os.path.isdir(validated_source):
                # Copiar directorio recursivamente
                if os.path.exists(validated_dest) and not os.path.isdir(validated_dest):
                    raise NotADirectoryError(f"El destino existe y no es un directorio: {destination}")

                def copy_recursive(src, dst):
                    if not os.path.exists(dst):
                        os.makedirs(dst)

                    for item in os.listdir(src):
                        src_item = os.path.join(src, item)
                        dst_item = os.path.join(dst, item)

                        # Validar cada elemento por seguridad
                        self._validate_path(src_item)
                        self._validate_path(dst_item)

                        if os.path.isdir(src_item):
                            copy_recursive(src_item, dst_item)
                        else:
                            if os.path.exists(dst_item) and not overwrite:
                                continue

                            with open(src_item, 'rb') as src_file:
                                with open(dst_item, 'wb') as dst_file:
                                    dst_file.write(src_file.read())

                # Si el destino es un directorio existente, copiar dentro de él
                if os.path.isdir(validated_dest) and os.path.exists(validated_dest):
                    validated_dest = os.path.join(validated_dest, os.path.basename(validated_source))
                    validated_dest = self._validate_path(validated_dest)

                copy_recursive(validated_source, validated_dest)

            return True

        except PermissionError:
            raise PermissionError(f"No tiene permisos para copiar: {source} a {destination}")
        except OSError as e:
            raise e
