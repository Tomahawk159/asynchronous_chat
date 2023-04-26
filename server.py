import json
import select
import sys
import time

from socket import socket, AF_INET, SOCK_STREAM

from log import server_log_config
from decorators import log


@log
def process_client_message(message, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :param client:
    :return:
    """

    server_log_config.logger.info(
        f"Отработала функция process_client_message: {message}"
    )
    if "action" in message and message["action"] in ("presence", "send"):
        response = {"response": 200, "msg": message}
    else:
        response = {"response": 400, "error": "Bad Request"}
    send_msg_client(client, response)


@log
def send_msg_client(client, response):
    """
    Кодирование и отправка сообщения клиенту

    :param client:
    :param response:
    """

    server_log_config.logger.info("Отработала функция send_msg_client")
    js_message = json.dumps(response)
    encoded_message = js_message.encode("utf-8")
    client.send(encoded_message)


@log
def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 0000 -a 0.0.0.0
    :return:
    """

    server_log_config.logger.info("Отработала функция main")
    try:
        if "-p" in sys.argv:
            listen_port = int(sys.argv[sys.argv.index("-p") + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        server_log_config.logger.critical(
            "После параметра -'p' необходимо указать номер порта."
        )
        sys.exit(1)
    except ValueError:
        server_log_config.logger.error("Порт должен быть в диапазоне от 1024 до 65535.")
        sys.exit(1)
    try:
        if "-a" in sys.argv:
            listen_address = sys.argv[sys.argv.index("-a") + 1]
        else:
            listen_address = "0.0.0.0"
    except IndexError:
        server_log_config.logger.critical(
            "После параметра 'a'- необходимо указать адрес."
        )
        sys.exit(1)

    clients = []
    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(10)

    while True:
        try:
            client, addr = transport.accept()
        except (ValueError, json.JSONDecodeError):
            print("Принято некорретное сообщение от клиента.")
            client.close()
        else:
            print("Получен запрос на соединение с %s" % str(addr))
            clients.append(client)
        finally:
            w = []
            try:
                _, w, _ = select.select([], clients, [], 0)
            except Exception as e:
                print(e)

            for s_client in w:
                try:
                    encoded_response = s_client.recv(4096)
                    json_response = encoded_response.decode("utf-8")
                    response = json.loads(json_response)
                    print(response)
                    for s_client in w:
                        process_client_message(response, s_client)
                except:
                    # Удаляем клиента, который отключился
                    clients.remove(s_client)


if __name__ == "__main__":
    main()
