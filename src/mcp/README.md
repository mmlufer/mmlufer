# Servidores MCP (Model Context Protocol)

Este directorio contiene implementaciones de servidores MCP para diferentes casos de uso.

## Estructura

```
mcp/
├── servers/               # Implementaciones específicas de servidores
│   ├── db/                # Servidores para bases de datos
│   └── tools/             # Utilidades específicas para servidores
├── common/                # Código compartido entre servidores
└── tests/                 # Pruebas unitarias e integración
```

## Servidores Disponibles



## Desarrollo de Nuevos Servidores

Para crear un nuevo servidor MCP, sigue estos pasos:

1. Crea un nuevo directorio bajo `servers/`
2. Implementa la clase del servidor extendiendo `MCP` o `FastMCP`
3. Define herramientas y recursos
4. Implementa las pruebas unitarias en `tests/`

## Configuración

Los servidores MCP se configuran en:
- **Cursor**: `.cursor/mcp.json`
- **Claude Desktop**: `claude_desktop_config.json`

Ejemplo de configuración:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["-m", "src.mcp.servers.filesystem.server"]
    }
  }
}
```
