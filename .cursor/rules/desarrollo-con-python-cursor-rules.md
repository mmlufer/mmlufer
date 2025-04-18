---
description: "Mejores practicas para el desarrollo con Python, incluyendo estructura de proyecto y patrones de implementación."
globs: 
alwaysApply: false
---
---
name: desarrollo-con-python
description: "Mejores prácticas para el desarrollo con Python, incluyendo estructura de proyecto y patrones de implementación."
globs: ["**/*.py", "**/requirements.txt"]
---

## Estructura de Proyecto
- Organizar el código en módulos y paquetes lógicos
- Mantener una estructura de directorios clara y consistente
- Separar código de pruebas, configuración y documentación

## Estilo y Convenciones
- Seguir la guía de estilo PEP 8 para consistencia del código
- Utilizar nombres descriptivos para variables, funciones y clases
- Mantener la longitud de línea dentro de los límites recomendados (79-88 caracteres)
- Aplicar sangría consistente (4 espacios por nivel)

## Tipado y Documentación
- Implementar anotaciones de tipo para mejor legibilidad y mantenimiento
- Documentar todas las funciones y clases con docstrings informativos
- Mantener comentarios actualizados y relevantes
- Generar documentación automática cuando sea posible

## Gestión de Dependencias
- Utilizar entornos virtuales para aislar dependencias
- Mantener un archivo requirements.txt o pyproject.toml actualizado
- Especificar versiones exactas o rangos seguros de dependencias
- Minimizar el número de dependencias externas

## Buenas Prácticas de Código
- Implementar manejo adecuado de errores con bloques try-except
- Utilizar list/dict comprehensions para código conciso
- Aplicar la sentencia `with` para gestión adecuada de recursos
- Preferir código explícito sobre soluciones implícitas
- Evitar efectos secundarios en funciones

## Testing
- Escribir pruebas unitarias para funciones y clases
- Implementar pruebas de integración para flujos completos
- Mantener cobertura de código alta (>80%)
- Automatizar pruebas en el flujo de trabajo

## Seguridad
- Validar todas las entradas de usuario
- No incluir secretos o contraseñas en el código fuente
- Utilizar variables de entorno para configuraciones sensibles
- Aplicar principios de menor privilegio

## Rendimiento
- Perfilar el código para identificar cuellos de botella
- Optimizar partes críticas del código
- Preferir operaciones vectorizadas cuando sea posible
- Considerar la concurrencia o paralelismo para tareas intensivas