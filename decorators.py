import sys
import logging
import inspect


if sys.argv[0].find("client") == -1:
    logger = logging.getLogger("server")
else:
    logger = logging.getLogger("client")


def log(func):
    def wrap(*args, **kwargs):
        data = func(*args, **kwargs)
        logger.info(
            f"Функция {func.__name__} ({args}, {kwargs}) вызвана из функции {inspect.stack()[1][3]}"
        )

        return data

    return wrap
