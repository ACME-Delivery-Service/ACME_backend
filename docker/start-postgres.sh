#!/usr/bin/env bash
set -e
docker-compose -p acme -f docker/compose-postgres.yml down
docker-compose -f docker/compose-postgres.yml build
docker-compose -p acme -f docker/compose-postgres.yml up -d