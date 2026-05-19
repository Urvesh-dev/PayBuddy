import os
from collections.abc import Generator
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.employee import Employee, EmployeeStatus, EmploymentType, Gender

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://paybuddy:paybuddy@localhost:5432/paybuddy_test",
)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:",
)


@pytest.fixture(scope="session")
def engine():
    if TEST_DATABASE_URL.startswith("sqlite"):
        eng = create_engine(
            TEST_DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        eng = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture
def db_session(engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    TestingSession = sessionmaker(bind=connection)
    session = TestingSession()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_employee(db_session: Session) -> Employee:
    employee = Employee(
        employee_id="EMP001",
        full_name="Jane Doe",
        email="jane.doe@example.com",
        phone_number="+14155552671",
        job_title="Software Engineer",
        department="Engineering",
        country="United States",
        salary=95000,
        currency="USD",
        date_of_joining=date(2022, 3, 15),
        employment_type=EmploymentType.FULL_TIME,
        manager_name="John Manager",
        status=EmployeeStatus.ACTIVE,
        gender=Gender.FEMALE,
        city="San Francisco",
        bonus=5000,
        last_appraisal_rating=4.5,
        age_band="30-39",
        experience_years=8,
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    return employee
