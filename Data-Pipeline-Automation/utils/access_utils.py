"""
Utilitaires Microsoft Access pour le projet CAMRAIL.
Connexion et requêtes sur bases .mdb /.accdb.
Nécessite : Microsoft Access Database Engine (ODBC) installé sur Windows.
"""
import os
import pandas as pd
from loguru import logger

# Optionnel : pyodbc pour connexion Access
try:
    import pyodbc
    ACCESS_AVAILABLE = True
except ImportError:
    ACCESS_AVAILABLE = False
    pyodbc = None


def get_access_connection(db_path: str) -> "pyodbc.Connection":
    """
    Établit une connexion ODBC vers une base Microsoft Access.
    
    Args:
        db_path: Chemin vers le fichier .mdb ou .accdb
        
    Returns:
        Connexion pyodbc
        
    Raises:
        RuntimeError: Si pyodbc ou le pilote Access n'est pas disponible
    """
    if not ACCESS_AVAILABLE:
        raise RuntimeError("pyodbc non installé. Exécutez : pip install pyodbc")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Base Access introuvable : {db_path}")
    
    # Pilote selon l'extension (.accdb = 64-bit, .mdb = ancien)
    ext = os.path.splitext(db_path)[1].lower()
    if ext == '.accdb':
        driver = "{Microsoft Access Driver (*.mdb, *.accdb)}"
    else:
        driver = "{Microsoft Access Driver (*.mdb, *.accdb)}"
    
    conn_str = f"Driver={driver};DBQ={os.path.abspath(db_path)};"
    
    try:
        conn = pyodbc.connect(conn_str)
        logger.info(f"✔️ Connexion Access établie : {db_path}")
        return conn
    except pyodbc.Error as e:
        logger.error(f"❌ Erreur connexion Access. Vérifiez que le pilote ODBC est installé.")
        logger.error("   Téléchargement : https://www.microsoft.com/download/details.aspx?id=54920")
        raise


def read_access_table(db_path: str, table_name: str) -> pd.DataFrame:
    """
    Lit une table Access et retourne un DataFrame.
    
    Args:
        db_path: Chemin vers .mdb ou .accdb
        table_name: Nom de la table
        
    Returns:
        pd.DataFrame
        
    Example:
        df = read_access_table("data/erp.accdb", "Transactions")
    """
    conn = get_access_connection(db_path)
    try:
        df = pd.read_sql(f"SELECT * FROM [{table_name}]", conn)
        logger.info(f"✔️ Table {table_name} lue ({len(df)} lignes)")
        return df
    finally:
        conn.close()


def export_for_access_import(sqlite_path: str, excel_path: str) -> None:
    """
    Exporte le DWH SQLite vers Excel dans un format compatible
    avec l'import Microsoft Access (Données externes > Excel).
    
    Workflow : SQLite → Excel → Import manuel dans Access
    
    Args:
        sqlite_path: Chemin vers supply_chain_dwh.sqlite
        excel_path: Chemin du fichier .xlsx à créer
    """
    from .excel_utils import export_dwh_to_excel
    export_dwh_to_excel(sqlite_path, excel_path)
    logger.info("💡 Pour importer dans Access : Données > Nouvelle source de données > Fichier > Excel")
