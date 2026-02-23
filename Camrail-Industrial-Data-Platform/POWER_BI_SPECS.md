# Spécifications Fonctionnelles & Cloud Data : 
# Tableau de Bord Power BI Maintenance Prédictive (Architecture Azure / Kafka)

## 🎯 Objectif Business Exécutif
Permettre à un Directeur Logistics & Supply Chain d'identifier en temps réel quelles locomotives risquent de tomber en panne (Scoring IA Random Forest) afin d'appliquer une maintenance prescriptive réduisant les coûts logistiques de -30%.

## 🗂️ Sources de Données (Intégration Power BI / Cloud Azure)

> 💡 **L'Architecture "Cloud Native" (Big Data)** : Les temps de l'import "Fichier Plat CSV" sont révolus. Le dashboard se connecte désormais de façon sécurisée au Data Warehouse de Production Cloud.

1. **DirectQuery (PostgreSQL Azure) :** La Source de Vérité est le Cluster Microsoft Azure PostgreSQL provisionné par Terraform. 
   - **Connecteur Power BI :** Renseigner l'URI Flexible Server `camrail-dwh-prod.postgres.database.azure.com`
   - **Authentification :** Renseigner le tuple de sécurité (`camrail_admin` / `enterprise_password_2026!`)
   - **Table Cible :** Vue matérialisée `sensor_metrics` comportant les signaux et les probabilités d'Anomaly Detection (calculées par l'API AKS).
2. **Streaming Direct (Power BI REST API) - Vision Future :** Intégration d'un connecteur Broker Kafka poussant, sans aucun rafraîchissement manuel, les données à la milliseconde près.

## 🎨 Modèle de Conception (Design UI/UX)
- **Couleurs Corporate SRE :** Mode de fond "Dark" ou "Grafana Style" industriel, indicateurs en bleu corporate Bolloré/Camrail. Nuances critiques (Oranges/Rouges) en cas d'Alerting franchit.
- **Topologie :** Minimaliste. Focus sur les métriques actionnables (Actionable Insights).

## ⚙️ Construction des Visuels (Monitoring Ops & Business)

### Écran 1 : Control Room Logistique 4.0
*C'est l'écran opérationnel temps réel connecté au Flux IoT Azure.*
- **KPI Haut Gauche** : Volume d'évènements Kafka ingérés & Flotte Active.
- **KPI Haut Droite (Clé de Voûte)** : "Alertes Machine Learning" - Nombre de locomotives dont la `risk_probability` > 85%. Indicateur critique en police dynamique rouge.
- **Camembert ou Graphique en Donut** : Répartition de l'état du parc (Normal / Usure Légère / Défaillance Imminente).
- **Jauge Centrale (Thermique)** : Température agrégée des moteurs, corrélée aux anomalies de refroidissement.

### Écran 2 : Vision Data Science & Diagnostics Deep-Dive
*Pour l'Ingénieur de Fiabilité (SRE) et les techniciens*
- **Line Chart (Courbes Multiples)** : Analyse longitudinale de l'usure asynchrone (Pression VS Temps).
- **Scatter Plot (Nuage de Points AI Drift)** : Corrélation matricielle entre Vibrations (Y) et Température (X), soulignant dynamiquement notre *Feature Engineering* (les clusters générant le plus de risques).
- **Matrice Azure Connect** : 
    - Colonnes Cloud DB: *Loco_ID | Température | Vibrations | Predict Binary | Probabilité (%)*
    - Formatage Conditionnel : Fond de la cellule en Infrarouge (RGB) dès que la probabilité ML frôle les 0.75.

## 📸 Complément Démo : Dashboard Streamlit
En mode local, le **Dashboard Streamlit "Camrail Live Monitor"** (localhost:8501) offre une interface interactive de test de l'API ML : sliders pour simuler la télémétrie, affichage "OPÉRATION NOMINALE" ou "DANGER DÉTECTÉ" selon les prédictions.

![Dashboard Streamlit — Vue générale](../docs/screenshots/01_cidp_dashboard_vue_generale.png)

![Cas nominal](../docs/screenshots/01_cidp_dashboard_vue_generale.png)  
![Alerte danger](../docs/screenshots/02_cidp_dashboard_alerte_danger.png)

## 💡 Astuce (Pitch d'Entretien Technique Sénior)
Lors de la présentation de ce dashboard à des CTO (ex: Alstom, Thales, ESIEA) : 
> *"Ce Dashboard Power BI n'est pas un concept isolé. C'est l'aboutissement visuel ("Front-End d'affichage") d'une infrastructure robuste. Les données qu'il exploite sont ingérées nativement par des micro-services Apache Kafka sur de hauts volumes (IoT Streaming), puis processées unitairement par une IA propulsée sous Kubernetes (AKS) qui expose enfin les probabilités de pannes asynchrones dans une vraie base PostgreSQL Cloud. Le BI complète parfaitement cette architecture scalable, en sécurisant la prise de décision."*
