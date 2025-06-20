##SELON LA COMPOSANTE ORTHORADIALE (s'avère être négligeable)
conduction2plaquesfixe.py : Simule la diffusion thermique dans une plaque en contact avec un matériau froid, en traçant la température au point milieu gauche au cours du temps. Les CI sont fixées.

conduction2plaques.py : Modélise l’équilibrage thermique de deux moitiés de barre initialement à 100 °C et 0 °C, affichant l’évolution temporelle des températures aux centres gauche et droit. Les CI changent au cours du temps.

conduction3plaques.py : Modélise la diffusion dans trois plaques accolées à températures initiales différentes, et suit l'évolution des températures aux centres des trois plaques. Les CI changent au cours du temps.



##SELON LA COMPOSANTE RADIALE
conduction_radiale.py: Calcule la puissance surfacique moyenne reçue à la surface en fonction de la température imposée et conserve la mémoire au cours du temps.

Bilan_cond_radiale1.0.py : Résout la diffusion thermique 1D dans une barre de 2 m entre une surface et une cave à températures fixées, puis trace et calcule la puissance surfacique instantané et moyen sur 1 h.

Bilan_cond_radiale2.0.py : Version améliorée de ilan_cond_radiale1.0.py

diffusionpuissancefinal.py: Utilise la température de surface horaire pour simuler la diffusion thermique en profondeur et tracer l'évolution horaire de la puissance moyenne reçue. Fichier dont on a augmenté la portabilité et que les autres groupes utiliseront par la suite.
