from database.manager import DBManager
from database.fill_up_db import fill_up_db

if __name__ == "__main__":
    db_manager = DBManager()
    db_manager.create_tables()
    fill_up_db()
