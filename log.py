import logging
import os
from datetime import datetime

from parameters import LOGGER_ENABLE


class LogTool:
    def __init__(self):
        self.filename = 'log\\' + datetime.now().strftime("%Y-%m-%d_%X.log").replace(':', '-')
        if not os.path.exists('log'):
            os.mkdir('log')

    def get_logging(self, device_name: str):
        logger = logging.getLogger(device_name)
        handler1 = logging.StreamHandler()
        handler2 = logging.FileHandler(self.filename, encoding='utf-8')

        logger.setLevel(logging.DEBUG)
        handler1.setLevel(logging.INFO)
        handler2.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s >>%(message)s")
        handler1.setFormatter(formatter)
        handler2.setFormatter(formatter)

        logger.addHandler(handler1)
        logger.addHandler(handler2)

        if not LOGGER_ENABLE:
            logger.disabled = True
        return logger
