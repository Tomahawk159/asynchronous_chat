import sys
import json
import socket
import time
import threading

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
    to_user = input("Введите получателя сообщения: ")
    message = input("Введите сообщение для отправки: ")

    client_log_config.logger.info(f"Формируется сообщение {action}")
    message = {
        "action": action,
        "time": time.time(),
        "from": username,
        "message": text,
        "to": to_user,
    }
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
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    while True:
        command = input("Введите команду: ")
        if command == "message":
            create_message(sock, username)
        elif command == "exit":
            send_message(sock)
            print("Завершение соединения.")
            client_log_config.logger.info("Завершение работы по команде пользователя.")
            time.sleep(0.5)
            break
        else:
            print(
                "Команда не распознана, попробойте снова. help - вывести поддерживаемые команды."
            )


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
    else:
        receiver = threading.Thread(target=send_message, args=(sock, username))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(
            target=user_interactive(username=username), args=(sock, username)
        )
        user_interface.daemon = True
        user_interface.start()
        client_log_config.logger.debug("Запущены процессы")

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break

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
