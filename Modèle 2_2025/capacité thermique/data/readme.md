Les fichiers `ne_10m_coastline.shp`, `.shx` et `.dbf` (Natural Earth) décrivent les lignes côtières mondiales à 10m de résolution.  
Ils sont utilisés pour **délimiter les zones terrestres** lors des calculs ou visualisations de **diffusion thermique et de température**.

**`grid_1800_land_water_ice.csv`**  
Contient les proportions de terre, d’eau et de glace pour chaque section (résultat de *proportion_terre_glace_eau.py*).

**`1800_Capacity.csv`**  
  ➤ Capacité thermique calculée pour chaque section, avec des profondeurs spécifiques :  
  &nbsp;&nbsp;&nbsp;&nbsp;• Terre : 1 m  
  &nbsp;&nbsp;&nbsp;&nbsp;• Glace : 2 m  
  &nbsp;&nbsp;&nbsp;&nbsp;• Eau : 10 m

**`1800_Capacity_5cm.csv`**  
Variante simplifiée où chaque section utilise une profondeur unique de **5 cm**, quel que soit le type de sol.



