from decimal import Decimal

from pydantic import BaseModel, Field


class CountrySalaryStats(BaseModel):
    country: str
    min_salary: Decimal
    max_salary: Decimal
    avg_salary: Decimal
    employee_count: int
    currency: str | None = None


class JobTitleSalaryStats(BaseModel):
    country: str
    job_title: str
    avg_salary: Decimal
    employee_count: int
    min_salary: Decimal
    max_salary: Decimal


class DepartmentPayroll(BaseModel):
    department: str
    total_payroll: Decimal
    avg_salary: Decimal
    employee_count: int


class SalaryPercentile(BaseModel):
    percentile: int
    salary: Decimal


class TopEmployee(BaseModel):
    employee_id: str
    full_name: str
    job_title: str
    department: str
    country: str
    salary: Decimal
    currency: str


class StatusCount(BaseModel):
    status: str
    count: int


class HiringTrendPoint(BaseModel):
    year: int
    month: int
    count: int


class GenderPayGap(BaseModel):
    gender: str
    avg_salary: Decimal
    employee_count: int


class DashboardInsights(BaseModel):
    total_employees: int
    active_employees: int
    inactive_employees: int
    median_salary: Decimal | None
    country_stats: list[CountrySalaryStats]
    department_payroll: list[DepartmentPayroll]
    top_paid_employees: list[TopEmployee]
    country_employee_counts: dict[str, int]
    salary_percentiles: list[SalaryPercentile]
    status_breakdown: list[StatusCount]
    hiring_trend: list[HiringTrendPoint]
    gender_pay_gap: list[GenderPayGap] = Field(default_factory=list)


class InsightsFilterParams(BaseModel):
    country: str | None = None
    department: str | None = None
    job_title: str | None = None
