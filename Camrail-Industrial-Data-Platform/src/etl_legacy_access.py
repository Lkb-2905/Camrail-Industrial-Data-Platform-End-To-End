import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import logging

# Configuration du Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_from_access(db_path: str, table_name: str) -> pd.DataFrame:
    """
    Extrait les données d'une table Microsoft Access historique en utilisant pyodbc.
    Ceci démontre la capacité à requêter des bases de données legacy souvent
    utilisées par les opérationnels (Logistique, Supply Chain).
    """
    try:
        logger.info(f"Tentative de connexion à la base MS Access : {db_path}")
        
        # Chaine de connexion standard pour MS Access sous Windows
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={db_path};'
        )
        
        # Connexion à Access
        conn = pyodbc.connect(conn_str)
        
        # Requête SQL pour extraire les données
        query = f"SELECT * FROM {table_name}"
        logger.info(f"Exécution de la requête : {query}")
        
        # Lecture avec pandas
        df = pd.read_sql(query, conn)
        conn.close()
        
        logger.info(f"Extraction réussie ! {len(df)} lignes récupérées depuis Access.")
        return df

    except pyodbc.Error as e:
        logger.warning(f"[SIMULATION] Impossible de se connecter à Access (Pilote manquant ou fichier absent).")
        logger.warning(f"Détail de l'erreur pyodbc : {e}")
        logger.info("-> Basculement sur notre fichier Excel de secours pour la démonstration.")
        
        # Fallback sur le fichier Excel ou CSV pour que la démo fonctionne tout le temps
        # C'est une excellente pratique de Data Engineering (Fallback Mechanism)
        fallback_path = "../data/source_donnees.xlsx"
        df = pd.read_excel(fallback_path)
        logger.info(f"Fallback réussi : {len(df)} lignes récupérées depuis le fichier local.")
        return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyage et préparation de la donnée métier.
    Exemples: typage, gestion des valeurs nulles, renommage.
    """
    logger.info("Début de la transformation des données...")
    
    # Nettoyage des noms de colonnes : suppression des espaces, passage en minuscules
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # Remplir les valeurs manquantes pour les colonnes catégorielles
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna("NON_RENSEIGNE")
        
    logger.info("Transformation terminée avec succès.")
    return df

def load_to_postgresql(df: pd.DataFrame, db_uri: str, target_table: str):
    """
    Charge les données nettoyées dans une base de données PostgreSQL moderne.
    """
    try:
        logger.info(f"Connexion au Data Warehouse PostgreSQL pour la table : {target_table}")
        engine = create_engine(db_uri)
        
        # Push des données (On remplace les données existantes pour l'exemple)
        df.to_sql(target_table, engine, if_exists='replace', index=False)
        logger.info(f"Chargement réussi de {len(df)} lignes dans la table '{target_table}'.")
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement dans PostgreSQL : {e}")
        logger.info("Simulation : Les données sont prêtes à être intégrées via l'ETL.")

if __name__ == "__main__":
    # --- DÉMONSTRATEUR ETL LOGISTIQUE : Access -> PostgreSQL ---
    print("="*60)
    print("🚀 DÉMARRAGE PIPELINE ETL : MS Access vers PostgreSQL")
    print("="*60)
    
    # 1. Chemin vers votre base Access historique (Legacy)
    # Souvent partagée sur un réseau d'entreprise par les équipes opérationnelles
    ACCESS_DB_PATH = r"C:\data\historique_flotte.accdb"
    TABLE_NOM = "Logs_Maintenance"
    
    # 2. URI de votre base PostgreSQL moderne
    # (Remplacez par votre URI PostgreSQL locale ou Cloud)
    POSTGRES_URI = "postgresql://user:password@localhost:5432/camrail_dw"
    
    # Exécution du Pipeline
    donnees_brutes = extract_from_access(ACCESS_DB_PATH, TABLE_NOM)
    donnees_propres = transform_data(donnees_brutes)
    load_to_postgresql(donnees_propres, POSTGRES_URI, target_table="fact_maintenance")
    
    print("="*60)
    print("✅ PIPELINE TERMINÉ AUTOMATIQUEMENT")
    print("Aperçu des données prêtes pour Power BI (Data Warehouse) :")
    print(donnees_propres.head(3))
