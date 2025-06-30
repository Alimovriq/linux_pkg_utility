import os
import logging


from logging.handlers import  RotatingFileHandler


class CustomFormatter(logging.Formatter):
    """
    Кастомный форматер логов в цвете для консоли
    """
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def set_logger() -> logging.Logger:
    """
    Устанавливает логирование
    :return: класс логирования
    """
    logger = logging.getLogger("linux_pkg_utility")
    logger.setLevel(logging.DEBUG)

    # папка для логов
    os.makedirs("logs", exist_ok=True)

    # для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())

    # для файла
    file_handler = RotatingFileHandler("logs/log_info.log", maxBytes=2*1024*1024,
                                       backupCount=3, encoding="UTF-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    ))

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = set_logger()
