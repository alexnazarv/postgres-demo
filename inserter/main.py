from datetime import date
from math import ceil
from typing import Any, Dict, List, Optional, Tuple

from configs.config_data import get_data_config
from configs.config_getting_varchar_data import BASE_PARAMS, URL
from configs.config_postgres import config
from connection import AbstractConnection

from inserter import Inserter

CHUNK_SIZE: int = 500000
COUNT_ROWS: int = 20000000
CHUNKS_NUM = ceil(COUNT_ROWS / CHUNK_SIZE)
ISOLATION_LEVEL='SERIALIZABLE'

DATA_CONFIG: Optional[Dict[str, List[Tuple[int, Any]]]] = \
                    {
                    'varchar': [(11000, BASE_PARAMS)],
                    'integer':[(2000000, (1, 50000000))],
                    'date': [(300, (date(2023,1,1), date(2023,12,31)))]
                    }
DATA_CONFIG = get_data_config(DATA_CONFIG)


def main():
    with AbstractConnection(config=config, isolation_level=ISOLATION_LEVEL) as cur:
        inserter = Inserter(data_config=DATA_CONFIG, url=URL)
        chunks_generator = inserter.generate_chunks(chunks_num=CHUNKS_NUM, chunk_size=CHUNK_SIZE)

        for chunk in chunks_generator:
           inserter.insert_rows(cursor=cur, chunk=chunk, table_name='test_table')


if __name__ == '__main__':
    main()
