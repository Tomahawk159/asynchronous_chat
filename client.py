import sys
import json
import socket
import time

from log import client_log_config
from decorators import log


@log
def create_presence_message(account_name):
    """
    Создание сообщения для сервера

    :param account_name:
    :return:
    """
    client_log_config.logger.info("Формируется сообщение presence")
    message = {
        "action": "presence",
        "time": time.time(),
        "user": {"account_name": account_name},
    }
    return message


@log
def create_message(action, text):
    """
    Создание сообщения для сервера

    :param action:
    :param text:
    :return:
    """
    client_log_config.logger.info(f"Формируется сообщение {action}")
    message = {"action": action, "time": time.time(), "from": username, "message": text}
    return message


@log
def read_message():
    """
    Получение сообщения от сервера

    :return:
    """
    client_log_config.logger.info("Ожидание сообщения от сервера")
    encoded_response = sock.recv(4096)
    json_response = encoded_response.decode("utf-8")
    response = json.loads(json_response)
    return response


@log
def send_message(message):
    """
    Отправка сообщения серверу

    :param message:
    :return:
    """
    client_log_config.logger.info("Отправка сообщения серверу")
    json_message = json.dumps(message)
    encoded_message = json_message.encode("utf-8")
    sock.send(encoded_message)


@log
def main():
    """
    Основная функция
    """
    global sock, username

    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        username = sys.argv[3]
    except IndexError:
        client_log_config.logger.error("Не заданы параметры командной строки")
        sys.exit(1)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, server_port))
        client_log_config.logger.info("Установлено соединение с сервером")
    except ConnectionRefusedError:
        client_log_config.logger.error("Не удалось подключиться к серверу")
        sys.exit(1)

    message = create_presence_message(username)
    send_message(message)
    response = read_message()
    client_log_config.logger.info(f"Ответ от сервера: {response}")

    while True:
        action = input("Введите команду: ")

        if action == "exit":
            break

        if action == "send":
            text = input("Введите сообщение: ")
            message = create_message(action, text)
            send_message(message)
            response = read_message()
            print(response)
            client_log_config.logger.info(f"Ответ от сервера: {response}")

    sock.close()
    client_log_config.logger.info("Отключение от сервера")


if __name__ == "__main__":
    main()
