# Mini RevOps Data Sync Platform

A portfolio-style data engineering project that simulates how a SaaS company might unify data from multiple business systems into a single reporting layer for operations, support, and customer health analysis.

## Overview

This project models a small Revenue Operations data platform by combining mock CRM, support, and product usage data into a centralized PostgreSQL warehouse. The pipeline ingests raw source files, standardizes messy records across systems, builds staging views for cleanup and normalization, and produces an account-level analytics mart used in a Metabase dashboard.

The goal was to build something that feels closer to a real internal business system than a typical classroom dataset project.

## Business Problem

Modern SaaS teams often work across disconnected tools such as CRMs, support systems, and product telemetry platforms. When customer and account data are spread across multiple systems, it becomes harder to answer practical business questions such as:

- Which accounts are healthy versus at risk?
- How does support load differ by plan type?
- Which accounts are active in the product?
- How many leads are converting into customers?
- Which customer segments may need more attention?

This project addresses that by creating a simplified Customer 360 / Account Health pipeline.

## Tech Stack

- Python
- SQL
- PostgreSQL
- Metabase
- Docker
- CSV mock source files

## Architecture

```text
Mock source data
(CRM, support, product usage CSVs)
        |
        v
Python ingestion scripts
        |
        v
PostgreSQL raw tables
        |
        v
Staging SQL views
(cleaning, normalization, deduplication)
        |
        v
Analytics mart
fct_account_health
        |
        v
Metabase dashboard
```

## Data Sources

The project uses generated mock business data from four source files:

- `crm_accounts.csv`
- `crm_leads.csv`
- `support_tickets.csv`
- `product_events.csv`

These files intentionally include realistic data quality issues such as:

- duplicate leads
- inconsistent company naming across systems
- mixed email casing
- blank values
- unresolved support tickets

## Project Structure

```text
revops-data-sync/
├── data/
│   ├── crm_accounts.csv
│   ├── crm_leads.csv
│   ├── support_tickets.csv
│   └── product_events.csv
├── scripts/
│   ├── generate_mock_data.py
│   └── load_to_postgres.py
├── sql/
│   ├── schema.sql
│   ├── staging.sql
│   └── marts.sql
└── README.md
```

## Pipeline Flow

### 1. Mock data generation
A Python script generates realistic CRM, support, and product usage datasets.

### 2. Raw ingestion
The generated CSV files are loaded into PostgreSQL raw tables:

- `raw_crm_accounts`
- `raw_crm_leads`
- `raw_support_tickets`
- `raw_product_events`

### 3. Staging layer
SQL staging views standardize account names and emails, clean values, and remove duplicate leads:

- `stg_accounts`
- `stg_leads`
- `stg_support_tickets`
- `stg_product_events`

### 4. Analytics layer
The final mart table, `fct_account_health`, combines CRM, support, and product usage metrics into one account-level model.

## Main Metrics in `fct_account_health`

The account health mart includes metrics such as:

- total leads
- converted leads
- total tickets
- closed tickets
- average resolution hours
- total product events
- active users
- events in the last 30 days
- health score
- account health status

## Dashboard

The Metabase dashboard surfaces key account and operational metrics through visual cards such as:

- Account Health Distribution
- Top 10 At-Risk Accounts
- Average Resolution Hours by Plan
- Product Activity by Plan
- Top Healthy Accounts

## How to Run Locally

### Prerequisites

- Python installed
- PostgreSQL installed and running
- Docker Desktop installed and running
- Metabase Docker image pulled locally

### Step 1: generate mock data

```bash
python scripts/generate_mock_data.py
```

### Step 2: load data into PostgreSQL

Make sure your `DB_CONFIG` in `scripts/load_to_postgres.py` matches your local PostgreSQL settings.

Then run:

```bash
python scripts/load_to_postgres.py
```

### Step 3: create staging layer

Run the SQL in `sql/staging.sql` against the `revops_sync` database.

### Step 4: create analytics mart

Run the SQL in `sql/marts.sql` against the `revops_sync` database.

### Step 5: start Metabase locally

If the container already exists:

```bash
docker start metabase
```

If you need to create it:

```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

Then open:

```text
http://localhost:3000
```

Connect Metabase to PostgreSQL using your local connection settings.

## Presenting It Locally

Yes. This project can be presented locally on your machine.

As long as these are available:
- PostgreSQL is running
- Docker Desktop is running
- the Metabase container is running
- your project files remain on your computer

you can open the dashboard at `http://localhost:3000` and present it from your laptop.

If the dashboard does not open, usually you just need to run:

```bash
docker start metabase
```

If PostgreSQL is not running, start PostgreSQL first, then open Metabase.

## Resume-Ready Summary

Built a mini RevOps data platform that integrated mock CRM, support, and product usage data into PostgreSQL, transformed records through staging and analytics layers, and surfaced account health metrics in a Metabase dashboard for operational reporting.

## Future Improvements

Potential next steps for the project include:

- adding automated scheduling
- replacing mock CSVs with live API ingestion
- adding dbt models
- adding data quality checks
- adding dashboard filters by plan type and industry
- building additional marts for conversion funnel and support trends
