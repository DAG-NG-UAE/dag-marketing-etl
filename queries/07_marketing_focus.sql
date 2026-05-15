-- QUERY 07: Where should we focus our marketing investment?
-- PURPOSE:  Summarises performance by channel to identify
--           which marketing channels deserve more investment

SELECT
    channel,
    SUM(sessions) AS total_sessions,
    SUM(new_users) AS new_users,
    ROUND(AVG(bounce_rate)::numeric, 2) AS avg_bounce_rate,
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_sec,
    ROUND(SUM(sessions) * 100.0 / SUM(SUM(sessions)) OVER(), 1) AS pct_of_traffic
FROM ga_traffic
GROUP BY channel
ORDER BY total_sessions DESC;