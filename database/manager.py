import re
from pathlib import Path

import psycopg2

from settings import DB_NAME

from database.config import get_config
from database.setub_db.setup import setup


def get_script(file: Path):
    """Получение sql-скрипта из файла *.sql"""
    print(file)
    if file.exists() and re.fullmatch(r".*[.]sql$", str(file)):
        with open(file) as file:
            script = file.read()
        return script
    raise OSError("Нет такого файла или разрешение файла не sql.")


class DBInitial(type):
    _is_db_exists = False
    _instances = {}

    @classmethod
    def __prepare__(metacls, name, bases):
        if not metacls._is_db_exists:
            setup()
            metacls._is_db_exists = True

        return super().__prepare__(name, bases)

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DBInitial, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class DBManager(metaclass=DBInitial):
    __config: dict[str, str] = get_config()
    scripts_dir: Path = Path(__file__).resolve().parent / "sql_scripts"

    def __init__(self):
        self.connection = psycopg2.connect(dbname=DB_NAME, **self.__config)

    def close(self):
        self.connection.close()

    def _execute(self, script: str):
        """Выполнение транзакции sql-скрипта
        в рамках текущего соединения с БД."""
        with self.connection as con:
            with con.cursor() as cur:
                cur.execute(script)
                cur.close()

    def create_tables(self):
        self._execute(
            get_script(
                self.scripts_dir / "create_tables.sql"
            )
        )

    def __del__(self):
        """Закрытие соединения с БД
        перед удалением объекта менеджера."""
        self.close()


manager = DBManager()
manager.create_tables()
