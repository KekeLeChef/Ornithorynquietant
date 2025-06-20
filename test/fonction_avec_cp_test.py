import pandas as pd
import numpy as np
from scipy.spatial import cKDTree


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

# Construire un KDTree pour faire correspondre les points les plus proches
capacity_coords = np.array(list(zip(capacity_parsed['latitude'], capacity_parsed['longitude'])))
capacity_values = capacity_parsed['heat_capacity'].values
tree = cKDTree(capacity_coords)

# Créer la grille vide
capacity_grid = np.full((len(latitudes), len(longitudes)), np.nan)

# Remplissage intelligent : valeur la plus proche dans la grille
for i, lat in enumerate(latitudes):
    for j, lon in enumerate(longitudes):
        dist, idx = tree.query([lat, lon], k=1)
        if dist < 5:  # tolérance de distance en degrés (ajustable)
            capacity_grid[i, j] = capacity_values[idx]
        else:
            capacity_grid[i, j] = None

# Stockage dans la liste comme pour l'albédo
list_capacity = [capacity_grid]

# Facultatif : affichage test
print("Grille de capacité thermique alignée avec les grilles d'albédo :")
print(capacity_grid)
var=None
for i in range(len(capacity_grid)):
    for j in range(len(capacity_grid[0])):
        if capacity_grid[i][j]=="nan":
            var=True


def get_Cp(x, y, z, phi, theta, list_Cp , latitudes, longitudes):

    Cp_grid_mapped = np.zeros_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            lon, lat = np.degrees(phi[i, j]), 90 - np.degrees(theta[i, j])
            if lon > 180:
                lon -= 360
            lat_idx = (np.abs(latitudes - lat)).argmin()
            lon_idx = (np.abs(longitudes - lon)).argmin()
            Cp_grid_mapped[i, j] = [lat_idx,lon_idx]

    return Cp_grip_mapped





