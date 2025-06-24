
**`Calcul_capacité_thermique_api.py`**  
   Script utilisant une API externe pour obtenir les données thermiques.  
   *Demander à Kevin pour obtenir les droits d’accès à cette API.*

**`proportion_terre_glace_eau.py`**  
Calcule la proportion de terre, d’eau et de glace pour chaque latitude et longitude, sur les 1800 sections définies.

**`Calcul_1800_capacité_fraction_terrestre.py`**  
Utilise les proportions issues du script précédent pour calculer la capacité thermique par section, en tenant compte du type de sol et de la latitude.

**`sum_capacity.py`**  
Calcule la somme des capacités thermiques de toutes les sections pour vérifier la cohérence avec la capacité thermique terrestre globale.
