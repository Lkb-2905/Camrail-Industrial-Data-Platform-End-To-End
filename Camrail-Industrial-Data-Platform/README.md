🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
# ⚡ CIDP : Camrail Industrial Data Platform
![Terraform](https://img.shields.io/badge/Terraform-Infrastructure_As_Code-purple) ![Azure_DevOps](https://img.shields.io/badge/Azure_Pipelines-CI/CD-blue) ![Kubernetes](https://img.shields.io/badge/Kubernetes-AKS_Cluster-blue) ![Grafana](https://img.shields.io/badge/Grafana-SRE_Dashboards-orange)

**Version:** 3.0.0 Enterprise | **Date:** Février 2026  
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
L'**Industrial Data Platform (End-to-End)** démontre de magistrales capacités d'architecture orientée *Data-Driven* globale. Ce projet hybride réunit l'Ingénierie de la Donnée (ETL SQL) et la Data Science (Moteurs ML connectés Base de Données) dans une usine logicielle ferroviaire critique de grande ampleur.

Il illustre de A à Z les compétences absolues suivantes :

✅ **Architecture E2E Hexagonale :** Isolation de l'ETL (Extrait Moteur) et de la ML Data Science.
✅ **Azure DevOps CI/CD :** Pipeline automatisé des tests jusqu'au déploiement (AKS).
✅ **Infrastructure as Code (Terraform) :** Provisionnement complet et auditable de l'architecture Microsoft Azure.
✅ **Kubernetes (AKS) :** Conteneurisation et auto-scaling horizontal de l'IA (API ML + Workers Kafka).
✅ **Observabilité Grafana / Prometheus :** Dashboards complets d'analyse des anomalies métiers (SRE).
✅ **Streaming IoT Temps Réel (Kafka) :** Ingestion continue et asynchrone des flux capteurs massifs.
✅ **Data Warehouse Cloud (PostgreSQL) :** Stockage relationnel lourd, robuste avec des capacités géospatiales.
✅ **Mode Local (Bootstrap) :** Exécution autonome sans PostgreSQL/Kafka via `bootstrap_local.py` et API Flask.

### Pourquoi ce projet ?
| Aspect | Démonstration |
| --- | --- |
| **Scalabilité** | L'Auto-Scaler Kubernetes multiplie les conteneurs API selon la charge Kafka. |
| **Maintenabilité** | L'Infrastructure `main.tf` permet un redéploiement complet en < 10min. |
| **Innovation** | Le CI/CD Azure Pipelines garantit 0 bug en production lors des upgrades IA. |
| **Sécurité** | Gestion Cloud Azure sécurisant les connexions Pods / Database via Secrets K8s. API sécurisée par `X-API-KEY` transmise dans le Dashboard Streamlit. |
| **Performance** | Monitoring visuel temps réel via Dashboards Grafana couplés à Prometheus. |

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Diagramme de Flux (Vue Logique & Local)
```mermaid
flowchart TD
    %% Styling
    classDef client fill:#38bdf8,stroke:#0284c7,stroke-width:2px,color:#000
    classDef app fill:#4ade80,stroke:#16a34a,stroke-width:2px,color:#000
    classDef intel fill:#facc15,stroke:#ca8a04,stroke-width:2px,color:#000
    classDef data fill:#f87171,stroke:#dc2626,stroke-width:2px,color:#fff
    classDef darkBox fill:#27272a,stroke:#52525b,stroke-width:2px,color:#fff

    subgraph Client Layer
        O[👤 Opérateur Logistique]:::darkBox -->|Pilotage| R[Streamlit Dashboard<br>Port 8501]:::client
    end

    subgraph Application Layer
        N[Flask API Backend<br>Port 5000]:::app
        S[Service Métier]:::darkBox
        N -->|Orchestration| S
    end

    subgraph Data Sources
        OM[Kafka / PostgreSQL<br>Données Réelles]:::data
        SL[Simulateur Local<br>Données Synthétiques]:::darkBox
    end

    subgraph Intelligence Layer
        P[Python Engine<br>Scikit-Learn]:::intel
    end

    %% Connections
    R -->|HTTP GET/POST| N
    N -.->|API Request| OM
    N -->|Fallback| SL
    S -->|Shell / API Execution| P
    P -->|JSON Output| S

    %% Custom styles for Subgraphs
    style Client Layer fill:#3f3f46,stroke:#52525b,color:#fff
    style Application Layer fill:#3f3f46,stroke:#52525b,color:#fff
    style Data Sources fill:#3f3f46,stroke:#52525b,color:#fff
    style Intelligence Layer fill:#3f3f46,stroke:#52525b,color:#fff
```

### Architecture Infra (Cloud)

### Diagramme de Flux
```mermaid
graph TD
    subgraph Client Layer
        U[👤 Opérateur Logistique]
        P[BI Dashboard Live]
        U -->|Pilotage| P
    end

    subgraph Azure DevOps CI/CD
        AZ[Pipeline Azure<br>Build, Test, Push]
    end

    subgraph Azure Kubernetes Service (AKS)
        K[Apache Kafka Broker]
        O[Microservice Consumer ETL]
        PR[Prometheus SRE]
        GF[Grafana Dashboards]
        M[API Flask ML Predict]
        
        K -->|Consumer Topic| O
        M -->|Exposition /metrics| PR
        PR -->|Data Source| GF
    end

    subgraph Infrastructure
        TF[Terraform IaC]
        AZ --> TF
        TF -.->|Provisioning| K
        TF -.->|Deploy| D
    end

    subgraph Data Sources
        S[Capteurs IoT Trains]
    end

    subgraph Cloud Postgres DB
        D[(PostgreSQL Flexible<br>Data Warehouse)]
    end

    S -->|Producteur Kafka| K
    O -->|Bulk Upsert| D
    D -->|Lecture DB| M
    M -->|JSON Response| P

    style P fill:#4FC3F7,color:#000
    style K fill:#FF9800,color:#fff
    style O fill:#4CAF50,color:#fff
    style M fill:#FFD600,color:#000
    style D fill:#336791,color:#fff
    style S fill:#FF5252,color:#fff
    style PR fill:#E6522C,color:#fff
    style GF fill:#F46800,color:#fff
    style AZ fill:#0078D7,color:#fff
    style TF fill:#844FBA,color:#fff
```

### Flux de Données Détaillé
1. **Infrastructure as Code** : Terraform instancie l'Event Hub, Azure Postgres et le Cluster Kubernetes de 0.
2. **Déploiement CI/CD** : Toute modification Master déclenche Azure DevOps qui compile l'image Docker, exécute `Pytest` et déploie le YAML sur AKS.
3. **Architecture Distribuée (K8s)** : Les pods ETL capturent les évènements Kafka et l'A.I API lit depuis la base Azure.
4. **Mode Local (Bootstrap)** : En absence de PostgreSQL/Kafka, `bootstrap_local.py` entraîne le modèle depuis les CSV (`data/sensors.csv`, `data/maintenance.csv`) et génère `models/latest.pkl`, permettant à l'API et au Dashboard Streamlit de fonctionner en autonomie.
5. **Monitoring Ops (Grafana)** : Prometheus scrape les métriques (`/metrics`) du conteneur ML, que Grafana expose sous forme de Dashboard exécutif temps réel.
6. **Diffusion Live** : Dashboard Streamlit (port 8501) appelle l'API (port 5000) avec authentification `X-API-KEY` pour afficher les prédictions en temps réel.

---

## 🛠️ STACK TECHNOLOGIQUE

### Technologies Core
| Composant | Technologie | Version | Justification Technique |
| --- | --- | --- | --- |
| **Infrastructure Cloud** | Terraform / Azure | Latest | Déploiement automatisé (IaC) de l'usine logicielle complète sur le Cloud Microsoft Azure. |
| **SGBD Cloud** | PostgreSQL | 15+ | Data Warehouse Enterprise-Grade pour stockage massif relationnel et analytique. |
| **Intelligence Artificielle**| Scikit-Learn | Latest | Algorithmes Random Forest industriels pour la maintenance prédictive. |
| **Orchestration & DevOps**| Kubernetes (AKS) | Latest | Auto-scaling des Pods API et des Workers Kafka via CI/CD Azure Pipelines. |
| **Dashboard Interactif** | Streamlit | Latest | Interface de démo temps réel avec sliders (Débit, Pression, Vibration, Température) et appel API sécurisé. |

### Bibliothèques Complémentaires
* **Loguru :** Remplacement intelligent du standard logger pour une traccabilité magistrale.
* **Pyenv :** Verrouillage strict de l'environnement Python utilisé.
* **Pydantic :** Validation des payloads API et compatibilité v1/v2 (`.dict()` / `.model_dump()`).

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Fonctionnalités Principales
**Usine Numérique Cloud Native**
* Déploiement asynchrone orchestré par Terraform sur Azure Kubernetes Service. Supervision E2E Grafana.

**Algorithmes de Machine Learning sur PostgreSQL**
* Calcul des scores de risques vitaux enregistrés directement dans la base de données distante.

**Mode Local (Bootstrap)**
* Script `bootstrap_local.py` : entraînement du modèle depuis les CSV locaux → `models/latest.pkl`. Permet une démo complète sans infrastructure Cloud.

**Dashboard Streamlit**
* Interface "Camrail Live Monitor" (localhost:8501) avec outil de test manuel : sliders pour simuler la télémétrie, bouton "Interroger l'API Neural Network", affichage "OPÉRATION NOMINALE" ou "DANGER DÉTECTÉ" selon les prédictions.

**Mécanismes SRE (Site Reliability Engineering)**
* Alerting Prometheus actif bloquant l'API si le modèle de Machine Learning diverge ou tombe en latence.

### 🛡️ Sécurité & Robustesse
| Aspect | Implémentation |
| --- | --- |
| **Résilience Kubernetes** | Le Load Balancer Kubernetes reroute le flux en millisecondes si un Worker s'arrête. |
| **Sécurité d'API** | Schema Validation via Pydantic et X-API-KEY intégrée dans les Pods IA. Le Dashboard Streamlit transmet automatiquement le header `X-API-KEY` à l'API Flask. |
| **Traçabilité SRE** | Dashboard complet Grafana monitorant la santé de chaque micro-service. |
| **Timeout & Erreurs** | Timeout API 15s, messages d'erreur explicites (API injoignable, ReadTimeout). |

---

## 🚀 DÉMARRAGE RAPIDE

### Prérequis
* Docker Desktop & Kubernetes (mode Cloud)
* Terraform Azure CLI (`az`) (mode Cloud)
* Python (v3.12+ pour le mode local)

### Déploiement Architecte (Cloud Microsoft Azure)
```bash
# 1. Provisionner l'infrastructure Cloud complète
cd terraform
terraform init && terraform apply -auto-approve

# 2. Le CI/CD Azure DevOps compile et déploie les Pods ML 
# sur AKS automatiquement au moindre push GitHub.
```

### Lancement Développeur (Mode Local — Recommandé pour démo)
```powershell
# 1. Créer l'environnement virtuel et installer les dépendances
cd Camrail-Industrial-Data-Platform
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 2. Bootstrap du modèle (entraînement depuis CSV)
$env:PYTHONPATH = (Get-Location).Path
python bootstrap_local.py

# 3. Démarrer l'API Flask (Terminal 1)
python api/api.py

# 4. Démarrer le Dashboard Streamlit (Terminal 2)
streamlit run dashboard/app.py
```

**Accès Immédiat :**
* API : **http://127.0.0.1:5000** (GET `/health`, POST `/predict` avec header `X-API-KEY: entreprise_secret_key_2026`)
* Dashboard : **http://localhost:8501** — Camrail Live Monitor

### Lancement Mode Complet (PostgreSQL + Kafka)
```bash
python run_platform.py
```

---

## 📖 GUIDE D'UTILISATION

### Scénario de Pilotage
1. **Lancement Kafka & Microservices :** Laissez les Deployments Kubernetes assurer l'ingestion asynchrone IoT.
2. **Supervision BI Connectée :** En utilisant le connecteur DirectQuery PostgreSQL, connectez vos outils Power BI/Grafana pour surveiller la santé des locomotives à la seconde près.
3. **Démo Recruteur :** Lancer l'API + Dashboard, afficher le cas nominal (Vibration 2, Température 45), puis simuler une alerte (Vibration 7+, Température 85+) et montrer le message "DANGER DÉTECTÉ".

### Captures d'Écran
**📸 Résultat de l'exécution (Local)**  
![Exécution Local](execution_screenshot.png)

**📸 Dashboard Streamlit — Vue générale**  
![Camrail Live Monitor](../docs/screenshots/01_cidp_dashboard_vue_generale.png)

**📸 Cas nominal — Opération normale**  
![Opération nominale](../docs/screenshots/01_cidp_dashboard_vue_generale.png)

**📸 Cas alerte — Danger détecté**  
![Alerte danger](../docs/screenshots/02_cidp_dashboard_alerte_danger.png)

**📸 Bootstrap et démarrage API**  
![Bootstrap et API](../docs/screenshots/04_cidp_bootstrap_api_demarrage.png)

> 💡 Convention de nommage des captures : voir `../docs/screenshots/README.md`

---

## ✨ QUALITÉ & BEST PRACTICES

### Standards de Code
* **Modularité (Hexagonale) :** Couches réparties avec rigueur.
* **Clean Code Data :** L'intelligence ne pervertit pas les couches basses, la connexion est une API via SGBD.
* **Error Handling :** Exception Management `try-except sys.exit(1)` garantissant la pureté du pipeline.
* **Compatibilité Pydantic :** Gestion transparente Pydantic v1 et v2 pour les payloads API.

### Métriques d'Excellence
✅ **Couverture fonctionnelle :** L'Extrême bout-en-bout d'une compétence d'Ingénieur Full-Stack Data en action.
✅ **Performance globale :** Architecture `Zero-Downtime` SQL Supportée.
✅ **Tests automatisés :** `pytest tests/test_api.py` — 4 tests (health, unauthorized, schema validation, bad method).

---

## 🗺️ ROADMAP & ÉVOLUTIONS

**Version Actuelle : 3.0.0 (Enterprise V3) ✅**
* Architecture streaming IoT globale (**Apache Kafka**).
* Socle Cloud Native via **Microsoft Azure Kubernetes Service (AKS)**.
* Déploiement Data Engineer Zero-Touch par Infrastructure As Code (**Terraform**).
* CI/CD Intégral : Sécurité et Build poussés via **Azure Pipelines**.
* Observabilité exécutif (Dashboarding) assuré conjointement par **Grafana / Prometheus**.
* **Mode Local Bootstrap** : Exécution autonome sans PostgreSQL/Kafka.
* **Dashboard Streamlit** : Interface de démo avec authentification API intégrée.

**Version 3.0.0 (Vision Long Terme) 🔮**
* Implémentation complète Digital Twin (Jumeau Numérique 3D) couplé aux flux Kafka temps réel.

---

## 🤝 CONTRIBUTION
L'Avenir passera par l'Intelligence de la Donnée Logistique :
1. Forker.
2. Proposer une implémentation `Prophet`/`LSTM`.
3. Réaliser une Pull Request de Génie.

---

## 📄 LICENCE
Ce projet est développé dans un cadre académique et hautement professionnel. Droits réservés.

## 👨‍💻 AUTEUR
**KAMENI TCHOUATCHEU GAETAN BRUNEL**  
Ingénieur Logiciel & Data Scientist en devenir | Étudiant ESIEA  

📧 Email : gaetanbrunel.kamenitchouatcheu@et.esiea.fr  
🐙 GitHub : @Lkb-2905  

🙏 **REMERCIEMENTS**
* **Bolloré Logistics & Camrail :** Pour l'envergure des architectures d'Ingénierie de Haute Technologie.
* **ESIEA :** Pour l'esprit d'initiative.

⭐ Laissez une étoile pour soutenir le Full-Stack Data Engineering Camerounais !  
Fait avec ❤️, Scikit et SQLAlchemy.  

© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
