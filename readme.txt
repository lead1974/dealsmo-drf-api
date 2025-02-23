# create virtual environment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements/local.txt   

git reset --hard origin/main  
docker system prune -a

# migrations from scratch
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
docker compose -f local.yml run --rm backend python manage.py migrate --fake-initial
docker compose -f local.yml run --rm backend python manage.py flush
docker compose -f local.yml run --rm backend python manage.py showmigrations


pip install -r requirements/local.txt

# error mailhog The requested image's platform (linux/amd64) does not match the detected host platform
# solution run in terminal (backend): export DOCKER_DEFAULT_PLATFORM=linux/amd64
django-admin startproject base .

# generate secret key
python -c "import secrets; print(secrets.token_hex(38))"

# create new apps
python manage.py startapp users

# add apps to INSTALLED_APPS
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# run server
python manage.py runserver

# create superuser
python manage.py createsuperuser

docker-compose -f local.yml run --rm backend env

# Before building, ensure no conflicting containers are running
docker-compose -f local.yml down

# Build and run services
docker-compose -f local.yml build --no-cache
docker-compose -f local.yml up --build -d --remove-orphans

# Check logs
docker-compose -f local.yml logs backend