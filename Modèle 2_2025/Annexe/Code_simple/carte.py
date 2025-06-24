"""Code qui permet d'afficher les differents points de température sur une carte en ligne à partir du fichier CSV contenant position et température"""

import pandas as pd
import plotly.express as px

# 1) Charger le CSV que vous avez généré
df = pd.read_csv("temperature_grid6.csv") #mettre votre fichier csv

# 2) Tracer la carte avec slider sur l’heure H
fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lng",
    color="T_C",               # température en °C
    animation_frame="H",       # curseur sur l’heure linéaire H
    projection="natural earth",
    color_continuous_scale="RdYlBu_r",
    title="Température du sol (°C) — évolution horaire"
)

# 3) Ajustements esthétiques
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="lightgray",
        showcountries=True
    ),
    coloraxis_colorbar=dict(title="T (°C)")
)

# 4) Afficher la carte interactive
fig.show()
