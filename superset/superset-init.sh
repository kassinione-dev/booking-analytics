#!/usr/bin/env bash
# Инициализация Superset при каждом старте контейнера.
# Все шаги идемпотентны: повторный `docker compose up` ничего не ломает.
set -euo pipefail

echo "[superset-init] миграции метабазы"
superset db upgrade

echo "[superset-init] администратор ${SUPERSET_ADMIN_USERNAME}"
superset fab create-admin \
  --username "${SUPERSET_ADMIN_USERNAME}" \
  --firstname Superset \
  --lastname Admin \
  --email "${SUPERSET_ADMIN_EMAIL}" \
  --password "${SUPERSET_ADMIN_PASSWORD}" ||
  echo "[superset-init] администратор уже создан"

echo "[superset-init] роли и права"
superset init

# TODO(Амир): подключение к ClickHouse через clickhouse-connect
#   (SQLAlchemy URI clickhousedb+connect://...) и импорт дашборда.
#   Пока дашборд импортируется вручную, сервис стартует без него.
