import os
import psycopg2 as pg
from dotenv import load_dotenv
from pathlib import Path


def connect():
    dotenv_path = Path('../.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    
    # print(db_name, db_user, db_password, db_host, db_port)

    try:
        connection = pg.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        return connection
    except Exception as e:
        print(e)
        return None
