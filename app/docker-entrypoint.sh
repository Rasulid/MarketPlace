#!/bin/bash
set -e

# Ожидание запуска сервера PostgreSQL
until pg_isready --timeout=0 --dbname=${POSTGRES_DB}
do
  sleep 1
done

# Выполнение команды DROP TABLE
psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL
    DROP TABLE IF EXISTS admins;
    DROP TABLE IF EXISTS users;
EOSQL

# Оригинальный скрипт docker-entrypoint.sh
exec "$@"