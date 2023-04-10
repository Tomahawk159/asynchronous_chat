"""Программа-клиент"""

import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time


def main():
    """Загружаем параметы коммандной строки,разбираем ответ сервера"""
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        print("Порт должен быть в диапазоне от 1024 до 65535.")
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = {
        "action": "presence",
        "time": time.time(),
        "user": {"account_name": "guest"},
    }
    js_message = json.dumps(message_to_server)
    encoded_message = js_message.encode("utf-8")
    transport.send(encoded_message)

    try:
        encoded_response = transport.recv(4096)
        json_response = encoded_response.decode("utf-8")
        response = json.loads(json_response)
        print(response)
    except (ValueError, json.JSONDecodeError):
        print("Не удалось декодировать сообщение сервера.")


if __name__ == "__main__":
    main()
