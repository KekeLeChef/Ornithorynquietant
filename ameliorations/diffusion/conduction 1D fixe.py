"""on considere deux plaques avec celle de droite de temperature fixe, et on trace la temperature de celle de gauche en fonction du temps"""


import numpy as np
import matplotlib.pyplot as plt



L_left = 0.5          # Longueur du matériau gauche (m)
N_left = 51           # Nombre de points dans le matériau gauche (doit être impair pour un point milieu)
dx = L_left / (N_left - 1)
x_left = np.linspace(0, L_left, N_left)

alpha1 = 1e-4         # Diffusivité thermique du matériau gauche (m^2/s)
T1_initial = 100.0    # Température initiale uniforme du matériau gauche (°C)
T2_fixed = 0.0       # Température constante du matériau droit (°C)



# Pas de temps respectant la condition de stabilité explicite
dt = 0.25 * dx**2 / alpha1
t_final = 20000.0
n_steps = int(np.ceil(t_final / dt))

# On identifie l'indice du point milieu dans le matériau gauche
mid_index_left = (N_left - 1) // 2


# Initialisation du champ de température


T = np.ones(N_left) * T1_initial  # Température dans le bloc gauche, initialement T1_initial

# Tableaux pour enregistrer l'évolution au point milieu
times = np.linspace(0, t_final, n_steps+1)
T_mid_history = np.zeros(n_steps+1)
T_mid_history[0] = T[mid_index_left]

# Boucle temporelle (Euler explicite 1D)

for n in range(1, n_steps+1):
    T_old = T.copy()
    T_new = T_old.copy()

    # Mise à jour des points intérieurs (i = 1 à N_left-2)
    for i in range(1, N_left-1):
        # Si i est juste avant la frontière droite, la température du voisin droit est T2_fixed
        if i == N_left - 2:
            T_right = T2_fixed
        else:
            T_right = T_old[i + 1]
        T_new[i] = T_old[i] + dt * alpha1 * (T_right - 2*T_old[i] + T_old[i-1]) / dx**2

    # Condition isolée à gauche (flux nul): T_new[0] = T_new[1]
    T_new[0] = T_new[1]

    # À l'interface (dernier point à droite du matériau gauche), on fixe directement T2
    T_new[N_left-1] = T2_fixed

    # Mise à jour pour l'itération suivante
    T = T_new.copy()

    # Enregistrement de la température au point milieu
    T_mid_history[n] = T[mid_index_left]

# Tracé du résultat


plt.figure(figsize=(8, 5))
plt.plot(times, T_mid_history, color='orange')
plt.xlabel('Temps (s)')
plt.ylabel('Température au point milieu (°C)')
plt.title('Évolution de la température au point milieu du matériau gauche')
plt.grid(True)
plt.show()
