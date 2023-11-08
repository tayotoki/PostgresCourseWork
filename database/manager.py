import re
from pathlib import Path
from typing import Any, Mapping, Sequence, MutableSequence

import psycopg2

from settings import DB_NAME

from database.config import get_config
from database.db_create.setup import setup


def get_script(file: Path):
    """Получение sql-скрипта из файла *.sql"""
    if file.exists() and re.fullmatch(r".*[.]sql$", str(file)):
        with open(file) as file:
            script = file.read()
        return script
    raise OSError("Нет такого файла или разрешение файла не sql.")


def is_empty_result(*args) -> bool:
    for arg in args:
        if isinstance(arg, (MutableSequence, tuple, frozenset)):
            return is_empty_result(*arg)
        if arg:
            return False
    else:
        return True


class DBInitial(type):
    """Метакласс для создания базы данных
    перед созданием класса. Также реализаует
    паттерн 'одиночка' для классов,
    созданных данным метаклассом."""
    _is_db_exists = False
    _instances = {}

    @classmethod
    def __prepare__(metacls, name, bases):
        """Создание БД перед пространством имен класса"""
        if not metacls._is_db_exists:
            setup()  # Создание БД.
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

    def _execute(self, script: str,
                 params: Sequence | Mapping[str, Any] | None = None) -> list[tuple[Any]] | None:
        """Выполнение транзакции в рамках
        текущего соединения с БД."""
        with self.connection as con:
            with con.cursor() as cur:
                cur.execute(script, params)
                try:
                    result = cur.fetchall()
                except psycopg2.ProgrammingError:
                    return  # У курсора нет никаких результатов.
                finally:
                    cur.close()

        if not is_empty_result(*result):
            return result

    def create_tables(self):
        self._execute(
            script=get_script(
                self.scripts_dir / "create_tables.sql"
            )
        )

    def get_companies_and_vacancies_count(self) -> list[tuple[Any]] | None:
        result = self._execute(
            script=get_script(
                self.scripts_dir / "get_company_and_vacancies_count.sql"
            )
        )

        return result

    def get_vacancies_with_higher_salary(self):
        avg_low, avg_high = self.get_avg_salary()

        result = self._execute(
            script="""
                SELECT * FROM vacancies
                WHERE (salary).salary_from > %s
                      AND (salary).salary_to > %s
                      AND salary IS NOT NULL
                      AND (salary).currency = 'RUR';
            """,
            params=(avg_low, avg_high)
        )

        return result

    def get_vacancies_with_keyword(self, keyword: str):
        result = self._execute(
            script="""
                SELECT * FROM vacancies
                WHERE name ~* %(keyword)s;
            """,
            params={"keyword": f".*{keyword}.*"}
        )

        return result

    def get_all_vacancies(self) -> list[tuple[Any]]:
        result = self._execute(
            script=get_script(
                self.scripts_dir / "get_all_vacancies.sql"
            )
        )

        return result

    def get_avg_salary(self) -> list[tuple[int]]:
        result = self._execute(
            script=get_script(
                self.scripts_dir / "get_avg_salary.sql"
            )
        )

        return result

    def __del__(self):
        """Закрытие соединения с БД
        перед удалением объекта менеджера."""
        self.close()

