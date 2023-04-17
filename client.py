import time
import sys
import json

from socket import socket, AF_INET, SOCK_STREAM

from log import client_log_config


def create_server_message(action, name):
    """
    Создание сообщения для сеервера

    :param action, name:
    """

    client_log_config.logger.info("Отработала функция create_server_message")
    msg_to_server = {
        "action": action,
        "time": time.time(),
        "user": {"account_name": name},
    }
    return msg_to_server


def send_msg_server(trans):
    """
    Кодирование и отправка сообщения серверу

    :param trans:
    """

    client_log_config.logger.info("Отработала функция send_msg_server")
    message_to_server = create_server_message("presence", "guest")

    js_message = json.dumps(message_to_server)
    encoded_message = js_message.encode("utf-8")
    trans.send(encoded_message)

    process_server_message(trans)


def process_server_message(transport):
    """
    Обработчик сообщений от сервера, проверяет корректность,

    :param transport:
    """

    client_log_config.logger.info("Отработала функция process_server_message")
    try:
        encoded_response = transport.recv(4096)
        json_response = encoded_response.decode("utf-8")
        response = json.loads(json_response)
        print(response)
    except (ValueError, json.JSONDecodeError):
        client_log_config.logger.error("Не удалось декодировать сообщение сервера.")


def main():
    """Загружаем параметы коммандной строки,разбираем ответ сервера"""

    client_log_config.logger.info("Отработала функция main")
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        client_log_config.logger.error("Порт должен быть в диапазоне от 1024 до 65535.")
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))

    send_msg_server(transport)


if __name__ == "__main__":
    main()
