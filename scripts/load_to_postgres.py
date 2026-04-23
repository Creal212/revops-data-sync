from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

import psycopg2

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "revops_sync",
    "user": "postgres",
    "password": "5899",
}


def empty_to_none(value: str) -> Optional[str]:
    value = value.strip()
    return value if value != "" else None


def run_schema(conn) -> None:
    schema_path = SQL_DIR / "schema.sql"
    sql_text = schema_path.read_text(encoding="utf-8")

    with conn.cursor() as cur:
        cur.execute(sql_text)
    conn.commit()
    print("Schema created successfully.")


def load_crm_accounts(conn) -> None:
    file_path = DATA_DIR / "crm_accounts.csv"

    with conn.cursor() as cur, file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["account_crm_id"],
                empty_to_none(row["company_name"]),
                empty_to_none(row["website_domain"]),
                empty_to_none(row["industry"]),
                int(row["employee_count"]) if row["employee_count"] else None,
                empty_to_none(row["plan_type"]),
                empty_to_none(row["created_at"]),
            )
            for row in reader
        ]

        cur.executemany(
            """
            INSERT INTO raw_crm_accounts (
                account_crm_id,
                company_name,
                website_domain,
                industry,
                employee_count,
                plan_type,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )

    conn.commit()
    print(f"Loaded {len(rows)} rows into raw_crm_accounts.")


def load_crm_leads(conn) -> None:
    file_path = DATA_DIR / "crm_leads.csv"

    with conn.cursor() as cur, file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["lead_id"],
                empty_to_none(row["full_name"]),
                empty_to_none(row["email"]),
                empty_to_none(row["company_name"]),
                empty_to_none(row["website_domain"]),
                empty_to_none(row["source"]),
                empty_to_none(row["created_at"]),
                empty_to_none(row["status"]),
            )
            for row in reader
        ]

        cur.executemany(
            """
            INSERT INTO raw_crm_leads (
                lead_id,
                full_name,
                email,
                company_name,
                website_domain,
                source,
                created_at,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )

    conn.commit()
    print(f"Loaded {len(rows)} rows into raw_crm_leads.")


def load_support_tickets(conn) -> None:
    file_path = DATA_DIR / "support_tickets.csv"

    with conn.cursor() as cur, file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["ticket_id"],
                empty_to_none(row["account_name"]),
                empty_to_none(row["requester_email"]),
                empty_to_none(row["priority"]),
                empty_to_none(row["status"]),
                empty_to_none(row["category"]),
                empty_to_none(row["created_at"]),
                empty_to_none(row["resolved_at"]),
            )
            for row in reader
        ]

        cur.executemany(
            """
            INSERT INTO raw_support_tickets (
                ticket_id,
                account_name,
                requester_email,
                priority,
                status,
                category,
                created_at,
                resolved_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )

    conn.commit()
    print(f"Loaded {len(rows)} rows into raw_support_tickets.")


def load_product_events(conn) -> None:
    file_path = DATA_DIR / "product_events.csv"

    with conn.cursor() as cur, file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["event_id"],
                empty_to_none(row["account_name"]),
                empty_to_none(row["user_email"]),
                empty_to_none(row["event_type"]),
                empty_to_none(row["feature_name"]),
                empty_to_none(row["event_time"]),
            )
            for row in reader
        ]

        cur.executemany(
            """
            INSERT INTO raw_product_events (
                event_id,
                account_name,
                user_email,
                event_type,
                feature_name,
                event_time
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            rows,
        )

    conn.commit()
    print(f"Loaded {len(rows)} rows into raw_product_events.")


def main() -> None:
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        run_schema(conn)
        load_crm_accounts(conn)
        load_crm_leads(conn)
        load_support_tickets(conn)
        load_product_events(conn)
        print("All raw data loaded successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
