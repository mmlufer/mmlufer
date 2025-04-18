import os
import shutil
import re
from pathlib import Path

# Palabras clave para buscar en los nombres de archivo (insensible a mayúsculas/minúsculas)
KEYWORDS = ["ippta", "planeador", "entregable", "formato"]

# Extensiones de imagen comunes (insensible a mayúsculas/minúsculas)
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif']

def es_numero_cedula(nombre_carpeta):
    """Verifica si el nombre de la carpeta parece ser un número de cédula (solo dígitos)."""
    return nombre_carpeta.isdigit()

def obtener_nombre_extensionista(nombre_carpeta_origen):
    """Extrae las dos primeras palabras del nombre de la carpeta para el nombre consolidado."""
    partes = nombre_carpeta_origen.split()
    if len(partes) >= 2:
        return f"{partes[0].upper()} {partes[1].upper()}"
    elif len(partes) == 1:
        return partes[0].upper()
    else:
        return "SIN_NOMBRE" # Caso improbable

def normalizar_nombre_archivo(nombre_archivo):
    """Convierte el nombre a minúsculas y quita la extensión para la búsqueda de palabras clave."""
    nombre_base, _ = os.path.splitext(nombre_archivo)
    return nombre_base.lower()

def archivo_cumple_criterios(nombre_archivo):
    """Verifica si un archivo es imagen o PDF y contiene una palabra clave."""
    nombre_normalizado = normalizar_nombre_archivo(nombre_archivo)
    _, extension = os.path.splitext(nombre_archivo)
    extension = extension.lower()

    es_tipo_valido = extension == '.pdf' or extension in IMAGE_EXTENSIONS
    if not es_tipo_valido:
        return False

    for keyword in KEYWORDS:
        # Usamos \b para asegurar que la palabra clave esté completa (word boundary)
        if re.search(r'\b' + re.escape(keyword) + r'\b', nombre_normalizado):
            return True
    return False


def obtener_ruta_destino_unica(ruta_destino_base, nombre_archivo_original):
    """Genera una ruta de destino única si el archivo ya existe."""
    destino = os.path.join(ruta_destino_base, nombre_archivo_original)
    if not os.path.exists(destino):
        return destino

    nombre_base, extension = os.path.splitext(nombre_archivo_original)
    contador = 1
    while True:
        nuevo_nombre = f"{nombre_base}_{contador}{extension}"
        nuevo_destino = os.path.join(ruta_destino_base, nuevo_nombre)
        if not os.path.exists(nuevo_destino):
            return nuevo_destino
        contador += 1

def procesar_extensionista(ruta_carpeta_extensionista, ruta_destino_general):
    """Procesa la carpeta de un extensionista: busca, copia y genera lista."""
    nombre_carpeta_origen = os.path.basename(ruta_carpeta_extensionista)
    nombre_propuesto = obtener_nombre_extensionista(nombre_carpeta_origen)
    nombre_consolidado_base = f"CONSOLIDADO_{nombre_propuesto}"

    # Confirmar nombre con el usuario
    confirmacion = input(f"Se propone el nombre '{nombre_consolidado_base}' para la carpeta consolidada de '{nombre_carpeta_origen}'. ¿Es correcto? (s/N): ")
    if confirmacion.lower() != 's':
        nuevo_nombre_base = input("Introduce el nombre base para la carpeta consolidada (ej: CONSOLIDADO_NOMBRE APELLIDO): ")
        if not nuevo_nombre_base.strip():
            print("Nombre inválido. Omitiendo este extensionista.")
            return
        nombre_consolidado_final = nuevo_nombre_base
    else:
        nombre_consolidado_final = nombre_consolidado_base

    ruta_destino_extensionista = os.path.join(ruta_destino_general, nombre_consolidado_final)
    print(f"Creando carpeta de destino: {ruta_destino_extensionista}")
    os.makedirs(ruta_destino_extensionista, exist_ok=True)

    archivos_copiados = []

    print(f"Buscando archivos en: {ruta_carpeta_extensionista}")
    # Iterar sobre las carpetas de usuarios (asumiendo que están directamente bajo la del extensionista)
    for item_usuario in os.listdir(ruta_carpeta_extensionista):
        ruta_item_usuario = os.path.join(ruta_carpeta_extensionista, item_usuario)
        # Comprobar si es una carpeta y si su nombre parece un número de cédula
        # Ajuste: buscar recursivamente SIN asumir que las carpetas de usuario están al primer nivel
        # y SIN validar el nombre de la carpeta contenedora (usuario)
        # -> El recorrido recursivo se hace sobre toda la carpeta del extensionista

    for raiz, _, archivos in os.walk(ruta_carpeta_extensionista):
        for nombre_archivo in archivos:
            if archivo_cumple_criterios(nombre_archivo):
                ruta_origen_archivo = os.path.join(raiz, nombre_archivo)
                ruta_destino_archivo = obtener_ruta_destino_unica(ruta_destino_extensionista, nombre_archivo)
                nombre_archivo_destino = os.path.basename(ruta_destino_archivo) # Nombre final (puede tener sufijo)

                try:
                    print(f"  Copiando: {ruta_origen_archivo} -> {ruta_destino_archivo}")
                    shutil.copy2(ruta_origen_archivo, ruta_destino_archivo) # copy2 preserva metadatos
                    archivos_copiados.append(nombre_archivo_destino)
                except Exception as e:
                    print(f"  ERROR al copiar {ruta_origen_archivo}: {e}")

    if archivos_copiados:
        archivos_copiados.sort()
        ruta_lista = os.path.join(ruta_destino_extensionista, "lista_archivos.txt")
        try:
            with open(ruta_lista, 'w', encoding='utf-8') as f:
                for nombre in archivos_copiados:
                    f.write(f"{nombre}\n")
            print(f"Creada lista de archivos: {ruta_lista}")
        except Exception as e:
            print(f"ERROR al crear lista de archivos {ruta_lista}: {e}")
    else:
        print(f"No se encontraron archivos que cumplan los criterios para {nombre_consolidado_final}.")

def main():
    print("--- Consolidador de Archivos de Extensionistas ---")

    while True:
        ruta_origen_base = input("Introduce la ruta de la carpeta que contiene las carpetas de los extensionistas: ")
        if os.path.isdir(ruta_origen_base):
            break
        print("Ruta de origen no válida o no encontrada. Inténtalo de nuevo.")

    while True:
        ruta_destino_general = input("Introduce la ruta donde se crearán las carpetas CONSOLIDADO_*: ")
        # Intentamos crearla por si no existe y para validar permisos
        try:
            os.makedirs(ruta_destino_general, exist_ok=True)
            # Pequeña prueba de escritura para asegurar permisos
            test_file = os.path.join(ruta_destino_general, ".test_write")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            break
        except OSError as e:
             print(f"Ruta de destino no válida o no se tienen permisos de escritura ({e}). Inténtalo de nuevo.")
        except Exception as e:
            print(f"Error inesperado con la ruta de destino: {e}. Inténtalo de nuevo.")


    print("\nIniciando proceso...")

    for nombre_carpeta_extensionista in os.listdir(ruta_origen_base):
        ruta_completa_extensionista = os.path.join(ruta_origen_base, nombre_carpeta_extensionista)
        if os.path.isdir(ruta_completa_extensionista):
            print(f"\nProcesando extensionista: {nombre_carpeta_extensionista}")
            procesar_extensionista(ruta_completa_extensionista, ruta_destino_general)
        else:
            print(f"Omitiendo (no es directorio): {nombre_carpeta_extensionista}")

    print("\n--- Proceso completado ---")

if __name__ == "__main__":
    main()
