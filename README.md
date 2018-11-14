# Basic setup
## Dependencies

Debian specific:
```bash
aptitude install python3 python3-setuptools libpython3.5
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
```postgresql
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
python3 manage.py createsuperuser --email=j.doe@innopolis.ru --region=RU --contacts_id=1
python3 manage.py collectstatic
```
> superuser: email=j.doe@innopolis.ru password=12345678

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

## Problems
```bash
# bind(): No such file or directory [core/socket.c line 230]
mkdir -p /var/run/uwsgi
chmod -R 777 /var/run/uwsgi

# /usr/local/bin/uwsgi: error while loading shared libraries: libpython3.5m.so.1.0: cannot open shared object file: No such file or directory
ln -s /usr/lib/x86_64-linux-gnu/libpython3.6m.so.1.0 /usr/lib/x86_64-linux-gnu/libpython3.5m.so.1.0
```

### Error: That port is already in use.
```sudo lsof -t -i tcp:8000 | xargs kill -9