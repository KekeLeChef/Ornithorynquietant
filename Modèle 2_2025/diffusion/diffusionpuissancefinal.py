import numpy as np
import matplotlib.pyplot as plt

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

    D=5e-6     # coeff de diffusion provisoire
    T_lim = 15.0      # température en profondeur (°C), provisoire aussi car elle change en fonction de la postion , /!\ cette temperature est pour 10m (environ temperature moyenne anuelle de surface)


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

# Exemple d’utilisation et tracé
if __name__ == "__main__":
    temps_surface = [10,10,12,12,15,15,18,18,10,10,12,12,15,15,18,18,10,10,12,12,15,15,18,18,10,10,12,12,15,15,18,18,10,10,12,12,15,15,18,18,10,10,12,12,15,15,18,18]  # T_surf pour heures 1,2,3,...
    puissances = []

    for T_s in temps_surface:
        p = puissance_cond(T_s,3600,0,0)
        puissances.append(p)
        print(f"T_surf={T_s:.1f}°C → puissance moyenne reçue = {p:.2f} W/m²")

    # Tracé des puissances par heure
    heures = np.arange(1, len(temps_surface) + 1)
    plt.figure(figsize=(8,5))
    plt.plot(heures, puissances, marker='o', linestyle='-')
    plt.xticks(heures)
    plt.xlabel("Numéro de l'heure")
    plt.ylabel("Puissance moyenne reçue (W/m²)")
    plt.title("Puissance surfacique reçue chaque heure")
    plt.grid(True)
    plt.show()
