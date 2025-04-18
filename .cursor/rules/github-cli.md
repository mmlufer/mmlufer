---
description: Gestión del Repositorio con GitHub
globs: 
alwaysApply: false
---
# Reglas para Gestión del Repositorio con GitHub CLI

## Configuración Inicial

1. **Instalación de GitHub CLI**
   ```bash
   # Windows (con winget)
   winget install GitHub.cli

   # Windows (con scoop)
   scoop install gh

   # macOS
   brew install gh

   # Linux
   sudo apt install gh  # Ubuntu/Debian
   ```

2. **Autenticación**
   ```bash
   gh auth login
   ```
   Seleccionar:
   - GitHub.com
   - HTTPS
   - Authenticate with web browser

## Comandos Esenciales

### Gestión del Repositorio

1. **Crear Repositorio**
   ```bash
   gh repo create mmlufer --private --clone
   ```

2. **Clonar Repositorio**
   ```bash
   gh repo clone usuario/mmlufer
   ```

3. **Ver Estado**
   ```bash
   gh repo view
   gh repo view --web  # Abrir en navegador
   ```

### Issues y PRs

1. **Gestión de Issues**
   ```bash
   gh issue create --title "título" --body "descripción"
   gh issue list
   gh issue view número
   gh issue close número
   ```

2. **Pull Requests**
   ```bash
   gh pr create --title "título" --body "descripción"
   gh pr list
   gh pr checkout número
   gh pr review número --approve
   ```

### Flujo de Trabajo

1. **Crear Nueva Feature**
   ```bash
   # Crear rama y issue
   gh issue create --title "Nueva feature" --body "Descripción"
   gh issue develop [número] --name feature/nombre

   # Trabajar en los cambios...

   # Crear PR
   gh pr create --title "Feature: nombre" --body "Descripción"
   ```

2. **Revisar Cambios**
   ```bash
   gh pr list
   gh pr checkout número
   gh pr review número --comment "Comentarios"
   ```

3. **Merge de Cambios**
   ```bash
   gh pr merge número --squash
   ```

## Aliases Recomendados

Configurar aliases para comandos frecuentes:
```bash
gh alias set co 'pr checkout'
gh alias set rv 'pr review'
gh alias set prc 'pr create --title "$1" --body "$2"'
gh alias set is 'issue create --title "$1" --body "$2"'
```

## Mejores Prácticas

1. **Commits y Mensajes**
   - Usar commits atómicos
   - Seguir convención de mensajes:
     ```
     tipo(alcance): mensaje

     [cuerpo]

     [pie]
     ```
   - Tipos: feat, fix, docs, style, refactor, test, chore

2. **Branches**
   - Formato: `tipo/descripción`
   - Tipos comunes:
     - feature/
     - bugfix/
     - hotfix/
     - docs/
     - refactor/

3. **Pull Requests**
   - Incluir descripción clara
   - Referenciar issues relacionados
   - Agregar etiquetas apropiadas
   - Solicitar revisores relevantes

4. **Issues**
   - Usar plantillas cuando estén disponibles
   - Incluir pasos de reproducción para bugs
   - Agregar etiquetas relevantes
   - Asignar a responsables

## Automatizaciones

1. **Workflows Comunes**
   ```bash
   # Crear feature con issue y branch
   gh workflow feature "Título" "Descripción"

   # Revisar y mergear PR
   gh workflow review número
   ```

2. **Scripts Útiles**
   ```bash
   # Crear alias para workflow
   gh alias set wf 'workflow run'
   ```

## Seguridad

1. **Tokens y Autenticación**
   - Usar autenticación con navegador por defecto
   - Para CI/CD, usar tokens con alcance mínimo necesario
   - Rotar tokens regularmente

2. **Permisos**
   - Revisar permisos de colaboradores regularmente
   - Usar roles con mínimo privilegio necesario
   - Configurar branch protection rules

## Checklist de Configuración

- [ ] GitHub CLI instalado y actualizado
- [ ] Autenticación configurada
- [ ] Aliases configurados
- [ ] Plantillas de PR e Issues configuradas
- [ ] Branch protection rules establecidas
- [ ] Workflows configurados
- [ ] Permisos revisados
