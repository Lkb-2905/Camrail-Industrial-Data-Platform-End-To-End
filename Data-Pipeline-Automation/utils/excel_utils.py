"""
Utilitaires Excel pour le projet CAMRAIL.
Lecture, écriture et export de données vers des fichiers .xlsx.
Compatible avec Power BI, reporting manuel et échanges métier.
"""
import os
import pandas as pd
from loguru import logger
from datetime import datetime


def read_excel(path: str, sheet_name=0) -> pd.DataFrame:
    """
    Lit un fichier Excel (.xlsx) et retourne un DataFrame.
    
    Args:
        path: Chemin vers le fichier .xlsx
        sheet_name: Nom ou index de la feuille (0 = première)
    
    Returns:
        pd.DataFrame
        
    Example:
        df = read_excel("data/transactions.xlsx", sheet_name="Feuille1")
    """
    try:
        df = pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl')
        logger.info(f"✔️ Excel lu : {path} ({len(df)} lignes)")
        return df
    except Exception as e:
        logger.error(f"❌ Erreur lecture Excel {path}: {e}")
        raise


def write_excel(df: pd.DataFrame, path: str, sheet_name: str = "Données") -> None:
    """
    Écrit un DataFrame dans un fichier Excel (.xlsx).
    
    Args:
        df: DataFrame à exporter
        path: Chemin de destination
        sheet_name: Nom de la feuille Excel
    """
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        df.to_excel(path, sheet_name=sheet_name, index=False, engine='openpyxl')
        logger.success(f"✔️ Excel créé : {path} ({len(df)} lignes)")
    except Exception as e:
        logger.error(f"❌ Erreur écriture Excel {path}: {e}")
        raise


def export_dwh_to_excel(db_path: str, output_path: str) -> None:
    """
    Exporte le contenu du DWH SQLite vers un fichier Excel multi-feuilles.
    Chaque table devient une feuille.
    
    Args:
        db_path: Chemin vers supply_chain_dwh.sqlite
        output_path: Chemin vers le fichier .xlsx de sortie
    """
    import sqlite3
    conn = sqlite3.connect(db_path)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Feuille 1 : Transactions
        df_transac = pd.read_sql_query("SELECT * FROM fact_transactions", conn)
        df_transac.to_excel(writer, sheet_name='Transactions', index=False)
        
        # Feuille 2 : Statistiques par site
        df_stats = pd.read_sql_query("SELECT * FROM aggr_daily_site_stats", conn)
        df_stats.to_excel(writer, sheet_name='Stats_Sites', index=False)
        
        # Feuille 3 : Synthèse (KPI)
        df_kpi = pd.DataFrame([{
            'Métrique': 'Total transactions',
            'Valeur': len(df_transac),
            'Date export': datetime.now().strftime('%Y-%m-%d %H:%M')
        }, {
            'Métrique': 'Sites actifs',
            'Valeur': df_stats['site_location'].nunique(),
            'Date export': datetime.now().strftime('%Y-%m-%d %H:%M')
        }])
        df_kpi.to_excel(writer, sheet_name='KPI_Synthèse', index=False)
    
    conn.close()
    logger.success(f"✔️ DWH exporté vers Excel : {output_path}")


def export_erp_excel_template(output_path: str, num_rows: int = 100) -> None:
    """
    Génère un fichier Excel modèle pour saisie ERP (format attendu par le pipeline).
    Utile pour les opérationnels qui saisissent dans Excel.
    
    Args:
        output_path: Chemin du fichier .xlsx
        num_rows: Nombre de lignes vides à prévoir
    """
    from datetime import datetime, timedelta
    import numpy as np
    
    base_date = datetime.now() - timedelta(days=7)
    template = pd.DataFrame({
        'transaction_id': [f'TRX-{i}' for i in range(num_rows)],
        'machine_id': [''] * num_rows,
        'date': [(base_date + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M') for i in range(num_rows)],
        'volume_transferred': [0.0] * num_rows,
        'status_code': ['OK'] * num_rows
    })
    write_excel(template, output_path, sheet_name='Transactions_ERP')
    logger.info(f"✔️ Modèle ERP Excel créé : {output_path}")
