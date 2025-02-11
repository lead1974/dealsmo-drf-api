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

