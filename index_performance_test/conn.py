from contextlib import contextmanager

import psycopg2

DB_USER: str = 'postgres'
DB_PASSWORD: str = 'postgres'
DB_HOST: str = 'localhost'
DB_PORT: int = 5432
DB_NAME: str = 'testdb'
DB_SCHEMA: str = 'public'
DB_MAX_SIZE: int = 10
DB_MIN_SIZE: int = 1
ISOLATION_LEVEL: str = 'REPEATABLE READ'


@contextmanager
def make_conn() -> psycopg2.connect:
    try:
        conn = psycopg2.connect(  
                        host=DB_HOST, 
                        database=DB_NAME,
                        user=DB_USER,  
                        password=DB_PASSWORD)

        conn.set_session(isolation_level=ISOLATION_LEVEL, autocommit=True)
        cursor = conn.cursor()
        yield cursor
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
