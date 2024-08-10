
# Importar librerías necesarias
import os
import glob
import pandas as pd
import numpy as np

def buscar_duplicados_entre_archivos(carpeta):
    archivos_csv = glob.glob(f"{carpeta}/*.csv")
    problemas = []
    duplicados = {}
    lot_numbers = []  # Lista para almacenar todos los lot numbers
    i = 1

    for archivo in archivos_csv:
        i += 1
        try:
            df = pd.read_csv(archivo)
            if 'Lot Number' in df.columns:
                for indice, fila in df.iterrows():
                    lot_number = fila['Lot Number']
                    if pd.notna(lot_number) and not isinstance(lot_number, str):
                        lot_number = str(int(lot_number))
                    elif pd.isna(lot_number) or lot_number == "":
                        problemas.append((archivo, indice, "Lot number faltante o vacío"))
                        continue

                    if lot_number in duplicados:
                        duplicados[lot_number].append((archivo, indice))
                    else:
                        duplicados[lot_number] = [(archivo, indice)]
                    
                    lot_numbers.append(lot_number)  # Añadir a la lista de lot numbers
            else:
                print(f"Advertencia: El archivo {archivo} no contiene la columna 'Lot Number'.")
        except Exception as e:
            print(f"Error al leer el archivo {archivo}: {e}")

    return duplicados, problemas, lot_numbers

def unirCSVs(carpeta, nombre_archivo_final):
    # Construir la ruta completa para buscar archivos CSV
    ruta_busqueda = os.path.join(carpeta, "*.csv")

    # Encontrar todos los archivos CSV en la carpeta
    archivos_csv = glob.glob(ruta_busqueda)

    # Comprobar si se encontraron archivos CSV
    if not archivos_csv:
        print("No se encontraron archivos CSV en la carpeta.")
        return

    # Leer el primer archivo completamente
    df_final = pd.read_csv(archivos_csv[0])

    # Leer y unir el resto de los archivos
    for archivo in archivos_csv[1:]:
        df = pd.read_csv(archivo)
        df_final = pd.concat([df_final, df], ignore_index=True)

    # Guardar el archivo final en formato CSV
    df_final.to_csv(nombre_archivo_final, index=False)
    print(f"Archivo final '{nombre_archivo_final}' creado con éxito.")

# Uso de la función
carpeta = "C:\\Users\\kamil\\Dropbox\\PC\\Desktop\\Trabajo\\Code\\Public-Auction-of-Texas\\Error Validation\\Datos"
duplicados, problemas, lot_numbers = buscar_duplicados_entre_archivos(carpeta)

# Imprimir duplicados y problemas
# ... (Código para imprimir duplicados y problemas) ...

# Estadísticas y detección de números atípicos
# Convertir lot numbers a números y filtrar los no numéricos
lot_numbers_numericos = [int(x) for x in lot_numbers if x.isdigit()]

# Calcular la media y la desviación estándar
media = np.mean(lot_numbers_numericos)
desviacion_estandar = np.std(lot_numbers_numericos)

# Definir umbral para considerar un número como atípico
umbral = 2  # Por ejemplo, números que están a más de 2 desviaciones estándar de la media

# Encontrar números atípicos
numeros_atipicos = [x for x in lot_numbers_numericos if abs(x - media) > umbral * desviacion_estandar]


if numeros_atipicos:
    print("\nNúmeros de lote atípicos:")
    for numero in numeros_atipicos:
        print("\nLot number:", numero)
        # Obtener los detalles asociados al número atípico del diccionario 'duplicados'
        detalles = duplicados.get(str(numero))
        if detalles:
            for archivo, fila in detalles:
                # Formatear y mostrar cada detalle
                print(f" - Archivo: {archivo}, Fila: {fila}")
else:
    print("\nNo se encontraron ids extraños.")


if duplicados:
    bandera = False
    for lot_number, details in duplicados.items():
        if len(details) > 1:  # Verifica si el lote está duplicado
            print("\nDuplicados encontrados:\n")
            bandera=True
            print(f"Lot number {lot_number} duplicado en:")
            for archivo, fila in details:
                print(f" - Archivo: {archivo}, Fila: {fila}")
    if not bandera:
        print("\nNo se encontraron duplicados")

       

if problemas:
    print("\nProblemas encontrados:")
    for archivo, indice, mensaje in problemas:
        print(f"\nArchivo: {archivo}, Fila: {indice}, Problema: {mensaje}")
else:
    print("\nNo se encontraron problemas.\n")



# Preguntar al usuario si desea proceder
respuesta = input("¿Proseguir con la unión? (s/n): ").strip().lower()
if respuesta == 's':
    unirCSVs(carpeta, "archivo_final.csv")
else:
    print("Unión cancelada.")



