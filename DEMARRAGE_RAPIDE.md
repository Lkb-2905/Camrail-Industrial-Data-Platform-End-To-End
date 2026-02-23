# 🚀 Guide de démarrage rapide - Projet CAMRAIL

## Prérequis

- **Python 3.12** (recommandé, via pyenv-win ou installation standard)
- Les dépendances sont installées via `pip install -r requirements.txt`

## 📸 Captures d'écran

Pour documenter vos démos, placez les captures dans `docs/screenshots/` et renommez-les selon la convention définie dans **[docs/screenshots/README.md](docs/screenshots/README.md)**.

## Exécution des 3 composants

### 1. Data Pipeline Automation (DPA)

```powershell
cd "Data-Pipeline-Automation\src"
python main_pipeline.py
```

**Résultat :** Base SQLite créée dans `database/supply_chain_dwh.sqlite` et export Excel dans `reports/rapport_supply_chain.xlsx`

---

### 2. Predictive Maintenance Dashboard (PM-D)

Exécuter dans l'ordre :

```powershell
cd "Predictive-Maintenance-Dashboard\src"
python data_generator.py      # Génère raw_telemetry.csv
python data_processing.py     # Crée processed_telemetry.csv
python model_training.py      # Entraîne et sauvegarde le modèle
```

---

### 3. Camrail Industrial Data Platform (CIDP)

#### Mode local (sans PostgreSQL/Kafka)

```powershell
cd "Camrail-Industrial-Data-Platform"

# 1. Créer le modèle à partir des CSV
python bootstrap_local.py

# 2. Démarrer l'API Flask
python api/api.py

# 3. (Optionnel) Démarrer le dashboard Streamlit
streamlit run dashboard/app.py
```

L'API écoute sur `http://127.0.0.1:5000`. Test : `GET /health` ou `POST /predict` avec header `X-API-KEY: entreprise_secret_key_2026`.

#### Mode complet (PostgreSQL + Kafka)

Utiliser `run_platform.py` lorsque PostgreSQL et Kafka sont configurés (voir `.env`).

---

## Tests

```powershell
cd "Camrail-Industrial-Data-Platform"
$env:PYTHONPATH = (Get-Location).Path
python -m pytest tests/ -v
```

---

## Notes de compatibilité

- **Pydantic** : Le projet gère Pydantic v1 (`.dict()`) et v2 (`.model_dump()`)
- **scikit-learn** : En cas d'erreur `numpy.dtype size changed`, exécuter :  
  `pip install --upgrade scikit-learn numpy`
