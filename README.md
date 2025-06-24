# Ornithorynquietant 🌏🦆

**« Quand c’est mignon, mais un peu déroutant. »**  
Un projet de simulation climatique en Python 
---

## 🧭 Présentation du projet

Le projet **Ornithorynquietant** est une initiative visant à explorer les fondements de la modélisation climatique à travers la programmation scientifique en Python. Il se décline en deux versions successives :

### 🔹 Modèle 1 – 2024
Première version simplifiée permettant de conceptualiser les mécanismes de base des simulations climatiques. Il s'agit d'une simulation statique conçue l'année dernière. Il existait une barre faisant evoluer les heures de la journée, cependant les calculs se faisaient sans prendre en compte les etats précédants donc sans prendre en compte l'évolution temporel.

### 🔹 Modèle 2 – 2025
Une version plus avancée intégrant :
- L'évolution **temporelle** de la température.
- Un découpage de la Terre en **cellules géographiques** pour un calcul local.
- Des mécanismes de **diffusion thermique**, rotation terrestre, inclinaison, ou autres phénomènes.
- Des résultats exploitables pour l'analyse dynamique du climat terrestre.
- Création de csv pour les capacités thermiques de chaque région.
- Modèles basés sur la création de csv pour chaque heure utilisé à la simulation suivante.


Ce projet s'est principalment focalisé sur :
- Comprendre les bases physiques du climat.
- Apprendre la modélisation numérique.
- Structurer un projet scientifique en Python.


---

## 📁 Structure du projet

```bash
Ornithorynquietant/
├── modele_1_2024/           # Première version du modèle
│   ├── albedo               # dossier contenant les données albedo de la nasa
│   ├── data                 # dossier contenant les données par l'affichage de la Terre
│   ├── fonctions.py         # Fonctions auxiliaires
│   └── ...                  # Toutes les autres fonctions python et les pdf du rendue de l'année dernière 
├── modele_2_2025/           # Deuxième version (avec temporel)
│   ├── Annexe               # Contient une autre version test et des archives des précédents test dynamiques
│   ├── capacite thermique   # Ensemble des fichier servant à la création des documents pour les calculs de capacités thermiques ainsi que les différents test 
│   ├── convection           # Ensemble des différents test pour les modèle de convection (non utilisé dans notre modèle par manque de temps)
│   ├── diffusion            # Ensemble des éléments pour le modèle de diffusion 
│   ├── Final                # Le fichier contenant l'ensemble des élémnents essentiel au lancement du programme, 
│   ├── Synthèse.pdf         # Fichier de synthèse
│   └── ...
└── README.md                # Ce fichier

