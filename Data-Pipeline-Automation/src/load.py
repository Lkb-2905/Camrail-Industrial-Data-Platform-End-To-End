import sqlite3
import pandas as pd
from loguru import logger
import os

def load_data(df_transac, df_stats, db_path, schema_path, export_excel_path=None):
    logger.info("💾 [LOAD] Chargement dans la base de données SQL...")
    
    # Initialisation de la BDD et création des schémas depuis le fichier .sql
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    conn.executescript(schema)
    logger.info("✔️ Schémas de base de données validés.")

    # Chargement (Overwriting the table in this simulation to keep it clean)
    df_transac.to_sql('fact_transactions', conn, if_exists='replace', index=False)
    logger.info(f"✔️ {len(df_transac)} transactions chargées.")
    
    df_stats.to_sql('aggr_daily_site_stats', conn, if_exists='replace', index=False)
    logger.info(f"✔️ {len(df_stats)} agrégats quotidiens chargés.")
    
    conn.commit()
    
    # Export Excel optionnel (reporting, échanges métier)
    if export_excel_path:
        try:
            import sys
            utils_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils')
            if utils_path not in sys.path:
                sys.path.insert(0, utils_path)
            from excel_utils import export_dwh_to_excel
            os.makedirs(os.path.dirname(export_excel_path), exist_ok=True)
            export_dwh_to_excel(db_path, export_excel_path)
        except Exception as e:
            logger.warning(f"⚠️ Export Excel ignoré (openpyxl ?) : {e}")
    
    conn.close()
    logger.success(f"🎇 Pipeline terminé ! Base de données disponible : {db_path}")
