-- QUERY 06: Are we growing over time?
-- PURPOSE:  Shows week by week traffic trend to identify
--           growth patterns, peaks and declining periods

SELECT
    DATE_TRUNC('week', date) AS week,
    SUM(sessions) AS total_sessions,
    SUM(total_users) AS total_users,
    SUM(new_users) AS new_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate
FROM ga_traffic
GROUP BY DATE_TRUNC('week', date)
ORDER BY week ASC;