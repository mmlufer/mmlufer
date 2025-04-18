---
> Prioridad: Media
> Tiempo Estimado: 1 hora
> Dependencias: Ninguna
---
# T001 - Consolidar Archivos Extensionistas

## 1. Resumen
Tarea para automatizar la búsqueda y consolidación de archivos específicos (imágenes y PDFs con palabras clave en el nombre) desde una estructura de carpetas de extensionistas y usuarios hacia una carpeta de destino organizada por extensionista.

### 2. Objetivos Específicos
- Solicitar al usuario la ruta de origen (conteniendo carpetas de extensionistas) y la ruta de destino.
- Identificar carpetas de extensionistas en la ruta origen.
- Para cada extensionista:
    - Proponer un nombre para la carpeta consolidada (ej: `CONSOLIDADO_NOMBRE APELLIDO`) basado en las dos primeras palabras del nombre de su carpeta origen y solicitar confirmación del usuario.
    - Crear la carpeta consolidada en la ruta de destino.
    - Buscar recursivamente dentro de la carpeta del extensionista, en las subcarpetas de usuarios (identificadas por iniciar con número de cédula).
    - Identificar archivos de imagen (cualquier formato común) y archivos PDF.
    - Filtrar aquellos cuyo nombre (ignorando mayúsculas/minúsculas y extensión) contenga "ippta", "planeador", "entregable" o "formato".
    - Copiar los archivos identificados a la carpeta consolidada del extensionista.
    - Gestionar colisiones de nombres de archivo añadiendo un sufijo numérico (ej: `archivo_1.pdf`, `archivo_2.pdf`).
    - Generar un archivo `lista_archivos.txt` dentro de cada carpeta consolidada, con los nombres de los archivos copiados ordenados alfabéticamente.

### 3. Criterios de Éxito Clave
- [ ] El script solicita correctamente las rutas de origen y destino.
- [ ] El script identifica correctamente las carpetas de los extensionistas.
- [ ] El script propone y confirma correctamente los nombres de las carpetas consolidadas.
- [ ] Se crean las carpetas `CONSOLIDADO_...` en el destino.
- [ ] Se buscan archivos recursivamente en las carpetas de usuarios.
- [ ] Se identifican y filtran correctamente imágenes y PDFs según las palabras clave.
- [ ] Los archivos filtrados se copian a la carpeta consolidada correcta.
- [ ] Las colisiones de nombres se manejan añadiendo sufijos numéricos.
- [ ] Se genera un archivo `lista_archivos.txt` en cada carpeta consolidada.
- [ ] El archivo `lista_archivos.txt` contiene los nombres correctos ordenados alfabéticamente.
- [ ] Los archivos originales no son modificados.

## 4. Contexto Breve
Se necesita consolidar evidencia documental (imágenes y PDFs específicos) generada por extensionistas durante visitas a usuarios. La estructura actual está dispersa por extensionista y usuario, dificultando el acceso rápido a ciertos tipos de documentos (IPPTA, Planeadores, etc.). Esta tarea centraliza estos archivos clave por extensionista para facilitar su revisión y gestión.

## Pasos Principales (Enfocados en el IDE/IA)
1.  **Ejecutar el script:** Navegar al directorio `src/scripts` y ejecutar `python "T001 - Consolidar Archivos Extensionistas.py"`.
2.  **Proporcionar Rutas:** Ingresar la ruta de la carpeta que contiene los directorios de los extensionistas cuando el script lo solicite.
3.  **Proporcionar Destino:** Ingresar la ruta donde se crearán las carpetas `CONSOLIDADO_...`.
4.  **Confirmar Nombres:** Confirmar o modificar los nombres propuestos para las carpetas `CONSOLIDADO_...` para cada extensionista.
5.  **Verificar Resultados:** Una vez finalizado el script, revisar las carpetas `CONSOLIDADO_...` creadas en la ruta de destino, verificar los archivos copiados y el contenido de `lista_archivos.txt`.

## 5. Fase de Ejecución: Realización de la Tarea
(Completar solo en la etapa de ejecución de la tarea)

### Orientaciones para la implementacion de la tarea

- La realizacion de la tarea debe hacerce con python.
- La tarea tiene **un script principal y único** ubicado en `src/scripts/` llamado `T001 - Consolidar Archivos Extensionistas.py`.
- La ejecución de la tarea implica que el usuario interactúe con el script via línea de comandos para proporcionar rutas y confirmar nombres. Los resultados (carpetas consolidadas) se guardarán en la ruta de destino especificada por el usuario.
- El seguimiento de la documentacion de la tarea se realizará en este mismo documento.

### Changelog Tarea
- [Fecha]: Creación inicial de la tarea y script.

### Referencias
- Ninguna por el momento.

### Ubicación de los Productos
- La ruta será definida por el usuario durante la ejecución del script.

### Verificación
- [ ] Verificar manualmente una muestra de carpetas `CONSOLIDADO_...` para asegurar que contienen los archivos correctos.
- [ ] Verificar el contenido y orden de algunos `lista_archivos.txt`.
- [ ] Comprobar que los archivos originales no han sido alterados.

### Como reproducir el resultado
- Ejecutar `python src/scripts/"T001 - Consolidar Archivos Extensionistas.py"` y proporcionar las mismas rutas de origen y destino.

### Resultados Finales
- Carpetas `CONSOLIDADO_Nombre Apellido` en la ruta de destino, cada una conteniendo los archivos relevantes copiados y un `lista_archivos.txt`.

---

## Checklist de Documentación (Pre-implementación)

- [X] Título claro y descriptivo
- [X] Objetivos específicos y medibles
- [X] Pasos detallados y secuenciales (para el usuario)
- [ ] Ejemplos de código o configuración (N/A para este doc)
- [X] Comandos y prompts específicos (Comando de ejecución)
- [X] Puntos de verificación (En sección Verificación)
- [X] Referencias y recursos adicionales (Sección existe)
- [ ] Consideraciones de rendimiento o seguridad (N/A por ahora)
- [ ] Problemas conocidos y soluciones (N/A por ahora)
- [X] Criterios de éxito verificables
