🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
# ⚡ PM-D PCR : Predictive Maintenance Dashboard (Sécurité E2E)
![Sécurité](https://img.shields.io/badge/Plan-Continuité-red) ![Kubernetes](https://img.shields.io/badge/K8s-Resilience-blue) ![Qualité](https://img.shields.io/badge/Qualité-ISO27001-yellow)

**Version:** 3.0.0 Enterprise | **Date:** Février 2026  
**Auteur:** KAMENI TCHOUATCHEU GAETAN BRUNEL  
**Contact:** gaetanbrunel.kamenitchouatcheu@et.esiea.fr  

---

## 📋 TABLE DES MATIÈRES
1. [Vue d'ensemble du projet](#-vue-densemble-du-projet)
2. [Architecture Technique (Menaces)](#️-architecture-technique)
3. [Stack Technologique & PCA](#️-stack-technologique)
4. [Fonctionnalités Clés (Reprise PRA)](#-fonctionnalités-clés)
5. [Démarrage Rapide (Secours)](#-démarrage-rapide)
6. [Qualité & Best Practices](#-qualité--best-practices)

---

## 🎯 VUE D'ENSEMBLE DU PROJET

### Contexte & Objectifs
Ce document définit la stratégie complète de résilience opérationnelle et le **Plan de Continuité d'Activité (PCA)** de la flotte IoT de maintenance prédictive, s'appuyant désormais sur Kafka et Microsoft Azure. 

Il illustre de A à Z les compétences absolues suivantes :

✅ **Auto-Healing K8s :** Les Pods d'API ML redémarrent automatiquement via Kubernetes en cas de Crash Memoire.
✅ **Data Science Sécurisée :** L'authentification par Header `X-API-KEY` bloque les attaques d'inférence. Le Dashboard Streamlit transmet automatiquement la clé API à l'endpoint `/predict`. Validation Pydantic (v1/v2) rejette les payloads forgés.
✅ **Automatisation Terraform :** Déploiement "Zero-Touch" en < 5min sur un Cloud vierge.
✅ **Tolérance aux pannes (Kafka) :** Les données de télémétrie ne sont jamais perdues hors de PostgreSQL, le broker Kafka les stocke temporairement.

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Flux de Données Détaillé (BIA - Business Impact Analysis)
| Menace Identifiée | Probabilité | Impact Métier | Sévérité |
| --- | --- | --- | --- |
| **API ML Injoignable** | Élevée (3/5) | Load Balancer AKS reroute le trafic instantanément vers un Replica | 🟢 Mineur |
| **Base Azure PostgreSQL Down** | Moyenne (2/5) | Kafka bufferise la donnée IoT le temps que le Failover Base s'active | 🟠 Moyen |
| **Vol de Données MQTT/IoT** | Faible (1/5) | Attaque rejetée, absence de TLS/Client Key sur les ingress | 🔴 Critique |
| **Data Drift (Modèle Obsolète)**| Très Faible | Alerte immédiate déclenchée par les rules SRE Prometheus | 🔴 Critique |

---

## 🛠️ STACK TECHNOLOGIQUE

### Stratégies de Continuité (PCA)
* **Failover-by-Design** : L'ingestion des paramètres températures/vibrations n'est *plus synchrone*. Si la base de données PostgreSQL subit un lock, le producteur IoT n'est pas affecté. Le système `confluent_kafka` absorbe tout dans le nuage.

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Procédures de Reprise (PRA)
**Reprise et Cold Reboot Global via Infra-As-Code**
En cas de cyberattaque massive compromise (Ransomware), l'entreprise ne paie pas : elle détruit tout.
```bash
# Depuis la CI/CD ou l'ordinateur blindé de l'architecte Cloud Azure
terraform destroy -auto-approve
terraform apply -auto-approve
# Le Data Warehouse Cloud, le cluster Kubernetes et l'Ingress IA sont recréés purs.
```

### 🛡️ Sécurité & Robustesse Cloud
| Aspect | Implémentation |
| --- | --- |
| **Résilience K8s** | Liveness & Readiness Probes Kubernetes installés sur `/health` |
| **Sécurité Payload**| Validation forte Pydantic `BaseModel` rejetant les JSON forgés (XSS, Buffer Overflows) |

---

## 🚀 DÉMARRAGE RAPIDE (MODE SECOURS LOCAL)

### Mode Bootstrap (sans PostgreSQL/Kafka) — Recommandé pour démo
En absence d'infrastructure Cloud, le script `bootstrap_local.py` entraîne le modèle depuis les CSV locaux (`data/sensors.csv`, `data/maintenance.csv`) et génère `models/latest.pkl`. L'API Flask et le Dashboard Streamlit fonctionnent alors en autonomie totale.
```powershell
cd Camrail-Industrial-Data-Platform
$env:PYTHONPATH = (Get-Location).Path
python bootstrap_local.py
python api/api.py
# Terminal 2 :
streamlit run dashboard/app.py
```
**Accès :** API `http://127.0.0.1:5000` | Dashboard `http://localhost:8501` (X-API-KEY transmise automatiquement).

### Redémarrage de la flotte Docker locale (Mode Dégradé)
Si le Cloud tombe, l'usine tourne en Fallback sur les boitiers serveurs locaux (Edge Computing).
```powershell
docker-compose down -v
docker-compose up -d --build
Write-Host "🚀 Flotte Data Streaming Fallback déployée. Brokers ZooKeeper sécurisés."
```

### Références visuelles
![Bootstrap et démarrage API](../docs/screenshots/04_cidp_bootstrap_api_demarrage.png)

---

## ✨ QUALITÉ & BEST PRACTICES

### Métriques d'Excellence
✅ **Performance réseau :** Pydantic rejette directement depuis le RAM buffer l'IoC corrompue `O(1)`.
✅ **Auditabilité :** Loguru conserve la rotation asynchrone des traces (10 MB/30 Days).
✅ **Isolement :** Secrets injectés dans Kubernetes via Azure KeyVault/Secrets natifs, aucune donnée en dur.

---
Ce projet est Confidentiel. Réservé à un usage académique et professionnel rigoureux.  
© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
