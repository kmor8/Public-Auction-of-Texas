import pandas as pd


# Función para mostrar los lot numbers que tienen solo "master" en su value
def limpiar_master(lot_numbers_dict):
    return {lot: sources for lot, sources in lot_numbers_dict.items() if sources == ['master']}

# Función para mostrar los lot numbers que tienen solo "post" en su value
def limpiar_post(lot_numbers_dict):
    return {lot: sources for lot, sources in lot_numbers_dict.items() if sources == ['post']}

# Leer el archivo Excel del master y del post
df_master = pd.read_excel('Original//master.xlsx')
df_post = pd.read_excel('Original//post.xlsx')

# Crear un diccionario para almacenar los lot numbers y su origen
lot_numbers_dict = {}

# Procesar el archivo master
for lot in df_master['Lot Number']:
    lot = int(lot)
    lot_numbers_dict[lot] = ['master']

# Procesar el archivo post
for lot in df_post['Lot Number']:
    lot = int(lot)
    if lot in lot_numbers_dict:
        lot_numbers_dict[lot].append('post')
    else:
        lot_numbers_dict[lot] = ['post']


# Llamar a la función
solo_master =limpiar_master(lot_numbers_dict)
solo_post = limpiar_post(lot_numbers_dict)
# Eliminar filas en df_master que tienen lot numbers en solo_master_lots
df_master_cleaned = df_master[~df_master['Lot Number'].isin(solo_master)]
df_post_cleaned = df_post[~df_post['Lot Number'].isin(solo_post)]
# Guardar el DataFrame limpio en un nuevo archivo Excel
df_master_cleaned.to_excel('Limpio//master_limpio.xlsx', index=False)
df_post_cleaned.to_excel('Limpio//post_limpio.xlsx', index=False)

print("REPORTE MASTER")
print(f'Número de lotes eliminados: {len(solo_master)}')
print(f'Número de filas restantes en master limpio: {len(df_master_cleaned)}')


print("\nREPORTE POST")
print(f'Número de lotes eliminados: {len(solo_post)}')
print(f'Número de filas restantes en master limpio: {len(df_post_cleaned)}')


