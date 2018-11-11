# Basic setup
## Dependencies

Debian specific:
```bash
aptitude install python3 python3-setuptools
easy_install3 pip
```

Python specific:
```bash
# Install Django and its extensions
pip install django djangorestframework django-rest-auth
# Install Postgres module
pip install psycopg2-binary
```

## Install

Create DB user
```sql
# su - postgres
# psql

> GRANT ALL PRIVILEGES ON DATABASE acme_db TO acme_db;
> CREATE USER acme_db WITH ENCRYPTED PASSWORD 'hahaha';
```

Checks dependencies and settings
```bash
python3 manage.py check --deploy
```

Runs DB setup
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
```
> superuser: login=root password=acme_admin

## Start server
```bash
python3 manage.py runserver 0.0.0.0:8080
```

# Deployment
> Developers should run `makemigrations` before push, if they have changed any models
```bash
python3 manage.py migrate
```
or
```bash
./deployment.sh
```

# Working with Nginx
```bash
aptitude install nginx python3-dev
aptitude install libpcre3 libpcre3-dev
pip install uwsgi -I --no-cache-dir

mkdir /run/uwsgi
chmod 777 -R /run/uwsgi

uwsgi --ini config/uwsgi/backend.ini
```

## Setup Emperor
```bash
mkdir /etc/uwsgi
mkdir /etc/uwsgi/vassals

# link uwsgi ini files in /etc/uwsgi/
# link uwsgi service files in /etc/systemd/system/

systemctl start emperor.uwsgi
```