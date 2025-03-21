build:
	CHECK_DB=true docker compose -f local.yml up --build -d --remove-orphans

build-no-cache:
	CHECK_DB=true docker compose -f local.yml build --no-cache

up:
	CHECK_DB=true docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

down-v:
	docker compose -f local.yml down -v

show-logs:
	docker compose -f local.yml logs

show-logs-backend:
	docker compose -f local.yml logs backend

makemigrations:
	docker compose -f local.yml run --rm backend python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm backend python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm backend python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm backend python manage.py createsuperuser

volume:
	docker volume inspect src_local_postgres_data

dealsmo-db:
	docker compose -f local.yml exec postgres psql --username=balda --dbname=dealsmoDB

flake8:
	docker compose -f local.yml exec backend flake8 .

black-check:
	docker compose -f local.yml exec backend black --check --exclude=migrations .

black-diff:
	docker compose -f local.yml exec backend black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec backend black --exclude=migrations .

isort-check:
	docker compose -f local.yml exec backend isort . --check-only --skip venv --skip migrations

isort-diff:
	docker compose -f local.yml exec backend isort . --diff --skip venv --skip migrations

isort:
	docker compose -f local.yml exec backend isort . --skip venv --skip migrations

es-create:
	docker compose -f local.yml exec backend python manage.py search_index --create	
es-populate:
	docker compose -f local.yml exec backend python manage.py search_index --populate	
es-sync:
	docker compose -f local.yml exec backend python manage.py search_index --rebuild	

db-backup:
	docker compose -f local.yml exec postgres backup
db-backup-view:
	docker compose -f local.yml exec postgres backups
db-restore:
	docker compose -f local.yml exec postgres restore <backup-file-name-from-docker-postgres-backups-dir> 

pytest:
	docker compose -f local.yml run --rm backend pytest -p no:warnings --cov=backend --cov=.-v

pytest-report:
	docker compose -f local.yml run --rm backend pytest -p no:warnings --cov=core_apps --cov-report=html


deploy:
	docker compose -f local.yml exec backend python manage.py check --deploy
