"""

Ce programme permet de calculer le gradient de température selon l'axe (Ox), on considère que les composantes sur (Oy) et (Oz) sont nulles.
Ici on considère l'axe (Oy) le long de l'axe de rotation de la Terre et l'axe (Ox) le long de l'équateur.
On le calcule pour une latitude de 0 (+ ou - 3.1°) et une longitude allant de lon_min à lon_max, pour une heure H.


"""

import numpy as np
import pandas as pd


# VARIABLES
fichier = "temperature_bon3_Tatmo_288.csv"  # fichier avec les valeurs de températures
H = 10  # choix de l'heure entre 0 et 23 (choix de la colonne du fichier csv)
lat_choisie = 0  # latitude à laquelle on se place


# Chargement de la matrice de température taille (1800, 24) --> attention à la taille du fichier!
temperature_matrix = np.loadtxt(fichier, delimiter=",")




# Génération des grilles latitude / longitude
latitudes = np.linspace(-90, 90, 30)         # 30 latitudes
longitudes = np.linspace(0, 180, 60)         # 60 longitudes

# Construction de la grille complète
lat_all, lon_all = np.meshgrid(latitudes, longitudes, indexing='ij')  # matrices 2D (30, 60)

lat_flat = lat_all.flatten()     # latitudes de chaque point (vecteur 1D de taille 1800)
lon_flat = lon_all.flatten()     # longitudes de chaque point (vecteur 1D de taille 1800)


# Température à une heure fixée
T_colonne = temperature_matrix[:, H]



# Sélection des points avec 0 <= lon <= 180 et |lat - lat_choisie| < 3.2°
mask = (lon_flat >= 0) & (lon_flat <= 180) & (np.abs(lat_flat - lat_choisie) <= 3.2)
indices_selectionnes = np.where(mask)[0]

lat_sel = lat_flat[indices_selectionnes]
lon_sel = lon_flat[indices_selectionnes]
T_sel = T_colonne[indices_selectionnes]



# Filtrage : un seul point par longitude (celui avec latitude la plus proche de lat_choisie)
points_uniques = {}
for i in range(len(lon_sel)):
    lon = lon_sel[i]
    lat = lat_sel[i]
    if lon not in points_uniques or abs(lat - lat_choisie) < abs(points_uniques[lon][1] - lat_choisie):
        points_uniques[lon] = (T_sel[i], lat)

# Tri des longitudes
lon_sorted = sorted(points_uniques.keys())
T_sorted = np.array([points_uniques[lon][0] for lon in lon_sorted])

# Calcul du gradient avec Euler
dx_deg = lon_sorted[1] - lon_sorted[0]
dx = dx_deg * 111000  # en mètres

dT_dx = np.zeros(len(T_sorted) - 1)
for i in range(len(T_sorted) - 1):
    dT_dx[i] = (T_sorted[i+1] - T_sorted[i]) / dx




# Affichage
print("Heure choisie :", H, "h")
print("Latitude choisie :", lat_choisie)
print("Longitudes utilisées :", [round(float(lon), 5) for lon in lon_sorted])
print("Températures :", [round(float(t), 3) for t in T_sorted])
print("Gradient dT/dx (K/m) :", dT_dx)
