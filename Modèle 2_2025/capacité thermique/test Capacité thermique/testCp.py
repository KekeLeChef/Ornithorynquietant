import rasterio
import numpy as np
from shapely.geometry import box
from rasterio.windows import from_bounds

CAPACITES_THERMIQUES = {
    0: 4180,    # Par défaut si non analysé, de l'eau
    10: 2500,   # Forêt (valeur indicative)
    20: 2000,   # Savane
    30: 1800,   # Herbe
    40: 1500,   # Cultures
    50: 1400,   # Zones arbustives
    60: 1200,   # Sol nu
    70: 830,    # Sable/désert
    80: 4180,   # Eau
    90: 2090,   # Neige/glace
    100: 1000   # Zones bâties
}


def capacite_thermique_moyenne(lat, lon, geotiff_path):
    delta_deg = 0.09  # Environ 10 km en degrés (approximatif)
    min_lon, max_lon = lon - delta_deg/2, lon + delta_deg/2
    min_lat, max_lat = lat - delta_deg/2, lat + delta_deg/2

    with rasterio.open(geotiff_path) as src:
        window = from_bounds(min_lon, min_lat, max_lon, max_lat, src.transform)
        data = src.read(1, window=window)
        data = data[data != src.nodata]  # retirer les pixels vides

        if data.size == 0:
            return None

        classes, counts = np.unique(data, return_counts=True)

        total = 0
        total_weight = 0

        for cls, count in zip(classes, counts):
            if cls in CAPACITES_THERMIQUES:
                total += CAPACITES_THERMIQUES[cls] * count
                total_weight += count

        if total_weight == 0:
            return None

        return total / total_weight

#exemple
lat = 32.0
lon = 13.4

tiff_file = "ESA_WorldCover_10m_2021_V200_N30E012_Map.tif"

result = capacite_thermique_moyenne(lat, lon, tiff_file)
print(f"Capacité thermique massique moyenne : {result:.2f} J/kg·K")
