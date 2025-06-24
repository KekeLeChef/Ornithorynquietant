## MODÈLE DYNAMIQUE 3D (composante globale)

**`modèle_dynamique_test_1.py`** : Calcule, pour chaque heure d’une journée, le flux solaire incident et la température sur les **1800 cases** de la grille mondiale (albédo ESA). Stocke ces 24 × 1800 valeurs dans un CSV utilisable.

**`modèle_dynamique_test_2.py`** : Version enrichie : ajoute la **capacité thermique interpolée** (KD-Tree) sur la même grille, applique le bilan radiatif heure par heure avec inertie thermique (≈mémoire), enregistre le champ de température dans *temperature_bon3_Tatmo_288.csv* et propose une **visualisation 3D interactive**.

**`modèle_dynamique_test_3.py`** : Version améliorée de **`modèle_dynamique_test_2.py`**
