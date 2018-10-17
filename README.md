# Basic setup
## Dependencies

Debian specific:
```
aptitude install python3 python3-setuptools
easy_install3 pip
```

Python specific:
```
# Install Django and its extensions
pip install django djangorestframework django-rest-swagger
# Install Postgres module
pip install psycopg2-binary
```

## Install

Checks dependencies and settings
```
python3 manage.py check --deploy
```

Runs DB setup
```
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
```
> superuser: login=root password=acme_admin

## Start server
```
python3 manage.py runserver 0.0.0.0:8080
```

# Deployment
```
python3 manage.py migrate
python3 manage.py makemigrations
```

# Working with Nginx
```
aptitude install nginx python3-dev
aptitude install libpcre3 libpcre3-dev
pip install uwsgi -I --no-cache-dir
```

```
uwsgi --home /application --chdir /application -w backend_app.wsgi
```
