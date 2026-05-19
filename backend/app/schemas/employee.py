import re
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

import phonenumbers
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.employee import EmployeeStatus, EmploymentType, Gender

VALID_COUNTRIES = {
    "United States",
    "United Kingdom",
    "Canada",
    "Germany",
    "France",
    "India",
    "Australia",
    "Singapore",
    "Japan",
    "Brazil",
    "Netherlands",
    "Spain",
    "Italy",
    "Mexico",
    "South Africa",
}


def validate_country_value(v: str) -> str:
    if v not in VALID_COUNTRIES:
        raise ValueError(f"Country must be one of: {', '.join(sorted(VALID_COUNTRIES))}")
    return v


_E164_PATTERN = re.compile(r"^\+[1-9]\d{6,14}$")


def validate_phone_value(v: str, *, strict: bool = True) -> str:
    v = v.strip()
    try:
        parsed = phonenumbers.parse(v, None)
    except phonenumbers.NumberParseException as exc:
        raise ValueError("Invalid phone number format") from exc

    is_ok = (
        phonenumbers.is_valid_number(parsed)
        if strict
        else phonenumbers.is_possible_number(parsed)
    )
    if is_ok:
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    # Allow legacy seeded values on update (E.164 shape but not libphonenumber-valid)
    if not strict and _E164_PATTERN.match(v):
        return v

    raise ValueError("Invalid phone number")


class EmployeeBase(BaseModel):
    """Shared fields — no input validators (avoids re-validating seeded DB rows on read)."""

    employee_id: Annotated[str, Field(min_length=1, max_length=32)]
    full_name: Annotated[str, Field(min_length=1, max_length=200)]
    email: EmailStr
    phone_number: Annotated[str, Field(min_length=7, max_length=32)]
    job_title: Annotated[str, Field(min_length=1, max_length=120)]
    department: Annotated[str, Field(min_length=1, max_length=120)]
    country: Annotated[str, Field(min_length=2, max_length=80)]
    salary: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    currency: Annotated[str, Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")]
    date_of_joining: date
    employment_type: EmploymentType
    manager_name: Annotated[str, Field(min_length=1, max_length=200)]
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    gender: Gender | None = None
    city: str | None = Field(default=None, max_length=120)
    bonus: Annotated[Decimal | None, Field(ge=0, decimal_places=2)] = None
    last_appraisal_rating: Annotated[Decimal | None, Field(ge=0, le=5)] = None
    age_band: str | None = Field(default=None, max_length=20)
    experience_years: Annotated[int | None, Field(ge=0, le=60)] = None


class EmployeeCreate(EmployeeBase):
    @field_validator("country")
    @classmethod
    def validate_country(cls, v: str) -> str:
        return validate_country_value(v)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        return validate_phone_value(v)


class EmployeeUpdate(BaseModel):
    employee_id: str | None = Field(default=None, min_length=1, max_length=32)
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=7, max_length=32)
    job_title: str | None = Field(default=None, min_length=1, max_length=120)
    department: str | None = Field(default=None, min_length=1, max_length=120)
    country: str | None = Field(default=None, min_length=2, max_length=80)
    salary: Annotated[Decimal | None, Field(gt=0, decimal_places=2)] = None
    currency: str | None = Field(default=None, min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")
    date_of_joining: date | None = None
    employment_type: EmploymentType | None = None
    manager_name: str | None = Field(default=None, min_length=1, max_length=200)
    status: EmployeeStatus | None = None
    gender: Gender | None = None
    city: str | None = None
    bonus: Annotated[Decimal | None, Field(ge=0, decimal_places=2)] = None
    last_appraisal_rating: Annotated[Decimal | None, Field(ge=0, le=5)] = None
    age_band: str | None = None
    experience_years: Annotated[int | None, Field(ge=0, le=60)] = None

    @field_validator("country")
    @classmethod
    def validate_country(cls, v: str | None) -> str | None:
        if v is not None:
            return validate_country_value(v)
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is not None:
            # Lenient on update so legacy seeded rows remain editable
            return validate_phone_value(v, strict=False)
        return v


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class EmployeeFilterParams(BaseModel):
    search: str | None = None
    country: str | None = None
    department: str | None = None
    job_title: str | None = None
    status: EmployeeStatus | None = None
    employment_type: EmploymentType | None = None
    salary_min: Decimal | None = Field(default=None, ge=0)
    salary_max: Decimal | None = Field(default=None, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: str = "created_at"
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
