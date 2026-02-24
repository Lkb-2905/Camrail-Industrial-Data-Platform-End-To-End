"""
Exemples d'utilisation Excel et Access dans le projet CAMRAIL.
À exécuter depuis la racine du projet :

  pip install -r exemples_excel_access/requirements.txt
  python exemples_excel_access/run_exemples.py

Les fichiers générés sont dans exemples_excel_access/output/
"""
import os
import sys
import logging

# Configurer le logging (équivalent loguru, sans dépendance externe)
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Chemin racine du projet et utils DPA
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dpa_utils = os.path.join(root, "Data-Pipeline-Automation", "utils")
if dpa_utils not in sys.path:
    sys.path.insert(0, dpa_utils)


def _log_success(msg):
    """Affiche un message de succès (style loguru.success)."""
    logging.info(msg)

def exemple_1_export_excel():
    """Exemple 1 : Export du DWH SQLite vers Excel (reporting)"""
    logger.info("=" * 50)
    logger.info("EXEMPLE 1 : Export DWH → Excel")
    logger.info("=" * 50)
    
    db_path = os.path.join(root, "Data-Pipeline-Automation", "database", "supply_chain_dwh.sqlite")
    excel_path = os.path.join(root, "exemples_excel_access", "output", "rapport_supply_chain.xlsx")
    
    if not os.path.exists(db_path):
        logger.warning("⚠️ Exécutez d'abord le pipeline DPA : python Data-Pipeline-Automation/src/main_pipeline.py")
        return

    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    from excel_utils import export_dwh_to_excel
    export_dwh_to_excel(db_path, excel_path)
    _log_success(f"✅ Rapport Excel créé : {excel_path}")


def exemple_2_modele_erp_excel():
    """Exemple 2 : Génération d'un modèle Excel pour saisie ERP"""
    logger.info("=" * 50)
    logger.info("EXEMPLE 2 : Modèle Excel pour saisie ERP")
    logger.info("=" * 50)
    
    output_path = os.path.join(root, "exemples_excel_access", "output", "modele_saisie_erp.xlsx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    from excel_utils import export_erp_excel_template
    export_erp_excel_template(output_path, num_rows=50)
    _log_success(f"✅ Modèle créé : {output_path}")
    logger.info("💡 Les opérationnels peuvent saisir les transactions dans ce fichier.")


def exemple_3_lecture_excel():
    """Exemple 3 : Lecture d'un fichier Excel"""
    logger.info("=" * 50)
    logger.info("EXEMPLE 3 : Lecture d'un fichier Excel")
    logger.info("=" * 50)
    
    # Utiliser le rapport généré par l'exemple 1, ou le modèle
    excel_path = os.path.join(root, "exemples_excel_access", "output", "rapport_supply_chain.xlsx")
    if not os.path.exists(excel_path):
        excel_path = os.path.join(root, "Data-Pipeline-Automation", "reports", "rapport_supply_chain.xlsx")
    if not os.path.exists(excel_path):
        logger.warning("⚠️ Aucun fichier Excel trouvé. Exécutez l'exemple 1 ou le pipeline.")
        return
    
    from excel_utils import read_excel
    df = read_excel(excel_path, sheet_name="Transactions")
    logger.info(f"📊 Feuille 'Transactions' : {len(df)} lignes")
    logger.info(f"   Colonnes : {list(df.columns)}")
    _log_success("✅ Lecture Excel OK")


def exemple_4_pipeline_avec_excel():
    """Exemple 4 : Pipeline avec source Excel + export Excel"""
    logger.info("=" * 50)
    logger.info("EXEMPLE 4 : Pipeline complet (source Excel → DWH → export Excel)")
    logger.info("=" * 50)
    
    # D'abord générer un modèle, le remplir (simulé), puis lancer le pipeline
    from excel_utils import export_erp_excel_template
    modele = os.path.join(root, "exemples_excel_access", "output", "donnees_erp.xlsx")
    os.makedirs(os.path.dirname(modele), exist_ok=True)
    export_erp_excel_template(modele, num_rows=20)
    
    # Simuler des données (en prod, l'utilisateur remplit Excel)
    import pandas as pd
    from datetime import datetime, timedelta
    df = pd.read_excel(modele, engine='openpyxl')
    df['volume_transferred'] = [10 + i * 2 for i in range(len(df))]
    df['status_code'] = ['OK'] * 15 + ['WARN'] * 3 + ['ERR'] * 2
    df.to_excel(modele, index=False, sheet_name='Transactions_ERP')
    
    # Lancer le pipeline avec source Excel
    sys.path.insert(0, os.path.join(root, "Data-Pipeline-Automation", "src"))
    from extract import extract_from_excel
    from transform import transform_data
    from load import load_data
    
    base_dir = os.path.join(root, "Data-Pipeline-Automation")
    api_file, erp_file = extract_from_excel(modele)
    df_transac, df_stats = transform_data(api_file, erp_file)
    db_path = os.path.join(base_dir, "database", "supply_chain_excel_demo.sqlite")
    schema_path = os.path.join(base_dir, "sql", "schema.sql")
    excel_out = os.path.join(root, "exemples_excel_access", "output", "rapport_final.xlsx")
    os.makedirs(os.path.dirname(excel_out), exist_ok=True)
    load_data(df_transac, df_stats, db_path, schema_path, export_excel_path=excel_out)
    _log_success(f"✅ Pipeline avec Excel terminé : {excel_out}")


def exemple_5_access():
    """Exemple 5 : Connexion Access (lecture) — nécessite base .accdb et pilote ODBC"""
    logger.info("=" * 50)
    logger.info("EXEMPLE 5 : Lecture depuis Microsoft Access")
    logger.info("=" * 50)
    
    try:
        from access_utils import read_access_table, ACCESS_AVAILABLE
        if not ACCESS_AVAILABLE:
            logger.warning("⚠️ pyodbc non installé : pip install pyodbc")
            return
        
        # Chercher une base Access dans le projet (exemple)
        access_path = os.path.join(root, "exemples_excel_access", "data", "demo.accdb")
        if not os.path.exists(access_path):
            logger.info("💡 Pour tester Access : créez une base demo.accdb avec une table 'Transactions'")
            logger.info("   Ou exportez le DWH en Excel puis importez dans Access (Données > Excel)")
            return
        
        df = read_access_table(access_path, "Transactions")
        _log_success(f"✅ Table lue : {len(df)} lignes")
    except Exception as e:
        logger.warning(f"⚠️ Access : {e}")
        logger.info("   Le pilote Microsoft Access ODBC doit être installé sur Windows.")


if __name__ == "__main__":
    logger.info("🚀 Exemples Excel / Access - Projet CAMRAIL")
    exemple_1_export_excel()
    exemple_2_modele_erp_excel()
    exemple_3_lecture_excel()
    exemple_4_pipeline_avec_excel()
    exemple_5_access()
    _log_success("✅ Tous les exemples terminés. Consultez le dossier output/.")
