import logging

formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s")

log = logging.FileHandler("client.log", encoding="utf8")
log.setFormatter(formatter)

logger = logging.getLogger("client")
logger.addHandler(log)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logger.critical("Критическая ошибка")
    logger.error("Ошибка")
    logger.debug("Отладочная информация")
    logger.info("Информационное сообщение")
