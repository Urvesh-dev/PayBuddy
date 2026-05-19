#!/usr/bin/env python3
"""
Bulk seed script for PayBuddy employees.

Performance strategy:
- TRUNCATE + bulk INSERT via SQLAlchemy executemany in batches (default 1000)
- Single transaction per batch with commit at end
- Pre-generated rows in memory to avoid ORM overhead

Expected runtime (10k rows): ~3-8s on local PostgreSQL, ~1-2s on SSD with tuned PG.

Usage:
  python scripts/seed_employees.py [--count 10000] [--reset]
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

# Allow running from repo root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import phonenumbers
from phonenumbers import PhoneNumberType
from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import Session, sessionmaker

from app.models.employee import Employee, EmployeeStatus, EmploymentType, Gender

# (country name, currency, ISO region for valid phone generation)
COUNTRIES = [
    ("United States", "USD", "US"),
    ("United Kingdom", "GBP", "GB"),
    ("Canada", "CAD", "CA"),
    ("Germany", "EUR", "DE"),
    ("France", "EUR", "FR"),
    ("India", "INR", "IN"),
    ("Australia", "AUD", "AU"),
    ("Singapore", "SGD", "SG"),
    ("Japan", "JPY", "JP"),
    ("Brazil", "BRL", "BR"),
    ("Netherlands", "EUR", "NL"),
    ("Spain", "EUR", "ES"),
    ("Italy", "EUR", "IT"),
    ("Mexico", "MXN", "MX"),
    ("South Africa", "ZAR", "ZA"),
]

DEPARTMENTS = [
    "Engineering",
    "Product",
    "Design",
    "Marketing",
    "Sales",
    "Finance",
    "HR",
    "Operations",
    "Legal",
    "Customer Success",
    "Data Science",
    "IT",
]

JOB_TITLES = {
    "Engineering": [
        "Software Engineer",
        "Senior Software Engineer",
        "Staff Engineer",
        "Engineering Manager",
        "DevOps Engineer",
        "QA Engineer",
    ],
    "Product": ["Product Manager", "Associate PM", "Director of Product"],
    "Design": ["UX Designer", "UI Designer", "Design Lead"],
    "Marketing": ["Marketing Manager", "Content Strategist", "SEO Specialist"],
    "Sales": ["Account Executive", "Sales Manager", "SDR"],
    "Finance": ["Financial Analyst", "Controller", "Accountant"],
    "HR": ["HR Business Partner", "Recruiter", "HR Manager"],
    "Operations": ["Operations Manager", "Program Manager"],
    "Legal": ["Legal Counsel", "Compliance Officer"],
    "Customer Success": ["CS Manager", "Support Specialist"],
    "Data Science": ["Data Scientist", "ML Engineer", "Analytics Lead"],
    "IT": ["Systems Administrator", "IT Support Lead"],
}

CITIES = {
    "United States": ["New York", "San Francisco", "Austin", "Seattle", "Chicago"],
    "United Kingdom": ["London", "Manchester", "Edinburgh"],
    "Canada": ["Toronto", "Vancouver", "Montreal"],
    "Germany": ["Berlin", "Munich", "Hamburg"],
    "France": ["Paris", "Lyon"],
    "India": ["Bangalore", "Mumbai", "Hyderabad", "Delhi"],
    "Australia": ["Sydney", "Melbourne"],
    "Singapore": ["Singapore"],
    "Japan": ["Tokyo", "Osaka"],
    "Brazil": ["São Paulo", "Rio de Janeiro"],
    "Netherlands": ["Amsterdam"],
    "Spain": ["Madrid", "Barcelona"],
    "Italy": ["Milan", "Rome"],
    "Mexico": ["Mexico City", "Guadalajara"],
    "South Africa": ["Johannesburg", "Cape Town"],
}

SALARY_RANGES = {
    "USD": (45000, 220000),
    "GBP": (35000, 150000),
    "EUR": (38000, 160000),
    "INR": (600000, 4500000),
    "CAD": (50000, 180000),
    "AUD": (55000, 190000),
    "SGD": (48000, 200000),
    "JPY": (4000000, 18000000),
    "BRL": (60000, 350000),
    "MXN": (250000, 1200000),
    "ZAR": (200000, 1500000),
}

AGE_BANDS = ["20-29", "30-39", "40-49", "50-59", "60+"]
MANAGERS = [
    "Alex Thompson",
    "Maria Garcia",
    "James Wilson",
    "Priya Sharma",
    "Emily Chen",
    "Robert Kim",
    "Sarah Johnson",
    "Michael Brown",
]


def load_names() -> tuple[list[str], list[str]]:
    scripts_dir = Path(__file__).parent
    first = (scripts_dir / "first_names.txt").read_text().strip().splitlines()
    last = (scripts_dir / "last_names.txt").read_text().strip().splitlines()
    if not first or not last:
        raise FileNotFoundError("Run scripts/generate_names.py first")
    return first, last


def random_phone(region: str) -> str:
    """Generate a valid E.164 phone number for the given ISO region."""
    example = phonenumbers.example_number_for_type(region, PhoneNumberType.MOBILE)
    if example is None:
        example = phonenumbers.example_number_for_type(region, PhoneNumberType.FIXED_LINE)
    if example is None:
        raise ValueError(f"No example phone number for region {region}")
    # Vary the national number slightly while keeping validity
    for _ in range(20):
        candidate = phonenumbers.parse(
            f"+{example.country_code}{example.national_number + random.randint(0, 9999)}",
            None,
        )
        if phonenumbers.is_valid_number(candidate):
            return phonenumbers.format_number(candidate, phonenumbers.PhoneNumberFormat.E164)
    return phonenumbers.format_number(example, phonenumbers.PhoneNumberFormat.E164)


def random_join_date() -> date:
    start = date(2015, 1, 1)
    end = date(2025, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def generate_row(index: int, first_names: list[str], last_names: list[str]) -> dict:
    country, currency, region = random.choice(COUNTRIES)
    department = random.choice(DEPARTMENTS)
    job_title = random.choice(JOB_TITLES[department])
    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"
    employee_id = f"EMP{index:06d}"
    email = f"{first.lower()}.{last.lower()}{index}@paybuddy.internal"
    phone = random_phone(region)
    lo, hi = SALARY_RANGES[currency]
    salary = Decimal(str(random.randint(lo, hi)))
    bonus = Decimal(str(int(float(salary) * random.uniform(0, 0.15)))) if random.random() > 0.3 else None
    gender = random.choice(list(Gender))
    status = EmployeeStatus.ACTIVE if random.random() > 0.08 else EmployeeStatus.INACTIVE
    employment_type = random.choices(
        list(EmploymentType),
        weights=[70, 10, 15, 5],
    )[0]

    return {
        "employee_id": employee_id,
        "full_name": full_name,
        "email": email,
        "phone_number": phone,
        "job_title": job_title,
        "department": department,
        "country": country,
        "salary": salary,
        "currency": currency,
        "date_of_joining": random_join_date(),
        "employment_type": employment_type.value,
        "manager_name": random.choice(MANAGERS),
        "status": status.value,
        "gender": gender.value,
        "city": random.choice(CITIES.get(country, ["Unknown"])),
        "bonus": bonus,
        "last_appraisal_rating": Decimal(str(round(random.uniform(2.5, 5.0), 1))),
        "age_band": random.choice(AGE_BANDS),
        "experience_years": random.randint(0, 25),
    }


def bulk_insert_batch(session: Session, batch: list[dict]) -> None:
    """Insert via table core API so PG enums get string values, not Python enum names."""
    session.execute(insert(Employee.__table__), batch)


def seed(count: int, reset: bool, batch_size: int) -> None:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://paybuddy:paybuddy@localhost:5432/paybuddy",
    )
    first_names, last_names = load_names()

    engine = create_engine(database_url, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)

    start = time.perf_counter()
    with Session() as session:
        if reset:
            session.execute(text("TRUNCATE TABLE employees RESTART IDENTITY CASCADE"))
            session.commit()
            print("Truncated employees table")

        batch: list[dict] = []
        for i in range(1, count + 1):
            batch.append(generate_row(i, first_names, last_names))
            if len(batch) >= batch_size:
                bulk_insert_batch(session, batch)
                session.commit()
                print(f"Inserted {i}/{count}")
                batch.clear()

        if batch:
            bulk_insert_batch(session, batch)
            session.commit()
            print(f"Inserted {count}/{count}")

    elapsed = time.perf_counter() - start
    print(f"Seeded {count} employees in {elapsed:.2f}s ({count / elapsed:.0f} rows/sec)")


def main():
    parser = argparse.ArgumentParser(description="Seed PayBuddy employee data")
    parser.add_argument("--count", type=int, default=10000)
    parser.add_argument("--reset", action="store_true", help="Truncate table before seeding")
    parser.add_argument("--batch-size", type=int, default=1000)
    args = parser.parse_args()
    seed(args.count, args.reset, args.batch_size)


if __name__ == "__main__":
    main()
