from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.services.insights_service import InsightsService


def get_employee_repository(db: Session = Depends(get_db)) -> EmployeeRepository:
    return EmployeeRepository(db)


def get_employee_service(
    repo: EmployeeRepository = Depends(get_employee_repository),
) -> EmployeeService:
    return EmployeeService(repo)


def get_insights_service(
    repo: EmployeeRepository = Depends(get_employee_repository),
) -> InsightsService:
    return InsightsService(repo)
