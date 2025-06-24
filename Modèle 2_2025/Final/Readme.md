## Codes principaux

Le code fonctionne avec tous les éléments ici présents :
- Le fichier modele_dynamique permet de produire un fichier csv en fonction du mois de l'année et de la durée de simulation
- Le fichier afffichage_3D permet d'afficher un des fichier csv de température (A MODIFIERRRRRRR)
- Le fichier fonctions regroupe l'intégralité des fonctions utilisées dans ces deux programmes
- Le fichier test_perf.py tente d'utiliser un système permettant d'utiliser plus de cœur du processeur pour que les calculs soient plus rapidement
  
## 12_mois

Contient les fichiers de température des 12 mois. Lors de l'affichage 3D, les valeurs sont lues dans les fichiers rescpectifs et affichées sur le modèle 3D. Cela évite le calcul permanent des températures

## Albedo

Contient les valeurs d'albédo pour différentes surfaces selon le découpage 3D fait dans le code de modélisation 3D.

## Data

Contient la position des continents. Cela permet d'afficher les contours sur la Terre en 3D
