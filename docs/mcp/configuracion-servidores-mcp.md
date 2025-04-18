# Configuración de servidores MCP (Model Context Protocol)

## Descripción

Esta guía proporciona instrucciones detalladas para configurar y utilizar el Model Context Protocol (MCP) en diferentes entornos de desarrollo utilizando Python.

## Prerrequisitos Generales

- Python 3.8+ (recomendado 3.10+)
- pip (Python Package Manager)
- Permisos de administrador para ciertas instalaciones
- PowerShell o Terminal de Windows

## Implementación con Python SDK

### Instalación del SDK

```bash
# Instalación del SDK de Python
pip install modelcontextprotocol

# Verificar la instalación
pip show modelcontextprotocol
```

### Estructura Básica del Servidor MCP

```python
from mcp import MCPServer, Resource, Tool

class FileSystemServer(MCPServer):
    def __init__(self):
        super().__init__("filesystem")

    async def initialize(self):
        # Configurar recursos y herramientas
        self.register_tool(
            Tool(
                name="list_files",
                description="Lista archivos en un directorio",
                handler=self.list_files
            )
        )

    async def list_files(self, path: str):
        # Implementación de la herramienta
        pass

# Iniciar el servidor
server = FileSystemServer()
server.start()
```

### Usando el Servidor Filesystem

El servidor MCP Filesystem implementado en Python incluye funcionalidades extendidas:

```python
from src.mcp.servers.filesystem import FilesystemServer

# Inicializar con directorios permitidos
server = FilesystemServer(allowed_directories=['/ruta/permitida'])

# Operaciones básicas
content = server.read_file('/ruta/permitida/archivo.txt')
server.write_file('/ruta/permitida/nuevo.txt', 'Contenido del archivo')
files = server.list_directory('/ruta/permitida')

# Operaciones avanzadas
# Copiar archivos o directorios
server.copy_file('/ruta/origen.txt', '/ruta/destino.txt', overwrite=False)

# Eliminar archivos o directorios vacíos
server.delete_file('/ruta/archivo_a_eliminar.txt')

# Eliminar directorios recursivamente con todo su contenido
server.delete_directory_recursive('/ruta/directorio', confirm=True)
```

## Configuración por IDE/Editor

### Claude Desktop

1. **Ubicación de Configuración**

   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Configuración con Python SDK**
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "python",
         "args": [
           "-m",
           "src.mcp.servers.filesystem.run_filesystem_server"
         ],
         "env": {
           "PYTHONPATH": "${env:PYTHONPATH}"
         }
       }
     }
   }
   ```

3. **Configuración Docker**

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "--mount", "type=bind,src=C:\\ruta\\directorio\\trabajo,dst=/projects/trabajo",
           "--mount", "type=bind,src=C:\\ruta\\directorio\\secundario,dst=/projects/secundario,ro",
           "mcp/filesystem",
           "/projects"
         ]
       }
     }
   }
   ```

### Cursor

1. **Ubicación de Configuración**

   ```
   .cursor/mcp.json
   ```

2. **Configuración Base**

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "python",
         "args": [
           "-m",
           "src.mcp.servers.filesystem.run_filesystem_server"
         ]
       }
     }
   }
   ```

3. **Configuración con URL**

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "url": "https://gitmcp.io/_/modelcontextprotocol/servers/tree/main/src/filesystem"
       }
     }
   }
   ```

### Visual Studio Code

1. **Ubicación de Configuración**

   ```
   .vscode/mcp.json
   ```

2. **Configuración Base**

   ```json
   {
     "servers": {
       "filesystem": {
         "type": "sse",
         "url": "https://gitmcp.io/_/modelcontextprotocol/servers/tree/main/src/filesystem"
       }
     }
   }
   ```

## Solución de Problemas

### Problemas Comunes

#### 1. Errores de Conexión

- **Síntoma**: "Could not connect to MCP server filesystem"
- **Solución**:
  ```bash
  # Reinstalación limpia
  pip uninstall modelcontextprotocol
  pip install modelcontextprotocol
  ```

#### 2. Errores de Ruta

- **Síntoma**: "FileNotFoundError" o "Path not found"
- **Verificación**:
  - Comprobar permisos de directorios
  - Verificar sintaxis de rutas (usar rutas absolutas)
  - Verificar que los directorios especificados existen

#### 3. Problemas de Permisos

- **Síntoma**: "PermissionError" o errores similares
- **Solución**:
  - Ejecutar PowerShell como administrador
  - Verificar permisos de usuario
  - Comprobar políticas de ejecución

#### 4. Problemas con Importaciones en Python

- **Síntoma**: "ImportError: attempted relative import with no known parent package"
- **Solución**:
  - Ejecutar el servidor como módulo usando: `python -m src.mcp.servers.filesystem.run_filesystem_server`
  - Verificar que la estructura de directorios es correcta
  - Comprobar que PYTHONPATH incluye el directorio raíz del proyecto

### Logs y Diagnóstico

- Claude Desktop: `%APPDATA%\Claude\logs\`
- Cursor: `.cursor/logs/mcp.log`
- VS Code: `.vscode/logs/`

## Mejores Prácticas

### Estructura de Directorios

- Separar directorios de trabajo y recursos
- Evitar rutas con caracteres especiales
- Mantener rutas cortas cuando sea posible

### Variables de Entorno

- Usar variables de entorno para rutas dinámicas
- Mantener configuración sensible en variables de entorno
- Documentar variables requeridas

### Seguridad

- Especificar siempre directorios permitidos explícitamente
- Evitar dar acceso a directorios del sistema
- Utilizar el parámetro `ro` (read-only) en Docker para directorios que solo necesitan acceso de lectura
- Para operaciones destructivas como `delete_directory_recursive`, usar siempre el parámetro `confirm=true`

### Mantenimiento

- Actualizar paquetes regularmente
- Mantener copias de configuración
- Monitorear logs periódicamente
- Ejecutar pruebas después de actualizar

## Referencias Oficiales

- [Documentación Oficial MCP](https://modelcontextprotocol.io/docs)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk/)
- [Repositorio de Servidores MCP](https://github.com/modelcontextprotocol/servers)

## Recursos Relacionados

- [Roadmap del Servidor MCP Filesystem](/docs/mcp/mcp_filesystem_roadmap.md) - Plan de desarrollo del servidor MCP Filesystem.
- [Changelog del Servidor MCP Filesystem](/docs/mcp/mcp_filesystem_changelog.md) - Historial de cambios del servidor MCP Filesystem.
- [Documentación Principal](/README.md) - Documentación general del proyecto.
- [Documentación de Tests](/tests/README.md) - Guía para las pruebas de servidores MCP.

## Apéndice

### Glosario

- **MCP**: Model Context Protocol
- **IDE**: Integrated Development Environment
- **CLI**: Command Line Interface
- **SSE**: Server-Sent Events (tipo de transporte para MCP)

### Versiones Compatibles

| Software | Versión Mínima | Versión Recomendada |
| -------- | -------------- | ------------------- |
| Python   | 3.8            | 3.10+               |

---

_Última actualización: 2025-04-15 - 11:25 am_

> **Nota**: Este documento está en constante evolución. Consulta regularmente las actualizaciones del repositorio oficial para obtener la información más reciente.
