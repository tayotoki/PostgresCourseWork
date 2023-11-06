from pathlib import Path
from credentials.db import PG_USER, PG_PASSWORD

BASE_DIR = Path(__file__).resolve().parent


# API settings.
EMPLOYERS_NAMES = [
    "СБЕР",
    "Яндекс",
    "SkyEng",
    "SkyPro",
    "МТС",
    "Билайн",
    "YOTA",
    "Мегафон",
    "Московский метрополитен",
    "IT"
]

# Database settings.
DB_INI_FILE = BASE_DIR / "database.ini"

DB_NAME = "vacancy_parser"

DEFAULT_PG_CONFIG = {
    "postgresql": {
        "host": "localhost",
        "user": PG_USER,
        "password": PG_PASSWORD,
        "port": 5432,
    }
}
