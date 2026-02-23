import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import joblib
from datetime import datetime
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.config import config

load_dotenv()

# Logging rotation et rétention d'entreprise
logger.add("logs/training.log", rotation="10 MB", retention="30 days")

def train_model() -> None:
    """
    Interroge le Data Warehouse, ré-entraîne le modèle Random Forest de prédiction
    de maintenance, et le sauvegarde dans le Model Registry.
    
    Raises:
        Exception: En cas d'erreur lors de l'apprentissage réseau de neurones / Scikit-Learn.
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        registry_dir = os.path.join(base_dir, config['model']['registry_dir'])
        
        logger.info("🧠 [TRAIN] Extraction SRE des features sur PostgreSQL...")
        
        if not os.path.exists(registry_dir):
            os.makedirs(registry_dir, exist_ok=True)
            
        db_user = os.getenv("POSTGRES_USER", "camrail_admin")
        db_pass = os.getenv("POSTGRES_PASSWORD", "enterprise_password_2026!")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "camrail_dwh")
        
        database_uri = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(database_uri)
        
        df = pd.read_sql("SELECT flow_rate, pressure, vibration, temperature, critical_risk FROM sensor_metrics", engine)
            
        if df.empty:
            logger.warning("⚠️ [TRAIN] DWH Vide. Algorithme abandonné par sécurité.")
            return
            
        X = df[['flow_rate', 'pressure', 'vibration', 'temperature']]
        y = df['critical_risk']
        
        if len(y.unique()) < 2:
            logger.warning("⚠️ [TRAIN] Moins de 2 classes détectées. Ajustement de secours activé.")
            X.loc[len(X)] = [400, 3.2, 5.5, 65.8]
            y.loc[len(y)] = 1
            
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Model Registry (Versioning niveau CAC40)
        today_date = datetime.now().strftime("%Y_%m_%d")
        versioned_name = f"model_{today_date}.pkl"
        versioned_path = os.path.join(registry_dir, versioned_name)
        latest_path = os.path.join(registry_dir, config['model']['latest_name'])
        
        joblib.dump(model, versioned_path)
        joblib.dump(model, latest_path) # Écrase la symlink logique
        
        logger.info(f"✅ [TRAIN] Modèle déployé ! Version : {versioned_name} | Tag: LATEST.")
        
    except Exception as e:
        logger.error(f"❌ [TRAIN] Crash durant l'entraînement Machine Learning : {e}")
        raise

if __name__ == "__main__":
    train_model()
