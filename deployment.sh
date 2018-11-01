#!/usr/bin/env bash
systemctl stop emperor.uwsgi

git pull
python3 manage.py migrate

systemctl start emperor.uwsgi
