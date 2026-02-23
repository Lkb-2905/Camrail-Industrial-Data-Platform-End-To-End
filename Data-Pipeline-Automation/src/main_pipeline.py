import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from loguru import logger
from extract import extract_data
from transform import transform_data
from load import load_data

def run_pipeline():
    logger.info("🚀 --- DÉMARRAGE DU PIPELINE AUTOMATISÉ ---")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data_raw")
    db_path = os.path.join(base_dir, "database", "supply_chain_dwh.sqlite")
    schema_path = os.path.join(base_dir, "sql", "schema.sql")
    excel_report_path = os.path.join(base_dir, "reports", "rapport_supply_chain.xlsx")
    
    try:
        # 1. EXTRACT
        api_data, erp_data = extract_data(raw_dir)
        
        # 2. TRANSFORM
        df_transac, df_stats = transform_data(api_data, erp_data)
        
        # 3. LOAD (SQLite + export Excel optionnel)
        load_data(df_transac, df_stats, db_path, schema_path, export_excel_path=excel_report_path)
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors de l'exécution du pipeline: {e}")

if __name__ == "__main__":
    run_pipeline()
