import logging
import logging.handlers


formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s")

log = logging.handlers.TimedRotatingFileHandler(
    "server.log", encoding="utf8", interval=1, when="D"
)
log.setFormatter(formatter)

logger = logging.getLogger("server")
logger.addHandler(log)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger.critical("Критическая ошибка")
    logger.error("Ошибка")
    logger.debug("Отладочная информация")
    logger.info("Информационное сообщение")
