import rasterio
import numpy as np
import csv

# Charger le masque terre/eau réel
src = rasterio.open("C:/Users/Simon/Downloads/gshhs_land_water_mask_3km_i.tif")
mask = src.read(1)
h, w = mask.shape
print("Dimensions du raster :", h, "×", w)
print("Valeurs uniques présentes :", np.unique(mask))

# Paramètres de la grille
n_lat, n_lon = 30, 60
lat_step_px = h / n_lat
lon_step_px = w / n_lon

# Fonction pour estimer la fraction glace
def estimate_ice_frac(lat_deg):
    return 1.0 if abs(lat_deg) > 75 else 0.0

# Construction du tableau
table = []
for i in range(n_lat):
    lat_center = 90 - (i + .5) * 180 / n_lat
    for j in range(n_lon):
        lon_center = -180 + (j + .5) * 360 / n_lon

        ys = slice(int(i * lat_step_px), int((i + 1) * lat_step_px))
        xs = slice(int(j * lon_step_px), int((j + 1) * lon_step_px))
        cell = mask[ys, xs]

        total = cell.size
        water = np.sum(cell == 0)
        land = np.sum(cell == 100)
        ice = 0
        if estimate_ice_frac(lat_center) == 1.0:
            ice = total - land
            water = 0

        pct_water = round(100 * water / total, 1)
        pct_land = round(100 * land / total, 1)
        pct_ice = round(100 * ice / total, 1)

        table.append({
            "lat_idx": i, "lon_idx": j,
            "lat_center_deg": round(lat_center, 2),
            "lon_center_deg": round(lon_center, 2),
            "%_water": pct_water,
            "%_land": pct_land,
            "%_ice": pct_ice
        })

# Sauvegarde CSV
with open("grid_1800_real_land_water_ice.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=table[0].keys())
    writer.writeheader()
    writer.writerows(table)

print("✅ Fichier généré : grid_1800_real_land_water_ice.csv")