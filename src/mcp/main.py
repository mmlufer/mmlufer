#!/usr/bin/env python
"""
Punto de entrada principal para servidores MCP.
Permite ejecutar diferentes servidores MCP según los argumentos proporcionados.
"""

import sys
import argparse
import importlib.util
from pathlib import Path

def main():
    """
    Función principal que analiza los argumentos y ejecuta el servidor correspondiente.
    """
    parser = argparse.ArgumentParser(description="Ejecutar servidores MCP")
    parser.add_argument(
        "--server",
        type=str,
        default="filesystem",
        choices=["filesystem"],
        help="Nombre del servidor a ejecutar (por defecto: filesystem)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activar modo de depuración"
    )

    args = parser.parse_args()

    try:
        # Establecer la ruta al archivo del servidor
        base_dir = Path(__file__).parent
        server_path = base_dir / "servers" / args.server / "server.py"

        if not server_path.exists():
            print(f"Error: No se encontró el servidor en {server_path}")
            return 1

        # Cargar el módulo dinámicamente usando importlib.util
        spec = importlib.util.spec_from_file_location(
            f"server_{args.server}", server_path
        )
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)

        # Si el servidor tiene una función init, la llamamos con los argumentos
        if hasattr(server_module, "init") and callable(server_module.init):
            server_module.init(debug=args.debug)

        # Obtener la instancia del servidor
        if hasattr(server_module, "mcp"):
            mcp_server = server_module.mcp
            print(f"Ejecutando servidor MCP: {mcp_server.name}")
            mcp_server.run()
        else:
            print(f"Error: El módulo {args.server} no expone una instancia MCP")
            return 1

    except ImportError as e:
        print(f"Error al importar el servidor '{args.server}': {e}")
        return 1
    except Exception as e:
        print(f"Error al ejecutar el servidor '{args.server}': {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
