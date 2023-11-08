"""Заполнение базы данных данными из API."""

from tqdm import tqdm

from database.manager import DBManager
from api.headhunter import HeadHunterAPI
from settings import EMPLOYERS_NAMES


hh_api = HeadHunterAPI()
db_manager = DBManager()


def fill_up_db():
    employers = [
        hh_api.get_employer(search_text=text)
        for text in EMPLOYERS_NAMES
    ]

    for employer in tqdm(
            employers,
            desc="Получение данных о работодателе из API и выгрузка данных в базу данных",
            unit="object"
    ):
        db_manager._execute(
            f"""INSERT INTO employers VALUES (%s, %s, %s, %s);""", (
                    employer.id,
                    employer.name,
                    employer.description,
                    employer.vacancies_url
            )
        )

        employer_vacancies = hh_api.get_vacancies_by_employer(employer=employer)

        for vacancy in employer_vacancies:
            db_manager._execute(
                f"""INSERT INTO vacancies 
                    (vacancy_id,
                     employer_id,
                     name,
                     alternate_url,
                     area,
                     description,
                     responsibility,
                     salary,
                     published_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", (
                        vacancy.id,
                        vacancy.employer_id,
                        vacancy.name,
                        vacancy.alternate_url,
                        vacancy.area,
                        vacancy.description,
                        vacancy.responsibility,
                        tuple(vacancy.salary.__dict__.values()) if vacancy.salary else None,
                        vacancy.published_at
                )
            )


if __name__ == "__main__":
    fill_up_db()
