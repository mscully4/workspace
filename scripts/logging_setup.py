from logging import getLogger, DEBUG, Logger, Formatter
from logging.handlers import RotatingFileHandler
import os

MAX_BYTES = 100000000

def get_logger(name: str, log_level: str=DEBUG):
    logger = getLogger(name)
    logger.setLevel(log_level)
    return logger

def add_handler(logger: Logger, log_path: str, file_name: str="/logs.txt", log_level: int = DEBUG, max_bytes=MAX_BYTES) -> Logger:
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    file_handler = RotatingFileHandler(log_path + file_name, maxBytes=max_bytes)
    formatter = Formatter('%(asctime)s:%(filename)s:Line %(lineno)d:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    logger.addHandler(file_handler)
    return logger
