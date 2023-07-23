import os
import sys
import time
from functools import wraps

sys.path.append(os.path.dirname("/home/alexnazarv/Desktop/repos_private/postgres-demo/inserter/logger.py"))
from logger import create_logger

logger_s = create_logger(loggername=os.path.basename(__file__).split('.')[0],
                         stream_handler=True)

logger_f = create_logger(loggername=os.path.basename(__file__).split('.')[0] + '_f',
                         path_to_file='inserter/logs/log_executes.log')


def timed(func):
    """
    Decorator.
    Prints amount of seconds spent to execute wrapped function.
    """
    @wraps(func)
    def timed_func(*args, **kwargs):
        time0 = time.time()
        res = func(*args, **kwargs)
        logger_f.info(f"Finished '{func.__name__}' in {time.time() - time0:.4f} seconds")
        logger_s.info(f"Finished '{func.__name__}' in {time.time() - time0:.4f} seconds")
        return res
    return timed_func
