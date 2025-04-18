---
description: Reglas y guías para la implementación y uso de Model Context Protocol (MCP)
globs: 
alwaysApply: false
---
# Reglas MCP para Cursor

## Descripción

Reglas y guías para la implementación y uso de Model Context Protocol (MCP)

## Estructura del Proyecto

### Organización de Archivos

```
proyecto/
├── mcp/
│   ├── servers/
│   │   ├── __init__.py
│   │   └── filesystem.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── file_tools.py
│   └── config/
│       └── mcp_config.json
├── .cursor/
│   └── mcp.json
└── requirements.txt
```

## Configuración de MCP

### 1. Archivo de Configuración

Ubicación: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": [
        "-m",
        "mcp.servers.filesystem",
        "--config",
        "./mcp/config/mcp_config.json"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "MCP_ENV": "development"
      }
    }
  }
}
```

### 2. Estructura del Servidor

Archivo: `mcp/servers/filesystem.py`

```python
from modelcontextprotocol import MCPServer, Tool
from mcp.tools.file_tools import list_files, read_file, write_file

class CursorFileSystem(MCPServer):
    def __init__(self, config_path: str):
        super().__init__("cursor-filesystem")
        self.config_path = config_path

    async def initialize(self):
        # Registrar herramientas
        self.register_tool(
            Tool("list_files", "Lista archivos en el workspace", list_files)
        )
        self.register_tool(
            Tool("read_file", "Lee el contenido de un archivo", read_file)
        )
        self.register_tool(
            Tool("write_file", "Escribe contenido en un archivo", write_file)
        )
```

## Mejores Prácticas

### 1. Desarrollo

- Usar tipado estático con Python type hints
- Implementar logging comprehensivo
- Manejar errores y excepciones apropiadamente
- Documentar todas las herramientas y recursos

### 2. Seguridad

- Validar todas las entradas de usuario
- Limitar acceso a directorios específicos
- Usar variables de entorno para configuración sensible
- Implementar rate limiting cuando sea necesario

### 3. Testing

```python
# test_mcp_server.py
import pytest
from mcp.servers.filesystem import CursorFileSystem

@pytest.fixture
async def server():
    server = CursorFileSystem("./config/test_config.json")
    await server.initialize()
    yield server
    await server.shutdown()

async def test_list_files(server):
    result = await server.execute_tool("list_files", {"path": "."})
    assert isinstance(result, list)
```

## Comandos Útiles

### Desarrollo

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest mcp/tests/

# Verificar tipos
mypy mcp/

# Ejecutar servidor en modo desarrollo
python -m mcp.servers.filesystem --config ./mcp/config/dev_config.json
```

### Producción

```bash
# Construir distribución
python setup.py sdist bdist_wheel

# Instalar en modo producción
pip install dist/mcp_cursor_server-*.whl
```

## Integración con Claude

### 1. Prompts Recomendados

- "Analiza el código en el archivo actual"
- "Busca todos los archivos Python en el proyecto"
- "Crea un nuevo archivo de test para este módulo"

### 2. Ejemplos de Uso

```python
# Ejemplo de interacción con Claude
async def example_claude_interaction():
    # Listar archivos en el workspace
    files = await server.execute_tool("list_files", {"path": "."})

    # Leer contenido de un archivo
    content = await server.execute_tool("read_file", {"path": "main.py"})

    # Crear un nuevo archivo
    await server.execute_tool("write_file", {
        "path": "new_module.py",
        "content": "# Nuevo módulo creado por Claude\n"
    })
```

## Solución de Problemas

### Problemas Comunes

1. **Error de Conexión**

   - Verificar que Python está en el PATH
   - Comprobar que el servidor MCP está ejecutándose
   - Revisar logs en `.cursor/logs/mcp.log`

2. **Errores de Importación**

   - Verificar PYTHONPATH
   - Comprobar estructura del proyecto
   - Revisar dependencias en requirements.txt

3. **Problemas de Permisos**
   - Verificar permisos de archivos
   - Comprobar variables de entorno
   - Revisar configuración de seguridad

## Referencias

- [Documentación MCP](mdc:mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/https:/modelcontextprotocol.io/docs)
- [Python SDK MCP](mdc:mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/https:/github.com/modelcontextprotocol/python-sdk)
- [Ejemplos de Implementación](mdc:mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/mmlufer/https:/github.com/modelcontextprotocol/examples)

---

_Última actualización: [fecha actual]_
