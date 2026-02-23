# Spécifications Fonctionnelles & Cloud Data : 
# Tableau de Bord Power BI Supply Chain (Data Pipeline Automation)

## 🎯 Objectif Business Exécutif
Permettre à un Responsable Supply Chain de piloter l'activité des sites logistiques (Douala, Yaoundé, Ngaoundéré, Bélabo, Edéa) via des KPI agrégés : volume transféré, alertes critiques, machines actives par site et par jour.

## 🗂️ Sources de Données (Intégration Power BI)

### Mode local (SQLite)
- **Connecteur Power BI :** Importer les données ou se connecter à `database/supply_chain_dwh.sqlite`
- **Tables cibles :**
  - `fact_transactions` : Transactions détaillées (machine_id, date, volume_transferred, status_code, site_location, critical_alert)
  - `aggr_daily_site_stats` : Agrégats quotidiens par site (day, site_location, total_volume, total_alerts, active_machines)

### Mode Cloud (PostgreSQL Azure)
- **DirectQuery :** URI Flexible Server Azure PostgreSQL
- **Tables :** Même schéma que ci-dessus, déployé sur le DWH Cloud.

## 🎨 Modèle de Conception (Design UI/UX)
- **Couleurs Corporate :** Style industriel, indicateurs en bleu Bolloré/Camrail. Nuances critiques (Oranges/Rouges) pour les alertes.
- **Topologie :** Minimaliste. Focus sur les métriques actionnables (Actionable Insights).

## ⚙️ Construction des Visuels (Monitoring Supply Chain)

### Écran 1 : Vue Exécutive Supply Chain
- **KPI Haut Gauche** : Volume total transféré (sum total_volume).
- **KPI Haut Droite** : Nombre total d'alertes critiques (sum total_alerts).
- **Graphique en Barres** : Répartition du volume par site_location.
- **Table** : Top 10 machines par volume transféré.

### Écran 2 : Analyse Quotidienne par Site
- **Line Chart** : Évolution du volume et des alertes dans le temps (day).
- **Matrice** : site_location | day | total_volume | total_alerts | active_machines.
- **Formatage Conditionnel** : Cellule rouge si total_alerts > seuil.

## 📸 Références visuelles
![Exécution Pipeline ETL](../docs/screenshots/05_dpa_pipeline_execution.png)  
![Base DWH SQLite](../docs/screenshots/06_dpa_sqlite_dwh.png)

## 💡 Astuce (Pitch d'Entretien Technique)
> *"Le pipeline ETL DPA consolide les données API et ERP vers un DWH unique (SSOT). Power BI exploite les agrégats pour un pilotage Supply Chain en temps quasi-réel."*
