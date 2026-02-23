# 🚀 Guide de démarrage rapide - Projet CAMRAIL

## Prérequis

- **Python 3.12** (recommandé, via pyenv-win ou installation standard)
- Les dépendances sont installées via `pip install -r requirements.txt`

## 📸 Captures d'écran

Pour documenter vos démos, placez les captures dans `docs/screenshots/` et renommez-les selon la convention définie dans **[docs/screenshots/README.md](docs/screenshots/README.md)**.

## Lancement Développeur (Mode Local — Recommandé pour démo)

> 💡 Utilisez le Python de **pyenv** si `python` ou `pip` ne sont pas configurés :  
> `& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe"`

### 1. Data Pipeline Automation (DPA)

```powershell
cd "c:\Users\pc\Desktop\projet CAMRAIL\Data-Pipeline-Automation"
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" -m pip install -r requirements.txt
cd src
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" main_pipeline.py
```

**Résultat :** Base SQLite dans `database/supply_chain_dwh.sqlite` et export Excel dans `reports/rapport_supply_chain.xlsx`

---

### 2. Predictive Maintenance Dashboard (PM-D)

Exécuter dans l'ordre :

```powershell
cd "c:\Users\pc\Desktop\projet CAMRAIL\Predictive-Maintenance-Dashboard"
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" -m pip install -r requirements.txt
cd src
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" data_generator.py
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" data_processing.py
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" model_training.py
```

---

### 3. Camrail Industrial Data Platform (CIDP)

#### Mode local (sans PostgreSQL/Kafka)

```powershell
cd "c:\Users\pc\Desktop\projet CAMRAIL\Camrail-Industrial-Data-Platform"
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" -m pip install -r requirements.txt

# Terminal 1 — Bootstrap + API (ordre requis)
$env:PYTHONPATH = (Get-Location).Path
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" bootstrap_local.py
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" api/api.py

# Terminal 2 — Dashboard
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" -m streamlit run dashboard/app.py
```

**Ordre requis :** Bootstrap + API en premier ; le Dashboard interroge l'API sur le port 5000 (sinon ReadTimeout).  
L'API écoute sur `http://127.0.0.1:5000`. Test : `GET /health` ou `POST /predict` avec header `X-API-KEY: entreprise_secret_key_2026`.

#### Mode complet (PostgreSQL + Kafka)

Utiliser `run_platform.py` lorsque PostgreSQL et Kafka sont configurés (voir `.env`).

---

## Tests

```powershell
cd "c:\Users\pc\Desktop\projet CAMRAIL\Camrail-Industrial-Data-Platform"
$env:PYTHONPATH = (Get-Location).Path
& "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.12.10\python.exe" -m pytest tests/ -v
```

---

## Notes de compatibilité

- **Pydantic** : Le projet gère Pydantic v1 (`.dict()`) et v2 (`.model_dump()`)
- **scikit-learn** : En cas d'erreur `numpy.dtype size changed`, exécuter :  
  `pip install --upgrade scikit-learn numpy`
