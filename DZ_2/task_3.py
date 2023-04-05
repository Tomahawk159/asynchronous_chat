"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:

a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);

b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;

c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными.
"""

import yaml

data_dict = {
    "product": ["computer", "printer", "keyboard", "mouse"],
    "number_of_goods": 5,
    "price": {
        "computer": "200€-1000€",
        "printer": "100€-300€",
        "keyboard": "5€-50€",
        "mouse": "4€-7€",
    },
}


with open("file.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data_dict, f, default_flow_style=False, allow_unicode=True)

with open("file.yaml", "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)


print(data_dict == data)
