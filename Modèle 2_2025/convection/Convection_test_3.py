import numpy as np
import matplotlib.pyplot as plt

# Données physiques air (~35°C)
rho_air = 1.145
mu = 1.872e-5
k = 0.0263
cp_air = 1005
nu = mu / rho_air
Pr = cp_air * mu / k

# Données plaques (ex: aluminium)
rho_plaque = 2700
cp_plaque = 900
e = 0.05
L = 500_000
A = L**2
U = 6
T_air = 15 + 273.15

T_hot = 30 + 273.15
T_cold = 27 + 273.15

# Temps de simulation
dt = 60
t_max = 24 * 3600
n_steps = int(t_max / dt)

# Stockage résultats
times = np.arange(0, t_max, dt)
q_net_list = []

# Masse des plaques
volume = A * e
m_plaque = rho_plaque * volume

# Convection
Re = U * L / nu
Nu = 0.037 * Re**(4/5) * Pr**(1/3)
h = Nu * k / L

for t in times:
    # Flux (W/m²)
    q_hot = h * (T_hot - T_air)
    q_cold = h * (T_air - T_cold)

    # Flux net réellement transféré via l'air
    q_net = min(q_hot, q_cold)
    q_net_list.append(q_net)

    # Énergie échangée
    Q_hot = q_hot * A * dt
    Q_cold = q_cold * A * dt

    dT_hot = -Q_hot / (m_plaque * cp_plaque)
    dT_cold = Q_cold / (m_plaque * cp_plaque)

    T_hot += dT_hot
    T_cold += dT_cold

# Affichage du flux net
plt.figure(figsize=(10, 5))
plt.plot(times / 3600, q_net_list)
plt.xlabel("Temps (heures)")
plt.ylabel("Flux net transféré (W/m²)")
plt.title("Flux thermique net entre les plaques (via l'air)")
plt.grid()
plt.tight_layout()
plt.show()
