import logging
from typing import Optional
from logging.handlers import RotatingFileHandler


def configure_root_logger(level: int = logging.INFO, logfile: Optional[str] = None) -> logging.Logger:
    root = logging.getLogger()
    if root.handlers:
        return root
    root.setLevel(level)
    format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(format)
    root.addHandler(handler)
    if logfile:
        file_handler = RotatingFileHandler(logfile, maxBytes=10_000_000, backupCount=3)
        file_handler.setFormatter(format)
        root.addHandler(file_handler)
    return root


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
