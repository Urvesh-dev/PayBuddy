from decimal import Decimal

from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee, EmployeeStatus
from app.schemas.employee import EmployeeCreate, EmployeeFilterParams, EmployeeUpdate

def _enum_to_str(value) -> str:
    if value is None:
        return "unknown"
    return value.value if hasattr(value, "value") else str(value)


SORTABLE_COLUMNS = {
    "employee_id",
    "full_name",
    "email",
    "job_title",
    "department",
    "country",
    "salary",
    "date_of_joining",
    "status",
    "created_at",
}


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def _apply_filters(self, query, filters: EmployeeFilterParams):
        if filters.search:
            term = f"%{filters.search.lower()}%"
            query = query.where(
                or_(
                    func.lower(Employee.full_name).like(term),
                    func.lower(Employee.email).like(term),
                    func.lower(Employee.employee_id).like(term),
                    func.lower(Employee.job_title).like(term),
                    func.lower(Employee.department).like(term),
                )
            )
        if filters.country:
            query = query.where(Employee.country == filters.country)
        if filters.department:
            query = query.where(Employee.department == filters.department)
        if filters.job_title:
            query = query.where(Employee.job_title == filters.job_title)
        if filters.status:
            query = query.where(Employee.status == filters.status)
        if filters.employment_type:
            query = query.where(Employee.employment_type == filters.employment_type)
        if filters.salary_min is not None:
            query = query.where(Employee.salary >= filters.salary_min)
        if filters.salary_max is not None:
            query = query.where(Employee.salary <= filters.salary_max)
        return query

    def list_employees(self, filters: EmployeeFilterParams) -> tuple[list[Employee], int]:
        base = select(Employee)
        base = self._apply_filters(base, filters)

        count_query = select(func.count()).select_from(base.subquery())
        total = self.db.scalar(count_query) or 0

        sort_col = getattr(Employee, filters.sort_by, Employee.created_at)
        if filters.sort_by not in SORTABLE_COLUMNS:
            sort_col = Employee.created_at
        order_fn = asc if filters.sort_order == "asc" else desc

        offset = (filters.page - 1) * filters.page_size
        rows = (
            self.db.execute(
                base.order_by(order_fn(sort_col))
                .offset(offset)
                .limit(filters.page_size)
            )
            .scalars()
            .all()
        )
        return list(rows), total

    def get_by_id(self, employee_pk: int) -> Employee | None:
        return self.db.get(Employee, employee_pk)

    def get_by_employee_id(self, employee_id: str) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.employee_id == employee_id))

    def get_by_email(self, email: str) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.email == email))

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.model_dump())
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update(self, employee: Employee, data: EmployeeUpdate) -> Employee:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self.db.delete(employee)
        self.db.commit()

    def distinct_values(self, column: str) -> list[str]:
        col = getattr(Employee, column)
        result = self.db.execute(
            select(col).distinct().where(col.isnot(None)).order_by(col)
        )
        return [row[0] for row in result.all()]

    def country_salary_stats(self, country: str | None = None) -> list[dict]:
        q = select(
            Employee.country,
            func.min(Employee.salary).label("min_salary"),
            func.max(Employee.salary).label("max_salary"),
            func.avg(Employee.salary).label("avg_salary"),
            func.count(Employee.id).label("employee_count"),
            func.max(Employee.currency).label("currency"),
        ).group_by(Employee.country)
        if country:
            q = q.where(Employee.country == country)
        rows = self.db.execute(q).all()
        return [
            {
                "country": r.country,
                "min_salary": r.min_salary,
                "max_salary": r.max_salary,
                "avg_salary": r.avg_salary,
                "employee_count": r.employee_count,
                "currency": r.currency,
            }
            for r in rows
        ]

    def job_title_salary_stats(
        self, country: str | None = None, job_title: str | None = None
    ) -> list[dict]:
        q = select(
            Employee.country,
            Employee.job_title,
            func.avg(Employee.salary).label("avg_salary"),
            func.count(Employee.id).label("employee_count"),
            func.min(Employee.salary).label("min_salary"),
            func.max(Employee.salary).label("max_salary"),
        ).group_by(Employee.country, Employee.job_title)
        if country:
            q = q.where(Employee.country == country)
        if job_title:
            q = q.where(Employee.job_title == job_title)
        rows = self.db.execute(q).all()
        return [
            {
                "country": r.country,
                "job_title": r.job_title,
                "avg_salary": r.avg_salary,
                "employee_count": r.employee_count,
                "min_salary": r.min_salary,
                "max_salary": r.max_salary,
            }
            for r in rows
        ]

    def department_payroll(self, country: str | None = None) -> list[dict]:
        q = select(
            Employee.department,
            func.sum(Employee.salary + func.coalesce(Employee.bonus, 0)).label("total_payroll"),
            func.avg(Employee.salary).label("avg_salary"),
            func.count(Employee.id).label("employee_count"),
        ).group_by(Employee.department)
        if country:
            q = q.where(Employee.country == country)
        rows = self.db.execute(q).all()
        result = [
            {
                "department": r.department,
                "total_payroll": r.total_payroll,
                "avg_salary": r.avg_salary,
                "employee_count": r.employee_count,
            }
            for r in rows
        ]
        return sorted(result, key=lambda x: x["total_payroll"], reverse=True)

    def top_paid(self, limit: int = 10, country: str | None = None) -> list[Employee]:
        q = select(Employee).order_by(desc(Employee.salary)).limit(limit)
        if country:
            q = q.where(Employee.country == country)
        return list(self.db.scalars(q).all())

    def median_salary(self, country: str | None = None) -> Decimal | None:
        dialect = self.db.get_bind().dialect.name
        if dialect == "postgresql":
            q = select(func.percentile_cont(0.5).within_group(Employee.salary))
            if country:
                q = q.where(Employee.country == country)
            return self.db.scalar(q)

        q = select(Employee.salary).order_by(Employee.salary)
        if country:
            q = q.where(Employee.country == country)
        salaries = [row[0] for row in self.db.execute(q).all()]
        if not salaries:
            return None
        n = len(salaries)
        mid = n // 2
        if n % 2 == 0:
            return (salaries[mid - 1] + salaries[mid]) / 2
        return salaries[mid]

    def salary_percentiles(self, country: str | None = None) -> list[dict]:
        percentiles = [10, 25, 50, 75, 90]
        dialect = self.db.get_bind().dialect.name
        if dialect == "postgresql":
            result = []
            for p in percentiles:
                q = select(func.percentile_cont(p / 100).within_group(Employee.salary))
                if country:
                    q = q.where(Employee.country == country)
                value = self.db.scalar(q)
                if value is not None:
                    result.append({"percentile": p, "salary": value})
            return result

        q = select(Employee.salary).order_by(Employee.salary)
        if country:
            q = q.where(Employee.country == country)
        salaries = [row[0] for row in self.db.execute(q).all()]
        if not salaries:
            return []
        n = len(salaries)
        return [
            {
                "percentile": p,
                "salary": salaries[min(int((p / 100) * n), n - 1)],
            }
            for p in percentiles
        ]

    def status_breakdown(self, country: str | None = None) -> list[dict]:
        q = select(Employee.status, func.count(Employee.id)).group_by(Employee.status)
        if country:
            q = q.where(Employee.country == country)
        rows = self.db.execute(q).all()
        return [{"status": _enum_to_str(r[0]), "count": r[1]} for r in rows]

    def hiring_trend(self, country: str | None = None) -> list[dict]:
        year_col = func.extract("year", Employee.date_of_joining).label("year")
        month_col = func.extract("month", Employee.date_of_joining).label("month")
        q = (
            select(year_col, month_col, func.count(Employee.id).label("count"))
            .group_by(year_col, month_col)
            .order_by(year_col, month_col)
        )
        if country:
            q = q.where(Employee.country == country)
        rows = self.db.execute(q).all()
        return [
            {"year": int(r.year), "month": int(r.month), "count": r.count}
            for r in rows
        ]

    def gender_pay_gap(self, country: str | None = None) -> list[dict]:
        q = (
            select(
                Employee.gender,
                func.avg(Employee.salary).label("avg_salary"),
                func.count(Employee.id).label("employee_count"),
            )
            .where(Employee.gender.isnot(None))
            .group_by(Employee.gender)
        )
        if country:
            q = q.where(Employee.country == country)
        rows = self.db.execute(q).all()
        return [
            {
                "gender": _enum_to_str(r.gender),
                "avg_salary": r.avg_salary,
                "employee_count": r.employee_count,
            }
            for r in rows
            if r.gender is not None
        ]

    def count_all(self) -> int:
        return self.db.scalar(select(func.count(Employee.id))) or 0

    def count_by_status(self, status: EmployeeStatus, country: str | None = None) -> int:
        q = select(func.count(Employee.id)).where(Employee.status == status)
        if country:
            q = q.where(Employee.country == country)
        return self.db.scalar(q) or 0

    def country_employee_counts(self) -> dict[str, int]:
        rows = self.db.execute(
            select(Employee.country, func.count(Employee.id)).group_by(Employee.country)
        ).all()
        return {r[0]: r[1] for r in rows}
