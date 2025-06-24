import numpy as np
import shapefile
import matplotlib.pyplot as plt
from matplotlib import cm
from fonctions_modifie2 import update_sun_vector, project_to_sphere, get_shape, get_albedo, calc_power_temp, update_plot, slider_update, set_mois, temp_dans_csv, puissance_cond, change_temp, get_Cp




#Surface

def P_abs_surf_solar(time, mois, sun_vector, x, y, z, phi, theta, constante_solaire, sigma, rayon_astre_m, list_albedo, latitudes, longitudes):
    """
    Calcule la puissance solaire reçue et la température en fonction de l'heure et du mois.

    Paramètres:
    time (float): Heure de la journée (1-24).
    mois (int): Mois de l'année (1-12).
    sun_vector (numpy.ndarray): Vecteur solaire initial.
    x, y, z (numpy.ndarray): Coordonnées de la grille sphérique.
    phi, theta (numpy.ndarray): Coordonnées angulaires de la grille sphérique.
    constante_solaire (float): Constante solaire (W/m^2).
    sigma (float): Constante de Stefan-Boltzmann (W/m^2/K^4).
    rayon_astre_ m (float): Rayon de l'astre en mètres.
    list_albedo (list): Grilles d'albédo pour chaque mois.
    latitudes, longitudes (numpy.ndarray): Latitudes et longitudes des données d'albédo.

    Retours:
    tuple: Puissance reçue (numpy.ndarray) et température (numpy.ndarray).

    La matrice de rotation fait pivoter le vecteur solaire autour de l'axe z. L'angle d'incidence est calculé,
    puis l'albédo est mappé sur la grille pour ajuster la puissance reçue. La température est déterminée
    par la loi de Stefan-Boltzmann.
    """
    angle_rotation = (time / 24) * 2 * np.pi  # Conversion du temps en angle
    rotation_matrix = np.array([
        [np.cos(angle_rotation), -np.sin(angle_rotation), 0],
        [np.sin(angle_rotation), np.cos(angle_rotation), 0],
        [0, 0, 1]
    ])

    sun_vector_rotated = np.dot(rotation_matrix, update_sun_vector(mois, sun_vector))

    normal = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
    cos_theta_incidence = np.clip(np.dot(normal.T, sun_vector_rotated), 0, 1).T

    albedo_grid_mapped = np.zeros_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            lon   , lat = np.degrees(phi[i, j]), 90 - np.degrees(theta[i, j])
            if lon > 180:
                lon -= 360
            albedo_grid_mapped[i, j] = get_albedo(lat, lon, mois, list_albedo, latitudes, longitudes)

    coef_reflexion = albedo_grid_mapped

    # Puissance solaire + albédo
    puissance_recue = constante_solaire * cos_theta_incidence * (1 - coef_reflexion)

#Ajout de l'effet de serre

    # Température constante de l'atmosphère (pour l'instant)
    T_atmo = 288 # Kelvin
    puissance_effet_serre = (sigma*T_atmo** 4)

    # Puissance totale reçue
    puissance_recue += puissance_effet_serre

    temperature = (puissance_recue / sigma) ** 0.25

    return puissance_recue, temperature


# Diffusion
def P_em_diffusion(T_surf,temps,lat,long):
    """
    Calcule la puissance surfacique moyenne reçue à la surface pendant un temps choisie (normalement 1h),
    pour une température de surface T_surf. L’état thermique interne est mémorisé
    d’un appel à l’autre pour garantir la continuité.

    Paramètre :
      - T_surf : température imposée à la surface (K)
      -temps: durée de diffusion
      -long:longitude
      -lat:latitude

    Retour :
      - puiss : puissance surfacique moyenne reçue pendant cette heure (W/m²)
    """
    # Paramètres physiques et numériques fixes
    N       = 13        # nœuds (precision du calcul, il faut un nombre impaire)
    L       = 10.0       # m, profondeur où la temperature est stable
    k       = 0.75       # conductivité

    #cette partie devra etre réutilisé en prennant en compte que le coeff de diffusion change en fonction de la position
    #c=capacité(long,lat) #capacité
    #v= (510e6*0.05)/1800    #volume du decopoupage
    #D=(v*k)/c  # coeff de diffusion

    D=5e-5     # coeff de diffusion provisoire
    T_lim = 288      # température en profondeur (K), provisoire aussi car elle change en fonction de la postion , /!\ cette temperature est pour 10m (environ temperature moyenne anuelle de surface)


    dx   = L / (N - 1)
    dt   = 0.25 * dx**2 / D
    steps = int(np.ceil(temps / dt))

    # Récupération ou initialisation du profil
    if not hasattr(P_em_diffusion, "T_state"):
        T = np.ones(N) * T_lim
    else:
        T = P_em_diffusion.T_state.copy()

    # impose immédiatement les températures aux deux extrémités
    T[0], T[-1] = T_lim, T_surf

    # calcul du flux surfacique à la surface à chaque pas
    flux = np.zeros(steps+1)
    flux[0] = -k * (T[1] - T[0]) / dx

    for n in range(1, steps+1):
        T_old = T.copy()
        T[1:-1] = (
            T_old[1:-1]
            + D * dt * (T_old[2:] - 2*T_old[1:-1] + T_old[:-2]) / dx**2
        )
        T[0], T[-1] = T_lim, T_surf
        flux[n] = -k * (T[1] - T[0]) / dx

    # stockage de l'état final pour l'appel suivant
    P_em_diffusion.T_state = T.copy()

    # puissance moyenne surfacique pendant l’heure
    puiss = flux.mean()
    return puiss

# Atmosphere

# #Ajout de l'effet de serre (dans P_abs_surf_solar)
#
#     # Température constante de l'atmosphère (pour l'instant)
#     T_atmo = 288 # Kelvin
#     puissance_effet_serre = (sigma*T_atmo** 4)
#
#     # Puissance totale reçue
#     puissance_recue += puissance_effet_serre
#
#     temperature = (puissance_recue / sigma) ** 0.25
#
#     return puissance_recue, temperature

def P_abs_atm_solar(lat: float, long: float, t: float, Pinc: float):
    AbsAtmo = 0.22
    return 0


def P_abs_atm_thermal(lat: float, long: float, t: float, T: float):
    return 0


def P_em_atm_thermal_up(lat: float, long: float, t: float):
    return 0


def P_em_atm_thermal_down(lat: float, long: float, t: float):
    return 0