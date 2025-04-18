---
description: Reglas y guías de seguridad para el desarrollo con MCP de GitHub, enfocadas en el manejo seguro de tokens, secretos y buenas prácticas de desarrollo. Incluye checklist de seguridad, ejemplos de configuración y guías para el manejo de variables de entorno.
globs: 
alwaysApply: false
---

# Reglas de Seguridad para Desarrollo

## Manejo de Tokens y Secretos

1. **Archivos de Entorno**
   - Usar siempre `.env` para almacenar tokens y secretos
   - Nunca incluir tokens en archivos de configuración o código
   - Asegurar que `.env` esté en `.gitignore`
   - Usar variables de entorno con `${env:VARIABLE}` en configuraciones

2. **Tokens de GitHub**
   - Usar tokens con el mínimo de permisos necesarios
   - Rotar tokens regularmente
   - Nunca compartir tokens en mensajes o commits
   - Usar tokens específicos para cada entorno (dev, prod, etc.)

3. **Archivos de Configuración**
   - Usar referencias a variables de entorno en lugar de valores directos
   - Validar la presencia de variables de entorno requeridas
   - Documentar las variables de entorno necesarias en README.md

## Desarrollo Seguro

1. **Control de Versiones**
   - Nunca incluir archivos sensibles en commits
   - Usar `.gitignore` para excluir archivos sensibles
   - Revisar cambios antes de commitear
   - Usar hooks de pre-commit para validar seguridad

2. **Documentación**
   - Documentar todos los secretos y tokens necesarios
   - Incluir instrucciones de seguridad en README.md
   - Mantener actualizada la documentación de seguridad

3. **Buenas Prácticas**
   - Usar MFA cuando esté disponible
   - Mantener dependencias actualizadas
   - Revisar logs y auditorías regularmente
   - Seguir el principio de mínimo privilegio

## Ejemplos de Configuración Segura

```json
// Ejemplo de configuración segura en mcp.json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

```bash
# Ejemplo de .gitignore para seguridad
.env
.env.*
*.secret
*.key
*.pem
credentials.json
```

## Checklist de Seguridad

- [ ] Verificar que `.env` está en `.gitignore`
- [ ] Usar variables de entorno para todos los secretos
- [ ] Documentar variables de entorno requeridas
- [ ] Revisar permisos de tokens regularmente
- [ ] Mantener dependencias actualizadas
- [ ] Seguir el principio de mínimo privilegio 