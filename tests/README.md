# 🧪 Guía de Tests

Este directorio contiene todas las pruebas automatizadas del proyecto. **IMPORTANTE: Los tests deben colocarse exclusivamente en este directorio, nunca en `/src`.**

## 🚀 Ejecución de Pruebas

```bash
# Todas las pruebas
python tests/run_tests.py

# Solo pruebas unitarias
python tests/run_tests.py --unit

# Solo pruebas de integración
python tests/run_tests.py --integration

# Con salida detallada
python tests/run_tests.py --verbose

# Con análisis de cobertura
pytest --cov=src/mcp tests/
```

## 📋 Tipos de Pruebas

### Unitarias (`unit/`)
- `test_filesystem_server.py`: Pruebas del servidor filesystem
- `test_operaciones_basicas.py`: Operaciones matemáticas fundamentales
- `test_operaciones_avanzadas.py`: Operaciones matemáticas complejas

### Integración (`integration/`)
- `test_filesystem_integration.py`: Integración de filesystem con clientes
- `test_recursos.py`: Pruebas de recursos básicos del servidor
- `test_recursos_ampliados.py`: Funcionalidades avanzadas de recursos

## 📊 Métricas de Cobertura

Se espera mantener una cobertura de código mayor al 80% para todas las funcionalidades esenciales.
Verificamos la cobertura durante el proceso de integración continua.

## ⚠️ Reglas Importantes

1. Todos los tests deben estar ubicados en la carpeta `/tests` (nunca en `/src`)
2. Los nombres de archivos deben seguir el formato `test_*.py`
3. Los tests deben ser independientes entre sí
4. Cada test debe seguir el patrón AAA (Arrange-Act-Assert)

Consulta nuestra documentación detallada sobre tests:

- [Guía Completa de Tests](./GUIA_TESTS.md) - Convenciones y mejores prácticas
- [Regla @mejores_practicas-tests-cursor-rules](../.cursor/rules/mejores_practicas-tests-cursor-rules.md) - Regla oficial del proyecto

## 🔗 Documentación Relacionada

- [Servidor MCP Filesystem](/docs/mcp/filesystem/README.md)
- [Estructura del Proyecto](/docs/desarrollo/estructura-proyecto.md)

---

_Última actualización: [Fecha Actual] - [hora]_
