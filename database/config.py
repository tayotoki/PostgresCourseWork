from configparser import ConfigParser
from pathlib import Path

from settings import DB_INI_FILE, DEFAULT_PG_CONFIG


class ConfigError(Exception):
    def __init__(self, message: str = "Invalid section/params in config file"):
        self.message = message

    def __repr__(self):
        return self.message

    __str__ = __repr__


def make_default_db_config(filename: Path = DB_INI_FILE):
    """Создание/запись в файл конфигурации стандартных настроек."""
    parser = ConfigParser()
    parser.read_dict(DEFAULT_PG_CONFIG)

    with open(filename, "w") as config_file:
        parser.write(config_file)


def config(filename: Path = DB_INI_FILE, section: str = "postgresql"):
    """Считывание файла конфигурации."""
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            db[param[0]] = param[1]
    else:
        raise ConfigError

    return db


def get_config():
    try:
        with open(DB_INI_FILE) as db_ini:
            data = db_ini.read()
    except FileNotFoundError:
        make_default_db_config()
    else:
        if not data:
            make_default_db_config()

    return config()
