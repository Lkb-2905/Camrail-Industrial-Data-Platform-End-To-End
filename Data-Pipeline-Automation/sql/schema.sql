-- Data Warehouse Supply Chain (Simulé)

-- Table détaillée des transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id TEXT,
    machine_id TEXT,
    date TEXT,
    volume_transferred REAL,
    status_code TEXT,
    site_location TEXT,
    installation_year INTEGER,
    critical_alert INTEGER
);

-- Vue matérialisée / Table pré-agrégée pour les Analystes et Data Scientists
CREATE TABLE IF NOT EXISTS aggr_daily_site_stats (
    day TEXT,
    site_location TEXT,
    total_volume REAL,
    total_alerts INTEGER,
    active_machines INTEGER
);
