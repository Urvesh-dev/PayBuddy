from fastapi import APIRouter, Depends, Query

from app.api.deps import get_insights_service
from app.schemas.insights import (
    CountrySalaryStats,
    DashboardInsights,
    JobTitleSalaryStats,
)
from app.services.insights_service import InsightsService

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/salary/country", response_model=list[CountrySalaryStats])
def salary_by_country(
    country: str | None = None,
    service: InsightsService = Depends(get_insights_service),
):
    return service.country_salary_stats(country)


@router.get("/salary/job-title", response_model=list[JobTitleSalaryStats])
def salary_by_job_title(
    country: str | None = None,
    job_title: str | None = None,
    service: InsightsService = Depends(get_insights_service),
):
    return service.job_title_salary_stats(country, job_title)


@router.get("/dashboard", response_model=DashboardInsights)
def dashboard_insights(
    country: str | None = None,
    service: InsightsService = Depends(get_insights_service),
):
    return service.dashboard(country)
