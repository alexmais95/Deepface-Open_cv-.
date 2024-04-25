import psycopg2
import logging
from logging.config import dictConfig
from log_conf import loggin_conf

dictConfig(loggin_conf)
logger = logging.getLogger('my_logger')

class DataPost:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname='photo_famely', 
            user='postgres',
            password=1234,
            host='localhost',
            port=5432)
        self.cursor = self.conn.cursor()


    def insert_into_db(self, name, photo_path):
        try:
            self.cursor.execute("INSERT INTO photo_by_name (name, photo_path) VALUES (%s, %s);", (name, photo_path))
            self.conn.commit()
            logger.debug(f'[INSERT]: insert to data_base : {name}, {photo_path}')
        except Exception as ex:
            logger.debug(f'[EXCEPTION]: {ex}')

    def close_con(self):
        self.cursor.close()
        self.conn.close()