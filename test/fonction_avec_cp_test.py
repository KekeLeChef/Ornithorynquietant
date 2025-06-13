import pandas as pd
import numpy as np



list_albedo = []
for i in range(1, 10):
    # Charger les données d'albédo
    csv_file_path = f'albedo/albedo0{i}.csv'
    albedo_data = pd.read_csv(csv_file_path)
    if i == 1:
        latitudes = albedo_data['Latitude/Longitude'].values
        longitudes = albedo_data.columns[1:].astype(float)
    # Convertir les données CSV en grille d'albédo
    albedo_grid = albedo_data.set_index('Latitude/Longitude').to_numpy()
    list_albedo.append(albedo_grid)
for i in range(10, 13):
    csv_file_path = f'albedo/albedo{i}.csv'
    albedo_data = pd.read_csv(csv_file_path)
    # Convertir les données CSV en grille d'albédo
    albedo_grid = albedo_data.set_index('Latitude/Longitude').to_numpy()
    list_albedo.append(albedo_grid)


# Charger et parser le fichier de capacité thermique
capacity_data = pd.read_csv("1800_Capacity.csv")
capacity_parsed = capacity_data.iloc[:, 0].str.split(';', expand=True)
capacity_parsed.columns = ['latitude', 'longitude', 'heat_capacity']
capacity_parsed['latitude'] = capacity_parsed['latitude'].astype(float)
capacity_parsed['longitude'] = capacity_parsed['longitude'].astype(float)
capacity_parsed['heat_capacity'] = capacity_parsed['heat_capacity'].astype(float)

# Extraire les latitudes/longitudes depuis les fichiers albédo
# Supposons que ceci a déjà été fait dans votre code pour list_albedo :
# latitudes = albedo_data['Latitude/Longitude'].values
# longitudes = albedo_data.columns[1:].astype(float)

# Créer une grille vide pour la capacité thermique
capacity_grid = np.full((len(latitudes), len(longitudes)), np.nan)

# Dictionnaire de correspondance
capacity_dict = {
    (round(lat, 6), round(lon, 6)): val
    for lat, lon, val in zip(capacity_parsed['latitude'], capacity_parsed['longitude'], capacity_parsed['heat_capacity'])
}

# Remplissage de la grille en utilisant les mêmes positions que pour l’albédo
for i, lat in enumerate(latitudes):
    for j, lon in enumerate(longitudes):
        key = (round(lat, 6), round(lon, 6))
        if key in capacity_dict:
            capacity_grid[i, j] = capacity_dict[key]

# Ajouter à une liste comme pour list_albedo
list_capacity = [capacity_grid]