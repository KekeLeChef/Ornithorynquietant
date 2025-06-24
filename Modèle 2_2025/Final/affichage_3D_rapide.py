import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
from matplotlib import cm
import shapefile
import pandas as pd
from fonctions_modifie2 import update_sun_vector, project_to_sphere, get_shape, get_albedo, calc_power_temp, update_plot, slider_update, set_mois, temp_dans_csv, puissance_cond, change_temp, get_Cp
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
capacity_data = pd.read_csv("grid_1800_cp.csv")
capacity_parsed = capacity_data
capacity_parsed.columns = ['latitude', 'longitude', 'cp_J_per_K']
capacity_parsed['latitude'] = capacity_parsed['latitude'].astype(float)
capacity_parsed['longitude'] = capacity_parsed['longitude'].astype(float)
capacity_parsed['cp_J_per_K'] = capacity_parsed['cp_J_per_K'].astype(float)

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


# Ensemble des mois
mois_labels = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# Mois de janvier par défaut
current_month = [1]

## Lecture csv de tous les fichiers et stockage des températures dans des matrices

for i in mois_labels :

    # Nom de variable qui change pour chaque mois
    var_name = f"temp_{i}"

    T_sur_24h = []
    rows, cols = 30, 60

    # Lecture du CSV complet
    data = np.loadtxt(f"12_mois/{i}.csv", delimiter=",")

    # Extraction de la colonne voulue (1800 valeurs)
    col_data = data[:, 0]

    # Reshape en 30 x 60
    T_reconstruit = col_data.reshape((rows, cols))

    # Lecture des valeurs de température sur les 24h
    for k in range(1,25):
        col_data = data[:,k-1]
        T_reconstruit = col_data.reshape((rows, cols))
        T_sur_24h.append(T_reconstruit)

    # création d'une variable par mois
    globals()[var_name] = np.array(T_sur_24h)

# Liste de toutes les températures
tous_fichiers = [temp_Janvier,temp_Février,temp_Mars,temp_Avril,temp_Mai,temp_Juin,temp_Juillet,temp_Août,temp_Septembre,temp_Octobre,temp_Novembre,temp_Décembre]


##  3D

# Création de la figure et de l'axe
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Définir les bornes min/max sur toutes les données (les 24 heures)
all_temps = tous_fichiers[0][0]
vmin = np.min(all_temps)
vmax = np.max(all_temps)

# Mappable pour la colorbar avec les vraies valeurs
mappable = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
mappable.set_array([])  # Nécessaire mais contenu vide ici

cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
cbar.set_label('Température (K)')


## Initialisation du graphique

# Affichage par défaut en janvier à l'heure 0
temp_dans_csv (tous_fichiers[0][0],x,y,z,ax,shapes,mappable,cbar )

# Création du slider
ax_slider = plt.axes([0.25, 0.02, 0.50, 0.03], facecolor='lightgoldenrodyellow')
time_slider = Slider(ax_slider, 'Time (h)', 1, 24, valinit=0, valstep=1)

# Liaison du slider à la fonction de mise à jour
time_slider.on_changed(lambda val: slider_update(val, current_month,tous_fichiers, ax, fig, shapes, x, y, z, constante_solaire, sigma, phi, theta, rayon_astre_m, list_albedo, latitudes, longitudes,mappable,cbar))

# Création des axes et boutons pour chaque mois
btn_mois = []

for i, mois in enumerate(mois_labels):
    ax_mois = plt.axes([0.1, 0.95 - i * 0.07, 0.1, 0.04])
    btn = Button(ax_mois, mois)
    btn.on_clicked(lambda event, m=i + 1: set_mois(m, current_month,tous_fichiers, time_slider, ax, fig, shapes, x, y, z, constante_solaire, sigma, phi, theta, rayon_astre_m, list_albedo, latitudes, longitudes,mappable,cbar))
    btn_mois.append(btn)

# Affichage de la figure
plt.show()





