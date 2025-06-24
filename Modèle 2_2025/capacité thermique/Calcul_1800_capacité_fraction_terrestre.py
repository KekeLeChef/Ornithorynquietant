import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Capacités thermiques spécifiques (J/kg·K)
C_WATER = 4184  # eau
C_SOIL = 1000   # sol/roche (valeur moyenne)
C_ICE = 2100    # glace

# Densités (kg/m³)
D_WATER = 1000
D_SOIL = 1600
D_ICE = 917

# Profondeurs moyennes considérées (en mètres)
DEPTH_WATER = 0.05  # 5 cm pour l'eau
DEPTH_SOIL = 0.05
DEPTH_ICE = 0.05

# Aire d'une cellule (283 333 km² en m²)
CELL_AREA_KM2 = 250000 # 250 000 km² par cellule
CELL_AREA_M2 = CELL_AREA_KM2 * 1e6


# Définir les dimensions de la grille
n_lat = 30  # lignes de latitude
n_lon = 60  # colonnes de longitude
total_cells = n_lat * n_lon

# Générer les bords de grille
lat_edges = np.linspace(-90, 90, n_lat + 1)
lon_edges = np.linspace(-180, 180, n_lon + 1)

# Calculer les centroïdes
lat_centers = 0.5 * (lat_edges[:-1] + lat_edges[1:])
lon_centers = 0.5 * (lon_edges[:-1] + lon_edges[1:])

# Créer toutes les combinaisons latitude × longitude
cells = []
for lat in lat_centers:
    for lon in lon_centers:
        cells.append({"latitude": lat, "longitude": lon})

df_cells = pd.DataFrame(cells)

# Charger les fractions depuis le CSV
fractions_df = pd.read_csv("grid_1800_land_water_ice.csv")
# print(fractions_df.head())
print(fractions_df.columns)
# Fusionner les fractions avec les cellules sur latitude et longitude
df_cells = df_cells.merge(fractions_df, on=["latitude", "longitude"], how="left")
print(df_cells.head())

cp_list = []

for i in df_cells.index:
    water_frac = df_cells.at[i, "water_frac"] / 100  # Convertir en fraction
    soil_frac = df_cells.at[i, "soil_frac"] / 100  # Convertir en fraction
    ice_frac = df_cells.at[i, "ice_frac"] / 100  # Convertir en fraction

    mass_water = D_WATER * CELL_AREA_M2 * DEPTH_WATER * water_frac
    mass_soil = D_SOIL * CELL_AREA_M2 * DEPTH_SOIL * soil_frac
    mass_ice = D_ICE * CELL_AREA_M2 * DEPTH_ICE * ice_frac

    heat_capacity = (mass_water * C_WATER + mass_soil * C_SOIL + mass_ice * C_ICE)
    # print(heat_capacity)
    # print(f"Cellule {i}: Eau={water_frac:.2f}, Sol={soil_frac:.2f}, Glace={ice_frac:.2f}, Capacité={heat_capacity:.2e} J/K")
    cp_list.append(heat_capacity)

print("Fichier 'capacites_thermiques_1800_final.csv' créé avec les colonnes latitude, longitude et cp.")


# Ajouter la colonne capacité thermique au DataFrame
df_cells["capacité thermique"] = cp_list

# Sauvegarder le fichier CSV
df_cells[["latitude", "longitude", "capacité thermique"]].to_csv("capacites_thermiques_1800_final.csv", index=False)

print("Fichier 'capacites_thermiques_1800_final.csv' créé avec les colonnes latitude, longitude et capacité thermique.")

# # Projection et carte
# fig = plt.figure(figsize=(14, 7))
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.coastlines()
# sc = ax.scatter(df_cells["longitude"], df_cells["latitude"],
#                 c=df_cells["heat_capacity_J_per_K"] / 1e18,
#                 cmap="viridis", s=40, edgecolor='k', transform=ccrs.PlateCarree())
# plt.title("Capacité thermique des cellules (~283 333 km²)")
# cbar = plt.colorbar(sc, label="Capacité thermique (×10¹⁸ J/K)")
# plt.show()











