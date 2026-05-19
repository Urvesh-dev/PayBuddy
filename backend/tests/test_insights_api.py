def test_country_salary_stats(client, sample_employee):
    response = client.get("/api/v1/insights/salary/country")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    us = next((c for c in data if c["country"] == "United States"), None)
    assert us is not None
    assert float(us["avg_salary"]) > 0


def test_job_title_salary_stats(client, sample_employee):
    response = client.get(
        "/api/v1/insights/salary/job-title?country=United%20States&job_title=Software%20Engineer"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_dashboard_insights(client, sample_employee):
    response = client.get("/api/v1/insights/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_employees"] >= 1
    assert "country_stats" in data
    assert "top_paid_employees" in data
    assert data["median_salary"] is not None
