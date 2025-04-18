# 📁 Estructura Detallada del Proyecto

Este documento describe la estructura detallada del proyecto, sus componentes principales y la organización de archivos y directorios.

## 📂 Estructura General

```
.
├── .env                    # Variables de entorno (no commitear)
├── .gitignore              # Archivos ignorados por git
├── mmlufer.code-workspace  # Configuración compartida entre IDEs
├── .cursor/                # Configuraciones de Cursor
├── .vscode/                # Configuraciones de VS Code
├── .windsurf/              # Configuraciones de Windsurf
├── src/                    # Código fuente
├── docs/                   # Documentación
├── tests/                  # Pruebas automatizadas
└── README.md               # Documentación principal
```

## 📂 Directorio `/src`

```
src/
├── mcp/                    # Servidores MCP
│   ├── main.py             # Punto de entrada principal
│   ├── Makefile            # Comandos y utilidades
│   ├── servers/            # Implementaciones específicas
│   │   └── db/             # Servidores para bases de datos
│   ├── tests/              # Pruebas específicas de MCP
│   └── common/             # Código compartido entre servidores
├── utils/                  # Utilidades generales
├── config/                 # Configuraciones y gestión de entorno
└── api/                    # APIs y servicios web
```

## 📂 Directorio `/docs`

```
docs/
├── README.md               # Índice de documentación
├── api/                    # Documentación de APIs
├── guias/                  # Guías de usuario y tutoriales
│   └── ide/                # Guías de configuración de IDEs
├── desarrollo/             # Guías de desarrollo
│   └── estructura-proyecto.md  # Este documento
├── analisis/               # Documentación de análisis
│   └── comparativos/       # Análisis comparativos
└── mcp/                    # Documentación de servidores MCP
    ├── README.md           # Índice de documentación MCP
    └── filesystem/         # Docs del servidor filesystem
```

## 📂 Directorio `/tests`

```
tests/
├── README.md               # Documentación de pruebas
├── conftest.py             # Configuración compartida
├── pytest.ini              # Configuración de pytest
├── run_tests.py            # Script para ejecutar tests
├── unit/                   # Pruebas unitarias
└── integration/            # Pruebas de integración
```

## 📂 Configuraciones de IDEs

```
.cursor/
├── settings.json           # Configuración de Cursor
└── rules/                  # Reglas y guías
    ├── github-cli.mdc      # Guía de GitHub CLI
    ├── seguridad.mdc       # Reglas de seguridad
    └── documentacion.mdc   # Guías de documentación

.vscode/
└── settings.json           # Configuración de VS Code

.windsurf/
└── config.json             # Configuración de Windsurf
```

## 🔗 Enlaces a Documentación Relacionada

- [Configuración de Servidores MCP](/docs/mcp/configuracion.md) - Guía de configuración
- [Convenciones de Código](/docs/desarrollo/convenciones.md) - Estándares de codificación
- [Guía de Pruebas](/tests/README.md) - Documentación de pruebas

---

_Última actualización: [Fecha Actual]_
