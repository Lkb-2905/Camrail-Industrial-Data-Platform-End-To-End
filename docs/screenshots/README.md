# 📸 Captures d'écran - Projet CAMRAIL

## Fichiers présents (analyse à jour)

| Fichier | Contenu | Projet |
|---------|---------|--------|
| `01_cidp_dashboard_vue_generale.png` | **Vue générale / Cas nominal** — LOCO_003, Débit 200, Pression 1.17, Vibrations 1.30, Température 28.33. Message : **OPÉRATION NOMINALE** (barre verte). Taux fiabilité 63 %. | CIDP |
| `02_cidp_dashboard_alerte_danger.png` | **Cas alerte** — LOCO_003, Vibrations 12.91, Température 114.5. Message : **DANGER DÉTECTÉ** (bannière rouge). Taux fiabilité 33 %. | CIDP |
| `09_cidp_dashboard_error_timeout.png` | **Dépannage** — Erreur ReadTimeout (API non démarrée). Valeurs config : Vibr. 4.64, Temp. 89. Vérifier que l'API Flask tourne sur le port 5000. | CIDP |

## Convention pour captures supplémentaires

Pour compléter la documentation, ajouter les fichiers suivants (à renommer selon ce schéma) :

| Fichier | Description | Projet |
|---------|-------------|--------|
| `04_cidp_bootstrap_api_demarrage.png` | Terminal : bootstrap + démarrage API Flask | CIDP |
| `05_dpa_pipeline_execution.png` | Exécution du pipeline ETL (logs Extract/Transform/Load) | DPA |
| `06_dpa_sqlite_dwh.png` | Base SQLite supply_chain_dwh ou vue DBeaver | DPA |
| `07_pmd_generation_donnees.png` | Exécution data_generator / data_processing | PM-D |
| `08_pmd_model_training.png` | Entraînement modèle (classification report, accuracy) | PM-D |

## Emplacement

Toutes les captures sont dans : `docs/screenshots/`

## Référencement dans la documentation

- Depuis un sous-projet : `../docs/screenshots/01_cidp_dashboard_vue_generale.png`
- Depuis la racine : `docs/screenshots/01_cidp_dashboard_vue_generale.png`
