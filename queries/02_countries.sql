-- QUERY 02: Which countries are our users from?
-- PURPOSE:  Shows traffic volume, engagement and time on site
--           broken down by country, ordered by most sessions

SELECT 
    country,
    SUM(sessions) AS total_sessions,
    SUM(total_users) AS total_users,
    SUM(new_users) AS new_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_on_site_sec
FROM ga_traffic
GROUP BY country
ORDER BY total_sessions DESC;