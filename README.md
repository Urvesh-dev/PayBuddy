# PayBuddy — Salary Management System

Production-ready HR salary management for organizations with **10,000+ employees**. Built with FastAPI, PostgreSQL, React, and Docker.

![Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)

## Features

- **Employee CRUD** — Search, filter, paginate, sort
- **Salary Insights Dashboard** — Country/job analytics, KPIs, charts
- **Optimized seeding** — 10k employees via bulk inserts
- **Tests** — Pytest (backend) + Vitest (frontend)
- **Docker Compose** — One-command local stack

## Quick Start (Docker)

```bash
# Start PostgreSQL, API, and frontend
docker compose up --build -d

# Seed 10,000 employees (from host, with DB exposed on :5432)
pip install -r backend/requirements.txt
DATABASE_URL=postgresql://paybuddy:paybuddy@localhost:5432/paybuddy \
  python scripts/seed_employees.py --count 10000 --reset
```

| Service   | URL |
|-----------|-----|
| Frontend  | http://localhost |
| API       | http://localhost:8000 |
| Swagger   | http://localhost:8000/docs |

**Login**: any email + password (mock auth).

### Troubleshooting: `could not translate host name "db"`

| Where you run the API | `DATABASE_URL` host |
|----------------------|---------------------|
| **Inside Docker Compose** | `db` (set in `docker-compose.yml`) |
| **On your machine** (`uvicorn`, seed script) | `localhost` |

1. Start the full stack (not only backend): `docker compose up --build -d`
2. Confirm DB is up: `docker compose ps` — `paybuddy-db` should be **healthy**
3. If you copied `backend/.env` with `@db:`, change it to `@localhost:` for local runs
4. Recreate containers after compose changes: `docker compose down && docker compose up --build -d`

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ (or use Docker for DB only)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # adjust DATABASE_URL if needed

# Start Postgres (optional via Docker)
docker compose up db -d

alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173 (proxies /api to :8000)
```

### Seed Data

```bash
# Generate name files (first run)
python scripts/generate_names.py

# Seed 10k employees (~3-8s on local PG)
DATABASE_URL=postgresql://paybuddy:paybuddy@localhost:5432/paybuddy \
  python scripts/seed_employees.py --count 10000 --reset
```

**Benchmark notes**

| Rows  | Batch | Typical time |
|-------|-------|--------------|
| 10,000 | 1,000 | 3–8 seconds |
| 1,000  | 500   | <1 second |

Uses `bulk_insert_mappings` + batched commits. `--reset` truncates the table (idempotent re-seed).

## Running Tests

```bash
# Backend (SQLite in-memory by default)
cd backend && pytest --cov=app -v

# With PostgreSQL
TEST_DATABASE_URL=postgresql://paybuddy:paybuddy@localhost:5432/paybuddy_test \
  pytest --cov=app -v

# Frontend
cd frontend && npm test
```

## Project Structure

```
PayBuddy/
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── api/       # Routes
│   │   ├── models/    # SQLAlchemy
│   │   ├── schemas/   # Pydantic
│   │   ├── services/
│   │   └── repositories/
│   ├── alembic/
│   └── tests/
├── frontend/          # React + TypeScript + MUI
├── scripts/           # seed_employees.py, name lists
├── docs/ARCHITECTURE.md
└── docker-compose.yml
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/employees` | List (search, filter, paginate) |
| POST | `/api/v1/employees` | Create |
| GET | `/api/v1/employees/{id}` | Detail |
| PUT | `/api/v1/employees/{id}` | Update |
| DELETE | `/api/v1/employees/{id}` | Delete |
| GET | `/api/v1/insights/salary/country` | Min/max/avg by country |
| GET | `/api/v1/insights/salary/job-title` | Avg by job title + country |
| GET | `/api/v1/insights/dashboard` | Full dashboard payload |

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for ER diagram, layering, indexes, and tradeoffs.

## Deployment

1. Build images: `docker compose build`
2. Set env vars: `DATABASE_URL`, `CORS_ORIGINS`
3. Run migrations on deploy: `alembic upgrade head`
4. Optional: run seed in staging only

**Render/Railway**: Deploy `backend` and `frontend` services; attach managed PostgreSQL; set `DATABASE_URL`.

## CI

GitHub Actions runs backend tests (PostgreSQL service), Ruff, frontend tests, and build on push/PR to `main`.

## Screenshots & Demo

After `docker compose up` and seeding:

1. **Login** — `hr@paybuddy.com` / any password
2. **Employees** — Filter by country, search, paginate
3. **Insights** — KPI cards, country salary chart, department payroll, hiring trend

Record a short walkthrough: Employees → Add → Insights dashboard with 10k seeded rows.

## License

MIT
