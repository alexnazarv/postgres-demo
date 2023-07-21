from contextlib import AbstractContextManager

import psycopg2
from configs.config_postgres import BasePostgresConfig

ISOLATION_LEVELS = ['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE', 'DEFAULT']


class AbstractConnection(AbstractContextManager):
    def __init__(self, config: BasePostgresConfig,
                 isolation_level: str = 'REPEATABLE READ'):
        self.conn = psycopg2.connect(  
                host=config.DB_HOST, 
                database=config.DB_NAME,
                user=config.DB_USER,  
                password=config.DB_PASSWORD)

        self.conn.set_session(isolation_level=isolation_level, autocommit=True)
        self.cursor = self.conn.cursor()


    def __enter__(self):
        return self.cursor


    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
