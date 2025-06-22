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

# Récupère la température T_ij du sol pour le mois et l'heure donnés à partir des fichiers CSV
def recuperer_T_ij_sol(month):
    filename = f"temperature_sol_mois/temperature_mois{month:02d}_sol_1800_sections.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        T_ij_sol = df["Temperature_K"].values   # Récupère la température de la section ij
        print(f"Température pour le mois {month}, heure {hour} : {T_ij_sol}")
    return T_ij_sol

# Calcule la puissance totale reçue par l'atmosphère (W) à partir des fichiers csv qui donne # la puissance solaire reçue par l'atmosphère et loi de Stefn-Boltzmann.
def puissance_total_reçu_atm(month, hour):
    T_ij_sol = recuperer_T_ij_sol(month)  # Récupère la température du sol pour le mois donné
    filename = f"puissance_reçu_atm/solar_power_month{month:02d}_hour{hour:02d}.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        puissance_totale = df["Power_W_m2"].sum() + sigma * (T_ij_sol**4)
        print(f"Puissance totale reçue pour le mois {month}, heure {hour} : {puissance_totale} W")
    return puissance_totale

# Gradient température de l'air dans l'atmosphère sur x (K/m)
def gradient_temperature_air_x():
    return dT_dx

# Gradient température de l'air dans l'atmosphère sur y (K/m)
def gradient_temperature_air_y():
    return dT_dy

# Calcule le changement de température dTij entre deux instants.
def dTij(month, hour):
    P_reçu_atm_ij = puissance_total_reçu_atm(month, hour)  # Récupère la puissance reçue par l'atmosphère
    dT_dt = P_reçu_atm_ij/cp_air_atm_section
    dx_dt = np.cos(np.radians(angle_inclinaison_vecteur_vitesse_vent_0_30N)) * vecteur_vitesse_vent_0_30N # Projection vecteur vitesse du vent sur l'axe x
    dy_dt = np.sin(np.radians(angle_inclinaison_vecteur_vitesse_vent_0_30N)) * vecteur_vitesse_vent_0_30N # Projection vecteur vitesse du vent sur l'axe y
    dT_dx = gradient_temperature_air_x()
    dT_dy = gradient_temperature_air_y()
    return dT_dt + dx_dt * dT_dx + dy_dt * dT_dy

# Calcule la température T_ij à l'instant n+1 à partir de T_ij à l'instant n et du changement de température dTij.
def T_ij_n_plus_1 (T_ij_n, dTij, dt):
    return T_ij_n + dTij * dt

# Calcule la puissance échangée entre l'air et le sol à l'instant n pour la section ij.
def Puissance_reçu_ij_n(T_atm_ij_n_plus_1, T_sol_ij_n, h):
    return h * (T_atm_ij_n_plus_1 - T_sol_ij_n)

# Début code principal
sigma = 5.67e-8  # Constante de Stefan-Boltzmann (W/m²/K⁴)
angle_inclinaison_vecteur_vitesse_vent_0_30N = 23 # Angle d'inclinaison du vecteur de convection (en degrés)
vecteur_vitesse_vent_0_30N = 30 # Vitesse du vent (en m/s)
cp_air_atm_section = cp_air_atm()









