from .connection import connect
from .create_db import create_db

connection = connect()


def setup():
    create_db(connection=connection)
