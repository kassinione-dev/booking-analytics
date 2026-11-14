"""Конфигурация Superset для booking-analytics.

Метабаза — Postgres, кэш — Redis, оба поднимаются в docker-compose.yml.
Секреты приходят из .env, значений по умолчанию здесь нет намеренно.
"""

import os
from urllib.parse import quote_plus

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# Пароль может содержать @, /, : — поэтому квотим.
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://"
    f"{quote_plus(os.environ['POSTGRES_USER'])}:"
    f"{quote_plus(os.environ['POSTGRES_PASSWORD'])}@"
    f"{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/"
    f"{os.environ['POSTGRES_DB']}"
)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))


def _redis_cache(db: int) -> dict[str, object]:
    """Отдельная Redis-база под каждый тип кэша, чтобы они не мешали друг другу."""
    return {
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": REDIS_HOST,
        "CACHE_REDIS_PORT": REDIS_PORT,
        "CACHE_REDIS_DB": db,
        "CACHE_DEFAULT_TIMEOUT": 300,
    }


CACHE_CONFIG = _redis_cache(1)
DATA_CACHE_CONFIG = _redis_cache(2)
FILTER_STATE_CACHE_CONFIG = _redis_cache(3)
EXPLORE_FORM_DATA_CACHE_CONFIG = _redis_cache(4)

# Superset стоит за публикацией порта Docker, ему нужны заголовки прокси.
ENABLE_PROXY_FIX = True
