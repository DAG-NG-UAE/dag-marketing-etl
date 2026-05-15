
-- QUERY 09: Which source brings the most engaged visitors?
-- PURPOSE:  Ranks traffic sources by quality not just volume —
--           best bounce rate, time on site and pages per session

SELECT
    source,
    medium,
    SUM(sessions) AS total_sessions,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_sec,
    ROUND(AVG(page_views)::numeric, 2) AS avg_pages_per_session,
    SUM(new_users) AS new_users
FROM ga_traffic
GROUP BY source, medium
HAVING SUM(sessions) > 15
ORDER BY avg_bounce_rate ASC, avg_time_sec DESC;