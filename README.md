# Описание
Приложение для парсинга вакансий с помощью публичного API Headhunter.
Используется список работодателей, у которых парсятся все вакансии.
Данные о работодателях и их вакансиях заносятся в базу данных PostgreSQL.
Для работы с базой данных используется python-скрипт с аргументами командной строки.

## Установка
Создать виртуальное окружение python версии 3.11(рекомедуется) в папке .../VacancyParser:

    python3.11 -m venv env
    source ./env/bin/activate
    pip install -r requirements.txt

Или с помощью poetry:

    poetry env use python3.11
    poetry shell
    poetry install

## Данные для авторизации в базе данных
Необходимо создать ```.env``` файл в ```.../HeadHunterParser```.
В файле нужно указать ```PG_LOGIN``` - логин пользователя(по умолчанию ```postgres```);
                      ```PG_PASSWORD``` - пароль пользователя(по умолчанию ```12345```).
Пример файла ```example_env_file``` находится в корневом каталоге.

## Параметры соединения с базой данных
Для переопределения стандартных параметров соединения с базой данных необходимо
переназначить значения в словаре ```DEFAULT_PG_CONFIG``` в файле ```settings.py```:

    ...
    DEFAULT_PG_CONFIG = {
        "postgresql": {
            "host": "localhost",
            "user": PG_USER,
            "password": PG_PASSWORD,
            "port": 5432,
        }
    }

## Создание базы данных и наполнение её данными
Для создания базы данных, создания таблиц, наполнение данными из API используется ```make```:

    make init_db

## Взаимодействие с базой
Для взаимодействия с инициализрованной после ```make init_db``` команды используется:

    ./db_interactive.py

При этом команда ```./db_interactive.py``` принимает аргументы командной строки:

    usage: db_user_interact.py [-h] [-gcvc] [-gvwhs] [-gvwk KEYWORD] [-gav] [-gas]

    Database-User adapter

    options:
      -h, --help            show this help message and exit
      -gcvc, --get_comp_and_vac_count
                            Show company name with vacancies count
      -gvwhs, --get_vacs_with_higher_salary
                            Show vacancies with greater than average salary
      -gvwk KEYWORD, --get_vacs_with_keyword KEYWORD
                            Shows vacancies whose names contain the passed keyword
      -gav, --get_all_vacs  Show all vacancies
      -gas, --get_avg_salary
                            Show average low and high salary

Примеры использования:

    ./db_user_interact.py -h  # Вызов справочной информации.
    ./db_user_interact.py -gvwk=разработчик  # Поиск по названиям вакансий без учета регистра.
    ./db_user_interact.py -gas  # Выводит среднюю минимальную и среднюю максимальную зарплату по вакансиям.