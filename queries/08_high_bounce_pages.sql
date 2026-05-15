-- QUERY 08: Which pages have the highest bounce rate?
-- PURPOSE:  Identifies pages that are failing visitors —
--           high bounce means people land and leave immediately

SELECT
    page_path,
    SUM(sessions) AS total_sessions,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_on_page_sec,
    SUM(total_users) AS total_users
FROM ga_traffic
GROUP BY page_path
HAVING SUM(sessions) > 20
ORDER BY avg_bounce_rate DESC
LIMIT 15;