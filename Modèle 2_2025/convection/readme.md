**`gradient_temperature_y`**: Calcul du gradient de température le long de l’axe Nord–Sud (Oy) à une heure donnée, pour une longitude fixé.

**`gradient_temperature_x`**: Calcul du gradient de température le long de l’axe équatorial (Ox) à une heure donnée pour une latitude donnée.

**`Convection_test_1.py`**: Calcul du flux de convection entre deux plaques via l’air, et visualisation des échanges en régime quasi-statique (≃évolue lentement).

**`Convection_test_2.py`**: Modèle amélioré de la version 1.

**`Convection_test_3.py`**: Modèle amélioré de la version 2. Produit un graphique du “Flux thermique net entre les plaques (via l’air)” sur 24 h.

**`modele_convectif.py`**: Évaluation, pour chaque section de l’atmosphère et du sol, le changement de température de l’air selon le rayon (dTij) sous l’effet du bilan radiatif et de la convection, puis calcul de la puissance échangée entre l’air et le sol. 
Produit un graphique montrant l'évolution de la température de l'air et du flux convectif échangé avec le sol.

**`puissance_solaire_reçu.py`**: Calcul la puissance solaire reçu dans l'atmosphère en fonction de l'inclinaison du soleil pour chaque mois et chaque heure. Génère un dossier avec 24 fichier x 12 mois contenant 1800 lignes avec les latitudes, les longitudes et la valeur associée.

**`puissance_reçu_atm`**: Dossier avec 24 fichier x 12 mois contenant 1800 lignes avec les latitudes, les longitudes et la valeur de puissance solaire reçu associée.

**`calcul_h.py`**: fontion pour calculer la constante de convection, utilisé et ajusté dans le code **`modele_convectif.py`**