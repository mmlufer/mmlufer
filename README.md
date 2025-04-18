# 🚀 Mi Ambiente Personal de Experimentación con IA e IDEs

Este repositorio sirve como mi espacio personal para exploración de código y experimentación con Inteligencia Artificial. Aquí puedo probar nuevas ideas, tecnologías y conceptos de manera segura y organizada.

## 🛠️ Configuración Rápida

1. Clona este repositorio
2. Crea un archivo `.env` en la raíz con tus variables de entorno
3. Las configuraciones de los IDEs se cargarán automáticamente

> ⚠️ **IMPORTANTE**: Nunca hagas commit del archivo `.env` al repositorio.

## 🧩 Estructura del Proyecto

```
.
├── src/                   # Código fuente
│   ├── mcp/               # Servidores MCP
│   ├── utils/             # Utilidades generales
│   ├── config/            # Configuraciones
│   └── api/               # APIs y servicios web
├── docs/                  # Documentación
├── tests/                 # Pruebas automatizadas
└── .cursor/               # Configuraciones de IDE
```

Para una estructura más detallada, consulta [Estructura del Repositorio](/docs/desarrollo/estructura-repositorio.md).

## 🔧 Características Principales

- Ambiente aislado para experimentación con IA
- Servidores MCP para integración con Claude
- Configuraciones optimizadas para múltiples IDEs
- Estructura modular para diferentes tipos de proyectos

## 📚 Documentación

- [Índice de Documentación](/docs/README.md) - Punto central de acceso a toda la documentación
- [Guía de MCP](/docs/mcp/README.md) - Documentación sobre servidores MCP
- [Guía de Tests](/tests/README.md) - Documentación sobre pruebas automatizadas

## 🚀 Uso Rápido

```bash
# Ejecutar el servidor MCP
python -m src.mcp.main --server nombre-servidor-mcp
```

Para más detalles sobre cómo utilizar los servidores MCP, consulta la [Guía de MCP](/docs/mcp/README.md).

## 🤝 Contribución

Este es un repositorio personal de experimentación, pero puedes:
- Crear ramas para tus propios experimentos
- Sugerir mejoras en la estructura
- Compartir ideas para nuevos experimentos

---

_Última actualización: [Fecha Actual]_
