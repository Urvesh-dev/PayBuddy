import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    Index,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EmploymentType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


def _enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    return [member.value for member in enum_cls]


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False)
    job_title: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    department: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    salary: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    date_of_joining: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(
            EmploymentType,
            name="employment_type_enum",
            native_enum=False,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
    manager_name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(
            EmployeeStatus,
            name="employee_status_enum",
            native_enum=False,
            values_callable=_enum_values,
        ),
        nullable=False,
        default=EmployeeStatus.ACTIVE,
        index=True,
    )
    gender: Mapped[Gender | None] = mapped_column(
        Enum(
            Gender,
            name="gender_enum",
            native_enum=False,
            values_callable=_enum_values,
        ),
        nullable=True,
    )
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    bonus: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    last_appraisal_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    age_band: Mapped[str | None] = mapped_column(String(20), nullable=True)
    experience_years: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_employees_country_department", "country", "department"),
        Index("ix_employees_country_job_title", "country", "job_title"),
        Index("ix_employees_salary", "salary"),
        Index("ix_employees_status_country", "status", "country"),
    )
