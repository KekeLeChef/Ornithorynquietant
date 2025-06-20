import os
print("Répertoire actuel :", os.getcwd())


import numpy as np
import shapefile
import matplotlib.pyplot as plt
import pandas as pd

# Chargement initial (mois de janvier)
temp_df = pd.read_csv('temperature_output_mois_01.csv', header=None)
temperatures = temp_df.to_numpy()
temp_min, temp_max = np.nanmin(temperatures), np.nanmax(temperatures)

# Création figure et axes
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Barre de couleur initialisée une seule fois
mappable = plt.cm.ScalarMappable(cmap='plasma')
mappable.set_array([temp_min, temp_max])
cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, pad=0.1)
cbar.set_label('Température (K)')

# Définition des fonctions

def update_sun_vector(mois, sun_vector):
    angle_inclinaison = np.radians(23 * np.cos(2 * np.pi * mois / 12))
    rotation_matrix_saison = np.array([
        [np.cos(angle_inclinaison), 0, np.sin(angle_inclinaison)],
        [0, 1, 0],
        [-np.sin(angle_inclinaison), 0, np.cos(angle_inclinaison)]
    ])
    return rotation_matrix_saison.dot(sun_vector)


def project_to_sphere(lon, lat, radius=1):
    lon, lat = np.radians(lon), np.radians(lat)
    x = radius * np.cos(lat) * np.cos(lon)
    y = radius * np.cos(lat) * np.sin(lon)
    z = radius * np.sin(lat)
    return x, y, z


def get_shape(shape):
    points = np.array(shape.points)[::300]
    lon, lat = points[:, 0], points[:, 1]
    return project_to_sphere(lon, lat, 6371e3 + 1e5) if len(lon) >= 2 else None


def update_plot(time, mois):
    global temperatures, temp_min, temp_max

    heure = int(time) % temperatures.shape[1]
    temp_grid = temperatures[:, heure].reshape(x.shape)

    ax.clear()
    for shape in shapes:
        shp = get_shape(shape)
        if shp:
            ax.plot(*shp, color='black', zorder=5)

    norm = (temp_grid - temp_min) / (temp_max - temp_min)
    ax.plot_surface(x, y, z, facecolors=plt.cm.plasma(norm), rstride=1, cstride=1, linewidth=0)

    mappable.set_array([temp_min, temp_max])
    cbar.update_normal(mappable)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(f'Température à {heure} h (mois = {mois})')
    fig.canvas.draw_idle()


def slider_update(val):
    update_plot(val, current_month[0])


def set_mois(mois):
    global temperatures, temp_min, temp_max

    current_month[0] = mois
    temp_df = pd.read_csv(f'temperature_output_mois_{mois:02d}.csv', header=None)
    temperatures = temp_df.to_numpy()
    temp_min, temp_max = np.nanmin(temperatures), np.nanmax(temperatures)

    slider_update(time_slider.val)

# Chargement des données SHP
sf = shapefile.Reader("data/ne_10m_coastline.shp")
shapes = sf.shapes()

# Grille sphérique
rayon_astre_m = 6371e3
phi, theta = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0, np.pi, 30))
x = rayon_astre_m * np.sin(theta) * np.cos(phi)
y = rayon_astre_m * np.sin(theta) * np.sin(phi)
z = rayon_astre_m * np.cos(theta)

# Slider temporel
from matplotlib.widgets import Slider, Button
current_month = [1]

time_slider_ax = plt.axes([0.25, 0.02, 0.50, 0.03])
time_slider = Slider(time_slider_ax, 'Heure (h)', 0, 23, valinit=0, valstep=1)
time_slider.on_changed(slider_update)

# Boutons mois
mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
for idx, label in enumerate(mois_labels, start=1):
    ax_btn = plt.axes([0.02, 0.85 - 0.06*(idx-1), 0.1, 0.04])
    btn = Button(ax_btn, label)
    btn.on_clicked(lambda event, m=idx: set_mois(m))

# Initial plot
update_plot(0, 1)

plt.show()