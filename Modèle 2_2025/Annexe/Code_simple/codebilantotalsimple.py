#attention pour l'instant le code presente des resultats peut réaliste, mais il utilise des fonctions simples avec les améliorations de 2025

"""code pour créer un fichier csv contenant les positions avec les températures pour une certaine durée (en heures), en utilisant différentes fonctions du groupe 3 de 2024"""


from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

stef = 5.67e-8  # constante de Stefan–Boltzmann

def convertir(degres):
    """Convertit degrés en radians."""
    return degres * 2*pi / 360

alpha = convertir(23.5)  # inclinaison Terre
R = 6_371_000            # rayon Terre (m)

# albédo par type de surface
glace, eau, neige = 0.60, 0.10, 0.80
desert, foret, terre = 0.35, 0.20, 0.15

def B_point(j):
    """Angle saisonnier pour le jour j."""
    return alpha * cos(2*pi * j / 365)

def dpuiss(lat, lng, H, puiss):
    """
    Flux direct reçu selon l'heure linéaire H (H=0→j=0,h=0, H=25→j=1,h=1, etc.).
    Renvoie la composante positive du vecteur solaire.
    """
    j = H // 24
    h = H % 24
    B = B_point(j)
    # vecteur normal local en cartesien
    theta = lng + (h-8)*2*pi/24 - pi/2
    colat = B + pi/2 - lat
    er = np.array([
        cos(theta)*sin(colat),
        sin(theta)*sin(colat),
        cos(colat)
    ])
    vec = np.dot(er, puiss)
    return max(vec, 0.0)

def albedo(lat, lng):
    '''Retourne l'albedo d'une maille en fonction de sa latitude et de sa longitude'''

    if lat >= 65 or lat <= -65 :
        return glace

    elif lng >= 160 or lng <= -140 :
        return eau

    elif lng <= -120 and lng >= -140 and lat >= -65 and lat <= 50 :
        return eau

    elif lng <= -80 and lng >= -120 and lat >= -65 and lat <= 20 :
        return eau

    elif lng <= 140 and lng >= -60 and lat >= -65 and lat <= -30 :
        return eau

    elif lng <= -60 and lng >= -80 and lat >= 10 and lat <= 40 :
        return eau

    elif lng <= 0 and lng >= -60 and lat >= 30 and lat <= 65 :
        return eau

    elif lng <= -20 and lng >= -60 and lat >= 10 and lat <= 30 :
        return eau

    elif lng <= 10 and lng >= -60 and lat >= 0 and lat <= 10 :
        return eau

    elif lng <= 10 and lng >= -40 and lat >= -30 and lat <= 0 :
        return eau

    elif lng <= 120 and lng >= 40 and lat >= 10 and lat <= 20 :
        return eau

    elif lng <= 100 and lng >= 40 and lat >= -30 and lat <= 10 :
        return eau

    elif lng <= 120 and lng >= 100 and lat >= -30 and lat <= -10 :
        return eau

    elif lng <= 140 and lng >= 120 and lat >= 0 and lat <= 30 :
        return eau

    elif lng <= 160 and lng >= 140 and lat >= 0 and lat <= 60 :
        return eau
    elif lng <= -60 and lng >= - 80 and lat<= 10 and lat >= 0 :
       return foret
    elif lng <= -40 and lng >= - 80 and lat <= 0 and lat >= -30 :
        return foret
    elif lng <= -60 and lng >= - 80 and lat <= -30 and lat >= -65 :
        return foret
    elif lng <= 40 and lng >= - 20 and lat <= 20  and lat >= -10 :
        return foret
    elif lng <= 140 and lng >= 100 and lat<= 40 and lat >= 30 :
        return foret
    elif lng <= 120 and lng >= 100 and lat<= 30 and lat >= 0 :
        return foret
    elif lng <= 160 and lng >= 100 and lat<= 0 and lat >= -10 :
        return foret
    elif lng <= 40 and lng >= 10 and lat<= -10 and lat >= -30 :
        return desert
    elif lng <= 60 and lng >= 0 and lat<= 40 and lat >= 20 :
        return desert
    elif lng <= 160 and lng >= 120 and lat<= -10 and lat >= -30 :
        return desert
    elif lng <= -80 and lng >= - 120 and lat<= 50 and lat >= 20 :
        return terre
    elif lng <= 140 and lng >= 0 and lat<= 60 and lat >= 30 :
        return terre
    elif lng <= 60 and lng >= 40 and lat<= 40 and lat >= 20 :
        return terre
    elif lng <= 100 and lng >= 40 and lat<= 40 and lat >= 20 :
        return terre
    else:
        return neige

def puiss_sol(lat, lng, H, puiss):
    """
    '''Calcule la puissance totale reçue par la pacelle de sol après les différents rebonds liés à l'effet de serre, mais sans prendre en compte la réémission propre au corps noir qu'est la Terre. On considère ici que l'albedo de l'atmosphère      est constant, égal à 0.8. On somme toutes les réfléxions et on a mis ici la somme de la série, qui est une série géométrique de raison strictement inférieure à 1.'''
    """
    # a = albedo(lat, lng)
    # direct = dpuiss(lat, lng, H, puiss)
    # # somme géométrique des multiples réflexions
    # return 0.8*(1-a)*direct / (1 - 0.2*a)
    T_atmo = 273 # Kelvin (a modifié)
    puissance_effet_serre = (sigma*T_atmo** 4)
    tot = dpuiss(lat, lng, H, puiss)+puissance_effet_serre
    t=dpuiss(lat, lng, H, puiss)
    return tot



def p_sol(lat, lng, H, puiss):
    """
    Flux reçue en tenant compte de la réémission infrarouge de la Terre.

    """
    a = albedo(lat, lng)
    P0 = puiss_sol(lat, lng, H, puiss)
    return P0*(1.2 - 0.4*a) / (1 - 0.2*a)

def puissance_cond(T_surf,temps,lat,long):
    """
    Calcule la puissance surfacique moyenne reçue à la surface pendant un temps choisie (normalement 1h),
    pour une température de surface T_surf. L’état thermique interne est mémorisé
    d’un appel à l’autre pour garantir la continuité.

    Paramètre :
      - T_surf : température imposée à la surface (°C)
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
    if not hasattr(puissance_cond, "T_state"):
        T = np.ones(N) * T_lim
    else:
        T = puissance_cond.T_state.copy()

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
    puissance_cond.T_state = T.copy()

    # puissance moyenne surfacique pendant l’heure
    puiss = flux.mean()
    return puiss

def temp(lat, lng, H, puiss):
    """
    Température noire (K) au point lat/lng à l'heure linéaire H.
    """
    p0 = p_sol(lat, lng, H, puiss)
    a = albedo(lat, lng)
    net = p0 * (1 - a)
    T = (net / stef)**0.25
    #print(f"heure linéaire {H}: T = {T-273.15:.2f} °C")
    return T

# Constantes
constante_solaire = 1361  # W/m^2, valeur moyenne au niveau de la Terre
rayon_astre = 6371  # km, par exemple le rayon de la Terre
sigma = 5.670e-8  # Constante de Stefan-Boltzmann en W/m^2/K^4
epaisseur_atmosphere = 600  # km, approximative thickness of Earth's atmosphere

rayon_astre_m = rayon_astre * 1000
epaisseur_atmosphere_m = epaisseur_atmosphere * 1000

C_CO2_moy = 400 #ppm
C_H2O_moy = 25000 #ppm

S_terre = 510 * 10**12 # m^2
# Capacité thermique massique du sol
Cpm = 1000  #J*kg**-1*K**-1
mu_sol_sec = 1000 #kg*m**-3
epaisseur = 5*10**-2 #m
# Cpm = 4180 #J*kg**-1*K**-1 pour l'eau

# Capacité thermique d'un carré
Cp = Cpm*mu_sol_sec*epaisseur*(S_terre/1800)
# print("Cp = ", Cp)

puiss = np.array([1340, 0, 0])

# Fonction calculant T1 en fonction de T0
def change_temp(temps,lat,long) :
    """mettre temps en heure et ca renvoie la temperature au point apres ce temps"""
    Ti=puiss_sol(0.0, 0.0, 0, puiss)
    Tf=0
    for i in range(1,temps+1):
        Pr=puiss_sol(lat, long, i, puiss)
        if i==1:
            Pc=0 # puissance_cond(Ti,3600,lat,long) test
            T = ((-sigma*(Ti**4)+Pr+Pc)*S_terre/325*3600)/Cp + Ti
            Tf=T
            data(Tf,lat,long,i)
        else:
            Pc=0 # puissance_cond(Tf,3600,lat,long)
            T = ((-sigma*(Tf**4)+Pr+Pc)*S_terre/325*3600)/Cp + Tf
            Tf=T
            data(Tf,lat,long,i)
    return Tf


# grille lat/lon
lats = np.arange(-90,  91, 15)   # toutes les 15° : 13 points en latitude
lngs = np.arange(-180, 181, 15)  # toutes les 15° : 25 points en longitude


# calcul sur toute la grille
datas = []
def data(T,lat,lng,H):
    datas.append({
                "lat": lat,
                "lng": lng,
                "H": H,
                "T_K": T,
                "T_C": T-273.15
            })
    return datas


def remp(T):
    for lat in lats:
        for lng in lngs:
            change_temp(T,lat,lng)

remp(24)
print(datas)

# mise en DataFrame et export CSV
df = pd.DataFrame(datas)
df.to_csv("temperature_grid6.csv", index=False)

print("Exporté temperature_grid1.csv")
