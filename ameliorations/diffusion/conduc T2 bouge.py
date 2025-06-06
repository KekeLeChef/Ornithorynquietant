import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Paramètres de la simulation
# --------------------------------------------------

L_left = 0.5          # Longueur du matériau gauche (m)
L_right = 0.5         # Longueur du matériau droit (m)
N_left = 51           # Nombre de points dans le matériau gauche (impair pour point milieu)
N_right = 51          # Nombre de points dans le matériau droit

dx = L_left / (N_left - 1)  # Même dx pour les deux matériaux
# Nombre total de nœuds en combinant les deux matériaux avec un seul nœud interface
N_total = N_left + N_right - 1

# Indices pour repérer les blocs dans le vecteur unifié
idx_left_end = N_left - 1       # indice du nœud interface (fin du bloc gauche)
idx_right_start = N_left - 1    # même indice pour début du bloc droit

alpha1 = 1e-4         # Diffusivité thermique du matériau gauche (m^2/s)
alpha2 = 1e-4         # Diffusivité thermique du matériau droit (m^2/s)

T1_initial = 100.0    # Température initiale uniforme du matériau gauche (°C)
T2_initial = 0.0      # Température initiale uniforme du matériau droit (°C)

# --------------------------------------------------
# Conditions numériques
# --------------------------------------------------

# Pas de temps respectant la condition de stabilité explicite
dt = 0.25 * dx**2 / max(alpha1, alpha2)
t_final = 10000.0
n_steps = int(np.ceil(t_final / dt))

# Indices des points milieux
mid_index_left = (N_left - 1) // 2        # milieu du bloc gauche (0-based)
mid_index_right = idx_right_start + (N_right - 1)//2  # milieu du bloc droit

# --------------------------------------------------
# Initialisation du champ de température unifié
# --------------------------------------------------

T = np.zeros(N_total)
# Bloc gauche (indices 0..N_left-1)
T[:N_left] = T1_initial
# Bloc droit (indices N_left-1..N_total-1)
T[idx_right_start:] = T2_initial

# Tableaux pour enregistrer l'évolution aux points milieux
times = np.linspace(0, t_final, n_steps+1)
T_mid_left_history = np.zeros(n_steps+1)
T_mid_right_history = np.zeros(n_steps+1)
T_mid_left_history[0] = T[mid_index_left]
T_mid_right_history[0] = T[mid_index_right]

# --------------------------------------------------
# Boucle temporelle (Euler explicite 1D unifié)
# --------------------------------------------------

for n in range(1, n_steps+1):
    T_old = T.copy()
    T_new = T_old.copy()

    # Mise à jour pour tous les nœuds intérieurs 1..N_total-2
    for i in range(1, N_total-1):
        # Choix de la diffusivité locale selon la position
        if i < idx_left_end:
            alpha = alpha1
        elif i > idx_right_start:
            alpha = alpha2
        else:
            # i == idx_left_end == idx_right_start correspond à l'interface
            alpha = alpha1

        T_new[i] = T_old[i] + dt * alpha * (T_old[i+1] - 2*T_old[i] + T_old[i-1]) / dx**2

    # Conditions aux limites isolées (flux nul)
    T_new[0] = T_new[1]
    T_new[N_total-1] = T_new[N_total-2]

    # Mise à jour du vecteur complet
    T = T_new.copy()

    # Enregistrement des températures aux points milieux
    T_mid_left_history[n] = T[mid_index_left]
    T_mid_right_history[n] = T[mid_index_right]

# --------------------------------------------------
# Tracé des résultats
# --------------------------------------------------

plt.figure(figsize=(8, 5))
plt.plot(times, T_mid_left_history, label='Point milieu matériau gauche', color='orange')
plt.plot(times, T_mid_right_history, label='Point milieu matériau droit', color='blue')
plt.xlabel('Temps (s)')
plt.ylabel('Température (°C)')
plt.title('Évolution des températures aux points milieux de chaque matériau')
plt.legend()
plt.grid(True)
plt.show()
