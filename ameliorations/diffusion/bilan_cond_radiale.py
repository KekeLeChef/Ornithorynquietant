import numpy as np
import matplotlib.pyplot as plt

def average_surface_flux(T_surface, T_depth=10.0, L=2.0, N=201,
                         alpha=5e-4, k=1.0, A=1.0, duration=3600.0):
    """
    Pour une barre 1D de longueur L (ici 2 m), 
    - extrémité haute (surface) à température fixe T_surface (°C),
    - extrémité basse (cave, 2 m plus bas) à température fixe T_depth (°C),
    résout l’équation de diffusion pendant `duration` secondes,
    puis renvoie la densité de flux surfacique à la surface et sa moyenne.

    Renvoie :
      - times         : instants (s)
      - flux_surf     : flux surfacique à x=0 (W/m²)
      - avg_flux_surf : flux moyen surfacique sur la durée (W/m²)
    """
    dx      = L / (N - 1)
    dt      = 0.25 * dx**2 / alpha #on admet loi de ...
    n_steps = int(np.ceil(duration / dt))
    times   = np.linspace(0, duration, n_steps+1)

    # Profil initial : on peut démarrer à T_depth partout
    T = np.ones(N) * T_depth

    # Conditions aux limites
    T[ 0] = T_surface  
    T[-1] = T_depth     

    # Stockage du flux à la surface
    flux_surf = np.zeros(n_steps+1)

    for n in range(1, n_steps+1):
        T_old = T.copy()

        # maj intérieure
        for i in range(1, N-1):
            T[i] = (T_old[i]
                    + alpha * dt / dx**2
                      * (T_old[i+1] - 2*T_old[i] + T_old[i-1]))
            
        # Réimposer les T aux extrema
        T[ 0] = T_surface
        T[-1] = T_depth

        # Flux à la surface (x=0) par la loi de Fourier
        # on prend le gradient vers l’intérieur : dT/dx ≈ (T[1]-T[0])/dx
        flux_surf[n] = -k * (T[1] - T[0]) / dx

    # Intégrale temporelle pour obtenir l'énergie reçue par m²
    energy_per_area = np.trapz(flux_surf, times)  # J/m²
    # Flux moyen surfacique sur toute la durée
    avg_flux_surf = energy_per_area / duration      # W/m²

    return times, flux_surf, avg_flux_surf


if __name__ == "__main__":
    # Exemple : on mesure T_surface = ..°C au sol et T_depth = ..°C dans la cave
    T_surface_input = 100.0  # °C
    T_depth_input   = 10.0  # °C

    times, flux_surf, avg_q = average_surface_flux(
        T_surface_input, T_depth_input)

    print(f"Flux surfacique moyen sur 1 h à la surface "
          f"(T_surface={T_surface_input}°C, T_depth={T_depth_input}°C) : "
          f"{avg_q:.2f} W/m²")

    # Tracé du flux surfacique en fonction du temps
    plt.figure(figsize=(8,5))
    plt.plot(times, flux_surf, color='tab:orange')
    plt.xlabel("Temps (s)")
    plt.ylabel("Flux surfacique à la surface (W/m²)")
    plt.title(f"Flux à la surface (T_surface={T_surface_input}°C)")
    plt.grid(True)
    plt.show()
