**`Calcul_capacité_thermique_api.py`**  
   Script utilisant une API externe pour obtenir les données thermiques.  
   *Demander à Kevin pour obtenir les droits d’accès à cette API.*

**`proportion_terre_glace_eau.py`**  
Calcule la proportion de terre, d’eau et de glace pour chaque latitude et longitude, sur les 1800 sections définies.

**`Calcul_1800_capacité_fraction_terrestre.py`**  
Utilise les proportions issues du script précédent pour calculer la capacité thermique par section, en tenant compte du type de sol et de la latitude.

**`sum_capacity.py`**  
Calcule la somme des capacités thermiques de toutes les sections pour vérifier la cohérence avec la capacité thermique terrestre globale.

**`grid_1800_land_water_ice.csv`**  
Contient les proportions de terre, d’eau et de glace pour chaque section (résultat de *proportion_terre_glace_eau.py*).

**`1800_Capacity.csv`**  
  ➤ Capacité thermique calculée pour chaque section, avec des profondeurs spécifiques :  
  &nbsp;&nbsp;&nbsp;&nbsp;• Terre : 1 m  
  &nbsp;&nbsp;&nbsp;&nbsp;• Glace : 2 m  
  &nbsp;&nbsp;&nbsp;&nbsp;• Eau : 10 m

**`1800_Capacity_5cm.csv`**  
Variante simplifiée où chaque section utilise une profondeur unique de **5 cm**, quel que soit le type de sol.


