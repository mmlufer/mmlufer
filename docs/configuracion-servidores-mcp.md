# Configuración de servidores MCP (Model Context Protocol)

## Descripción

Esta guía proporciona instrucciones detalladas para configurar y utilizar el Model Context Protocol (MCP) en diferentes entornos de desarrollo

## Prerrequisitos Generales

- Node.js (LTS recomendado)
- npm (Node Package Manager)
- Python 3.8+ (para SDK de Python)
- pip (Python Package Manager)
- Permisos de administrador para instalación global
- PowerShell o Terminal de Windows

## Implementaciones

### 1. Implementación con Node.js (Método Estándar)

#### Instalación Base

```powershell
# Instalación global del servidor MCP filesystem
npm install -g @modelcontextprotocol/server-filesystem

# Verificación de la instalación
npm list -g @modelcontextprotocol/server-filesystem
```

#### Verificación del Entorno

```powershell
# Verificar Node.js
node --version

# Verificar npm
npm --version

# Localizar ejecutables
where.exe node
where.exe npm
```

### 2. Implementación con Python SDK

#### Instalación del SDK

```bash
# Instalación del SDK de Python
pip install modelcontextprotocol

# Verificar la instalación
pip show modelcontextprotocol
```

#### Estructura Básica del Servidor MCP

```python
from modelcontextprotocol import MCPServer, Resource, Tool

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

## Configuración por IDE/Editor

### Claude Desktop

1. **Ubicación de Configuración**

   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Configuración Base (Node.js)**

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "C:\\ruta\\directorio\\trabajo",
           "C:\\ruta\\directorio\\secundario"
         ]
       }
     }
   }
   ```

3. **Configuración Alternativa (Python SDK)**
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "python",
         "args": [
           "-m",
           "mcp_server",
           "--workspace",
           "C:\\ruta\\directorio\\trabajo"
         ],
         "env": {
           "PYTHONPATH": "${env:PYTHONPATH}"
         }
       }
     }
   }
   ```

### Cursor

> Próximamente...

### Visual Studio Code

> Próximamente...

## Solución de Problemas

### Problemas Comunes

#### 1. Errores de Conexión

- **Síntoma**: "Could not connect to MCP server filesystem"
- **Solución**:
  ```powershell
  # Reinstalación limpia
  npm uninstall -g @modelcontextprotocol/server-filesystem
  npm cache clean --force
  npm install -g @modelcontextprotocol/server-filesystem
  ```

#### 2. Errores de Ruta

- **Síntoma**: "ENOENT" o "Path not found"
- **Verificación**:
  - Usar `where.exe` para localizar ejecutables
  - Comprobar permisos de directorios
  - Verificar sintaxis de rutas (doble barra invertida)

#### 3. Problemas de Permisos

- **Síntoma**: "Access denied" o errores similares
- **Solución**:
  - Ejecutar PowerShell como administrador
  - Verificar permisos de usuario
  - Comprobar políticas de ejecución

### Logs y Diagnóstico

- Claude Desktop: `%APPDATA%\Claude\logs\`
- Cursor: `[ruta pendiente]`
- VS Code: `[ruta pendiente]`

## Mejores Prácticas

### Estructura de Directorios

- Separar directorios de trabajo y recursos
- Evitar rutas con caracteres especiales
- Mantener rutas cortas cuando sea posible

### Variables de Entorno

- Usar variables de entorno para rutas dinámicas
- Mantener configuración sensible en variables de entorno
- Documentar variables requeridas

### Mantenimiento

- Actualizar paquetes regularmente
- Mantener copias de configuración
- Monitorear logs periódicamente

## Referencias

- [Documentación Oficial MCP](https://modelcontextprotocol.io/docs)
- [Node.js](https://nodejs.org/)
- [npm Documentation](https://docs.npmjs.com/)

## Apéndice

### Glosario

- **MCP**: Model Context Protocol
- **IDE**: Integrated Development Environment
- **CLI**: Command Line Interface

### Versiones Compatibles

| Software | Versión Mínima | Versión Recomendada |
| -------- | -------------- | ------------------- |
| Node.js  | 14.x           | 18.x LTS            |
| npm      | 6.x            | 9.x                 |

---

_Última actualización: [fecha actual]_

> **Nota**: Este documento está en constante evolución. Las secciones marcadas con "Próximamente" serán completadas en futuras actualizaciones.
