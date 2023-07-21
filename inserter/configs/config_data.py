"""
CONFIG explonation:
    Dict(
        DataType: str = List[Tuple(number_of_unique_values: int, range_of_values: Any)]
        )

Each DataType has a list of columns related to it
Each column is represented as a tuple consists of number_of_unique_values and it's range
"""
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from configs.config_getting_varchar_data import BASE_PARAMS

BASE_DATA_CONFIG: Optional[Dict[str, List[Tuple[int, Any]]]] = \
                    {
                    'varchar': [(10,BASE_PARAMS)],
                    'integer':[(40000, (1, 1000000))],
                    'date': [(300, (date(2023,1,1), date(2023,12,31)))]
                    }


def get_data_config(kwargs: Dict = {}):
        return {**BASE_DATA_CONFIG, **kwargs}


DATA_CONFIG = get_data_config()
