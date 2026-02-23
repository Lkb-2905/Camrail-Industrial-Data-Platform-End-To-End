"""
Script de bootstrap pour exécution locale sans PostgreSQL/Kafka.
Crée models/latest.pkl à partir des données CSV pour permettre à l'API de fonctionner.
Usage: python bootstrap_local.py
"""
import os
import sys
import joblib
import pandas as pd
from datetime import datetime
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Ajout du répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.config import config
from src.extract import extract_sensor_data, extract_maintenance_data

logger.add("logs/bootstrap.log", rotation="10 MB", retention="30 days")


def bootstrap_model_from_csv() -> None:
    """
    Entraîne le modèle à partir des CSV (sensors + maintenance) et enregistre dans models/latest.pkl.
    Permet de faire fonctionner l'API en environnement local sans PostgreSQL.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        registry_dir = os.path.join(base_dir, config['model']['registry_dir'])
        os.makedirs(registry_dir, exist_ok=True)

        logger.info("📡 [BOOTSTRAP] Extraction des données depuis CSV...")
        df_sensors = extract_sensor_data()
        df_maint = extract_maintenance_data()

        logger.info("⚙️ [BOOTSTRAP] Fusion et Feature Engineering...")
        df_merged = pd.merge(df_sensors, df_maint, on="loco_id", how="left")
        df_merged["critical_risk"] = (
            (df_merged["vibration"] > 3.0) & (df_merged["temperature"] > 60.0)
        ).astype(int)

        if df_merged["critical_risk"].nunique() < 2:
            logger.warning("⚠️ Moins de 2 classes : ajout de données synthétiques...")
            extra = pd.DataFrame([{
                "flow_rate": 400, "pressure": 3.2, "vibration": 5.5, "temperature": 65.8,
                "critical_risk": 1
            }])
            df_merged = pd.concat([df_merged, extra], ignore_index=True)

        X = df_merged[['flow_rate', 'pressure', 'vibration', 'temperature']]
        y = df_merged['critical_risk']

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        latest_path = os.path.join(registry_dir, config['model']['latest_name'])
        joblib.dump(model, latest_path)

        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        logger.success(f"✅ [BOOTSTRAP] Modèle créé : {latest_path} ({today})")
        logger.info("   Vous pouvez maintenant lancer l'API : python api/api.py")

    except Exception as e:
        logger.error(f"❌ [BOOTSTRAP] Erreur : {e}")
        raise


if __name__ == "__main__":
    bootstrap_model_from_csv()
