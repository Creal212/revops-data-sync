DROP VIEW IF EXISTS stg_product_events;
DROP VIEW IF EXISTS stg_support_tickets;
DROP VIEW IF EXISTS stg_leads;
DROP VIEW IF EXISTS stg_accounts;

DROP FUNCTION IF EXISTS normalize_company_name(TEXT);
DROP FUNCTION IF EXISTS normalize_email(TEXT);

CREATE OR REPLACE FUNCTION normalize_email(input_text TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT NULLIF(lower(trim(coalesce(input_text, ''))), '');
$$;

CREATE OR REPLACE FUNCTION normalize_company_name(input_text TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT NULLIF(
        regexp_replace(
            replace(
                replace(
                    replace(
                        replace(
                            replace(
                                replace(
                                    replace(
                                        replace(
                                            replace(
                                                replace(
                                                    lower(trim(coalesce(input_text, ''))),
                                                    '&',
                                                    'and'
                                                ),
                                                ' technologies',
                                                ' tech'
                                            ),
                                            ' technology',
                                            ' tech'
                                        ),
                                        ' systems',
                                        ' sys'
                                    ),
                                    ' solutions',
                                    ' sol'
                                ),
                                ' corporation',
                                ' corp'
                            ),
                            ' inc',
                            ''
                        ),
                        ' llc',
                        ''
                    ),
                    ' corp',
                    ''
                ),
                ' co',
                ''
            ),
            '[^a-z0-9]+',
            '',
            'g'
        ),
        ''
    );
$$;

CREATE VIEW stg_accounts AS
SELECT
    account_crm_id,
    trim(company_name) AS company_name,
    normalize_company_name(company_name) AS company_key,
    lower(trim(website_domain)) AS website_domain,
    industry,
    employee_count,
    plan_type,
    created_at::timestamp AS created_at
FROM raw_crm_accounts;

CREATE VIEW stg_leads AS
WITH ranked_leads AS (
    SELECT
        lead_id,
        trim(full_name) AS full_name,
        normalize_email(email) AS email,
        trim(company_name) AS company_name,
        normalize_company_name(company_name) AS company_key,
        lower(trim(website_domain)) AS website_domain,
        source,
        created_at::timestamp AS created_at,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY
                coalesce(normalize_email(email), lead_id),
                coalesce(normalize_company_name(company_name), '')
            ORDER BY created_at DESC, lead_id DESC
        ) AS dedupe_rank
    FROM raw_crm_leads
)
SELECT
    lead_id,
    full_name,
    email,
    company_name,
    company_key,
    website_domain,
    source,
    created_at,
    status
FROM ranked_leads
WHERE dedupe_rank = 1;

CREATE VIEW stg_support_tickets AS
SELECT
    ticket_id,
    trim(account_name) AS account_name,
    normalize_company_name(account_name) AS company_key,
    normalize_email(requester_email) AS requester_email,
    priority,
    status,
    category,
    created_at::timestamp AS created_at,
    resolved_at::timestamp AS resolved_at,
    CASE
        WHEN resolved_at IS NOT NULL THEN
            ROUND((EXTRACT(EPOCH FROM (resolved_at - created_at)) / 3600.0)::numeric, 2)
        ELSE NULL
    END AS resolution_hours
FROM raw_support_tickets;

CREATE VIEW stg_product_events AS
SELECT
    event_id,
    trim(account_name) AS account_name,
    normalize_company_name(account_name) AS company_key,
    normalize_email(user_email) AS user_email,
    event_type,
    feature_name,
    event_time::timestamp AS event_time,
    event_time::date AS event_date
FROM raw_product_events;