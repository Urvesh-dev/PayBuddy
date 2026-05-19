def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_employee(client):
    payload = {
        "employee_id": "EMP100",
        "full_name": "Alice Smith",
        "email": "alice.smith@example.com",
        "phone_number": "+14155552672",
        "job_title": "Product Manager",
        "department": "Product",
        "country": "United States",
        "salary": 120000,
        "currency": "USD",
        "date_of_joining": "2023-01-10",
        "employment_type": "full_time",
        "manager_name": "Bob Lead",
        "status": "active",
    }
    response = client.post("/api/v1/employees", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["employee_id"] == "EMP100"
    assert data["email"] == "alice.smith@example.com"


def test_create_employee_duplicate_email(client, sample_employee):
    payload = {
        "employee_id": "EMP999",
        "full_name": "Duplicate Email",
        "email": sample_employee.email,
        "phone_number": "+14155552673",
        "job_title": "Analyst",
        "department": "Finance",
        "country": "Canada",
        "salary": 80000,
        "currency": "CAD",
        "date_of_joining": "2021-06-01",
        "employment_type": "full_time",
        "manager_name": "Manager",
        "status": "active",
    }
    response = client.post("/api/v1/employees", json=payload)
    assert response.status_code == 409


def test_create_employee_invalid_salary(client):
    payload = {
        "employee_id": "EMP101",
        "full_name": "Bad Salary",
        "email": "bad.salary@example.com",
        "phone_number": "+14155552674",
        "job_title": "Intern",
        "department": "HR",
        "country": "Germany",
        "salary": -100,
        "currency": "EUR",
        "date_of_joining": "2024-02-01",
        "employment_type": "intern",
        "manager_name": "HR Lead",
        "status": "active",
    }
    response = client.post("/api/v1/employees", json=payload)
    assert response.status_code == 422


def test_list_employees_pagination(client, sample_employee):
    response = client.get("/api/v1/employees?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_employee(client, sample_employee):
    response = client.get(f"/api/v1/employees/{sample_employee.id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Jane Doe"


def test_get_employee_not_found(client):
    response = client.get("/api/v1/employees/99999")
    assert response.status_code == 404


def test_update_employee(client, sample_employee):
    response = client.put(
        f"/api/v1/employees/{sample_employee.id}",
        json={"salary": 100000, "job_title": "Senior Software Engineer"},
    )
    assert response.status_code == 200
    assert float(response.json()["salary"]) == 100000


def test_update_employee_legacy_phone(client, sample_employee):
    """Full-form update with E.164-shaped legacy phone (not libphonenumber-valid)."""
    response = client.put(
        f"/api/v1/employees/{sample_employee.id}",
        json={
            "employee_id": sample_employee.employee_id,
            "full_name": sample_employee.full_name,
            "email": sample_employee.email,
            "phone_number": "+658839374623",
            "job_title": "Updated Title",
            "department": sample_employee.department,
            "country": sample_employee.country,
            "salary": 99000,
            "currency": sample_employee.currency,
            "date_of_joining": str(sample_employee.date_of_joining),
            "employment_type": "full_time",
            "manager_name": sample_employee.manager_name,
            "status": "active",
        },
    )
    assert response.status_code == 200
    assert response.json()["job_title"] == "Updated Title"


def test_delete_employee(client, sample_employee):
    response = client.delete(f"/api/v1/employees/{sample_employee.id}")
    assert response.status_code == 200
    assert client.get(f"/api/v1/employees/{sample_employee.id}").status_code == 404


def test_search_employees(client, sample_employee):
    response = client.get("/api/v1/employees?search=jane")
    assert response.status_code == 200
    assert response.json()["total"] >= 1
