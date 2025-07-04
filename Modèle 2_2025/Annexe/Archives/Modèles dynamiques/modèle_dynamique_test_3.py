

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
from matplotlib import cm
import shapefile
import pandas as pd
from fonctions_modifie import update_sun_vector, project_to_sphere, get_shape, get_albedo, calc_power_temp, update_plot, slider_update, set_mois, temp_dans_csv,get_Cp
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


## Test températures sur 24H et stockage desdonnées dans un fichier csv pour les 1800 points

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
T0_flat = T0.flatten()
# t_apres_chgmt.append(T[10,5])

for i in range(1,25):

    P, T = calc_power_temp(i, 1, sun_vector, x, y, z, phi, theta, constante_solaire, sigma, rayon_astre_m, list_albedo, latitudes, longitudes)

    # Aplatir la matrice T (par lignes)
    T_flat = T.flatten()  # devient un tableau 1D de 1800 valeurs
    P_flat = P.flatten()
    # print(T_flat)
    # print(type(T_flat))

    if i  == 1 :

        # k c'est l'indice et j c'est l'élément
        for k,j in enumerate(T_flat) :
            T_flat[k] = change_temp(T0_flat[k],Cp,P_flat[k],3600)

    else :

        for k,j in enumerate(T_flat) :
            T_flat[k] = change_temp(temperature_matrix[:,i-2][k],Cp,P_flat[k],3600)


    # Mettre la colonne i-1 à jour avec les 1800 températures
    temperature_matrix[:, i - 1] = T_flat

    #
    # Tchange = change_temp(t_apres_chgmt[-1],Cp,P[10,5],3600)
    # t_apres_chgmt.append(Tchange)


# Sauvegarde dans un fichier CSV
np.savetxt("temperature_bon3_Tatmo_288.csv", temperature_matrix, delimiter=",")


# ## Lecture csv et stockage des infos dans une matrice
#
# T_sur_24h = []
# rows, cols = 30, 60
# # Lecture du CSV complet
# data = np.loadtxt("temperature_bon3_Tatmo_288.csv", delimiter=",")
#
# # Extraction de la colonne voulue (1800 valeurs)
# col_data = data[:, 0]  # shape = (1800,)
#
# # Reshape en 30 x 60 (ordre par lignes = C-order, comme flatten())
# T_reconstruit = col_data.reshape((rows, cols))
#
# for k in range(1,25):
#     col_data = data[:,k-1]
#     T_reconstruit = col_data.reshape((rows, cols))
#     T_sur_24h.append(T_reconstruit)
#
#
#
# ##  3D
#
# # Création de la figure et de l'axe
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
#
#
# # Définir les bornes min/max sur toutes les données (les 24 heures)
# all_temps = np.array(T_sur_24h)
# vmin = np.min(all_temps)
# vmax = np.max(all_temps)
#
# # Mappable pour la colorbar avec les vraies valeurs
# mappable = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# mappable.set_array([])  # Nécessaire mais contenu vide ici
#
# cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
# cbar.set_label('Température (K)')
# #
# # mappable = plt.cm.ScalarMappable(cmap='viridis')
# # mappable.set_array([np.min(T_reconstruit),np.max(T_reconstruit)])
# # cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
# # cbar.set_label('Température (K)')
#
# # Initialisation du graphique
# current_month = [1]
# temp_dans_csv (T_sur_24h[0],x,y,z,ax,shapes,mappable,cbar )
# #surf = ax.plot_surface(x, y, z, facecolors=plt.cm.viridis(T_reconstruit/np.max(T_reconstruit)), rstride=1, cstride=1, linewidth=1)
#
# #update_plot(0, current_month[0], ax, fig, shapes, x, y, z, constante_solaire, sigma, phi, theta, rayon_astre_m, list_albedo, latitudes, longitudes)
#
# # Création du slider
# ax_slider = plt.axes([0.25, 0.02, 0.50, 0.03], facecolor='lightgoldenrodyellow')
# time_slider = Slider(ax_slider, 'Time (h)', 1, 24, valinit=0, valstep=1)
#
# # Liaison du slider à la fonction de mise à jour
# time_slider.on_changed(lambda val: slider_update(T_sur_24h[val-1], current_month, ax, fig, shapes, x, y, z, constante_solaire, sigma, phi, theta, rayon_astre_m, list_albedo, latitudes, longitudes,mappable,cbar))
#
#
# # Création des axes et boutons pour chaque mois
# mois_labels = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
# btn_mois = []
#
# for i, mois in enumerate(mois_labels):
#     ax_mois = plt.axes([0.1, 0.95 - i * 0.07, 0.1, 0.04])
#     btn = Button(ax_mois, mois)
#     btn.on_clicked(lambda event, m=i + 1: set_mois(m, current_month, time_slider, ax, fig, shapes, x, y, z, constante_solaire, sigma, phi, theta, rayon_astre_m, list_albedo, latitudes, longitudes))
#     btn_mois.append(btn)
#
# # Affichage de la figure
# plt.show()





