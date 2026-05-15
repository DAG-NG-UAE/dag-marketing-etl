
-- QUERY 10: What does a new visitor look like vs a returning visitor?
-- PURPOSE:  Compares behaviour of first time visitors against
--           people who have visited the site before

SELECT
    CASE
        WHEN new_users = total_users THEN 'New Visitors'
        WHEN new_users = 0 THEN 'Returning Visitors'
        ELSE 'Mixed'
    END AS visitor_type,
    COUNT(*) AS total_rows,
    SUM(sessions) AS total_sessions,
    SUM(total_users) AS total_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_sec,
    ROUND(AVG(page_views)::numeric, 2) AS avg_pages_per_session
FROM ga_traffic
GROUP BY visitor_type
ORDER BY total_sessions DESC;