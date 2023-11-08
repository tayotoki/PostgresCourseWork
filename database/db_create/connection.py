import psycopg2

from database.config import get_config


def connect():
    config = get_config()

    conn = psycopg2.connect(dbname="postgres", **config)

    conn.autocommit = True

    return conn
