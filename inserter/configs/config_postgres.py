class BasePostgresConfig(object):
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'testdb'
    DB_SCHEMA: str = 'public'
    DB_MAX_SIZE: int = 10
    DB_MIN_SIZE: int = 1


class PostgresConfig(BasePostgresConfig):
    ...


config = PostgresConfig()
