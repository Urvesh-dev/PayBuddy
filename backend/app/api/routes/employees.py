from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_employee_service
from app.models.employee import EmployeeStatus, EmploymentType
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeFilterParams,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=PaginatedResponse[EmployeeResponse])
def list_employees(
    search: str | None = None,
    country: str | None = None,
    department: str | None = None,
    job_title: str | None = None,
    status: EmployeeStatus | None = None,
    employment_type: EmploymentType | None = None,
    salary_min: float | None = Query(default=None, ge=0),
    salary_max: float | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = "created_at",
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    service: EmployeeService = Depends(get_employee_service),
):
    filters = EmployeeFilterParams(
        search=search,
        country=country,
        department=department,
        job_title=job_title,
        status=status,
        employment_type=employment_type,
        salary_min=salary_min,
        salary_max=salary_max,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return service.list_employees(filters)


@router.get("/metadata/filters")
def get_filter_metadata(service: EmployeeService = Depends(get_employee_service)):
    return service.get_metadata()


@router.get("/{employee_pk}", response_model=EmployeeResponse)
def get_employee(
    employee_pk: int,
    service: EmployeeService = Depends(get_employee_service),
):
    return service.get_employee(employee_pk)


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    return service.create_employee(payload)


@router.put("/{employee_pk}", response_model=EmployeeResponse)
def update_employee(
    employee_pk: int,
    payload: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
):
    return service.update_employee(employee_pk, payload)


@router.delete("/{employee_pk}", response_model=MessageResponse)
def delete_employee(
    employee_pk: int,
    service: EmployeeService = Depends(get_employee_service),
):
    service.delete_employee(employee_pk)
    return MessageResponse(message="Employee deleted successfully")
