DROP TABLE IF EXISTS fct_account_health;

CREATE TABLE fct_account_health AS
WITH lead_metrics AS (
    SELECT
        company_key,
        COUNT(*) AS total_leads,
        COUNT(*) FILTER (WHERE status = 'Customer') AS converted_leads
    FROM stg_leads
    GROUP BY company_key
),
ticket_metrics AS (
    SELECT
        company_key,
        COUNT(*) AS total_tickets,
        COUNT(*) FILTER (WHERE status IN ('Resolved', 'Closed')) AS closed_tickets,
        ROUND(AVG(resolution_hours)::numeric, 2) AS avg_resolution_hours
    FROM stg_support_tickets
    GROUP BY company_key
),
event_metrics AS (
    SELECT
        company_key,
        COUNT(*) AS total_events,
        COUNT(DISTINCT user_email) AS active_users,
        COUNT(*) FILTER (WHERE event_date >= CURRENT_DATE - INTERVAL '30 days') AS events_last_30d
    FROM stg_product_events
    GROUP BY company_key
)
SELECT
    a.account_crm_id,
    a.company_name,
    a.company_key,
    a.website_domain,
    a.industry,
    a.employee_count,
    a.plan_type,
    a.created_at,

    COALESCE(l.total_leads, 0) AS total_leads,
    COALESCE(l.converted_leads, 0) AS converted_leads,

    COALESCE(t.total_tickets, 0) AS total_tickets,
    COALESCE(t.closed_tickets, 0) AS closed_tickets,
    COALESCE(t.avg_resolution_hours, 0) AS avg_resolution_hours,

    COALESCE(e.total_events, 0) AS total_events,
    COALESCE(e.active_users, 0) AS active_users,
    COALESCE(e.events_last_30d, 0) AS events_last_30d,

    CASE
        WHEN COALESCE(e.events_last_30d, 0) >= 80
             AND COALESCE(t.avg_resolution_hours, 9999) <= 48
             AND COALESCE(t.total_tickets, 0) <= 15
        THEN 'Healthy'

        WHEN COALESCE(e.events_last_30d, 0) >= 30
             AND COALESCE(t.avg_resolution_hours, 9999) <= 96
        THEN 'Monitor'

        ELSE 'At Risk'
    END AS account_health_status,

    ROUND(
        (
            LEAST(COALESCE(e.events_last_30d, 0), 100) * 0.45 +
            LEAST(COALESCE(e.active_users, 0) * 5, 100) * 0.20 +
            LEAST(COALESCE(l.converted_leads, 0) * 20, 100) * 0.15 +
            GREATEST(100 - LEAST(COALESCE(t.avg_resolution_hours, 0), 100), 0) * 0.20
        )::numeric,
        2
    ) AS health_score

FROM stg_accounts a
LEFT JOIN lead_metrics l
    ON a.company_key = l.company_key
LEFT JOIN ticket_metrics t
    ON a.company_key = t.company_key
LEFT JOIN event_metrics e
    ON a.company_key = e.company_key;