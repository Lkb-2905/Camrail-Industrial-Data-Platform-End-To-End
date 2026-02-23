# 📸 Captures d'écran - Projet CAMRAIL

## Fichiers présents (analyse à jour)

### Power BI — Dashboards Analytiques (README racine)

| Fichier | Contenu | Projet |
|---------|---------|--------|
| `10_powerbi_executive_summary.png` | **Synthèse des Opérations** — KPIs (Taux Erreur, Total Errors, Machines Actives, Total Transactions, Total Volume), courbe Volume par Jour, donut par status_code, barres Errors par machine_id. | Power BI |
| `11_powerbi_fiabilite_pipeline.png` | **Fiabilité du Pipeline** — Flux transactions (Total → status_code → machine_id), jauge Taux Erreur. Vue Data Quality. | Power BI |
| `12_powerbi_performance_parc.png` | **Performance du Parc** — Tableau machine_id × Volume/Errors/Taux Erreur (formatage conditionnel), nuage de points Volume vs Taux Erreur. | Power BI |
| `13_powerbi_analyse_shifts.png` | **Analyse Temporelle & Shifts** — Errors et Volume par Heure_Transaction, heatmap Jour_Semaine × Heure. | Power BI |

### CIDP — Dashboard Streamlit

| Fichier | Contenu | Projet |
|---------|---------|--------|
| `01_cidp_dashboard_vue_generale.png` | **Vue générale / Cas nominal** — OPÉRATION NOMINALE. | CIDP |
| `02_cidp_dashboard_alerte_danger.png` | **Cas alerte** — DANGER DÉTECTÉ (bannière rouge). | CIDP |
| `09_cidp_dashboard_error_timeout.png` | **Dépannage** — Erreur ReadTimeout (API non démarrée). | CIDP |

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
