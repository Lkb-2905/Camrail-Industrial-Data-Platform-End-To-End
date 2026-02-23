# 📊 Exemples Excel et Access - Projet CAMRAIL

Intégration **Excel** et **Microsoft Access** pour répondre aux besoins des équipes métier et au profil recruteur (TotalEnergies, etc.).

---

## 🎯 Cas d'usage

| Outil | Usage dans le projet |
|-------|---------------------|
| **Excel** | Source de données (saisie ERP), export de rapports, modèles pour opérationnels |
| **Access** | Lecture de bases legacy, migration SQLite → format Access pour utilisateurs métier |

---

## 🚀 Installation

```powershell
cd "c:\Users\pc\Desktop\projet CAMRAIL"
pip install openpyxl pyodbc pandas loguru
```

---

## 📁 Exemples disponibles

### 1. Export DWH → Excel
Export du Data Warehouse SQLite vers un rapport Excel multi-feuilles (Transactions, Stats par site, KPI).

```python
from Data-Pipeline-Automation.utils.excel_utils import export_dwh_to_excel
export_dwh_to_excel("database/supply_chain_dwh.sqlite", "reports/rapport.xlsx")
```

### 2. Modèle Excel pour saisie ERP
Génération d'un fichier Excel modèle que les opérationnels peuvent remplir. Le pipeline peut ensuite lire ce fichier.

```python
from Data-Pipeline-Automation.utils.excel_utils import export_erp_excel_template
export_erp_excel_template("output/modele_erp.xlsx", num_rows=100)
```

### 3. Lecture Excel comme source
Utiliser un fichier Excel comme source à la place du CSV ERP :

```python
from Data-Pipeline-Automation.src.extract import extract_from_excel
api_file, erp_csv = extract_from_excel("donnees/transactions.xlsx")
# Puis transform_data(api_file, erp_csv) et load_data(...)
```

### 4. Export pour import Access
Le DWH est exporté en Excel. Les utilisateurs Access peuvent importer via : **Données > Nouvelle source > Fichier > Excel**.

```python
from Data-Pipeline-Automation.utils.access_utils import export_for_access_import
export_for_access_import("database/supply_chain_dwh.sqlite", "rapport.xlsx")
```

### 5. Lecture depuis Access
Si une base Access existe (.accdb) :

```python
from Data-Pipeline-Automation.utils.access_utils import read_access_table
df = read_access_table("data/erp.accdb", "Transactions")
```

**Prérequis Access :** Pilote ODBC Microsoft Access (*Microsoft Access Database Engine*) — [Téléchargement](https://www.microsoft.com/download/details.aspx?id=54920).

---

## ▶️ Lancer tous les exemples

```powershell
cd "c:\Users\pc\Desktop\projet CAMRAIL"
python exemples_excel_access/run_exemples.py
```

Les fichiers générés sont dans `exemples_excel_access/output/`.

---

## 📋 Colonnes attendues (fichier Excel source)

Pour être compatible avec le pipeline, le fichier Excel doit contenir :

| Colonne | Type | Exemple |
|---------|------|---------|
| transaction_id | Texte | TRX-001 |
| machine_id | Texte | MCH-003 |
| date | Date/Heure | 2026-02-23 10:00 |
| volume_transferred | Nombre | 45.5 |
| status_code | Texte | OK, WARN, ERR |
