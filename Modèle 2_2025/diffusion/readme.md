## Selon la composante orthoradiale (s'avère être négligeable dans notre modèle final)
**`conduction2plaquesfixe.py`** : Simule la diffusion thermique dans une plaque en contact avec un matériau froid, en traçant la température au point milieu gauche au cours du temps. Les CI sont fixées.

**`conduction2plaques.py`** : Modélise l’équilibrage thermique de deux moitiés de barre initialement à 100 °C et 0 °C, affichant l’évolution temporelle des températures aux centres gauche et droit. Les CI changent au cours du temps.

**`conduction3plaques.py`** : Modélise la diffusion dans trois plaques accolées à températures initiales différentes, et suit l'évolution des températures aux centres des trois plaques. Les CI changent au cours du temps.



## Selon la composante radiale
**`conduction_radiale.py`**: Calcule la puissance surfacique moyenne reçue à la surface en fonction de la température imposée et conserve la mémoire au cours du temps.

**`bilan_cond_radiale1.0.py`** : Résout la diffusion thermique 1D dans une barre de 2 m entre une surface et une cave à températures fixées, puis trace et calcule la puissance surfacique instantané et moyen sur 1 h.

**`bilan_cond_radiale2.0.py`** : Version améliorée de bilan_cond_radiale1.0.py

**`diffusionpuissancefinal.py`**: Utilise la température de surface horaire pour simuler la diffusion thermique en profondeur et tracer l'évolution horaire de la puissance moyenne reçue. Fichier dont on a augmenté la portabilité et que les autres groupes utiliseront par la suite.


## Fichiers finaux
**`carte.py`**: Génère une carte interactive de la température du sol en fonction de la latitude, de la longitude et de l’heure, avec un curseur permettant de visualiser l’évolution horaire à partir de la lecture du fichier **temperature_grid6.csv**

**`bilantotalsimple.py`**: Simulation simplifiée du bilan radiatif et conductif de la surface terrestre dont on déduit les températures résultantes de la surface exportées via **temperature_grid6.csv**.



