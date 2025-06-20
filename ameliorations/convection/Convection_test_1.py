import numpy as np

# Constantes physiques de l'air à ~35°C
rho = 1.145      # kg/m³ (masse volumique)
mu = 1.872e-5    # Pa.s (viscosité dynamique)
k = 0.0263       # W/m.K (conductivité thermique)
cp = 1005        # J/kg.K (chaleur spécifique)
nu = mu / rho    # viscosité cinématique
Pr = cp * mu / k # nombre de Prandtl

# Données du problème
U = 6            # m/s (vitesse du vent)
L = 500_000      # m (longueur caractéristique = taille plaque)
T_hot = 50 + 273.15   # K
T_cold = 15 + 273.15  # K
T_air = 15 + 273.15   # K

# Calcul du nombre de Reynolds
Re = U * L / nu

# Calcul du nombre de Nusselt (pour plaque chauffée en régime laminaire ou transition)
Nu = 0.037 * Re**(4/5) * Pr**(1/3)  # Formule de Dittus-Boelter (approximation acceptable ici)

# Coefficient de convection
h = Nu * k / L

# Flux thermique par m² de la plaque chaude vers l’air
q_hot = h * (T_hot - T_air)  # W/m²

# Flux thermique par m² de l’air vers la plaque froide
q_cold = h * (T_air - T_cold)  # W/m²

# Flux net disponible pour transfert entre plaques via l'air
q_net = min(q_hot, q_cold)

print(f"Coefficient de convection h = {h:.2f} W/m²·K")
print(f"Flux de chaleur depuis plaque chaude : {q_hot:.2f} W/m²")
print(f"Flux de chaleur vers plaque froide : {q_cold:.2f} W/m²")
print(f"Flux net transmissible via l'air : {q_net:.2f} W/m²")
