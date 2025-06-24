### TRES IMPORTANT

Le fichier **`testCp`** permet de **calculer la capacité thermique** d'un carré de taille prédéfinie en utilisant les données de **l'ESA**.  
Pour cela, se rendre sur leur site : [https://worldcover2021.esa.int/download](https://worldcover2021.esa.int/download)  
Puis appuyer sur **"Download product"**.

**!! ATTENTION !!**  
Le fichier est **lourd**. Si vous voulez ne faire qu’un test, il est préférable de ne télécharger qu’**une image en `.tif`**.  
Pour cela, appuyer sur le lien au-dessus du bouton **"Download product"** :  
[https://doi.org/10.5281/zenodo.7254221](https://doi.org/10.5281/zenodo.7254221)  
Celui-ci donne accès aux **images sans avoir à télécharger un fichier `.zip`**.

**`sum_capacity.py`**
Calcule la somme des capacités thermiques de toutes les sections pour vérifier la cohérence avec la capacité thermique terrestre globale.

**`Calcul_capacité_thermique_api.py`**
Calcule, avec Google Earth Engine, la capacité thermique des sols dans un carré de 10 km autour d’un point donné, à partir de la carte ESA WorldCover 2020.






