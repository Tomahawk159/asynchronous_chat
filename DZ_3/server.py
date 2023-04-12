"""Программа-сервер"""

from socket import socket, AF_INET, SOCK_STREAM
import sys
import json


def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    """
    if (
        "action" in message
        and message["action"] == "presence"
        and "user" in message
        and message["user"]["account_name"] == "guest"
    ):
        return {"response": 200}
    return {"response": 400, "error": "Bad Request"}


def send_msg_client(client, response):
    """
    Кодирование и отправка сообщения клиенту

    :param trans:
    """
    js_message = json.dumps(response)
    encoded_message = js_message.encode("utf-8")
    client.send(encoded_message)
    client.close()


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 0000 -a 0.0.0.0
    :return:
    """
    try:
        if "-p" in sys.argv:
            listen_port = int(sys.argv[sys.argv.index("-p") + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print("После параметра -'p' необходимо указать номер порта.")
        sys.exit(1)
    except ValueError:
        print("Порт должен быть в диапазоне от 1024 до 65535.")
        sys.exit(1)
    try:
        if "-a" in sys.argv:
            listen_address = sys.argv[sys.argv.index("-a") + 1]
        else:
            listen_address = ""
    except IndexError:
        print("После параметра 'a'- необходимо указать адрес.")
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(3)

    while True:
        client, _ = transport.accept()
        try:
            encoded_response = client.recv(4096)
            json_response = encoded_response.decode("utf-8")
            response = json.loads(json_response)
            print(response)

            response = process_client_message(response)

            send_msg_client(client, response)

        except (ValueError, json.JSONDecodeError):
            print("Принято некорретное сообщение от клиента.")
            client.close()


if __name__ == "__main__":
    main()
