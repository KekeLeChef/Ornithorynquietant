import numpy as np
import matplotlib.pyplot as plt

# Paramètres physiques et numériques
L       = 10          # longueur de la barre (m)
N       = 13           # nombre de nœuds (impair pour point milieu exact)
dx      = L/(N-1)      # pas spatial
D       = 5e-4         # diffusivité (m²/s)
T0      = 10        # température initiale (°C) sur tout le segment
T_fixed = 15.0        # extrémité droite maintenue à cette T (°C)

dt      = 0.25*dx**2/D # pas de temps pour stabilité explicite
t_final = 100000.0      # durée totale (s)
n_steps = int(np.ceil(t_final/dt))
times   = np.linspace(0, t_final, n_steps+1)

# Initialisation
T = np.ones(N)*T0
T_history_left = np.zeros(n_steps+1)
T_history_left[0] = T[0]  # température à l'extrémité gauche (i=0)

# Boucle temporelle (Euler explicite)
for n in range(1, n_steps+1):
    T_old = T.copy()
    # mise à jour intérieure
    for i in range(1, N-1):
        T[i] = T_old[i] + D*dt*(T_old[i+1] - 2*T_old[i] + T_old[i-1])/dx**2
    # conditions aux limites
    T[0]   = T[1]       # bord gauche isolé
    T[-1]  = T_fixed    # bord droit fixe
    # enregistrement
    T_history_left[n] = T[0]

# Tracé
plt.figure(figsize=(8,5))
plt.plot(times, T_history_left, color='orange')
plt.xlabel('Temps (s)')
plt.ylabel('Température à l\'extrémité gauche (°C)')
plt.title('Evolution de la température à l\'extrémité libre')
plt.grid(True)
plt.show()
