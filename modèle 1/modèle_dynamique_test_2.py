import numpy as np
import pandas as pd
from fonctions import calc_power_temp

# Constantes (à adapter selon ton cas précis)
constante_solaire = 1361  # W/m^2
sigma = 5.670e-8
rayon_astre_m = 6371 * 1000
sun_vector = np.array([1, 0, 0])
S_terre = 510e12
Cp = 1000 * 1000 * (5e-2) * (S_terre/1800)

# Grille sphérique
phi, theta = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0, np.pi, 30))
x = rayon_astre_m * np.sin(theta) * np.cos(phi)
y = rayon_astre_m * np.sin(theta) * np.sin(phi)
z = rayon_astre_m * np.cos(theta)

# Charger albédos
list_albedo = []
for i in range(1, 13):
    albedo_data = pd.read_csv(f'albedo/albedo{i:02d}.csv')
    if i == 1:
        latitudes = albedo_data['Latitude/Longitude'].values
        longitudes = albedo_data.columns[1:].astype(float)
    albedo_grid = albedo_data.set_index('Latitude/Longitude').to_numpy()
    list_albedo.append(albedo_grid)

# Dimension matrice de température
L = 1800
l = 24

print("Début du script")
for mois in range(1, 13):
    print(f"Traitement du mois {mois}")
    temperature_matrix = np.zeros((1800, 24))

    for heure in range(24):
        print(f"  Heure {heure}")
        P, T = calc_power_temp(
            heure, mois, sun_vector, x, y, z, phi, theta,
            constante_solaire, sigma, rayon_astre_m,
            list_albedo, latitudes, longitudes
        )

        temperature_matrix[:, heure] = T.flatten()
        print(f"    Max température {T.max()}")

    filename = f"temperature_output_mois_{mois:02d}.csv"
    np.savetxt(filename, temperature_matrix, delimiter=",")
    print(f"Fichier créé : {filename}")

