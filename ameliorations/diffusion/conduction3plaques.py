import numpy as np
import matplotlib.pyplot as plt

"""
Simulation de la diffusion thermique dans une barre 1D composée de trois plaques
accollées (gauche, principale, droite), avec mise à jour entièrement basée sur
l’ancien profil pour garantir un traitement symétrique à l’interface.

Paramètres :
- L_seg     : longueur de chaque plaque (m)
- N_seg     : nombre de nœuds par plaque (impair pour point milieu exact)
- D         : diffusivité thermique homogène (m²/s)
- T_left    : température initiale plaque gauche (°C)
- T_main    : température initiale plaque principale (°C)
- T_right   : température initiale plaque droite (°C)
- t_final   : durée de la simulation (s)

Maillage :
- dx        = L_seg / (N_seg - 1)
- N_total   = 3 * N_seg - 2   (interfaces uniques, un nœud commun à chaque jonction)

Sorties :
- hL, hM, hR : températures aux centres des plaques gauche, principale et droite
- times      : vecteur des instants de simulation
"""

# Paramètres
L_seg   = 0.1        # m
N_seg   = 51          # impair
D       = 1e-4       # m²/s
T_left  = 50.0       # °C
T_main  =  0.0       # °C
T_right = 50.0       # °C
t_final = 1000.0     # s

# Maillage
dx      = L_seg / (N_seg - 1)
N_total = 3 * N_seg - 2

# Indices des centres
cL = (N_seg - 1)//2
cM = cL + (N_seg - 1)
cR = cM + (N_seg - 1)

# Initialisation de la température
T = np.zeros(N_total)
T[:N_seg]           = T_left
T[N_seg-1:2*N_seg-1] = T_main
T[2*N_seg-2:]       = T_right

# Discrétisation temporelle
dt      = 0.25 * dx**2 / D
n_steps = int(np.ceil(t_final / dt))
times   = np.linspace(0, t_final, n_steps+1)

# Préallocation des historiques
hL = np.empty(n_steps+1)
hM = np.empty(n_steps+1)
hR = np.empty(n_steps+1)
hL[0], hM[0], hR[0] = T[cL], T[cM], T[cR]

# Boucle d’Euler explicite, usage de T_old et T_new pour symétrie
for n in range(1, n_steps+1):
    T_old = T.copy()
    T_new = T_old.copy()   # on initialise avec l’ancien profil

    # mise à jour de chaque nœud intérieur à partir de T_old seul
    for i in range(1, N_total-1):
        lap = (T_old[i+1] - 2*T_old[i] + T_old[i-1]) / dx**2
        T_new[i] = T_old[i] + D * dt * lap

    # conditions aux limites isolées (flux nul)
    T_new[0]    = T_new[1]
    T_new[-1]   = T_new[-2]

    # on remplace l’ancien profil par le nouveau, en une seule opération
    T = T_new

    # enregistrement
    hL[n] = T[cL]
    hM[n] = T[cM]
    hR[n] = T[cR]

# Tracé des résultats
plt.figure(figsize=(8,5))
plt.plot(times, hL, label='Centre plaque gauche',  color='orange')
plt.plot(times, hM, label='Centre plaque principale', color='green')
plt.plot(times, hR, label='Centre plaque droite',   color='blue')
plt.xlabel('Temps (s)')
plt.ylabel('Température (°C)')
plt.title('Évolution au centre de chaque plaque')
plt.legend()
plt.grid(True)
plt.show()
