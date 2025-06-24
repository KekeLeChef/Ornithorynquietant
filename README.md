# Ornithorynquietant 🌏🦆

**« Quand c’est mignon, mais un peu déroutant. »**  
Un projet de simulation climatique en Python — version pédagogique et modulaire.

---

## 🧭 Présentation du projet

Le projet **Ornithorynquietant** est une initiative éducative visant à explorer les fondements de la modélisation climatique à travers la programmation scientifique en Python. Il se décline en deux versions successives :

### 🔹 Modèle 1 – 2024
Première version simplifiée permettant de conceptualiser les mécanismes de base des simulations climatiques. Il s'agit d'une simulation statique conçue l'année dernière. Il existait une barre faisant evoluer les heures de la journée, cependant les calculs se faisaient sans prendre en compte les etats précédants donc sans prendre en compte l'évolution temporel.

### 🔹 Modèle 2 – 2025
Une version plus avancée intégrant :
- L'évolution **temporelle** de la température.
- Un découpage de la Terre en **cellules géographiques** pour un calcul local.
- Des mécanismes de **diffusion thermique**, rotation terrestre, inclinaison, ou autres phénomènes.
- Des résultats exploitables pour l'analyse dynamique du climat terrestre.

Ce projet s’adresse principalement à des étudiants ou passionnés souhaitant :
- Comprendre les bases physiques du climat.
- Apprendre la modélisation numérique.
- Structurer un projet scientifique en Python.

---

## 📁 Structure du projet

```bash
Ornithorynquietant/
├── modele_1_2024/           # Première version du modèle
│   ├── main.py              # Script principal
│   ├── utils.py             # Fonctions auxiliaires
│   └── ...                  # Autres fichiers éventuels
├── modele_2_2025/           # Deuxième version (avancée)
│   ├── main.py              # Script principal avec évolution temporelle
│   ├── grille.py            # Gestion du maillage terrestre
│   ├── physique.py          # Calculs physiques de température
│   └── visualisation.py     # Graphiques de simulation
├── README.md                # Ce fichier
└── requirements.txt         # Dépendances Python (à créer si manquant)
