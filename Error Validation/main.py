
# Importar librerías necesarias
import os
import glob
import pandas as pd
import numpy as np

dic_pods = {}

def leer_nombres():
    lista_nombres = []
    ruta_archivo="nombres.txt"
    try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    nombre = linea.strip()  # Elimina los espacios en blanco y saltos de línea
                    if nombre:  # Evita agregar líneas vacías
                        lista_nombres.append(nombre)
    except FileNotFoundError:
            print(f"El archivo en la ruta {ruta_archivo} no se encontró.")
    except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
    return lista_nombres

def nombra_pod(carpeta):
    nombres = leer_nombres()
    archivos_csv = glob.glob(f"{carpeta}/*.csv")
    for archivo in archivos_csv:
            nombre_archivo = os.path.basename(archivo) 
            for nombre in nombres:
                if nombre.lower() in nombre_archivo.lower():
                    if 'stack' in nombre_archivo.lower():
                        nombre += ' Stack'
                    if 'flooring' in nombre_archivo.lower():
                        nombre += ' Flooring'
                    if 'tools/hoses' in nombre_archivo.lower():
                        nombre += ' Tools/Hoses'
                dic_pods[nombre_archivo] = nombre
                break  # Deja de buscar en la lista de nombres cuando encuentra una coincidencia

def buscar_duplicados_entre_archivos(carpeta):
    archivos_csv = glob.glob(f"{carpeta}/*.csv")
    problemas = []
    duplicados = {}
    CFI = []
    fill_in_lot = []
    lot_numbers = {}  # Lista para almacenar todos los lot numbers

    for archivo in archivos_csv:
        try:
            df = pd.read_csv(archivo)
            if 'Lot Number' in df.columns and 'Title' in df.columns:
                for indice, fila in df.iterrows():
                    lot_number = fila['Lot Number']
                    if pd.notna(lot_number) and not isinstance(lot_number, str):
                        lot_number = str(int(lot_number))
                    elif pd.isna(lot_number) or lot_number == "":
                        problemas.append((lot_number, "Empty Lot Number"))
                        continue

                    if lot_number in duplicados:
                        duplicados[lot_number].append((archivo, indice))
                    else:
                        duplicados[lot_number] = [(archivo, indice)]
                    
                    # Obtener el nombre de la persona desde dic_pods
                    nombre_persona = dic_pods.get(os.path.basename(archivo))
                    if nombre_persona:
                        if lot_number in lot_numbers:
                            if nombre_persona not in lot_numbers[lot_number]:
                                lot_numbers[lot_number].append(nombre_persona)  # Añadir el nombre a la lista si no está ya
                        else:
                            lot_numbers[lot_number] = [nombre_persona]  # Crear una nueva lista con el primer nombre

                    # Validar la columna Title
                    title = fila.get('Title', '').lower()  # Obtener el valor de la columna Title y convertirlo a minúsculas
                    
                    if 'cfi' in title:
                        CFI.append(lot_number)  # Añadir el archivo y el índice a la lista CFI
                    if 'fill in lot' in title:
                        fill_in_lot.append(lot_number)  # Añadir el archivo y el índice a la lista fill_in_lot
            else:
                print(f"Advertencia: El archivo {archivo} no contiene la columna 'Title' o 'Lot Number'.")
        except Exception as e:
            print(f"Error al leer el archivo {archivo}: {e}")


    return duplicados, problemas, lot_numbers,CFI, fill_in_lot

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
nombra_pod(carpeta)
duplicados, problemas, lot_numbers,CFI,fill_in_lot = buscar_duplicados_entre_archivos(carpeta)

# Estadísticas y detección de números atípicos
# Convertir lot numbers a números y filtrar los no numéricos
lot_numbers_numericos = [int(lot) for lot in lot_numbers.keys() if lot.isdigit()]

# Calcular la media y la desviación estándar
media = np.mean(lot_numbers_numericos)
desviacion_estandar = np.std(lot_numbers_numericos)

# Definir umbral para considerar un número como atípico
umbral = 2  # Por ejemplo, números que están a más de 2 desviaciones estándar de la media

# Encontrar números atípicos
numeros_atipicos = [lot for lot in lot_numbers_numericos if abs(lot - media) > umbral * desviacion_estandar]

if numeros_atipicos:
    print("\nWrong Lot Numbers:")
    for numero in numeros_atipicos:
        nombres = lot_numbers.get(str(numero), [])
            
        if nombres:
                nombre_str = ', '.join(nombres)  # Convertir la lista de nombres a una cadena separada por comas
        else:
                nombre_str = "No name"  # En caso de que no haya nombres

        print(f"- {nombre_str}, Lot number #{numero}, wrong label")
else:
    print("\nNo weird ids")

if duplicados:
    bandera = False
    for lot_number, details in duplicados.items():
        if len(details) > 1:  # Verifica si el lote está duplicado
            bandera=True
            print("\nDuplicates Found:") 
            # Obtener los nombres asociados al número de lote, si existen
            nombres = lot_numbers.get(str(lot_number), [])
            
            if nombres:
                if len(nombres) > 1:
                    nombre_str = ' & '.join(nombres)  # Unir nombres con & si hay más de uno
                else:
                    nombre_str = nombres[0]  # Solo un nombre
            else:
                nombre_str = "Desconocido"  # En caso de que no haya nombres

            print(f"- {nombre_str}, Lot number #{lot_number}, duplicated")
    
    if not bandera:
        print("\nNo duplicates")

if CFI:
    print("\nCFI:")
    for numero in CFI:
            nombres = lot_numbers.get(str(numero), [])
                
            if nombres:
                    nombre_str = ', '.join(nombres)  # Convertir la lista de nombres a una cadena separada por comas
            else:
                    nombre_str = "No name"  # En caso de que no haya nombres

            print(f"- {nombre_str}, Lot number #{numero}")
else:
     print("No CFI")

if fill_in_lot:
    print("\nFill in Lot:")
    for numero in fill_in_lot:
            nombres = lot_numbers.get(str(numero), [])
                
            if nombres:
                    nombre_str = ', '.join(nombres)  # Convertir la lista de nombres a una cadena separada por comas
            else:
                    nombre_str = "No name"  # En caso de que no haya nombres

            print(f"- {nombre_str}, Lot number #{numero}")
else:
     print("No CFI")

if problemas:
    print("\nOther problems:")
    for lot_number,mensaje in problemas:
        nombres = lot_numbers.get(str(numero), [])
            
        if nombres:
                nombre_str = ', '.join(nombres)  # Convertir la lista de nombres a una cadena separada por comas
        else:
                nombre_str = "No name"  # En caso de que no haya nombres

        print(f"- {nombre_str}, {mensaje}")
else:
    print("\nNo weird ids")

# Preguntar al usuario si desea proceder
respuesta = input("\n¿Proseguir con la unión? (s/n): ").strip().lower()
if respuesta == 's':
    unirCSVs(carpeta, "archivo_final.csv")
else:
    print("Unión cancelada.")



