-- QUERY 05: How engaged are our users overall?
-- PURPOSE:  Single row summary of overall website engagement
--           metrics across all traffic for the full period

SELECT
    ROUND(AVG(avg_session_duration_sec)::numeric, 2) AS avg_time_on_site_sec,
    ROUND(AVG(avg_session_duration_sec / 60)::numeric, 2) AS avg_time_on_site_mins,
    ROUND(AVG(bounce_rate)::numeric, 2) AS overall_bounce_rate,
    ROUND(AVG(page_views)::numeric, 2) AS avg_pages_per_session,
    SUM(sessions) AS total_sessions,
    SUM(total_users) AS total_users,
    SUM(new_users) AS total_new_users,
    ROUND(SUM(new_users) * 100.0 / SUM(total_users), 1) AS new_user_pct
FROM ga_traffic;