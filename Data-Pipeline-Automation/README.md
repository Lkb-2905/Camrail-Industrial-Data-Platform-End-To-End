🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
# ⚡ DPA : Data Pipeline Automation
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple) ![Azure](https://img.shields.io/badge/Azure_Pipelines-CI/CD-blue) ![Kubernetes](https://img.shields.io/badge/Kubernetes-Data_Pods-blue) ![Grafana](https://img.shields.io/badge/Grafana-SRE_Dashboards-orange)

**Version:** 1.0.0 Stable | **Date:** Février 2026  
**Auteur:** KAMENI TCHOUATCHEU GAETAN BRUNEL  
**Contact:** gaetanbrunel.kamenitchouatcheu@et.esiea.fr  

🚀 [Démarrage Rapide](#-démarrage-rapide) • 📚 [Documentation](#-guide-dutilisation) • 🎯 [Fonctionnalités](#-fonctionnalités-clés) • 🔧 [Installation](#-installation-rapide)

---

## 📋 TABLE DES MATIÈRES
1. [Vue d'ensemble du projet](#-vue-densemble-du-projet)
2. [Architecture Technique](#️-architecture-technique)
3. [Stack Technologique](#️-stack-technologique)
4. [Fonctionnalités Clés](#-fonctionnalités-clés)
5. [Démarrage Rapide](#-démarrage-rapide)
6. [Guide d'Utilisation](#-guide-dutilisation)
7. [Qualité & Best Practices](#-qualité--best-practices)
8. [Roadmap & Évolutions](#️-roadmap--évolutions)

---

## 🎯 VUE D'ENSEMBLE DU PROJET

### Contexte & Objectifs
Ce projet illustre l'implémentation robuste d'une architecture **Data-Driven (ETL)** pour le pilotage logistique des données de fret. Il répond aux exigences d'une gouvernance informatique moderne en unifiant les données, les fichiers épars et les signaux métiers.

Il illustre les compétences suivantes :

✅ **Azure DevOps CI/CD :** Pipeline automatisé des tests jusqu'au déploiement (AKS).
✅ **Infrastructure as Code (Terraform) :** Provisionnement complet et auditable de l'architecture Microsoft Azure.
✅ **Kubernetes (AKS) :** Conteneurisation et auto-scaling horizontal des pods ETL.
✅ **Observabilité Grafana / Prometheus :** Dashboards complets d'analyse des flux de données.
✅ **Streaming Asynchrone (Kafka) :** Les signaux logistiques sont bufferisés via topics.
✅ **Data Warehouse Cloud (PostgreSQL) :** Stockage sécurisé et hautement performant sur Microsoft Azure.

### Pourquoi ce projet ?
| Aspect | Démonstration |
| --- | --- |
| **Scalabilité** | L'Auto-Scaler Kubernetes multiplie les conteneurs ETL selon la charge de données arrivant dans Kafka. |
| **Maintenabilité** | L'Infrastructure `main.tf` (Terraform) permet de cloner l'environnement de production sur Azure en quelques minutes. |
| **Innovation** | Le CI/CD Azure Pipelines garantit 0 bug en production lors des déploiements logistiques. |
| **Sécurité** | Gestion Cloud Azure sécurisant les connexions Pods / Database via Secrets et authentifications fortes. |
| **Business Value** | Dote les gestionnaires de KPI calculés et requêtes avancées (Data Warehouse Azure). |

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Diagramme de Flux (Vue Logique & ETL Local)
```mermaid
flowchart TD
    %% Styling
    classDef client fill:#38bdf8,stroke:#0284c7,stroke-width:2px,color:#000
    classDef app fill:#4ade80,stroke:#16a34a,stroke-width:2px,color:#000
    classDef intel fill:#facc15,stroke:#ca8a04,stroke-width:2px,color:#000
    classDef data fill:#f87171,stroke:#dc2626,stroke-width:2px,color:#fff
    classDef darkBox fill:#27272a,stroke:#52525b,stroke-width:2px,color:#fff

    subgraph Client Layer
        O[👤 Opérateur Logistique]:::darkBox -->|Pilotage| R[Dashboard BI / DBeaver<br>SQL Analytics]:::client
    end

    subgraph Application Layer
        N[Python ETL Pipeline<br>main_pipeline.py]:::app
        S[Data Warehouse<br>SQLite / SQlAlchemy]:::darkBox
        N -->|Orchestration| S
    end

    subgraph Data Sources
        OM[Kafka / Azure SQL<br>Données Cloud]:::data
        SL[Sources Locales<br>CSVs / JSONs / Excel]:::darkBox
    end

    subgraph Intelligence Layer
        P[Python Transform<br>Pandas Analytics]:::intel
    end

    %% Connections
    R -->|Requêtes SQL| S
    N -.->|Extract Cloud| OM
    N -->|Extract Local| SL
    N -->|Transformation| P
    P -->|Dataframes Propres| N
    N -->|Load (SQL Insert)| S

    %% Custom styles for Subgraphs
    style Client Layer fill:#3f3f46,stroke:#52525b,color:#fff
    style Application Layer fill:#3f3f46,stroke:#52525b,color:#fff
    style Data Sources fill:#3f3f46,stroke:#52525b,color:#fff
    style Intelligence Layer fill:#3f3f46,stroke:#52525b,color:#fff
```

### Architecture Infra (Cloud)
```mermaid
graph TD
    subgraph Client Layer
        U[👤 Décideur Supply Chain]
        P[DBeaver / Dashboard BI]
        U -->|Pilotage| P
    end

    subgraph Azure DevOps CI/CD
        AZ[Pipeline Azure<br>Build, Test, Push]
    end

    subgraph Azure Kubernetes Service (AKS)
        K[Apache Kafka Cluster]
        E[Extracteur API JSON]
        T[Transformateur Pandas]
        L[Worker SQLAlchemy]
        PR[Prometheus SRE]
        GF[Grafana Dashboards]
        K -->|Consumer Topic| E
        E -->|Nettoyage| T
        T -->|Manipulation| L
        L -->|Metriques Santé| PR
        PR -->|Data Source| GF
    end

    subgraph Infrastructure
        TF[Terraform IaC]
        AZ --> TF
        TF -.->|Provisioning| K
        TF -.->|Deploy| D
    end

    subgraph Data Sources
        S[Terminaux Logistiques Fret]
    end

    subgraph Cloud PostgreSQL
        D[(Azure PostgreSQL<br>Data Warehouse)]
    end

    S -->|Producteur Kafka| K
    L -->|Upsert SQL/Bulk| D
    D -->|Requêtes Analytiques| P

    style P fill:#4FC3F7,color:#000
    style K fill:#FF9800,color:#fff
    style E fill:#4CAF50,color:#fff
    style T fill:#4CAF50,color:#fff
    style L fill:#4CAF50,color:#fff
    style D fill:#336791,color:#fff
    style S fill:#FF5252,color:#fff
    style PR fill:#E6522C,color:#fff
    style GF fill:#F46800,color:#fff
    style AZ fill:#0078D7,color:#fff
    style TF fill:#844FBA,color:#fff
```

### Flux de Données Détaillé
1. **Infrastructure as Code** : Terraform instancie Microsoft Azure PostgreSQL, Event Hubs et AKS.
2. **Déploiement CI/CD** : Azure DevOps compile et pousse l'image Docker ETL vers AKS pour son exécution en Pods.
3. **Extraction & Transformation (K8s)** : Les micro-services récupèrent la donnée Kafka en direct et fusionnent les tables via Pandas.
4. **Chargement SQL & SRE** : Les données sont chargées en Bulk Upsert sur Azure Postgres. Prometheus et Grafana monitorent le flux de santé absolu de l'architecture Big Data.

---

## 🛠️ STACK TECHNOLOGIQUE

### Technologies Core
| Composant | Technologie | Version | Justification Technique |
| --- | --- | --- | --- |
| **Orchestrateur** | Python | 3.12+ | L'outil complet de traitement universel par batch d'ingénierie. |
| **Base de Données** | SQLite | 3+ | DWH de fichier ultra-léger et transportable localement. |
| **Data Engine** | Pandas | Latest | Traitement et jointure rapide de la donnée en RAM. |
| **ORM et Mapping** | SQLAlchemy | Latest | Connectivité et sécurité des transactions SQL (pas de SQL syntax direct en paramètre métier). |

### Bibliothèques Complémentaires
* **Loguru/Logging :** Traçabilité exhaustive.
* **Openpyxl :** Lecture/écriture Excel (source ERP, export rapports).
* **PyODBC :** Connexion Microsoft Access (bases legacy, migration).
* **OS/Sys :** Commandes natives utiles à l'interaction Windows (Task Scheduler).

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Fonctionnalités Principales
**Gouvernance Data Temps Réel**
* Consolidations des flux épars vers une Base Unique.
* Création propre et persistante de `supply_chain_dwh.sqlite`.

**Système Avancé de Requêtage**
* Déploiement de scripts SQL analytiques poussés pour catégoriser la fiabilité du système (Hub Logistics Classification).

**Gestion des Risques**
* Tolérance du Pipeline en mode fail-safe sur corruption partielle de fichier.

### 🛡️ Sécurité & Robustesse
| Aspect | Implémentation |
| --- | --- |
| **Validation** | Vérification et parsing stricts avant transaction. |
| **Résilience** | Base de données SQL protégée des deadlocks et échecs (Rollbacks). |
| **Traçabilité** | Logs détaillés sur serveurs ou scripts chronologiques. |

---

## 🚀 DÉMARRAGE RAPIDE

### Prérequis
* Python (v3.12+)

### Installation Rapide
```powershell
# 1. Cloner le projet (Naviguer au sein du répertoire)
cd Data-Pipeline-Automation

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'Orchestrateur Complet
cd src
python main_pipeline.py
```
**Accès Immédiat :** Les tables historiques sont fraîches et disponibles instantanément dans `database/supply_chain_dwh.sqlite`.

---

## 📖 GUIDE D'UTILISATION

### Scénario de Pilotage
1. **Lancement Quotidien :** L'outil tourne la nuit via scheduler.
2. **Requêtage Expert :** Un Data Analyst peut soumettre `sql/advanced_queries.sql` au DBeaver de la base.
3. **Action:** Construction de Dashboard et exports métier sur l'activité des "Gares".

### Captures d'Écran
**📸 Résultat de l'exécution (Local)**  
![Exécution Local](execution_screenshot.png)

**📸 Exécution du Pipeline ETL**  
![Exécution du Pipeline ETL](../docs/screenshots/05_dpa_pipeline_execution.png)

**📸 Base de données DWH SQLite**  
![Base SQLite Supply Chain](../docs/screenshots/06_dpa_sqlite_dwh.png)

> 💡 Convention de nommage : voir `../docs/screenshots/README.md`

---

## ✨ QUALITÉ & BEST PRACTICES

### Standards de Code
* **Modularité (Engine) :** Couches E, T, et L isolées nativement.
* **Typage (Data) :** Cast structurés au sein des Dataframes.
* **Error Handling :** Blocs robustes limitant l'écrasement bdd en cas de corruption.

### Métriques d'Excellence
✅ **Architecture :** DWH Single Source of Truth respecté (SSOT).
✅ **Performance :** L'ORM insère des dizaines de milliers de lignes en lots optimisés (bulk).

---

## 🗺️ ROADMAP & ÉVOLUTIONS

**Version Actuelle : 2.0.0 (Enterprise V2) ✅**
* Architecture Data Streaming en Event-Driven via Apache Kafka.
* Virtualisation Globale : Orchestration via Docker Compose complet.
* Base de Données : Connecteur vers Cloud Azure PostgreSQL et Prometheus SRE.
* Documentation exhaustive DCE.

**Version 3.0.0 (Vision Long Terme) 🔮**
* Implémentation de Streaming Machine Learning Temps Réel.

---

## 🤝 CONTRIBUTION
Les contributions sont les bienvenues pour industrialiser ce socle métier logistique.
1. Forker.
2. Définir une Feature Branche.
3. Valider par PR documentée.

---

## 📄 LICENCE
Ce projet est développé dans un cadre académique et professionnel. Droits réservés.

## 👨‍💻 AUTEUR
**KAMENI TCHOUATCHEU GAETAN BRUNEL**  
Ingénieur Logiciel & Data Scientist en devenir | Étudiant ESIEA  

📧 Email : gaetanbrunel.kamenitchouatcheu@et.esiea.fr  
🐙 GitHub : @Lkb-2905  

🙏 **REMERCIEMENTS**
* **Camrail / Bolloré Logistics :** Pour l'approche industrielle robuste Data Management.
* **ESIEA :** Pour l'excellence informatique et académique.

⭐ Si ce projet vous semble pertinent pour la Supply Chain de demain, laissez une étoile !  
Fait avec ❤️, Python et du SQL.  

© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
