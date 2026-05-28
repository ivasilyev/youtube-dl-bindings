import logging
import threading
from sys import stdout

LOGGING_FORMAT = "%(asctime)s.%(msecs)06d [%(filename)s %(name)s] %(levelname)s %(funcName)s(%(lineno)s) - %(message)s"
DATE_FORMAT = "%Y.%m.%d %H:%M:%S"


class Log:
    _instance = None
    _lock = threading.Lock()  # Shared lock across all instances

    def __new__(cls):
        # First check (unlocked) for high performance after initialization
        if cls._instance is None:
            # Synchronize threads
            with cls._lock:
                # Second check (locked) to prevent race conditions
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # _LOG = get_logger()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(LOGGING_FORMAT)
        stdout_handler = logging.StreamHandler(stdout)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)


log = Log().logger
