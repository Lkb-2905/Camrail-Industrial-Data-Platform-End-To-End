import pandas as pd
import numpy as np
from loguru import logger
import os
from datetime import datetime, timedelta

def extract_data(out_dir):
    logger.info("📡 [EXTRACT] Connexion aux sources de données simulées...")
    os.makedirs(out_dir, exist_ok=True)
    
    # Simulation 1 : Données référentielles d'une "API" (JSON)
    api_file = os.path.join(out_dir, "api_reference_machines.json")
    machines = {
        'machine_id': [f"MCH-{str(i).zfill(3)}" for i in range(1, 21)],
        'site_location': np.random.choice(['Douala', 'Yaoundé', 'Ngaoundéré', 'Bélabo', 'Edéa'], size=20),
        'installation_year': np.random.randint(2010, 2023, size=20)
    }
    pd.DataFrame(machines).to_json(api_file, orient='records', indent=4)
    logger.info(f"✔️ Données API extraites : {api_file}")

    # Simulation 2 : Données transactionnelles brutes d'un "ERP" (CSV)
    erp_file = os.path.join(out_dir, "erp_daily_transactions.csv")
    recs = []
    base_date = datetime.now() - timedelta(days=7)
    for i in range(500):
        recs.append({
            'transaction_id': f"TRX-{i}",
            'machine_id': np.random.choice(machines['machine_id']),
            'date': (base_date + timedelta(minutes=i*15)).strftime("%Y-%m-%d %H:%M:%S"),
            'volume_transferred': np.random.uniform(10.5, 95.0),
            'status_code': np.random.choice(['OK', 'OK', 'WARN', 'ERR'])
        })
    pd.DataFrame(recs).to_csv(erp_file, index=False)
    logger.info(f"✔️ Données ERP extraites : {erp_file}")
    
    return api_file, erp_file


def extract_from_excel(excel_path: str, out_dir: str = None) -> tuple:
    """
    Source alternative : extraction depuis un fichier Excel.
    Utile quand les données ERP sont saisies dans Excel par les opérationnels.
    
    Args:
        excel_path: Chemin vers le fichier .xlsx
        out_dir: Dossier de sortie (défaut : data_raw)
    
    Returns:
        (api_file, erp_csv_path) - compatible avec transform_data()
    """
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(base_dir, 'utils'))
    from excel_utils import read_excel
    
    logger.info("📡 [EXTRACT] Lecture depuis Excel...")
    df = read_excel(excel_path, sheet_name=0)
    
    required = ['transaction_id', 'machine_id', 'date', 'volume_transferred', 'status_code']
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}. Attendues : {required}")
    
    out_dir = out_dir or os.path.join(base_dir, "data_raw")
    os.makedirs(out_dir, exist_ok=True)
    csv_temp = os.path.join(out_dir, "erp_from_excel.csv")
    df[required].to_csv(csv_temp, index=False)
    
    # Référentiel machines : générer si absent
    api_file = os.path.join(out_dir, "api_reference_machines.json")
    if not os.path.exists(api_file):
        extract_data(out_dir)  # Crée api + erp (on écrase erp ci-dessous)
    api_file = os.path.join(out_dir, "api_reference_machines.json")
    return api_file, csv_temp


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    extract_data(os.path.join(base_dir, "data_raw"))
