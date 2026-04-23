from __future__ import annotations

import csv
import random
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

NOW = datetime.now()

FIRST_NAMES = [
    "Ava", "Noah", "Liam", "Emma", "Olivia", "Mia", "Sophia", "Elijah", "James",
    "Lucas", "Amelia", "Harper", "Evelyn", "Benjamin", "Daniel", "Mason", "Chloe",
    "Logan", "Isabella", "Charlotte", "Ethan", "Alexander", "Sofia", "Ella",
    "Michael", "David", "Camila", "Luna", "Avery", "Aria", "Samuel", "Henry",
]

LAST_NAMES = [
    "Johnson", "Smith", "Brown", "Taylor", "Anderson", "Thomas", "Moore", "Martin",
    "Jackson", "White", "Harris", "Clark", "Lewis", "Walker", "Hall", "Allen",
    "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson",
]

COMPANY_PART_1 = [
    "NorthPeak", "BlueRiver", "CloudForge", "BrightPath", "Summit", "Velocity",
    "ClearBridge", "Nova", "Ironwood", "SilverLine", "Everstone", "CedarPoint",
    "Greenfield", "Vertex", "Skyline", "Redwood", "Apex", "PrimeWave",
]

COMPANY_PART_2 = [
    "Health", "Labs", "Systems", "Analytics", "Works", "Logic", "Partners",
    "Software", "Dynamics", "Solutions", "Ops", "Data", "Networks", "Cloud",
    "Digital", "Technologies",
]

INDUSTRIES = [
    "SaaS", "Fintech", "Healthcare", "Retail", "Education", "Logistics",
    "Manufacturing", "Marketing", "Cybersecurity", "E-commerce",
]

PLAN_TYPES = ["Free", "Starter", "Growth", "Pro", "Enterprise"]
LEAD_SOURCES = ["Website", "Referral", "LinkedIn", "Outbound", "Conference", "Webinar"]
LEAD_STATUSES = ["New", "Contacted", "Qualified", "Demo", "Customer", "Lost"]

TICKET_PRIORITIES = ["Low", "Medium", "High", "Urgent"]
TICKET_STATUSES = ["Open", "Pending", "Resolved", "Closed"]
TICKET_CATEGORIES = [
    "Billing", "Login Issue", "API Issue", "Integration", "Bug Report",
    "Feature Request", "Data Sync", "Access Request",
]

EVENT_TYPES = [
    "login",
    "view_dashboard",
    "create_workflow",
    "run_sync",
    "export_report",
    "invite_user",
    "update_settings",
    "connect_integration",
]

FEATURE_NAMES = [
    "dashboard",
    "workflow_builder",
    "account_view",
    "support_center",
    "integration_hub",
    "analytics",
    "report_export",
    "user_admin",
]

ACCOUNT_SUFFIXES = ["Inc", "LLC", "Co", "Corp", "Group", ""]

PROSPECT_COMPANIES = [
    "Falcon Ridge Media", "Oakline Insights", "Pioneer Health Group",
    "Delta Harbor Systems", "Riverbend Commerce", "Altitude Growth Labs",
    "Beacon Trail Logistics", "Cobalt Retail Partners", "Summerset AI Works",
    "Mariner Data House", "Golden State Metrics", "Atlas Revenue Labs",
]


def random_datetime_within(days_back: int) -> datetime:
    start = NOW - timedelta(days=days_back)
    delta = NOW - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def slugify_company(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", name.lower()).strip()
    cleaned = re.sub(r"\s+", "-", cleaned)
    return cleaned


def company_to_domain(name: str) -> str:
    base = slugify_company(name).replace("-", "")
    return f"{base}.com"


def maybe_blank(value: str, blank_rate: float = 0.0) -> str:
    return "" if random.random() < blank_rate else value


def maybe_case_variation(value: str) -> str:
    roll = random.random()
    if roll < 0.08:
        return value.upper()
    if roll < 0.16:
        return value.lower()
    return value


def variant_account_name(name: str) -> str:
    value = name

    if random.random() < 0.25:
        suffix = random.choice([s for s in ACCOUNT_SUFFIXES if s])
        value = f"{value} {suffix}"

    if random.random() < 0.15:
        value = value.replace("and", "&")

    if random.random() < 0.18:
        value = f" {value} "

    if random.random() < 0.14:
        value = value.replace("  ", " ")

    value = maybe_case_variation(value)

    if random.random() < 0.10:
        value = value.replace("Systems", "Sys")
        value = value.replace("Technologies", "Tech")
        value = value.replace("Solutions", "Sol")

    return value


def build_full_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def build_email(full_name: str, domain: str) -> str:
    first, last = full_name.lower().split()
    patterns = [
        f"{first}.{last}@{domain}",
        f"{first[0]}{last}@{domain}",
        f"{first}{last[0]}@{domain}",
        f"{first}_{last}@{domain}",
    ]
    return random.choice(patterns)


def write_csv(filename: str, rows: list[dict], fieldnames: list[str]) -> None:
    filepath = DATA_DIR / filename
    with filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_accounts(n: int = 200) -> list[dict]:
    seen_names = set()
    accounts = []

    while len(accounts) < n:
        name = f"{random.choice(COMPANY_PART_1)} {random.choice(COMPANY_PART_2)}"
        if name in seen_names:
            continue
        seen_names.add(name)

        created_at = random_datetime_within(730)

        accounts.append(
            {
                "account_crm_id": f"ACC-{1000 + len(accounts)}",
                "company_name": name,
                "website_domain": company_to_domain(name),
                "industry": random.choice(INDUSTRIES),
                "employee_count": random.choice([10, 15, 25, 40, 75, 120, 250, 500, 1000]),
                "plan_type": random.choices(
                    PLAN_TYPES,
                    weights=[10, 18, 28, 24, 20],
                    k=1,
                )[0],
                "created_at": created_at.isoformat(sep=" ", timespec="seconds"),
            }
        )

    return accounts


def build_leads(accounts: list[dict], n: int = 500) -> list[dict]:
    leads = []
    account_pool = random.sample(accounts, k=min(120, len(accounts)))

    for i in range(n):
        name = build_full_name()

        use_existing_account = random.random() < 0.45
        if use_existing_account:
            account = random.choice(account_pool)
            company_name = account["company_name"]
            domain = account["website_domain"]
        else:
            company_name = random.choice(PROSPECT_COMPANIES)
            domain = company_to_domain(company_name)

        status = random.choices(
            LEAD_STATUSES,
            weights=[18, 20, 18, 14, 16, 14],
            k=1,
        )[0]

        if use_existing_account and random.random() < 0.25:
            status = "Customer"

        email = build_email(name, domain)
        email = maybe_blank(email, blank_rate=0.08)

        if email and random.random() < 0.10:
            email = email.upper()

        leads.append(
            {
                "lead_id": f"LEAD-{10000 + i}",
                "full_name": name,
                "email": email,
                "company_name": variant_account_name(company_name),
                "website_domain": domain,
                "source": random.choice(LEAD_SOURCES),
                "created_at": random_datetime_within(365).isoformat(sep=" ", timespec="seconds"),
                "status": status,
            }
        )

    # Intentional duplicates
    for dup_index in random.sample(range(len(leads)), k=20):
        copied = dict(leads[dup_index])
        copied["lead_id"] = f"LEAD-DUP-{dup_index}"
        if copied["email"]:
            copied["email"] = copied["email"].lower()
        copied["company_name"] = variant_account_name(copied["company_name"].strip())
        leads.append(copied)

    return leads


def build_support_tickets(accounts: list[dict], n: int = 2000) -> list[dict]:
    tickets = []

    for i in range(n):
        account = random.choice(accounts)
        created_at = random_datetime_within(240)
        status = random.choices(
            TICKET_STATUSES,
            weights=[22, 18, 35, 25],
            k=1,
        )[0]

        if status in {"Resolved", "Closed"}:
            resolve_delay_hours = random.randint(2, 168)
            resolved_at = created_at + timedelta(hours=resolve_delay_hours)
            resolved_value = resolved_at.isoformat(sep=" ", timespec="seconds")
        else:
            resolved_value = ""

        requester_name = build_full_name()
        requester_email = build_email(requester_name, account["website_domain"])
        requester_email = maybe_blank(requester_email, blank_rate=0.05)

        if requester_email and random.random() < 0.06:
            requester_email = requester_email.upper()

        tickets.append(
            {
                "ticket_id": f"TICK-{50000 + i}",
                "account_name": variant_account_name(account["company_name"]),
                "requester_email": requester_email,
                "priority": random.choices(
                    TICKET_PRIORITIES,
                    weights=[20, 45, 25, 10],
                    k=1,
                )[0],
                "status": status,
                "category": random.choice(TICKET_CATEGORIES),
                "created_at": created_at.isoformat(sep=" ", timespec="seconds"),
                "resolved_at": resolved_value,
            }
        )

    return tickets


def build_product_events(accounts: list[dict], n: int = 20000) -> list[dict]:
    events = []
    account_users: dict[str, list[str]] = defaultdict(list)

    for account in accounts:
        user_count = random.randint(2, 12)
        users = []
        for _ in range(user_count):
            full_name = build_full_name()
            users.append(build_email(full_name, account["website_domain"]).lower())
        account_users[account["account_crm_id"]] = users

    for i in range(n):
        account = random.choice(accounts)
        users = account_users[account["account_crm_id"]]
        user_email = random.choice(users)

        if random.random() < 0.04:
            user_email = user_email.upper()

        event_type = random.choices(
            EVENT_TYPES,
            weights=[25, 20, 10, 12, 8, 8, 7, 10],
            k=1,
        )[0]

        events.append(
            {
                "event_id": f"EVT-{900000 + i}",
                "account_name": variant_account_name(account["company_name"]),
                "user_email": user_email,
                "event_type": event_type,
                "feature_name": random.choice(FEATURE_NAMES),
                "event_time": random_datetime_within(180).isoformat(sep=" ", timespec="seconds"),
            }
        )

    return events


def main() -> None:
    accounts = build_accounts(200)
    leads = build_leads(accounts, 500)
    tickets = build_support_tickets(accounts, 2000)
    events = build_product_events(accounts, 20000)

    write_csv(
        "crm_accounts.csv",
        accounts,
        [
            "account_crm_id",
            "company_name",
            "website_domain",
            "industry",
            "employee_count",
            "plan_type",
            "created_at",
        ],
    )

    write_csv(
        "crm_leads.csv",
        leads,
        [
            "lead_id",
            "full_name",
            "email",
            "company_name",
            "website_domain",
            "source",
            "created_at",
            "status",
        ],
    )

    write_csv(
        "support_tickets.csv",
        tickets,
        [
            "ticket_id",
            "account_name",
            "requester_email",
            "priority",
            "status",
            "category",
            "created_at",
            "resolved_at",
        ],
    )

    write_csv(
        "product_events.csv",
        events,
        [
            "event_id",
            "account_name",
            "user_email",
            "event_type",
            "feature_name",
            "event_time",
        ],
    )

    print("Mock data generated successfully.")
    print(f"Accounts: {len(accounts)}")
    print(f"Leads: {len(leads)}")
    print(f"Tickets: {len(tickets)}")
    print(f"Product events: {len(events)}")
    print(f"Files saved to: {DATA_DIR}")


if __name__ == "__main__":
    main()
