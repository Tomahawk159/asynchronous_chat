"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.
"""

import subprocess
import chardet


def ping_web_resources(web_resources):
    args = ['ping', web_resources]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in ping.stdout:
        result = chardet.detect(line)
        print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


ping_web_resources('yandex.ru')
ping_web_resources('youtube.com')