🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
# ⚡ PM-D : Predictive Maintenance Dashboard
![Terraform](https://img.shields.io/badge/Terraform-AKS_Provisioning-purple) ![AzureDevOps](https://img.shields.io/badge/Azure_DevOps-Automated_Deploy-blue) ![Kubernetes](https://img.shields.io/badge/Kubernetes-Cloud_Cluster-blue) ![Grafana](https://img.shields.io/badge/Grafana-MLOps_Monitoring-orange)

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
Ce projet démontre la mise en œuvre d'une architecture orientée **Data Science** pour la Maintenance Prédictive du matériel ferroviaire (Locomotives de fret pour Camrail / Bolloré Logistics). Il répond aux exigences de la Supply Chain logistique moderne en combinant télémétrie temps réel et anticipation des pannes par l'IA.

Il illustre les compétences suivantes :

✅ **Architecture Cloud Native :** Serveurs distribués sur environnement Azure Kubernetes Service (AKS).
✅ **Azure DevOps CI/CD :** Pipeline automatisé des tests jusqu'au déploiement (AKS).
✅ **Infrastructure as Code (Terraform) :** Provisionnement complet et auditable de l'architecture Microsoft Azure.
✅ **Data Science Intégrée :** Moteur prédictif Scikit-Learn (Random Forest) pour anticiper les pannes critiques.
✅ **Observabilité Grafana / Prometheus :** Dashboards complets d'analyse des anomalies métiers (SRE).
✅ **Data Streaming (Kafka) :** Les signaux télémétriques de la locomotive générés sont publiés en streaming complet via Broker.
✅ **Data Warehouse Distribué (PostgreSQL) :** Historisation et aggrégation dans Azure Postgres.

### Pourquoi ce projet ?
| Aspect | Démonstration |
| --- | --- |
| **Scalabilité** | L'Auto-Scaler Kubernetes (AKS) multiplie les conteneurs API ML selon la charge IoT détectée. |
| **Maintenabilité** | L'Infrastructure `main.tf` (Terraform) provisionne l'environnement Azure Data de 0 en < 5 minutes. |
| **Innovation** | Le CI/CD Azure Pipelines garantit 0 bug en production lors des déploiements logistiques des modèles d'IA. |
| **Sécurité** | Gestion Cloud Azure sécurisant les connexions Pods / Database via Secrets Kubernetes. |
| **Business Value** | Monitoring Dashboard exécutif en temps réel (Power BI / Grafana) pour prescriptibilité Data-Driven. |

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Diagramme de Flux (Vue Logique & ML Ops)
```mermaid
flowchart TD
    classDef client fill:#38bdf8,stroke:#0284c7,stroke-width:2px,color:#000
    classDef app fill:#4ade80,stroke:#16a34a,stroke-width:2px,color:#000
    classDef intel fill:#facc15,stroke:#ca8a04,stroke-width:2px,color:#000
    classDef data fill:#f87171,stroke:#dc2626,stroke-width:2px,color:#fff
    classDef darkBox fill:#27272a,stroke:#52525b,stroke-width:2px,color:#fff

    subgraph Client_Layer["Client Layer"]
        O[👤 Analyste Maintenance]:::darkBox -->|Pilotage| R[Power BI Dashboard<br>Monitoring Executif]:::client
    end

    subgraph Application_Layer["Application Layer"]
        N[Python Data Processing<br>data_processing.py]:::app
        S[Feature Engineering<br>& Scaling]:::darkBox
        R -->|Requête Dashboard| S
        N -->|API Request| OM
        N -->|Fallback| SL
        N -->|Orchestration| S
    end

    subgraph Data_Sources["Data Sources"]
        OM[Kafka / Azure IoT<br>Télémétrie Cloud]:::data
        SL[Générateur Local<br>data_generator.py]:::data
        SL -.-> OM
    end

    subgraph Intelligence_Layer["Intelligence Layer"]
        P[Python Engine<br>Random Forest Scikit-Learn]:::intel
    end

    S -->|Shell Execution| P
    P -->|JSON Output| S

    style Client_Layer fill:#3f3f46,stroke:#52525b,color:#fff
    style Application_Layer fill:#3f3f46,stroke:#52525b,color:#fff
    style Data_Sources fill:#3f3f46,stroke:#52525b,color:#fff
    style Intelligence_Layer fill:#3f3f46,stroke:#52525b,color:#fff
```

**Résultat visuel — Workflow ML :**

Les deux captures ci-dessous s'affichent directement dans le README.

**07 — Génération des données** — Exécution de `data_generator.py` et `data_processing.py` :

![Génération données PM-D](../docs/screenshots/07_pmd_generation_donnees.png)

**08 — Entraînement du modèle** — Exécution de `model_training.py` (classification report, accuracy) :

![Entraînement modèle Random Forest](../docs/screenshots/08_pmd_model_training.png)

### Architecture Infra (Cloud)

Vue d’ensemble du déploiement sur Microsoft Azure (AKS, PostgreSQL, CI/CD).

```mermaid
flowchart LR
    subgraph Client
        U[👤 Opérateur]
        P[Power BI]
        U --> P
    end

    subgraph CICD["Azure DevOps CI/CD"]
        AZ[Build · Test · Push]
    end

    subgraph AKS["Azure Kubernetes Service"]
        G[Générateur]
        K[Kafka]
        T[Worker ETL]
        M[IA Engine]
        PR[Prometheus]
        GF[Grafana]
        G --> K --> T
        M --> PR --> GF
    end

    subgraph Infra
        TF[Terraform]
    end

    subgraph Data
        S[Capteurs]
        D[(PostgreSQL)]
    end

    S --> G
    T --> D
    D --> M
    M --> P
    AZ --> TF
    TF --> AKS
```

### Flux de Données Détaillé
1. **Infrastructure as Code** : Terraform déploie le socle Cloud (Azure K8s, Postgres, Broker Kafka).
2. **Phase CI/CD** : Azure DevOps re-compile et auto-déploie sur les conteneurs Kubernetes chaque modification des variables ou de l'IA ML.
3. **Apprentissage (Data Science) sur K8s** : Le script IA (`model_training.py`) tourne sous conteneur, agrégeant l'historique Azure DB pour ajuster le Random Forest.
4. **Monitoring Ops (Grafana/Prometheus)** : Exposition du `metrics` des conteneurs ML sur Grafana, verrouillant ainsi tous crash en production.

---

## 🛠️ STACK TECHNOLOGIQUE

### Technologies Core
| Composant | Technologie | Version | Justification Technique |
| --- | --- | --- | --- |
| **Langage** | Python | 3.12+ | Standard mondial de la Data Science opérationnelle. |
| **Machine Learning** | Scikit-Learn | Latest | Algorithmes d'arbres (Random Forest) robustes. |
| **Data Manipulation** | Pandas / NumPy | Latest | Manipulation vectorielle des données industrielles. |
| **Visualisation** | Power BI | Latest | Création de tableaux de bord décisionnels d'entreprise. |

### Bibliothèques Complémentaires
* **Joblib :** Sérialisation et de-sérialisation ultra-rapide des modèles IA.
* **Pyenv :** Gestion rigoureuse des interpréteurs Python.

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Fonctionnalités Principales
**Supervision Temps Réel**
* Suivi des KPI critiques : Pression d'huile, Vibrations des essieux, Température.
* Historisation des alertes matérielles.

**Intelligence Artificielle Prédictive**
* Application du modèle Random Forest.
* Mécanisme de pondération des classes (`class_weight='balanced'`) pour les pannes rares.
* Calcul probabiliste de risque pour anticipation continue.

**Gestion des Risques**
* Détection de cotes critiques.

### 🛡️ Sécurité & Robustesse
| Aspect | Implémentation |
| --- | --- |
| **Validation** | Vérification stricte et imputation des données `NaN`. |
| **Résilience** | PCR complet rédigé pour la continuité opérationnelle. |
| **Traçabilité** | Logging clair des dysfonctionnements locaux. |

---

## 🚀 DÉMARRAGE RAPIDE

### Prérequis
* Python (v3.12+)

### Installation Rapide
```powershell
cd Predictive-Maintenance-Dashboard
pip install -r requirements.txt
cd src
python data_generator.py
python data_processing.py
python model_training.py
```

### Lancement Développeur (Mode Local — Recommandé pour démo)

> 💡 Utilisez le Python de **pyenv** si `python` ou `pip` ne sont pas configurés correctement.

```powershell
# 1. Installer les dépendances (pyenv recommandé)
cd "c:\Users\pc\Desktop\projet CAMRAIL\Predictive-Maintenance-Dashboard"
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" -m pip install -r requirements.txt

# 2. Lancer la solution (séquentiellement — ordre obligatoire)
cd src
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" data_generator.py      # Génère raw_telemetry.csv
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" data_processing.py     # Crée processed_telemetry.csv
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" model_training.py      # Entraîne et sauvegarde rf_failure_predict.joblib
```

**Accès Immédiat :** Le modèle `rf_failure_predict.joblib` et les CSV traités sont générés instantanément. Intégration possible avec CIDP (API ML) et Power BI.

---

## 📖 GUIDE D'UTILISATION

### Scénario de Pilotage
1. **Connexion :** Liez Power BI à l'URL HTTP Raw GitHub contenant le fichier de résultats.
2. **Supervision :** Observez la jauge critique. Si la probabilité d'avarie est forte, isolez la locomotive.
3. **Action :** Exporter le rapport vers le département maintenance technique (cf. `POWER_BI_SPECS.md`).

### Captures d'Écran

Chaque capture est affichée ci-dessous avec sa légende.

**07 — Génération des données** — Exécution de `data_generator.py` et `data_processing.py` :

![Génération données PM-D](../docs/screenshots/07_pmd_generation_donnees.png)

---

**08 — Entraînement du modèle** — Exécution de `model_training.py` (classification report, accuracy) :

![Entraînement modèle Random Forest](../docs/screenshots/08_pmd_model_training.png)

> 💡 Captures dans `docs/screenshots/` — Convention : voir `../docs/screenshots/README.md`

---

## ✨ QUALITÉ & BEST PRACTICES

### Standards de Code
* **Modularité :** Répartition en générateurs, processeurs et algos entraînés.
* **Qualité (Data) :** Dataframes Pandas purement typés pour la rigueur scientifique.
* **Error Handling :** Blocs Try/Except sur les opérations clés.

### Métriques d'Excellence
✅ **Couverture fonctionnelle :** Modèle prédictif déployé End-to-End.
✅ **Performance :** Sérialisation instantanée avec Joblib.
✅ **Disponibilité :** Architecture pensée pour la scalabilité.

---

## 🗺️ ROADMAP & ÉVOLUTIONS

**Version Actuelle : 2.0.0 (Enterprise V2) ✅**
* CI/CD Intégral : Déploiement Azure Kubernetes Service via Azure Pipelines.
* Infrastructure As Code via Terraform.
* Simulation télémétrique via Azure Event Hubs (Kafka).
* Moteur IA Scikit-Learn (Random Forest) couplé à PostgreSQL.
* Mode local : Workflow complet (data_generator → data_processing → model_training) sans Cloud.
* Alerting et Observabilité Grafana SRE (Metrics Prometheus).

**Version 3.0.0 (Vision Long Terme) 🔮**
* Digital Twin Temps Réel : Jumeau numérique 3D complet avec feedback IA Edge Computing.

---

## 🤝 CONTRIBUTION
Les contributions sont les bienvenues pour faire évoluer ce démonstrateur vers une solution industrielle.
1. Forker le projet.
2. Créer une branche d'évolution.
3. Lancer une PR pointue.

---

## 📄 LICENCE
Ce projet est développé dans un cadre académique et professionnel. Droits réservés.

## 👨‍💻 AUTEUR
**KAMENI TCHOUATCHEU GAETAN BRUNEL**  
Ingénieur Logiciel & Data Scientist en devenir | Étudiant ESIEA  

📧 Email : gaetanbrunel.kamenitchouatcheu@et.esiea.fr  
🐙 GitHub : @Lkb-2905  

🙏 **REMERCIEMENTS**
* **Camrail / Bolloré Logistics :** Pour l'inspiration des cas d'usage logistiques industriels.
* **ESIEA :** Pour l'excellence de la formation ingénieur.

⭐ Si ce projet vous semble pertinent pour la Supply Chain de demain, laissez une étoile !  
Fait avec ❤️, Pandas et Python.  

© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
