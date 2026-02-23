import os
import pandas as pd
from loguru import logger
from src.config import config

# Logging de production
logger.add("logs/extraction.log", rotation="10 MB", retention="30 days")

def extract_sensor_data() -> pd.DataFrame:
    """
    Extrait les données brutes des capteurs IoT industriels depuis le Data Lake (CSV).
    
    Returns:
        pandas.DataFrame: Un DataFrame contenant la télémétrie des locomotives.
    """
    logger.info("📡 [EXTRACT] Début de l'ingestion des capteurs IoT.")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sensors_path = os.path.join(base_dir, config['data']['raw_sensors'])
    
    try:
        df_sensors = pd.read_csv(sensors_path)
        logger.info(f"✅ [EXTRACT] Succès : {len(df_sensors)} enregistrements télémétriques ingérés.")
        return df_sensors
    except Exception as e:
        logger.error(f"❌ [EXTRACT] Échec critique de l'ingestion capteurs : {e}")
        raise

def extract_maintenance_data() -> pd.DataFrame:
    """
    Extrait le référentiel d'historique de maintenance via l'ERP d'entreprise.
    
    Returns:
        pandas.DataFrame: Un DataFrame contenant les fiches de révisions.
    """
    logger.info("📡 [EXTRACT] Connexion à la base GMAO Maintenance.")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    maintenance_path = os.path.join(base_dir, config['data']['raw_maintenance'])
    
    try:
        df_maint = pd.read_csv(maintenance_path)
        logger.info("✅ [EXTRACT] Succès : Référentiel maintenance chargé.")
        return df_maint
    except Exception as e:
        logger.error(f"❌ [EXTRACT] Impossible de charger l'ERP de maintenance : {e}")
        raise

if __name__ == "__main__":
    extract_sensor_data()
    extract_maintenance_data()
