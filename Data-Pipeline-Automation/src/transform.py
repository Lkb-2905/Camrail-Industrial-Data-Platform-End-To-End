import pandas as pd
from loguru import logger

def transform_data(api_path, erp_path):
    logger.info("⚙️ [TRANSFORM] Application des règles métiers de transformation...")
    
    # Chargement
    df_machines = pd.read_json(api_path)
    df_transactions = pd.read_csv(erp_path)
    
    # 1. Nettoyage des données (Standardisation des dates)
    df_transactions['date'] = pd.to_datetime(df_transactions['date'])
    
    # 2. Jointure (Merge) des données transactionnelles avec le référentiel machine
    logger.info("🔗 Jointure des tables transactionnelles et référentielles...")
    df_merged = pd.merge(df_transactions, df_machines, on='machine_id', how='left')
    
    # 3. Enrichissement (Feature Engineering Business)
    # Règle d'alerte : Volume trop faible + statut d'erreur
    df_merged['critical_alert'] = df_merged.apply(
        lambda row: 1 if row['status_code'] in ['WARN', 'ERR'] and row['volume_transferred'] < 20 else 0,
        axis=1
    )
    
    # 4. Agréation : Vue analytique journalière par site
    df_merged['day'] = df_merged['date'].dt.date
    df_daily_stats = df_merged.groupby(['day', 'site_location']).agg(
        total_volume=('volume_transferred', 'sum'),
        total_alerts=('critical_alert', 'sum'),
        active_machines=('machine_id', 'nunique')
    ).reset_index()
    
    logger.success("✅ Transformation terminée. Données prêtes pour le chargement DWH.")
    return df_merged, df_daily_stats
