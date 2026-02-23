import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
from loguru import logger
from src.config import config
from src.extract import extract_sensor_data, extract_maintenance_data

load_dotenv()

# Configuration logging entreprise
logger.add("logs/transform.log", rotation="10 MB", retention="30 days")

def transform_and_load() -> None:
    """
    Effectue le nettoyage, la jointure métier et le stockage analytique 
    dans le Data Warehouse de production.
    
    Raises:
        Exception: Si le pipeline ETL ne parvient pas à insérer les données.
    """
    try:
        df_sensors = extract_sensor_data()
        df_maint = extract_maintenance_data()
        
        logger.info("⚙️ [TRANSFORM] Nettoyage et jointure des données de production.")
        
        df_merged = pd.merge(df_sensors, df_maint, on="loco_id", how="left")
        
        # Ingénierie des variables (Feature Engineering)
        df_merged["critical_risk"] = ((df_merged["vibration"] > 3.0) & (df_merged["temperature"] > 60.0)).astype(int)
        
        
        # Azure / Local PostgreSQL Connection
        db_user = os.getenv("POSTGRES_USER", "camrail_admin")
        db_pass = os.getenv("POSTGRES_PASSWORD", "enterprise_password_2026!")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB", "camrail_dwh")
        
        database_uri = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(database_uri)
        
        df_merged.to_sql("sensor_metrics", engine, if_exists="replace", index=False)
        logger.info(f"✅ [Cloud DWH] Jointure SQL distante validée (PostgreSQL).")
            
    except Exception as e:
        logger.error(f"❌ [TRANSFORM/LOAD] Erreur fatale dans le pipeline ETL : {e}")
        raise

if __name__ == "__main__":
    transform_and_load()
