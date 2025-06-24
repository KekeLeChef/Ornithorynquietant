

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
from matplotlib import cm
import shapefile
import pandas as pd
from fonctions_modifie2 import update_sun_vector, project_to_sphere, get_shape, get_albedo, calc_power_temp, update_plot, slider_update, set_mois, temp_dans_csv, puissance_cond, change_temp, get_Cp
import csv
import os
import imageio.v2 as imageio



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



mois_labels = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
current_month = [1]

## Lecture csv de tous les fichiers et stockage des températures dans une liste de matrices

# liste de température sur 12 mois
print("📦 Chargement des fichiers de température mensuels en cours...")

tous_fichiers = []
rows, cols = 30, 60

for i in mois_labels:
    print(f"  → Chargement de {i}.csv...")
    T_sur_24h = []
    data = np.loadtxt(f"12_mois/{i}.csv", delimiter=",")

    for k in range(1, 25):
        col_data = data[:, k - 1]
        T_reconstruit = col_data.reshape((rows, cols))
        T_sur_24h.append(T_reconstruit)

    tous_fichiers.append(np.array(T_sur_24h))

print("✅ Tous les fichiers de température ont été chargés avec succès.\n")


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
#
# mappable = plt.cm.ScalarMappable(cmap='viridis')
# mappable.set_array([np.min(T_reconstruit),np.max(T_reconstruit)])
# cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
# cbar.set_label('Température (K)')



## Initialisation du graphique

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
    btn.on_clicked(lambda event, m=i + 1: set_mois(m, current_month, tous_fichiers, time_slider, ax, fig, shapes, x, y, z, constante_solaire, sigma, phi, theta, rayon_astre_m, list_albedo, latitudes, longitudes, mappable, cbar))
    btn_mois.append(btn)


def gif_24h_pour_mois(index_mois, tous_fichiers, x, y, z, shapes):

    os.makedirs("Gif/frames", exist_ok=True)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Définir min/max globaux
    all_temps = tous_fichiers[index_mois]
    vmin = np.min(all_temps)
    vmax = np.max(all_temps)

    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    mappable.set_array([])  # requis pour la colorbar

    cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
    cbar.set_label('Température (K)')

    images = []

    for h in range(24):
        ax.clear()
        ax.view_init(elev=20, azim=40)
        temp_dans_csv(tous_fichiers[index_mois][h], x, y, z, ax, shapes, mappable, cbar)
        plt.title(f"{mois_labels[index_mois]} - {h}h")
        fname = f"Gif/frames/{mois_labels[index_mois]}_{h:02d}.png"
        plt.savefig(fname)
        images.append(imageio.imread(fname))
        print(f"Image enregistrée : {fname}")

    gif_path = f"Gif/GIF_24h_{mois_labels[index_mois]}.gif"
    imageio.mimsave(gif_path, images, duration=2)
    print(f"GIF généré : {gif_path}")


def gif_12mois_heure_fixe(heure, tous_fichiers, x, y, z, shapes):
    import imageio.v2 as imageio
    import os

    os.makedirs("Gif/frames", exist_ok=True)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Définir min/max globaux
    all_temps = [tous_fichiers[i][heure - 1] for i in range(12)]
    vmin = np.min(all_temps)
    vmax = np.max(all_temps)

    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    mappable.set_array([])

    cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
    cbar.set_label('Température (K)')

    images = []

    for i in range(12):
        ax.clear()
        ax.view_init(elev=20, azim=40)
        temp_dans_csv(tous_fichiers[i][heure - 1], x, y, z, ax, shapes, mappable, cbar)
        plt.title(f"{mois_labels[i]} - {heure}h")
        fname = f"Gif/frames/{mois_labels[i]}_{heure:02d}h.png"
        plt.savefig(fname)
        images.append(imageio.imread(fname))
        print(f"Image enregistrée : {fname}")

    gif_path = f"Gif/GIF_12mois_{heure:02d}h.gif"
    imageio.mimsave(gif_path, images, duration=2)
    print(f"GIF généré : {gif_path}")


# Générer un GIF sur 24h en janvier
# gif_24h_pour_mois(0, tous_fichiers, x, y, z, shapes)


# Générer un GIF à 12h sur toute l'année
# gif_12mois_heure_fixe(12, tous_fichiers, x, y, z, shapes)


# Affichage de la figure
plt.show()





