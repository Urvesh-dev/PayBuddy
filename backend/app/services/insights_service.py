from decimal import Decimal

from app.repositories.employee_repository import EmployeeRepository
from app.schemas.insights import (
    CountrySalaryStats,
    DashboardInsights,
    DepartmentPayroll,
    GenderPayGap,
    HiringTrendPoint,
    JobTitleSalaryStats,
    SalaryPercentile,
    StatusCount,
    TopEmployee,
)


class InsightsService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def country_salary_stats(self, country: str | None = None) -> list[CountrySalaryStats]:
        rows = self.repo.country_salary_stats(country)
        return [CountrySalaryStats(**r) for r in rows]

    def job_title_salary_stats(
        self, country: str | None = None, job_title: str | None = None
    ) -> list[JobTitleSalaryStats]:
        rows = self.repo.job_title_salary_stats(country, job_title)
        return [JobTitleSalaryStats(**r) for r in rows]

    def dashboard(self, country: str | None = None) -> DashboardInsights:
        from app.models.employee import EmployeeStatus

        country_stats = self.country_salary_stats(country)
        department_payroll = [
            DepartmentPayroll(**r) for r in self.repo.department_payroll(country)
        ]
        top_paid = [
            TopEmployee(
                employee_id=e.employee_id,
                full_name=e.full_name,
                job_title=e.job_title,
                department=e.department,
                country=e.country,
                salary=e.salary,
                currency=e.currency,
            )
            for e in self.repo.top_paid(limit=10, country=country)
        ]
        counts = self.repo.country_employee_counts()
        if country:
            counts = {country: counts.get(country, 0)}

        total = self.repo.count_all() if not country else counts.get(country, 0)

        return DashboardInsights(
            total_employees=total,
            active_employees=self.repo.count_by_status(EmployeeStatus.ACTIVE, country),
            inactive_employees=self.repo.count_by_status(EmployeeStatus.INACTIVE, country),
            median_salary=self.repo.median_salary(country),
            country_stats=country_stats,
            department_payroll=department_payroll,
            top_paid_employees=top_paid,
            country_employee_counts=counts,
            salary_percentiles=[
                SalaryPercentile(**p) for p in self.repo.salary_percentiles(country)
            ],
            status_breakdown=[StatusCount(**s) for s in self.repo.status_breakdown(country)],
            hiring_trend=[HiringTrendPoint(**h) for h in self.repo.hiring_trend(country)],
            gender_pay_gap=[GenderPayGap(**g) for g in self.repo.gender_pay_gap(country)],
        )
