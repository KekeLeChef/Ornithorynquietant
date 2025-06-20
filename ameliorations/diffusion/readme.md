Se trouvent dans ce dossier les modèles python recensant mes modèles discrets de l'évolution de la température de surface terrestre par conduction au cours du temps.

Les fichiers "conduction2plaques" "conduction3plaques" modélisent la diffusion selon 1 dimension, entre 2 respectivement et 3 plaques. Ils voient leurs conditions limite évoluer au cours du temps, Contrairement au fichier "conduction2plaquesfixe" dont les conditions limites de température aux bords de la plaque ne varient pas.

Les fichiers bilan_cond_radialei.0 (i= 1;2; ou 3) correspondent à l'évolution de la puissance surfacique des plaques au cours du temps (chaque heure) 

Bilan _cond_radiale1.0.py : Résout la diffusion thermique 1D dans une barre de 2 m entre une surface et une cave à températures fixées, puis trace et calcule la puissance surfacique instantané et moyen sur 1 h.

Bilan _cond_radiale2.0.py : Simule pendant 1 h la diffusion dans une barre de 1 m avec un côté maintenu à 18 °C et l’autre à T_surf, renvoyant le flux et la puissance moyenne reçus en surface.

conduction2plaques.py : Modélise l’équilibrage thermique de deux moitiés de barre initialement à 100 °C et 0 °C, affichant l’évolution temporelle des températures aux centres gauche et droit.
