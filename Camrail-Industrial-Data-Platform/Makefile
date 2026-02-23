.PHONY: run run-dashboard train extract transform test freeze all

run:
	@echo "Démarrage de l'API Flask..."
	python api/api.py

run-dashboard:
	@echo "Démarrage du Dashboard Streamlit..."
	streamlit run dashboard/app.py

extract:
	@echo "Extraction des données réelles (Data Lake)..."
	python src/extract.py

transform:
	@echo "Transformation ETL (Data Warehouse)..."
	python src/transform.py

train:
	@echo "Entraînement de l'IA (Model Regisrty)..."
	python src/train.py

test:
	@echo "Lancement des Tests Unitaires PyTest..."
	pytest tests/ -v

freeze:
	@echo "Génération stricte du requirements-lock.txt..."
	pip freeze > requirements-lock.txt

all: extract transform train test run
