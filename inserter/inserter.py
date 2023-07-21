import random
from typing import Any, Tuple

from configs.config_data import DATA_CONFIG
from connection import AbstractConnection
from data_miner import DataMiner
from plugins.common import timed
from tqdm import tqdm


class Inserter(DataMiner):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def generate_chunks(self, chunks_num: int,
                        chunk_size: int) -> Tuple[Tuple[Any]]:
        """Automatization calling all "getting datatype" methods through builtin python method
           exec(str)
        """
        executable_string = ''
        methods_list = [_ for _ in self.__dir__() if 'getting' in _]
        for method in methods_list:
            executable_string += ('*self.' + method + '(),')
        exec('self.column_list = [%s]' %executable_string)


        def chunker(self, chunk_size):
            rows = list()
            for _ in range(chunk_size):
                row = [random.choice(col) for col in self.column_list]
                rows.append(tuple(row))
            return tuple(rows) 
        

        for _ in tqdm(range(chunks_num)):
            self.chunk = chunker(self, chunk_size)
            yield self.chunk


    @staticmethod
    def insert_rows(chunk: Tuple[Tuple[Any]], table_name: str,
                    cursor: AbstractConnection) -> None:

        table_config = []
        for key in DATA_CONFIG.keys():
            nums_of_datatype_col = len(DATA_CONFIG.get(key))
            for num in range(nums_of_datatype_col):
                table_config.append(f'{key}{num} {key:>20}')
        table_config = '\n,'.join(table_config)
        
        cursor.execute('CREATE TABLE IF NOT EXISTS %s (%s)' %(table_name, table_config))

        records_list_template = ','.join(['%s'] * len(chunk))
        insert_query = 'INSERT INTO %s VALUES %s' %(table_name, records_list_template)
        cursor.execute(insert_query, chunk)
