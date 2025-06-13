

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
import shapefile
import pandas as pd
from fonctions import update_sun_vector, project_to_sphere, get_shape, get_albedo, calc_power_temp, update_plot, slider_update, set_mois
import csv


# Charger les données SHP
sf = shapefile.Reader("data/ne_10m_coastline.shp")
shapes = sf.shapes()

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


# Constantes
constante_solaire = 1361  # W/m^2, valeur moyenne au niveau de la Terre
rayon_astre = 6371  # km, par exemple le rayon de la Terre
sigma = 5.670e-8  # Constante de Stefan-Boltzmann en W/m^2/K^4
epaisseur_atmosphere = 600  # km, approximative thickness of Earth's atmosphere

rayon_astre_m = rayon_astre * 1000
epaisseur_atmosphere_m = epaisseur_atmosphere * 1000

C_CO2_moy = 400 #ppm
C_H2O_moy = 25000 #ppm


# Grille sphérique pour représenter la surface de l'astre
phi = np.linspace(0, 2 * np.pi, 60)
theta = np.linspace(0, np.pi, 30)
phi, theta = np.meshgrid(phi, theta)

x = rayon_astre_m * np.sin(theta) * np.cos(phi)
y = rayon_astre_m * np.sin(theta) * np.sin(phi)
z = rayon_astre_m * np.cos(theta)

x_atmosphere = (rayon_astre_m + epaisseur_atmosphere_m) * np.sin(theta) * np.cos(phi)
y_atmosphere = (rayon_astre_m + epaisseur_atmosphere_m) * np.sin(theta) * np.sin(phi)
z_atmosphere = (rayon_astre_m + epaisseur_atmosphere_m) * np.cos(theta)


## Test temp sur 24H

sun_vector = np.array([1, 0, 0])

S_terre = 510 * 10**12 # m^2
# Capacité thermique massique du sol
Cpm = 1000  #J*kg**-1*K**-1
mu_sol_sec = 1000 #kg*m**-3
epaisseur = 5*10**-2 #m
# Cpm = 4180 #J*kg**-1*K**-1 pour l'eau

# Capacité thermique d'un carré
Cp = Cpm*mu_sol_sec*epaisseur*(S_terre/1800)
# print("Cp = ", Cp)

# Fonction calculant T1 en fonction de T0
def change_temp (Ti, Cp, Pr, dt) :
    T = ((-sigma*(Ti**4)+Pr)*S_terre/1800*dt)/Cp + Ti
    return T


temp_24h_point_au_pif = []
puissance_recue_24h =[]

# Nouvelles températures (pas statiques)
t_apres_chgmt = []

# Dimension matrice de température
L = 1800  # nombre de points
l = 24    # nombre de colonnes (heures)

# Initialisation de la matrice de température
temperature_matrix = np.zeros((L, l))

# première température prise en statique
P0, T0 = calc_power_temp(0, 1, sun_vector, x, y, z, phi, theta, constante_solaire, sigma, rayon_astre_m, list_albedo, latitudes, longitudes)
# t_apres_chgmt.append(T[10,5])

for i in range(1,2):
    P, T = calc_power_temp(i, 1, sun_vector, x, y, z, phi, theta, constante_solaire, sigma, rayon_astre_m, list_albedo, latitudes, longitudes)
    #mettre les T dans la colonne i (fichier csv : ligne les heures, colonne les 1800 points)

    # Aplatir la matrice T (par lignes)
    T_flat = T.flatten()  # devient un tableau 1D de 1800 valeurs
    print(T_flat)

    # Mettre la colonne i-1 à jour avec les 1800 températures
    temperature_matrix[:, i - 1] = T_flat

    #
    # Tchange = change_temp(t_apres_chgmt[-1],Cp,P[10,5],3600)
    # t_apres_chgmt.append(Tchange)


# Sauvegarde dans un fichier CSV
# np.savetxt("temperature_output2.csv", temperature_matrix, delimiter=",")

# print(t_apres_chgmt)

# for k in range(1,31) :
#     for i in range(1,25):
#         P, T = calc_power_temp(i, 1, sun_vector, x, y, z, phi, theta, constante_solaire, sigma, rayon_astre_m, list_albedo, latitudes, longitudes)
#         # temp_24h_point_au_pif.append(T[10, 5])
#         # puissance_recue_24h.append(P[10, 5])
#         # print("Ti =", t_apres_chgmt[i-1])
#         # print("Pr = ",P[10,5])
#         Tchange = change_temp(t_apres_chgmt[-1],Cp,P[10,5],3600)
#         t_apres_chgmt.append(Tchange)
#
# for i in range(1,25) :
#     print("1e jour",t_apres_chgmt[i])
#
# for i in range(1,25) :
#     print("31 jour",t_apres_chgmt[-i])

## Création fichiers






