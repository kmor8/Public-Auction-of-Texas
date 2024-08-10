import os
import zipfile
import shutil

def descomprimir_y_unir_imagenes(directorio_raiz, directorio_destino):
    # Crear el directorio destino si no existe
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino) 

    # Recorrer todos los archivos en el directorio raíz y subdirectorios
    for raiz, dirs, archivos in os.walk(directorio_raiz):
        for archivo in archivos:
            if archivo.endswith('.zip'):
                ruta_zip = os.path.join(raiz, archivo)
                with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                    # Extraer todos los archivos en un directorio temporal
                    zip_ref.extractall('temp_dir')

                    # Mover las imágenes extraídas al directorio destino
                    for nombre_archivo in os.listdir('temp_dir'):
                        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                            ruta_origen = os.path.join('temp_dir', nombre_archivo)
                            ruta_destino = os.path.join(directorio_destino, nombre_archivo)
                            shutil.move(ruta_origen, ruta_destino)

                    # Limpiar el directorio temporal
                    shutil.rmtree('temp_dir')

# Uso de la función
directorio_raiz = "C:\\Users\\kamil\\Dropbox\\PC\\Desktop\\Trabajo\\Code\\Public-Auction-of-Texas\\Error Validation\\ImagenesO"
directorio_destino = "C:\\Users\\kamil\\Dropbox\\PC\\Desktop\\Trabajo\\Code\\Public-Auction-of-Texas\\Error Validation\\ImagenesD"
descomprimir_y_unir_imagenes(directorio_raiz, directorio_destino)
