# 📝 Changelog: Servidor MCP Filesystem

Registro de cambios del servidor MCP Filesystem.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/)
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🚧 En Desarrollo
- Implementación de `read_multiple_files`
- Mejoras en manejo de errores

## [0.3.0] - 2024-04-18

### ✅ Añadido
- Implementación de `search_files` con soporte para:
  - Patrones glob (*.txt, test_*)
  - Expresiones regulares
  - Búsqueda recursiva o no recursiva
- Corrección de manejo de rutas en diferentes unidades de Windows
- Mejora de la documentación con diagramas y ejemplos completos

## [0.2.0] - 2024-04-18

### ✅ Añadido
- Implementación de `write_file`
- Implementación de `create_directory`
- Implementación de `get_file_info`
- Implementación de `list_allowed_directories`
- Pruebas básicas de funcionalidad

## [0.1.0] - 2024-04-10

### ✅ Añadido
- Estructura inicial del proyecto
- Configuración básica del servidor FastMCP
- Validación de rutas y directorios permitidos
- Implementación básica de `read_file` y `list_directory`

## 📚 Documentación Relacionada

- [Roadmap](./mcp_filesystem_roadmap.md) - Plan de desarrollo del servidor
- [Guía del Servidor](./README.md) - Documentación general
- [Implementación](/src/mcp/servers/filesystem/README.md) - Documentación técnica
- [Configuración](/docs/mcp/configuracion.md) - Guía de instalación y configuración

---

_Última actualización: 2024-04-18 - [hora]_
