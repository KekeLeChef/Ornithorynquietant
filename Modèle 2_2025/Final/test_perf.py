import numpy as np
import pandas as pd
import shapefile
from multiprocessing import Pool, cpu_count
from fonctions_modifie2 import (
    calc_power_temp,
    puissance_cond,
    change_temp,
    get_Cp
)

# Charger les données SHP
sf = shapefile.Reader("data/ne_10m_coastline.shp")
shapes = sf.shapes()

# Charger les données d'albédo
list_albedo = []
for i in range(1, 13):
    suffix = f'0{i}' if i < 10 else str(i)
    csv_file_path = f'albedo/albedo{suffix}.csv'
    albedo_data = pd.read_csv(csv_file_path)
    if i == 1:
        latitudes = albedo_data['Latitude/Longitude'].values
        longitudes = albedo_data.columns[1:].astype(float)
    albedo_grid = albedo_data.set_index('Latitude/Longitude').to_numpy()
    list_albedo.append(albedo_grid)

# Charger et parser le fichier de capacité thermique
capacity_data = pd.read_csv("grid_1800_cp.csv")
capacity_parsed = capacity_data
capacity_parsed.columns = ['latitude', 'longitude', 'cp_J_per_K']
capacity_parsed['latitude'] = capacity_parsed['latitude'].astype(float)
capacity_parsed['longitude'] = capacity_parsed['longitude'].astype(float)
capacity_parsed['cp_J_per_K'] = capacity_parsed['cp_J_per_K'].astype(float)

# Constantes
constante_solaire = 1361
rayon_astre = 6371 * 1000
sigma = 5.670e-8
S_terre = 510 * 10**12

# Grille sphérique
phi = np.linspace(0, 2 * np.pi, 60)
theta = np.linspace(0, np.pi, 30)
phi, theta = np.meshgrid(phi, theta)
x = rayon_astre * np.sin(theta) * np.cos(phi)
y = rayon_astre * np.sin(theta) * np.sin(phi)
z = rayon_astre * np.cos(theta)
x_flat, y_flat, z_flat = x.flatten(), y.flatten(), z.flatten()

# Fonction de calcul parallèle
def calcul_temperature(args):
    k, temp_avant, P_val, xk, yk, zk = args
    P_diff = puissance_cond(temp_avant, 3600, 0, 0)
    P_tot = P_diff + P_val
    Cp = get_Cp(xk, yk, zk, capacity_parsed)
    return change_temp(temp_avant, Cp, P_tot, 3600, sigma, S_terre)

if __name__ == "__main__":
    sun_vector = np.array([1, 0, 0])
    L, l = 1800, 24
    temperature_matrix = np.zeros((L, l))

    # Température initiale
    _, T0 = calc_power_temp(0,5, sun_vector, x, y, z, phi, theta,
                            constante_solaire, sigma, rayon_astre, list_albedo, latitudes, longitudes)
    temp_simu = T0.flatten()

    with Pool(processes=cpu_count()) as pool:

        # Boucle sur 600 heures (1 mois simulé)
        for i in range(1, 601):
            P, _ = calc_power_temp(i, 5, sun_vector, x, y, z, phi, theta,
                                   constante_solaire, sigma, rayon_astre, list_albedo, latitudes, longitudes)
            P_flat = P.flatten()
            args = [(k, temp_simu[k], P_flat[k], x_flat[k], y_flat[k], z_flat[k]) for k in range(L)]
            temp_simu = pool.map(calcul_temperature, args)
            temp_simu = np.array(temp_simu)

        # Boucle sur 24 heures pour enregistrement
        for h in range(1, 25):
            P, _ = calc_power_temp(h, 5, sun_vector, x, y, z, phi, theta,
                                   constante_solaire, sigma, rayon_astre, list_albedo, latitudes, longitudes)
            P_flat = P.flatten()
            temp_avant = temp_simu if h == 1 else temperature_matrix[:, h - 2]
            args = [(k, temp_avant[k], P_flat[k], x_flat[k], y_flat[k], z_flat[k]) for k in range(L)]
            T_flat = pool.map(calcul_temperature, args)
            temperature_matrix[:, h - 1] = T_flat

    # Sauvegarde CSV
    np.savetxt("temperature_600.csv", temperature_matrix, delimiter=",")

if __name__ == "__main__":
    sun_vector = np.array([1, 0, 0])
    L, l = 1800, 24
    temperature_matrix = np.zeros((L, l))

    # Température initiale
    _, T0 = calc_power_temp(0, 5, sun_vector, x, y, z, phi, theta,
                            constante_solaire, sigma, rayon_astre, list_albedo, latitudes, longitudes)
    temp_simu = T0.flatten()

    with Pool(processes=cpu_count()) as pool:

        # Boucle sur 600 heures (1 mois simulé)
        for i in range(1, 601):
            P, _ = calc_power_temp(i, 5, sun_vector, x, y, z, phi, theta,
                                   constante_solaire, sigma, rayon_astre, list_albedo, latitudes, longitudes)
            P_flat = P.flatten()
            args = [(k, temp_simu[k], P_flat[k], x_flat[k], y_flat[k], z_flat[k]) for k in range(L)]
            temp_simu = pool.map(calcul_temperature, args)
            temp_simu = np.array(temp_simu)

        # Boucle sur 24 heures pour enregistrement
        for h in range(1, 25):
            P, _ = calc_power_temp(h, 5, sun_vector, x, y, z, phi, theta,
                                   constante_solaire, sigma, rayon_astre, list_albedo, latitudes, longitudes)
            P_flat = P.flatten()
            temp_avant = temp_simu if h == 1 else temperature_matrix[:, h - 2]
            args = [(k, temp_avant[k], P_flat[k], x_flat[k], y_flat[k], z_flat[k]) for k in range(L)]
            T_flat = pool.map(calcul_temperature, args)
            temperature_matrix[:, h - 1] = T_flat

    # Sauvegarde CSV
    np.savetxt("Avril.csv", temperature_matrix, delimiter=",")
