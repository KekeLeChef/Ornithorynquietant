import numpy as np
import matplotlib.pyplot as plt

"""
Simulation de la diffusion thermique dans une barre 1D de longueur 2*L_bar,
constituée de deux moitiés identiques accolées, avec conditions initiales
différentes sur chaque moitié.

Paramètres :
- L_bar   : longueur d’une moitié de la barre (m)
- N_bar   : nombre de nœuds par moitié (impair pour point milieu exact)
- D       : diffusivité thermique homogène dans toute la barre (m²/s)
- T_left  : température initiale moitié gauche (°C)
- T_right : température initiale moitié droite (°C)
- t_final : durée de la simulation (s)

Maillage :
- dx      = L_bar / (N_bar - 1)
- N_total = 2 * N_bar - 1  (interface unique)

Sorties :
- hL, hR  : vecteurs des températures au centre de chaque moitié
- times   : vecteur des instants de simulation
"""

# Paramètres
L_bar   = 0.5        # m
N_bar   = 51        # impair
D       = 1.4e-4     # m²/s attention: change énormément résultats
T_left  = 10000.0      # °C
T_right = 0.0        # °C
t_final = 5000.0    # s

# Maillage
dx      = L_bar / (N_bar - 1)
N_total = 2 * N_bar - 1

# Indices des centres
center_left  = (N_bar - 1) // 2
center_right = center_left + (N_bar - 1)

# Initialisation de T
T = np.zeros(N_total)
for i in range(N_total):
    if i <= N_bar - 1:
        T[i] = T_left
    else:
        T[i] = T_right

# Discrétisation temporelle
dt      = 0.25 * dx**2 / D
n_steps = int(np.ceil(t_final / dt))
times   = np.linspace(0, t_final, n_steps+1)

# Historique
hL = np.empty(n_steps+1)
hR = np.empty(n_steps+1)
hL[0] = T[center_left]
hR[0] = T[center_right]

# Boucle temporelle
for n in range(1, n_steps+1):
    T_old = T.copy()
    # mettre à jour chaque nœud intérieur
    for i in range(1, N_total-1):
        T[i] = T_old[i] + D * dt *((T_old[i+1] - 2*T_old[i] + T_old[i-1]) / dx**2)

    # conditions aux limites isolées
    T[0]      = T[1]
    T[-1]     = T[-2]
    # enregistrer
    hL[n] = T[center_left]
    hR[n] = T[center_right]

# Tracé
plt.figure(figsize=(8,5))
plt.plot(times, hL, label='plaque gauche', color='orange')
plt.plot(times, hR, label='plaque droite', color='blue')
plt.xlabel('Temps (s)')
plt.ylabel('Température (°C)')
plt.title('Évolution dans les plaques')
plt.legend()
plt.grid(True)
plt.show()
