🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
# ⚡ DPA PCR : Data Pipeline Automation (Sécurité E2E)
![Sécurité](https://img.shields.io/badge/Plan-Continuité-red) ![ETL](https://img.shields.io/badge/ETL-Resilience-blue) ![Qualité](https://img.shields.io/badge/Qualité-ISO27001-yellow)

**Version:** 2.0.0 Enterprise | **Date:** Février 2026  
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
Ce document définit la stratégie complète de résilience opérationnelle et le **Plan de Continuité d'Activité (PCA)** du pipeline ETL Supply Chain, incluant les flux API/JSON, CSV, Excel et le Data Warehouse SQLite.

Il illustre de A à Z les compétences absolues suivantes :

✅ **Fail-Safe ETL :** Tolérance aux corruptions partielles de fichiers (CSV, JSON, Excel). Le pipeline ne plante pas en cas de source dégradée.
✅ **Validation & Rollback :** SQLAlchemy transactions avec rollback automatique en cas d'échec de chargement.
✅ **Multi-Source :** Fallback Excel (`extract_from_excel`) si les sources API/CSV sont indisponibles.
✅ **Export Contrôlé :** Rapport Excel multi-feuilles généré de façon atomique dans `reports/`.

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Flux de Données Détaillé (BIA - Business Impact Analysis)
| Menace Identifiée | Probabilité | Impact Métier | Sévérité |
| --- | --- | --- | --- |
| **API JSON indisponible** | Moyenne (2/5) | Utilisation de la source Excel ou CSV ERP en fallback | 🟢 Mineur |
| **Fichier CSV/Excel corrompu** | Moyenne (2/5) | Parsing strict, skip des lignes invalides, logs détaillés | 🟠 Moyen |
| **Base SQLite verrouillée** | Faible (1/5) | Rollback transaction, retry ou report manuel | 🟠 Moyen |
| **Export Excel échoué** | Faible (1/5) | DWH SQLite reste intact ; export manuel possible via `excel_utils` | 🟢 Mineur |
| **Perte du DWH** | Très faible | Reprise depuis sources brutes (data_raw, Excel) et relance `main_pipeline.py` | 🔴 Critique (PRA) |

---

## 🛠️ STACK TECHNOLOGIQUE

### Stratégies de Continuité (PCA)
* **Transaction atomique :** Les insertions SQLite passent par SQLAlchemy avec commits/rollbacks contrôlés.
* **Multi-source :** En cas d'indisponibilité des APIs, le pipeline peut s'alimenter depuis Excel (`extract_from_excel`) ou les fichiers CSV locaux.
* **Export non bloquant :** L'export Excel vers `reports/rapport_supply_chain.xlsx` n'impacte pas l'intégrité du DWH en cas d'échec.

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Procédures de Reprise (PRA)
**Reprise après perte du Data Warehouse**
```powershell
# 1. Vérifier la présence des sources
dir Data-Pipeline-Automation\data_raw
dir exemples_excel_access\output   # Si source Excel utilisée

# 2. Relancer le pipeline complet
cd Data-Pipeline-Automation\src
python main_pipeline.py

# 3. Le DWH est recréé et l'export Excel régénéré
```

**Export manuel en cas d'échec automatique**
```python
from utils.excel_utils import export_dwh_to_excel
export_dwh_to_excel("database/supply_chain_dwh.sqlite", "reports/rapport_supply_chain.xlsx")
```

### 🛡️ Sécurité & Robustesse
| Aspect | Implémentation |
| --- | --- |
| **Validation données** | Parsing strict Pandas, vérification des types avant insert. |
| **Résilience SQL** | Transactions SQLAlchemy, pas de SQL direct en paramètre (ORM). |
| **Traçabilité** | Loguru logs exhaustifs (exécution, erreurs, lignes ignorées). |
| **Sources Excel/Access** | Gestion des erreurs ODBC (pyodbc), fallback si pilote manquant. |

---

## 🚀 DÉMARRAGE RAPIDE (MODE SECOURS LOCAL)

### Redémarrage du pipeline ETL (sources locales uniquement)
Sans accès API Cloud, le pipeline s'exécute entièrement en local.
```powershell
cd Data-Pipeline-Automation\src
python main_pipeline.py
# Sources : data_raw/*.json, data_raw/*.csv
# Résultat : database/supply_chain_dwh.sqlite + reports/rapport_supply_chain.xlsx
```

### Mode fallback Excel
Si les fichiers JSON/CSV standards sont absents ou corrompus :
```python
# Dans extract.py ou script custom
from extract import extract_from_excel
api_data, erp_data = extract_from_excel("chemin/vers/transactions.xlsx")
# Puis transform_data() et load_data()
```

### Références visuelles
![Exécution Pipeline ETL](../docs/screenshots/05_dpa_pipeline_execution.png)  
![Base DWH SQLite](../docs/screenshots/06_dpa_sqlite_dwh.png)

---

## ✨ QUALITÉ & BEST PRACTICES

### Métriques d'Excellence
✅ **Atomicité :** Chargement DWH tout-ou-rien (rollback sur erreur).
✅ **Auditabilité :** Loguru conserve la rotation des traces (10 MB/30 Days).
✅ **Portabilité :** SQLite + Excel permettent un déploiement sans infrastructure Cloud.

---
Ce projet est Confidentiel. Réservé à un usage académique et professionnel rigoureux.  
© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés
