import numpy as np
import matplotlib.pyplot as plt

# Données physiques air (~35°C)
rho_air = 1.145      # kg/m³
mu = 1.872e-5        # Pa.s
k = 0.0263           # W/m.K
cp_air = 1005        # J/kg.K
nu = mu / rho_air
Pr = cp_air * mu / k

# Données plaques (ex: aluminium)
rho_plaque = 2700    # kg/m³
cp_plaque = 900      # J/kg.K
e = 0.05             # m (épaisseur de 5 cm)
L = 500_000          # m (taille plaque)
A = L**2             # m² (surface)

# Vent et température air
U = 6                # m/s
T_air = 35 + 273.15  # K

# Températures initiales des plaques
T_hot = 50 + 273.15   # K
T_cold = 20 + 273.15  # K

# Temps de simulation
dt = 60              # s (1 minute)
t_max = 3600 * 4     # 4 heures
n_steps = int(t_max / dt)

# Préparation pour enregistrement
times = np.arange(0, t_max, dt)
T_hot_list = []
T_cold_list = []

# Masse des plaques
volume = A * e
m_plaque = rho_plaque * volume

# Calcul du nombre de Reynolds et Nusselt
Re = U * L / nu
Nu = 0.037 * Re**(4/5) * Pr**(1/3)
h = Nu * k / L

for t in times:
    # Enregistrement des températures actuelles
    T_hot_list.append(T_hot - 273.15)
    T_cold_list.append(T_cold - 273.15)

    # Flux de chaleur entre plaques et air
    q_hot = h * (T_hot - T_air)     # W/m²
    q_cold = h * (T_air - T_cold)   # W/m²

    # Énergie échangée (positive = perte pour la plaque chaude)
    Q_hot = q_hot * A * dt          # J
    Q_cold = q_cold * A * dt        # J

    # Variation de température
    dT_hot = -Q_hot / (m_plaque * cp_plaque)
    dT_cold = Q_cold / (m_plaque * cp_plaque)

    # Mise à jour
    T_hot += dT_hot
    T_cold += dT_cold

# Affichage
plt.figure(figsize=(10, 5))
plt.plot(times / 3600, T_hot_list, label="Plaque chaude (°C)")
plt.plot(times / 3600, T_cold_list, label="Plaque froide (°C)")
plt.xlabel("Temps (heures)")
plt.ylabel("Température (°C)")
plt.title("Évolution des températures des plaques")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
