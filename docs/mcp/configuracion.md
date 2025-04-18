# ⚙️ Configuración de Servidores MCP

Guía para configurar e implementar servidores MCP (Model Context Protocol) en diferentes entornos.

## 📋 Prerrequisitos

- Python 3.8+ para SDK de Python
- Node.js LTS y npm para implementación con Node.js
- Permisos de administrador para instalación global

## 🛠️ Implementaciones

### Python SDK

```bash
# Instalación del SDK
pip install modelcontextprotocol

# Verificación
pip show modelcontextprotocol
```

### Node.js (Método Estándar)

```bash
# Instalación global del servidor filesystem
npm install -g @modelcontextprotocol/server-filesystem

# Verificación
npm list -g @modelcontextprotocol/server-filesystem
```

## 🔌 Integración con Claude Desktop

1. **Ubicación de Configuración**:
   ```bash
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Configuración Python**:
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
         ]
       }
     }
   }
   ```

3. **Configuración Node.js**:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "C:\\ruta\\directorio\\trabajo"
         ]
       }
     }
   }
   ```

## ⚠️ Solución de Problemas Comunes

- **Error de Conexión**: Reinstalar con `npm uninstall -g` seguido de `npm cache clean --force`
- **Error de Ruta**: Verificar rutas con `where.exe` y comprobar permisos
- **Error de Permisos**: Ejecutar terminal como administrador

## 📚 Documentación Relacionada

- [Servidor Filesystem](/docs/mcp/filesystem/README.md)
- [Guía de Tests](/tests/README.md)

---

_Última actualización: [Fecha Actual] - [hora]_
