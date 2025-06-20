# modélisation_modifiee.py
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button
import shapefile
import pandas as pd
from fonctions import (
    update_sun_vector,
    project_to_sphere,
    get_shape,
    get_albedo,
    calc_power_temp,
    update_plot,
    slider_update,
    set_mois
)

# Chargement des données de température pour le calcul du slider
# Le module fonctions charge déjà le CSV pour les tracés
temp_df = pd.read_csv('temperature_output2.csv', header=None)
temperatures = temp_df.to_numpy()
total_hours = temperatures.shape[1]

# Charger les données SHP
sf = shapefile.Reader("data/ne_10m_coastline.shp")
shapes = sf.shapes()

# Chargement et préparation des données d'albédo
list_albedo = []
for i in range(1, 10):
    df = pd.read_csv(f'albedo/albedo0{i}.csv')
    if i == 1:
        latitudes = df['Latitude/Longitude'].values
        longitudes = df.columns[1:].astype(float)
    list_albedo.append(df.set_index('Latitude/Longitude').to_numpy())
for i in range(10, 13):
    df = pd.read_csv(f'albedo/albedo{i}.csv')
    list_albedo.append(df.set_index('Latitude/Longitude').to_numpy())

# Constantes
constante_solaire = 1361        # W/m^2
rayon_astre = 6371               # km
sigma = 5.670e-8                # W/m^2/K^4
epaisseur_atmosphere = 600      # km
rayon_astre_m = rayon_astre * 1000

epaisseur_atmosphere_m = epaisseur_atmosphere * 1000

# Grille sphérique pour la surface
phi = np.linspace(0, 2 * np.pi, 60)
theta = np.linspace(0, np.pi, 30)
phi, theta = np.meshgrid(phi, theta)

x = rayon_astre_m * np.sin(theta) * np.cos(phi)
y = rayon_astre_m * np.sin(theta) * np.sin(phi)
z = rayon_astre_m * np.cos(theta)

# Configuration de la figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Affichage initial au temps=0, mois=1
current_month = [1]
update_plot(
    0,
    current_month[0],
    ax, fig,
    shapes,
    x, y, z,
    constante_solaire,
    sigma,
    phi, theta,
    rayon_astre_m,
    list_albedo,
    latitudes,
    longitudes
)

# Slider temporel (heure)
ax_slider = plt.axes([0.25, 0.02, 0.50, 0.03], facecolor='lightgoldenrodyellow')
time_slider = Slider(
    ax_slider,
    'Heure (h)',
    0,
    total_hours - 1,
    valinit=0,
    valstep=1,
    valfmt='%d h'
)
time_slider.on_changed(
    lambda val: slider_update(
        val,
        current_month,
        ax, fig,
        shapes,
        x, y, z,
        constante_solaire,
        sigma,
        phi, theta,
        rayon_astre_m,
        list_albedo,
        latitudes,
        longitudes
    )
)

# Boutons de sélection de mois
mois_labels = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]
for idx, label in enumerate(mois_labels, start=1):
    ax_btn = plt.axes([0.02, 0.85 - 0.06*(idx-1), 0.10, 0.04])
    btn = Button(ax_btn, label)
    btn.on_clicked(
        lambda event, m=idx: set_mois(
            m,
            current_month,
            time_slider,
            ax, fig,
            shapes,
            x, y, z,
            constante_solaire,
            sigma,
            phi, theta,
            rayon_astre_m,
            list_albedo,
            latitudes,
            longitudes
        )
    )

plt.show()
