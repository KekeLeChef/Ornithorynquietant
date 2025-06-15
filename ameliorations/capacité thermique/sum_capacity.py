import csv

def somme_colonne_six(fichier_csv, lignes_max=1800):
    somme = 0
    with open(fichier_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        compteur = 0
        for row in reader:
            if compteur >= lignes_max:
                break
            try:
                valeur = float(row[5])  # 6e colonne = index 5
                somme += valeur
                compteur += 1
            except (ValueError, IndexError):
                continue  # Ignore les lignes invalides
    return somme

# Exemple d'utilisation
fichier = 'capacite_thermique_par_cellule.csv'
resultat = somme_colonne_six(fichier)
print(f"Somme des 1800 premières lignes de la 6e colonne : {resultat} J/K.")
