"""

Ce programme permet de calculer le gradient de température selon l'axe (Oy), on considère que les composantes sur (Ox) et (Oz) sont nulles. Ici on considère l'axe (Oy) le long de l'axe de rotation de la Terre et l'axe (Ox) le long de l'équateur. Ici, on le calcule pour une longitude de 0 (+ ou - 3.1°) et une latitude allant de lat_min à lat_max, pour une heure H.


"""

import numpy as np
import pandas as pd

# VARIABLES
fichier = "temperature_bon3_Tatmo_288.csv" #fichier avec les valeurs de températures
H = 10 # choix de l'heure entre 0 et 23(choix de la colonne du fichier csv)
lat_min = 0 #valeurs des latitudes à prendre en compte
lat_max = 30



# Chargement de la matrice de température taille (1800, 24)
temperature_matrix = np.loadtxt(fichier, delimiter=",")



# Génération des grilles latitude / longitude
latitudes = np.linspace(-90, 90, 30)         # 30 latitudes
longitudes = np.linspace(-180, 180, 60)      # 60 longitudes

# Construction de la grille complète
lat_all, lon_all = np.meshgrid(latitudes, longitudes, indexing='ij') #deux matrices 2D (30, 60)

lat_flat = lat_all.flatten()     # latitudes de chaque points (vecteur 1D (1800))
lon_flat = lon_all.flatten()     # longitudes de chaque points (vecteur 1D (1800))



# Température à une heure fixé
T_colonne = temperature_matrix[:, H]



# Sélection des points avec 0 <= lat <= 30 et |lon| < 3.1°
mask = (lat_flat >= lat_min) & (lat_flat <= lat_max) & (np.abs(lon_flat) <= 3.1)
indices_selectionnes = np.where(mask)[0]

lat_sel = lat_flat[indices_selectionnes]
lon_sel = lon_flat[indices_selectionnes]
T_sel = T_colonne[indices_selectionnes]

# Filtrage : un seul point par latitude (celui avec longitude la plus proche de 0)
points_uniques = {}
for i in range(len(lat_sel)):
    lat = lat_sel[i]
    if lat not in points_uniques or abs(lon_sel[i]) < abs(points_uniques[lat][1]):
        points_uniques[lat] = (T_sel[i], lon_sel[i])

# Tri des latitudes
lat_sorted = sorted(points_uniques.keys())
T_sorted = np.array([points_uniques[lat][0] for lat in lat_sorted])



# Calcul du gradient avec Euler
dy_deg = lat_sorted[1] - lat_sorted[0]
dy = dy_deg * 111000  # en mètres

dT_dy = np.zeros(len(T_sorted) - 1)
for i in range(len(T_sorted) - 1):
    dT_dy[i] = (T_sorted[i+1] - T_sorted[i]) / dy



# Affichage
print ("Heure choisie", H, "h")
print("Latitudes utilisées :", [round(float(lat), 5) for lat in lat_sorted]) #ici arrondi à 5 décimales
print("Températures :", T_sorted)
print("Gradient dT/dy (K/m) :", dT_dy)
