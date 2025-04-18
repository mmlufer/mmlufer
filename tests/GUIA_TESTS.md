# 📘 Guía para Organización de Tests

Esta guía establece las convenciones a seguir para la organización y escritura de tests en el proyecto.

## 📁 Estructura de Directorios

```
/tests/                        # Directorio raíz para TODOS los tests
│
├── unit/                     # Tests unitarios
│   ├── test_module1.py
│   └── test_module2.py
│
├── integration/              # Tests de integración
│   ├── test_feature1.py
│   └── test_feature2.py
│
├── conftest.py               # Fixtures compartidas entre tests
├── run_tests.py              # Herramienta para ejecutar tests
└── pytest.ini                # Configuración de pytest
```

## ⚠️ Reglas Importantes

### 1. Ubicación de Tests

- ✅ **CORRECTO**: Todos los tests deben ubicarse EXCLUSIVAMENTE dentro del directorio `/tests`
- ❌ **INCORRECTO**: NO crear tests dentro de `/src` o sus subdirectorios

```
# ✅ CORRECTO
/tests/unit/test_filesystem.py

# ❌ INCORRECTO
/src/mcp/servers/filesystem/tests/test_filesystem.py
/src/mcp/servers/filesystem/test_filesystem.py
```

### 2. Nomenclatura

- Los archivos de tests deben nombrarse con el prefijo `test_`
- Las funciones de test deben seguir el patrón `test_[función]_[escenario]_[resultado_esperado]`

```python
# ✅ CORRECTO
def test_read_file_nonexistent_raises_error():
    ...

# ❌ INCORRECTO
def verify_read_file():
    ...
```

## 🧪 Tipos de Tests

### Tests Unitarios (`/tests/unit/`)

- Prueban unidades individuales de código (funciones, métodos)
- No tienen dependencias externas (usan mocks/stubs)
- Rápidos de ejecutar
- Usar marcador `@pytest.mark.unit`

### Tests de Integración (`/tests/integration/`)

- Prueban interacciones entre componentes
- Pueden utilizar recursos externos controlados
- Requieren más configuración
- Usar marcador `@pytest.mark.integration`

## 🔄 Estructura AAA

Todos los tests deben seguir la estructura Arrange-Act-Assert:

```python
def test_example():
    # Arrange - Preparar el entorno y datos
    server = FilesystemServer(['/ruta/permitida'])
    test_file = '/ruta/permitida/archivo.txt'

    # Act - Ejecutar la acción a probar
    result = server.read_file(test_file)

    # Assert - Verificar el resultado
    assert result == 'contenido esperado'
```

## 🛠️ Fixtures y Configuración

- Usar `conftest.py` para definir fixtures compartidas entre tests
- Preferir fixtures de pytest sobre setUp/tearDown
- Especificar el alcance de las fixtures:
  - `@pytest.fixture`: por defecto, se ejecuta para cada test
  - `@pytest.fixture(scope="module")`: se ejecuta una vez por módulo
  - `@pytest.fixture(scope="session")`: se ejecuta una vez por sesión

## 📋 Checklist de Calidad

Asegúrese de que todos los tests:

- [ ] Están ubicados correctamente en el directorio `/tests`
- [ ] Siguen la convención de nomenclatura adecuada
- [ ] Son independientes entre sí
- [ ] Incluyen casos normales, casos de error y casos límite
- [ ] No contienen secretos o credenciales
- [ ] Son deterministas (siempre dan el mismo resultado para los mismos inputs)
- [ ] Se limpian después de su ejecución

## 🔍 Buenas Prácticas Adicionales

1. **Parametrización**: Usar `@pytest.mark.parametrize` para probar múltiples casos
2. **Mocks**: Aislar el código de sus dependencias
3. **Categorización**: Usar marcadores para organizar tests por tipo o velocidad
4. **Claridad**: Preferir claridad sobre brevedad en el código de test

## 📊 Cobertura

La meta es mantener una cobertura de código superior al 80%, con énfasis en cubrir:
- Todos los caminos de ejecución
- Todas las ramas condicionales
- Todos los bloques de manejo de errores

Para verificar la cobertura:

```bash
pytest --cov=src/mcp tests/
```

---

Consulte también la regla `@mejores_practicas-tests-cursor-rules` para más detalles.
