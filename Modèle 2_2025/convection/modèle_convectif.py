import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Capacité thermique massique de l'air dans l'atm (J/(kg·K))
def cp_air_atm():
    cp_air = 1005  # Capacité thermique massique de l'air (J/(kg·K))
    masse_volumique_air = 1.2  # kg/m³ à 20 °C
    volume_terre = 4/3 * np.pi * (6371e3)**3  # Volume de la Terre (m³)
    volume_atm_terre = 4/3 * np.pi * (6371e3+10e3)**3  # Volume de l'atmosphère (avec 10 km d'épaisseur)
    volume_atm = volume_atm_terre - volume_terre  # Volume de l'atmosphère (m³)
    masse_atm = volume_atm * masse_volumique_air  # Masse atm (kg)
    masse_atm_section = masse_atm / 1800
    cp_air_atm_section = cp_air * masse_atm_section  # J/K
    return cp_air_atm_section

# # Récupère la température T_ij du sol pour le mois et l'heure donnés à partir des fichiers CSV
# def recuperer_T_ij_sol(month):
#     month = mois[month-1]  # Convertit le mois en nom
#     filename = f"12_mois/{month}.csv"
#     if os.path.exists(filename):
#         df = pd.read_csv(filename)
#         T_ij_sol = df["Temperature_K"].values   # Récupère la température de la section ij
#     return T_ij_sol

def recuperer_T_ij_sol(mois_index, heure, section_index):
    """
    Récupère la température du sol T_ij pour une section donnée (index i),
    à une heure et un mois donnés.

    Arguments :
    - mois_index : entier de 1 à 12
    - heure : entier de 0 à 23
    - section_index : entier de 0 à 1799 (index de la grille latitude/longitude)

    Retour :
    - température (float) en Kelvin
    """
    mois_nom = mois[mois_index - 1]  # Nom du mois
    filename = f"12_mois/{mois_nom}.csv"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Fichier non trouvé : {filename}")
    df = pd.read_csv(filename)
    # Vérifie si l'heure demandée correspond bien à une colonne
    if heure >= 24 or heure < 0:
        raise ValueError("L'heure doit être entre 0 et 23 inclus")
    try:
        temperature = df.iloc[section_index, heure]
    except IndexError:
        raise IndexError(f"Index de section {section_index} invalide")
    return temperature


# Calcule la puissance totale reçue par l'atmosphère (W) à partir des fichiers csv qui donne # la puissance solaire reçue par l'atmosphère et loi de Stefn-Boltzmann.
# def puissance_total_reçu_atm(month, hour, T_ij_sol):
#     filename = f"puissance_reçu_atm/solar_power_month{month:02d}_hour{hour:02d}.csv"
#     if os.path.exists(filename):
#         df = pd.read_csv(filename)
#         puissance_totale = df["Power_W_m2"].sum() + sigma * (T_ij_sol**4)
#         print(f"Puissance totale reçue pour le mois {month}, heure {hour} : {puissance_totale} W")
#     return puissance_totale

def puissance_total_reçu_atm(month, hour, lat, lon, T_ij_sol):
    """
    Récupère la puissance solaire reçue dans l’atmosphère pour une latitude et longitude données.
    
    Arguments :
    - month : entier (1 à 12)
    - hour : entier (0 à 23)
    - lat, lon : coordonnées géographiques
    - T_ij_sol : température du sol en Kelvin (float)

    Retour :
    - puissance locale totale reçue (float) en W/m²
    """
    # Fichier CSV de la puissance solaire reçue
    filename = f"puissance_reçu_atm/solar_power_month{month:02d}_hour{hour:02d}.csv"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Fichier non trouvé : {filename}")
    df = pd.read_csv(filename)
    # Calcul de l’index de latitude et longitude sur la grille
    lat_index = get_lat_index(lat)
    lon_index = get_lon_index(lon)
    section_index = 60 * lat_index + lon_index
    try:
        P_solaire_locale = df.loc[section_index, "Power_W_m2"]
    except IndexError:
        raise IndexError(f"Index {section_index} hors limites pour le fichier {filename}")
    # Ajout de la contribution thermique rayonnée par le sol
    P_total_locale = P_solaire_locale + sigma * (T_ij_sol**4)
    return P_total_locale

# Fonction pour obtenir l'index de latitude en fonction de la latitude
# Note : les latitudes sont de -90 à 90, mais on les mappe de 0 à 29 pour correspondre à la grille de 30 latitudes
def get_lat_index(lat):
    lat_min = -90
    lat_max = 90
    lat_step = (lat_max - lat_min) / (30 - 1)  # ≈ 6.2069
    return int(round((lat - lat_min) / lat_step))

# Fonction pour obtenir l'index de longitude en fonction de la longitude
# Note : les longitudes sont de -180 à 180, mais on les mappe de 0 à 59 pour correspondre à la grille de 60 longitudes
def get_lon_index(lon):
    lon_min = -180
    lon_max = 180
    lon_step = (lon_max - lon_min) / (60 - 1)  # ≈ 6.1017
    return int(round((lon - lon_min) / lon_step))

# Gradient température de l'air dans l'atmosphère sur x (K/m)
def gradient_temperature_air_x(fichier, H, lat_choisie, longitude_0_58):
    # Chargement de la matrice de température taille (1800, 24) --> attention à la taille du fichier!
    temperature_matrix = np.loadtxt(fichier, delimiter=",")
    # Génération des grilles latitude / longitude
    latitudes = np.linspace(-90, 90, 30)         # 30 latitudes
    longitudes = np.linspace(-180, 180, 60)         # 60 longitudes
    # Construction de la grille complète
    lat_all, lon_all = np.meshgrid(latitudes, longitudes, indexing='ij')  # matrices 2D (30, 60)
    lat_flat = lat_all.flatten()     # latitudes de chaque point (vecteur 1D de taille 1800)
    lon_flat = lon_all.flatten()     # longitudes de chaque point (vecteur 1D de taille 1800)
    # Température à une heure fixée
    T_colonne = temperature_matrix[:, H]
    # Sélection des points avec -180 <= lon <= 180 et |lat - lat_choisie| < 3.2°
    mask = (lon_flat >= -180) & (lon_flat <= 180) & (np.abs(lat_flat - lat_choisie) <= 3.2)
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
    longitudes = np.linspace(-180, 180, 60)
    target_lon = longitudes[longitude_0_58]
    idx_closest = np.argmin(np.abs(np.array(lon_sorted[:-1]) - target_lon))
    return dT_dx[idx_closest]

# Gradient température de l'air dans l'atmosphère sur y (K/m)
def gradient_temperature_air_y(fichier, H, lon_choisie, latitude_0_28):
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
    # Sélection des points avec -90 <= lat <= 90 et |lon - lon_choisie| < 3.2°
    mask = (lat_flat >= -90) & (lat_flat <= 90) & (np.abs(lon_flat - lon_choisie) <= 3.2)
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
    latitudes_grid = np.linspace(-90, 90, 30)
    target_lat = latitudes_grid[latitude_0_28]
    idx_closest = np.argmin(np.abs(np.array(lat_sorted[:-1]) - target_lat))
    return dT_dy[idx_closest]

# Calcule le changement de température dTij entre deux instants.
def dTij(month, hour, angle_inclinaison, vecteur_vitesse_vent, lat_choisie, lon_choisie, fichier, longitude_0_58, latitude_0_28, T_sol_ij_n):
    P_reçu_atm_ij = puissance_total_reçu_atm(month, hour, lat_choisie, lon_choisie, T_sol_ij_n)  # Récupère la puissance reçue par l'atmosphère
    dT_dt = P_reçu_atm_ij/cp_air_atm_section
    dx_dt = np.cos(np.radians(angle_inclinaison)) * vecteur_vitesse_vent # Projection vecteur vitesse du vent sur l'axe x
    dy_dt = np.sin(np.radians(angle_inclinaison)) * vecteur_vitesse_vent # Projection vecteur vitesse du vent sur l'axe y
    dT_dx = gradient_temperature_air_x(fichier, hour, lat_choisie, longitude_0_58)
    dT_dy = gradient_temperature_air_y(fichier, hour, lon_choisie, latitude_0_28)
    return dT_dt + dx_dt * dT_dx + dy_dt * dT_dy

# Calcule la température T_ij à l'instant n+1 à partir de T_ij à l'instant n et du changement de température dTij.
def T_ij_n_plus_1(T_ij_n, dTij, dt):
    return T_ij_n + dTij * dt

# Coefficient de convection (W/m²/K)
def calcul_h(T_atm_ij_n, T_sol_ij_n) :
    lam = 0.026 # en W / (m.K), la conductivité thermique de l'air
    Lc = 0.05 # en m, la longueur caractéristique correspondant à notre situation
    n = 1/4
    g = 9.81 # en m / s**2, la constante de gravité
    nu = 1.5e-5 # en m**2 / s, viscosité cinématique de l'air
    alpha = 2e-5 # en m**2 / s, diffusivité thermique de l'air
    beta = 1 / T_atm_ij_n
    Gr = (g * beta * (T_sol_ij_n - T_atm_ij_n) * Lc**3) / nu**2 # nombre de Grashof
    Pr = nu / alpha # nombre de Prandtl
    Ra = Gr * Pr # nombre de Rayleigh
    if Ra > 0:
        C = 0.54
        Nu = C * Ra**n
    else:
        C = 0.27
        Ra = abs(Ra) # Si Ra est négatif, on prend la valeur absolue pour le calcul de Nu
        Nu = C * Ra**n
    h = Nu * lam / Lc # par def du nombre de Nusselt
    return h

# Calcule la puissance échangée entre l'air et le sol à l'instant n pour la section ij.
def Flux_th_convectif_ij_n(T_atm_ij_n, T_sol_ij_n):
    h= calcul_h(T_atm_ij_n, T_sol_ij_n)  # Coefficient de convection
    return -h * (T_sol_ij_n - T_atm_ij_n)

# Début code principal
sigma = 5.67e-8  # Constante de Stefan-Boltzmann (W/m²/K⁴)
cp_air_atm_section = cp_air_atm()
mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre"] # Liste des mois
dt = 3600  # Pas de temps en secondes (1 heure)

# Vecteurs vitesse du vent et angle d'inclinaison

# 0 à 30°N
angle_inclinaison_vecteur_vitesse_vent_0_30N = -135 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_0_30N = 5.5 # Vitesse du vent (en m/s) donc 20 km/h
# 30 à 60°N
angle_inclinaison_vecteur_vitesse_vent_30_60N = 45 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_30_60N = 8 # Vitesse du vent (en m/s) donc 28.8 km/h
# 60 à 90°N
angle_inclinaison_vecteur_vitesse_vent_60_90N = 87 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_60_90N = 4.2 # Vitesse du vent (en m/s) donc 15.1 km/h
# 0 à 30°S
angle_inclinaison_vecteur_vitesse_vent_0_30S = 135 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_0_30S = 5.5 # Vitesse du vent (en m/s) donc 20 km/h
# 30 à 60°S
angle_inclinaison_vecteur_vitesse_vent_30_60S = -45 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_30_60S = 8 # Vitesse du vent (en m/s) donc 28.8 km/h
# 60 à 90°S
angle_inclinaison_vecteur_vitesse_vent_60_90S = -87 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_60_90S = 4.2 # Vitesse du vent (en m/s) donc 15.1 km/h


# POUR UTLILISER LA FONCTION DU GRADIENT SUR X, LA LONGITUDE [-180.0, -173.89831, -167.79661, -161.69492, -155.59322, -149.49153, -143.38983, -137.28814, -131.18644, -125.08475, -118.98305, -112.88136, -106.77966, -100.67797, -94.57627, -88.47458, -82.37288, -76.27119, -70.16949, -64.0678, -57.9661, -51.86441, -45.76271, -39.66102, -33.55932, -27.45763, -21.35593, -15.25424, -9.15254, -3.05085, 3.05085, 9.15254, 15.25424, 21.35593, 27.45763, 33.55932, 39.66102, 45.76271, 51.86441, 57.9661, 64.0678, 70.16949, 76.27119, 82.37288, 88.47458, 94.57627, 100.67797, 106.77966, 112.88136, 118.98305, 125.08475, 131.18644, 137.28814, 143.38983, 149.49153, 155.59322, 161.69492, 167.79661, 173.89831, 180.0] CORRESPOND A UNE VALEUR ENTRE 0 ET 58 RELATIVEMENT A LA LISTE DES LONGITUDES
# PAREIL POUR GRADIENT SUR Y MAIS AVEC LES LATITUDES [-90.0, -83.89831, -77.79661, -71.69492, -65.59322, -59.49153, -53.38983, -47.28814, -41.18644, -35.08475, -28.98305, -22.88136, -16.77966, -10.67797, -4.57627, 1.52542, 7.62712, 13.72881, 19.83051, 25.9322, 32.0339, 38.13559, 44.23729, 50.33898, 56.44068, 62.54237, 68.64407, 74.74576, 80.84746, 86.94915, 93.05085, 99.15254, 105.25424, 111.35593, 117.45763, 123.55932, 129.66102, 135.76271, 141.86441, 147.9661, 154.0678, 160.16949, 166.27119, 172.37288] CORRESPOND A UNE VALEUR ENTRE 0 ET 28 RELATIVEMENT A LA LISTE DES LATITUDES


# Grilles latitude / longitude
latitudes = np.linspace(-90, 90, 30)         # 30 latitudes
longitudes = np.linspace(-180, 180, 60)      # 60 longitudes
lat_all, lon_all = np.meshgrid(latitudes, longitudes, indexing='ij')  # (30, 60)
lat_flat = lat_all.flatten()    # (1800,)
lon_flat = lon_all.flatten()    # (1800,)

# Initialisation
T_ij_n = 15 + 273.15  # Température initiale de l'air en Kelvin (15 °C)


# Boucle principale sur les 12 mois et 24 heures
for mois_index in range(1, 13):
    mois_nom = mois[mois_index - 1]
    fichier_temperature = f"12_mois/{mois_nom}.csv"
    temperature_df = pd.read_csv(fichier_temperature)

    for heure in range(24):
        flux_convectifs = []
        for i in range(1799):
            lat_ij = lat_flat[i]
            lon_ij = lon_flat[i]

            longitude_0_58=get_lon_index(lon_ij)
            latitude_0_28=get_lat_index(lat_ij)

            # Sélection des bons paramètres de vent selon la latitude
            if 0 <= lat_ij < 30:
                angle = angle_inclinaison_vecteur_vitesse_vent_0_30N
                vitesse = vecteur_vitesse_vent_0_30N
            elif 30 <= lat_ij < 60:
                angle = angle_inclinaison_vecteur_vitesse_vent_30_60N
                vitesse = vecteur_vitesse_vent_30_60N
            elif 60 <= lat_ij <= 90:
                angle = angle_inclinaison_vecteur_vitesse_vent_60_90N
                vitesse = vecteur_vitesse_vent_60_90N
            elif -30 <= lat_ij < 0:
                angle = angle_inclinaison_vecteur_vitesse_vent_0_30S
                vitesse = vecteur_vitesse_vent_0_30S
            elif -60 <= lat_ij < -30:
                angle = angle_inclinaison_vecteur_vitesse_vent_30_60S
                vitesse = vecteur_vitesse_vent_30_60S
            else:
                angle = angle_inclinaison_vecteur_vitesse_vent_60_90S
                vitesse = vecteur_vitesse_vent_60_90S

            T_sol_ij_n = recuperer_T_ij_sol(mois_index, heure, i)  # Récupère la température du sol pour le mois donné

            dTij_n = dTij(mois_index, heure, angle, vitesse, lat_ij, lon_ij, fichier_temperature, longitude_0_58, latitude_0_28, T_sol_ij_n)  # Calcule le changement de température
            print(f"Changement de température dTij pour la section {i} (lat: {lat_ij}, lon: {lon_ij}) : {dTij_n:.2f} K")
            T_ij_n = T_ij_n_plus_1(T_ij_n, dTij_n, dt)
            print(f"Température T_ij à l'instant n+1 pour la section {i} (lat: {lat_ij}, lon: {lon_ij}) : {T_ij_n:.2f} K")
            # Calcul du flux convectif
            flux = Flux_th_convectif_ij_n(T_ij_n, T_sol_ij_n)
            flux_convectifs.append([lat_ij, lon_ij, flux])
            print(f"Flux convectif pour la section {i} (lat: {lat_ij}, lon: {lon_ij}) : {flux:.2f} W/m²")

        # Sauvegarde du CSV
        df_flux = pd.DataFrame(flux_convectifs, columns=["Latitude", "Longitude", "Flux_convectif_W_m2"])
        dossier_sortie = "flux_convectifs"
        os.makedirs(dossier_sortie, exist_ok=True)
        df_flux.to_csv(f"{dossier_sortie}/flux_{mois_nom}_heure{heure:02d}.csv", index=False)












