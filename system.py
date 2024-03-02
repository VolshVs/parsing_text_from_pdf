import os
import sqlalchemy as sq

from pathlib import Path
from dotenv import load_dotenv


def connecting():
    """Функция передает сведения для соединения с базой данных."""
    dotenv_path = Path('env/.env')
    load_dotenv(dotenv_path=dotenv_path)
    type_sql = os.getenv('TYPE_SQL')
    login = os.getenv('LOGIN')
    password = os.getenv('PASS')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    db_name = os.getenv('DB_NAME')
    DSN = (type_sql + '://' + login + ':' + password + '@' +
           host + ':' + port + '/' + db_name)
    engine = sq.create_engine(DSN)
    return engine
