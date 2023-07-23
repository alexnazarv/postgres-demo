import os
import random
from datetime import date, timedelta
from typing import Any, Dict, List, Tuple

import requests
from logger import create_logger

logger_f = create_logger(loggername=os.path.basename(__file__).split('.')[0] + '_f',
                         path_to_file=os.path.dirname(__file__) + '/logs/log_data.log')

logger_s = create_logger(loggername=os.path.basename(__file__).split('.')[0] + '_s',
                         stream_handler=True)

class DataMiner(object):
    def __init__(self, data_config = None, url:str = None):
        self.__url = url
        self.__data_config = data_config


    def getting_varchar_columns(self):
        columns = []
        varchar_columns = self.__data_config.get('varchar')

        # if varchar_columns:
        #     for col in varchar_columns:
        #         num_of_unique_names = col[0]
        #         params = col[1]
        #         self.__url = self.__url + '%s?' %num_of_unique_names
        #         try:
        #             names = requests.get(url=self.__url, 
        #                                  params=params) \
        #                             .json()
        #             logger_f.info(names)
        #             columns.append(names)
        #             return columns
        #         except Exception:
        #             response = requests.get(url=self.__url, 
        #                                     params=params)
        #             for logger in [logger_s, logger_f]:
        #                 logger.error('Error: status code: %s, text: %s', response.status_code, response.text)

        if varchar_columns:
            for col in varchar_columns:
                with open('./inserter/names.txt', 'r') as file:
                    names = [name.strip('\n') for name in file.readlines()]
                    columns.append(names)
            return columns
                

    def getting_integer_columns(self):
        columns = []
        integer_columns = self.__data_config.get('integer')

        if integer_columns:
            for column in integer_columns:
                num_of_unique_nums = column[0]
                nums_range = column[1]
                nums = set()

                while len(nums) < num_of_unique_nums:
                    nums.add(random.randint(*nums_range)) 
                
                nums = list(nums)
                columns.append(nums)
        return columns


    def getting_date_columns(self):
        columns = []
        date_columns = self.__data_config.get('date')

        if date_columns:
            for column in date_columns:
                num_of_unique_dates = column[0]
                date_range = column[1]
                dates_dif = (date_range[1] - date_range[0]).days
                dates = set()

                while len(dates) < num_of_unique_dates:
                    dates.add(str(date_range[0] + timedelta(days=random.randint(0,dates_dif))))
                
                dates = list(dates)
                columns.append(dates)
        return columns
