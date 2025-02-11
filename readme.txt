pip install -r requirements/local.txt

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

docker-compose -f local.yml run --rm api env

# error mailhog The requested image's platform (linux/amd64) does not match the detected host platform
# solution run in terminal (backend): export DOCKER_DEFAULT_PLATFORM=linux/amd64

docker-compose -f local.yml build --no-cache
docker-compose -f local.yml up

docker compose -f local.yml up --build -d --remove-orphans
docker compose -f local.yml logs api