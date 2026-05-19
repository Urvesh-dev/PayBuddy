.PHONY: up down seed test test-backend migrate

up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	cd backend && alembic upgrade head

seed:
	DATABASE_URL=postgresql://paybuddy:paybuddy@localhost:5432/paybuddy \
		PYENV_VERSION=3.12.1 python scripts/seed_employees.py --count 10000 --reset

test-backend:
	cd backend && PYENV_VERSION=3.12.1 python -m pytest -v --cov=app

test-frontend:
	cd frontend && npm test

test: test-backend test-frontend
