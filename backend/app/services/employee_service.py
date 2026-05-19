import math

from fastapi import HTTPException, status

from app.repositories.employee_repository import EmployeeRepository
from app.schemas.common import PaginatedResponse
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeFilterParams,
    EmployeeResponse,
    EmployeeUpdate,
)


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def list_employees(
        self, filters: EmployeeFilterParams
    ) -> PaginatedResponse[EmployeeResponse]:
        rows, total = self.repo.list_employees(filters)
        total_pages = math.ceil(total / filters.page_size) if total else 0
        return PaginatedResponse(
            items=[EmployeeResponse.model_validate(r) for r in rows],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages,
        )

    def get_employee(self, employee_pk: int) -> EmployeeResponse:
        employee = self.repo.get_by_id(employee_pk)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return EmployeeResponse.model_validate(employee)

    def create_employee(self, data: EmployeeCreate) -> EmployeeResponse:
        if self.repo.get_by_employee_id(data.employee_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee ID already exists",
            )
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )
        employee = self.repo.create(data)
        return EmployeeResponse.model_validate(employee)

    def update_employee(self, employee_pk: int, data: EmployeeUpdate) -> EmployeeResponse:
        employee = self.repo.get_by_id(employee_pk)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

        if data.employee_id and data.employee_id != employee.employee_id:
            existing = self.repo.get_by_employee_id(data.employee_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Employee ID already exists",
                )
        if data.email and data.email != employee.email:
            existing = self.repo.get_by_email(str(data.email))
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )

        updated = self.repo.update(employee, data)
        return EmployeeResponse.model_validate(updated)

    def delete_employee(self, employee_pk: int) -> None:
        employee = self.repo.get_by_id(employee_pk)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        self.repo.delete(employee)

    def get_metadata(self) -> dict:
        return {
            "countries": self.repo.distinct_values("country"),
            "departments": self.repo.distinct_values("department"),
            "job_titles": self.repo.distinct_values("job_title"),
        }
