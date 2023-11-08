from settings import DB_NAME


def create_db(connection):
    is_exists_sql = f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';"
    create_database_sql = f"CREATE DATABASE {DB_NAME};"

    cursor = connection.cursor()
    cursor.execute(is_exists_sql)
    is_exists = cursor.fetchall()

    if not is_exists:
        cursor.execute(create_database_sql)

    connection.close()
