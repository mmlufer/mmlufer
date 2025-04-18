#!/usr/bin/env python
"""
Script para ejecutar todos los tests del servidor MCP filesystem.

Uso:
    python run_tests.py [opciones]

Opciones:
    --unit: Ejecutar solo tests unitarios
    --integration: Ejecutar solo tests de integración
    --verbose: Mostrar salida detallada
"""

import sys
import pytest

if __name__ == "__main__":
    # Argumentos por defecto
    args = ["-v"]

    # Procesar argumentos de línea de comandos
    if "--unit" in sys.argv:
        args.append("-m")
        args.append("unit")

    if "--integration" in sys.argv:
        args.append("-m")
        args.append("integration")

    if "--verbose" in sys.argv or "-v" in sys.argv:
        args.append("-v")

    # Ejecutar pytest con los argumentos especificados
    sys.exit(pytest.main(args))
