DROP TABLE IF EXISTS raw_product_events;
DROP TABLE IF EXISTS raw_support_tickets;
DROP TABLE IF EXISTS raw_crm_leads;
DROP TABLE IF EXISTS raw_crm_accounts;

CREATE TABLE raw_crm_accounts (
    account_crm_id TEXT PRIMARY KEY,
    company_name TEXT,
    website_domain TEXT,
    industry TEXT,
    employee_count INT,
    plan_type TEXT,
    created_at TIMESTAMP
);

CREATE TABLE raw_crm_leads (
    lead_id TEXT PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    company_name TEXT,
    website_domain TEXT,
    source TEXT,
    created_at TIMESTAMP,
    status TEXT
);

CREATE TABLE raw_support_tickets (
    ticket_id TEXT PRIMARY KEY,
    account_name TEXT,
    requester_email TEXT,
    priority TEXT,
    status TEXT,
    category TEXT,
    created_at TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE raw_product_events (
    event_id TEXT PRIMARY KEY,
    account_name TEXT,
    user_email TEXT,
    event_type TEXT,
    feature_name TEXT,
    event_time TIMESTAMP
);