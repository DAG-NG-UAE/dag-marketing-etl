-- QUERY 03: Which devices are our users using?
-- PURPOSE:  Shows traffic split by device type with engagement
--           metrics to understand mobile vs desktop performance

SELECT 
    device,
    SUM(sessions) AS total_sessions,
    SUM(total_users) AS total_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_on_site_sec,
    ROUND(SUM(sessions) * 100.0 / SUM(SUM(sessions)) OVER(), 1) AS pct_of_traffic
FROM ga_traffic
GROUP BY device
ORDER BY total_sessions DESC;