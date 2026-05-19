"""create employees table

Revision ID: 001
Revises:
Create Date: 2026-05-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    employment_type = sa.Enum(
        "full_time", "part_time", "contract", "intern", name="employment_type_enum"
    )
    employee_status = sa.Enum("active", "inactive", name="employee_status_enum")
    gender = sa.Enum(
        "male", "female", "other", "prefer_not_to_say", name="gender_enum"
    )

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employee_id", sa.String(length=32), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("job_title", sa.String(length=120), nullable=False),
        sa.Column("department", sa.String(length=120), nullable=False),
        sa.Column("country", sa.String(length=80), nullable=False),
        sa.Column("salary", sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("date_of_joining", sa.Date(), nullable=False),
        sa.Column("employment_type", employment_type, nullable=False),
        sa.Column("manager_name", sa.String(length=200), nullable=False),
        sa.Column("status", employee_status, nullable=False),
        sa.Column("gender", gender, nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("bonus", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("last_appraisal_rating", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("age_band", sa.String(length=20), nullable=True),
        sa.Column("experience_years", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("employee_id"),
    )
    op.create_index("ix_employees_country", "employees", ["country"])
    op.create_index("ix_employees_department", "employees", ["department"])
    op.create_index("ix_employees_email", "employees", ["email"], unique=True)
    op.create_index("ix_employees_employee_id", "employees", ["employee_id"], unique=True)
    op.create_index("ix_employees_job_title", "employees", ["job_title"])
    op.create_index("ix_employees_salary", "employees", ["salary"])
    op.create_index("ix_employees_status", "employees", ["status"])
    op.create_index("ix_employees_date_of_joining", "employees", ["date_of_joining"])
    op.create_index(
        "ix_employees_country_department", "employees", ["country", "department"]
    )
    op.create_index(
        "ix_employees_country_job_title", "employees", ["country", "job_title"]
    )
    op.create_index("ix_employees_status_country", "employees", ["status", "country"])


def downgrade() -> None:
    op.drop_index("ix_employees_status_country", table_name="employees")
    op.drop_index("ix_employees_country_job_title", table_name="employees")
    op.drop_index("ix_employees_country_department", table_name="employees")
    op.drop_index("ix_employees_date_of_joining", table_name="employees")
    op.drop_index("ix_employees_status", table_name="employees")
    op.drop_index("ix_employees_salary", table_name="employees")
    op.drop_index("ix_employees_job_title", table_name="employees")
    op.drop_index("ix_employees_employee_id", table_name="employees")
    op.drop_index("ix_employees_email", table_name="employees")
    op.drop_index("ix_employees_department", table_name="employees")
    op.drop_index("ix_employees_country", table_name="employees")
    op.drop_table("employees")
    op.execute("DROP TYPE IF EXISTS employment_type_enum")
    op.execute("DROP TYPE IF EXISTS employee_status_enum")
    op.execute("DROP TYPE IF EXISTS gender_enum")
