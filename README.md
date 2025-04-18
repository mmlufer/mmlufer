# 🚀 Mi Ambiente Personal de Experimentación con IA e IDEs

Este repositorio sirve como mi espacio personal para exploración de código y experimentación con Inteligencia Artificial. Aquí puedo probar nuevas ideas, tecnologías y conceptos de manera segura y organizada.

## 🛠️ Configuración

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
```bash
PORT=3000
GITHUB_PERSONAL_ACCESS_TOKEN=tu_token_aquí
```

⚠️ **IMPORTANTE**: Nunca commits el archivo `.env` al repositorio. Está incluido en `.gitignore` por seguridad.

### Estructura del Proyecto
```
.
├── .env                    # Variables de entorno (no commitear)
├── .gitignore             # Archivos ignorados por git
├── mmlufer.code-workspace # Configuración compartida entre IDEs
├── .cursor/               # Configuraciones específicas de Cursor
│   ├── settings.json      # Ajustes específicos de Cursor
│   └── rules/             # Reglas y guías de Cursor
│       ├── github-cli.mdc # Guía de GitHub CLI
│       ├── seguridad.mdc  # Reglas de seguridad
│       └── documentacion.mdc # Guías de documentación
├── .vscode/               # Configuraciones específicas de VS Code
│   └── settings.json      # Ajustes específicos de VS Code
├── .windsurf/             # Configuraciones específicas de Windsurf
│   └── config.json        # Ajustes específicos de Windsurf
└── README.md              # Esta documentación
```

## 🔧 Configuración de IDEs

### Configuración Centralizada
El archivo `mmlufer.code-workspace` actúa como punto central de configuración:
- Configuraciones compartidas del editor
- Exclusiones de archivos
- Configuración de terminal
- Integración con Git
- Extensiones recomendadas
- Configuraciones específicas para cada IDE

### VS Code
- Formateo automático al guardar
- Reglas de estilo consistentes
- Exclusión de archivos innecesarios
- Configuraciones optimizadas para desarrollo

### Cursor
- Configuración optimizada para IA
- Autocompletado inteligente
- Análisis de código en tiempo real
- Integración con terminales según SO

### Windsurf
- Tema oscuro optimizado
- Fuente JetBrains Mono para mejor legibilidad
- Integración avanzada con Git
- Depuración mejorada con valores inline
- Terminal integrada personalizada
- Exclusión inteligente de archivos

### Configuraciones Específicas
Cada IDE mantiene sus configuraciones específicas en su propio directorio:
- `.vscode/settings.json`: Configuraciones exclusivas de VS Code
- `.cursor/settings.json`: Configuraciones exclusivas de Cursor
- `.windsurf/config.json`: Configuraciones exclusivas de Windsurf

Las configuraciones personales específicas están excluidas en `.gitignore`.

## 🔒 Seguridad

- Los tokens y secretos se manejan exclusivamente a través de variables de entorno
- El archivo `.env` está incluido en `.gitignore`
- Se siguen las mejores prácticas de seguridad para el manejo de tokens y secretos
- Se recomienda usar tokens con permisos mínimos necesarios

## 🌟 Características

- Ambiente aislado para experimentación
- Configuración segura para tokens y secretos
- Estructura flexible para diferentes tipos de proyectos
- Integración con GitHub
- Configuraciones optimizadas para múltiples IDEs
- Separación clara entre configuraciones compartidas y personales

## 📝 Notas de Uso

1. Clona este repositorio
2. Crea tu archivo `.env` con las variables necesarias
3. Las configuraciones de los IDEs se cargarán automáticamente
4. ¡Comienza a experimentar!

## 🤝 Contribución

Este es un repositorio personal de experimentación, pero siéntete libre de:
- Crear forks para tus propios experimentos
- Sugerir mejoras en la estructura
- Compartir ideas para nuevos experimentos
- Proponer mejoras en las configuraciones de IDEs

## 📚 Documentación

### Reglas y Guías de Cursor
Las reglas y guías se encuentran en `.cursor/rules/`:
- [Guía de GitHub CLI](.cursor/rules/github-cli.mdc): Comandos, flujos de trabajo y mejores prácticas para gestionar el repositorio con GitHub CLI.
- [Reglas de Seguridad](.cursor/rules/seguridad.mdc): Guías de seguridad para el desarrollo.
- [Guías de Documentación](.cursor/rules/documentacion.mdc): Estándares y mejores prácticas de documentación.
