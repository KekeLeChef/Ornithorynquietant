import numpy as np
import matplotlib.pyplot as plt

def compute_surf_flux(T_surf,
                      T_lim=18.0,
                      L=1.0,
                      N=51,
                      alpha=5e-4,
                      k=1.0,
                      A=1.0,
                      duration=3600.0):
    """
    Simule la diffusion dans une barre 1D de longueur L, extrémité gauche
    fixée à T_lim et extrémité droite à T_surf, sur une heure (3600 s),
    et renvoie :
      - times      : instants de calcul
      - flux_surf  : flux surfacique à la surface de la terre (W/m²)
      - avg_surf   : puissance moyenne surfacique reçue à la surface sur 1 h

    Paramètres :
      T_surf   : température de l'extrémité surface (°C)
      T_lim    : température de l'extrémité de la limite de variation de temperature (°C)
      L, N, alpha, k, A, duration  : voir Fourier diffusion 1D
    """
    dx      = L / (N - 1)
    dt      = 0.25 * dx**2 / alpha
    n_steps = int(np.ceil(duration / dt))
    times   = np.linspace(0, duration, n_steps+1)

    # profil initial
    T = np.ones(N) * T_lim
    T[0]   = T_lim
    T[-1]  = T_surf

    flux_surf = np.zeros(n_steps+1)
    flux_surf[0] = 0.0  # pas de gradient initial

    for n in range(1, n_steps+1):
        T_old = T.copy()
        # mise à jour intérieure
        for i in range(1, N-1):
            T[i] = (T_old[i]
                    + alpha * dt * (T_old[i+1] - 2*T_old[i] + T_old[i-1]) / dx**2)
        # conditions aux limites
        T[0]   = T_lim
        T[-1]  = T_surf
        # calcul du flux ("surf")
        flux_surf[n] = -k * (T[1] - T[0]) / dx * A #loi de Newton

    # énergie reçue par unité de surface (J/m²)
    E_surf = np.trapz(flux_surf, times)
    # puissance moyenne sur 1 h (W/m²)
    avg_surf = E_surf / duration

    return times, flux_surf, avg_surf

# Exemple d'utilisation
if __name__ == "__main__":
    T_surf_input = 15.0  # °C
    times, flux_surf, avg_surf = compute_surf_flux(T_surf_input, T_lim=18.0)

    print(f"Puissance surfacique moyenne (surf) : {avg_surf:.2f} W/m²")

    # Tracé du flux surfacique
    plt.figure(figsize=(8,5))
    plt.plot(times, flux_surf, label='surf', color='tab:blue')
    plt.xlabel("Temps (s)")
    plt.ylabel("Flux surfacique surface (W/m²)")
    plt.title(f"Flux à l'extrémité surface sur 1 h (T_surf={T_surf_input}°C)")
    plt.legend()
    plt.grid(True)
    plt.show()
