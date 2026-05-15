-- QUERY 04: Which pages are most visited?
-- PURPOSE:  Shows the most visited pages ranked by sessions
--           with engagement metrics for each page

SELECT 
    page_path,
    SUM(sessions) AS total_sessions,
    SUM(page_views) AS total_page_views,
    SUM(total_users) AS total_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_on_page_sec
FROM ga_traffic
GROUP BY page_path
ORDER BY total_sessions DESC
LIMIT 15;