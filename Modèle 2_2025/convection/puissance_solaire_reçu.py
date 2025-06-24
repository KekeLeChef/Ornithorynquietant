import numpy as np
import pandas as pd
import os
from math import sin, cos, radians

# Constantes physiques et géographiques
SOLAR_CONSTANT = 1361  # W/m²
AXIAL_TILT = 23.44  # inclinaison de l'axe terrestre en degrés
LAT_DIVISIONS = 30
LON_DIVISIONS = 60

# Grille des latitudes et longitudes (centre de chaque cellule)
latitudes = np.linspace(-90 + 180 / LAT_DIVISIONS / 2, 90 - 180 / LAT_DIVISIONS / 2, LAT_DIVISIONS)
longitudes = np.linspace(-180 + 360 / LON_DIVISIONS / 2, 180 - 360 / LON_DIVISIONS / 2, LON_DIVISIONS)

# Approximation du jour moyen de chaque mois (1-indexed)
MONTH_DAYS = {
    1: 15, 2: 45, 3: 74, 4: 105, 5: 135, 6: 162,
    7: 198, 8: 228, 9: 258, 10: 288, 11: 318, 12: 344
}

# Fonction pour calculer la déclinaison solaire (en degrés)
def solar_declination(day_of_year):
    return AXIAL_TILT * sin(2 * np.pi * (day_of_year - 81) / 365)

# Fonction pour l'angle horaire solaire local (en degrés)
def hour_angle(hour, longitude):
    return 15 * (hour - 12) + longitude

# Répertoire de sortie
output_dir = "puissance_reçu_atm"
os.makedirs(output_dir, exist_ok=True)

# Boucle principale : mois, heures, latitude/longitude
for month in range(1, 13):
    day_of_year = MONTH_DAYS[month]
    decl = solar_declination(day_of_year)

    for hour in range(24):
        records = []
        for lat in latitudes:
            for lon in longitudes:
                h_angle = hour_angle(hour, lon)

                # Conversion en radians
                lat_rad = radians(lat)
                decl_rad = radians(decl)
                h_rad = radians(h_angle)

                # Formule d'incidence solaire
                cos_theta = sin(lat_rad) * sin(decl_rad) + cos(lat_rad) * cos(decl_rad) * cos(h_rad)
                cos_theta = max(0, cos_theta)  # Pas de rayonnement si le soleil est sous l'horizon

                power = SOLAR_CONSTANT * cos_theta
                records.append([lat, lon, power])

        # Sauvegarde CSV
        df = pd.DataFrame(records, columns=["Latitude", "Longitude", "Power_W_m2"])
        filename = f"solar_power_month{month:02d}_hour{hour:02d}.csv"
        df.to_csv(os.path.join(output_dir, filename), index=False)
