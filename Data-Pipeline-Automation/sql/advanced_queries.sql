-- ===============================================================================
-- REQUÊTES ANALYTIQUES AVANCÉES (Pour démonstration en entretien Camrail / Bolloré Logistics)
-- ===============================================================================

-- 1. Détection des sites avec une augmentation anormale d'alertes 
-- Utilisation de CTE (Common Table Expressions) et Window Functions (LAG)
WITH DailyVariations AS (
    SELECT 
        site_location,
        day,
        total_alerts,
        LAG(total_alerts, 1) OVER (PARTITION BY site_location ORDER BY day) as previous_day_alerts
    FROM aggr_daily_site_stats
)
SELECT 
    site_location,
    day,
    total_alerts,
    previous_day_alerts,
    ((total_alerts - previous_day_alerts) * 100.0 / NULLIF(previous_day_alerts, 0)) AS alert_increase_percentage
FROM DailyVariations
WHERE total_alerts > previous_day_alerts
ORDER BY alert_increase_percentage DESC;


-- 2. Classement des Gares Logistiques par Fiabilité
-- (Densité de Rank sur le ratio de pannes)
SELECT 
    site_location,
    SUM(total_volume) as global_volume,
    SUM(total_alerts) as total_critical_incidents,
    DENSE_RANK() OVER (ORDER BY SUM(total_alerts) ASC) as reliability_rank
FROM aggr_daily_site_stats
GROUP BY site_location;
