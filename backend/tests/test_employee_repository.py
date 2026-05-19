from decimal import Decimal

from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeFilterParams, EmployeeUpdate


def test_repository_crud(db_session, sample_employee):
    repo = EmployeeRepository(db_session)

    found = repo.get_by_id(sample_employee.id)
    assert found is not None
    assert found.full_name == "Jane Doe"

    updated = repo.update(
        found,
        EmployeeUpdate(salary=Decimal("105000")),
    )
    assert updated.salary == Decimal("105000")

    rows, total = repo.list_employees(EmployeeFilterParams(search="jane", page=1, page_size=5))
    assert total >= 1
    assert any(e.id == sample_employee.id for e in rows)


def test_repository_create(db_session):
    repo = EmployeeRepository(db_session)
    data = EmployeeCreate(
        employee_id="EMP200",
        full_name="Repo Test",
        email="repo.test@example.com",
        phone_number="+14155552675",
        job_title="Data Analyst",
        department="Analytics",
        country="India",
        salary=Decimal("75000"),
        currency="INR",
        date_of_joining="2020-05-20",
        employment_type="full_time",
        manager_name="Analytics Lead",
        status="active",
    )
    created = repo.create(data)
    assert created.id is not None
    assert created.country == "India"
