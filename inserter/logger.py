import logging
import os
import sys
from logging import FileHandler, Formatter, Logger, StreamHandler

FMT='[%(asctime)s: %(levelname)s, %(name)s] %(message)s'


def create_logger(path_to_file: str = os.path.dirname(__file__) + '/logs/log_data.log',
                  loggername: str = os.path.basename(__file__).split('.')[0],
                  stream_handler: bool = False,
                  level=logging.DEBUG) -> Logger:    
    logger = logging.getLogger(loggername)
    logger.setLevel(level)
    formatter = Formatter(fmt=FMT)

    if stream_handler is True:
        handler = StreamHandler(stream=sys.stdout)    
    else:
        handler = FileHandler(filename=path_to_file)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
