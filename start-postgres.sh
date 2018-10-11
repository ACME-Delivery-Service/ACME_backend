#!/usr/bin/env bash
set -e
docker-compose -p acme -f compose-postgres.yml down
docker-compose -f compose-postgres.yml build
docker-compose -p acme -f compose-postgres.yml up -d