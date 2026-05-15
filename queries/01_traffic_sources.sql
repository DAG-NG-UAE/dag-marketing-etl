
-- QUERY 01: Where is our traffic coming from?
-- PURPOSE:  Shows all traffic sources, how many sessions each
--           got, user counts, and how engaged each source is

SELECT 
    source,
    medium,
    channel,
    SUM(sessions) AS total_sessions,
    SUM(total_users) AS total_users,
    SUM(new_users) AS new_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate
FROM ga_traffic
GROUP BY source, medium, channel
ORDER BY total_sessions DESC;