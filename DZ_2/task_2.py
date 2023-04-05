"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:

a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При
записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра.
"""

import json
import os


def write_order_to_json(item, quantity, price, buyer, date):
    orders = []
    dict_data = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date,
    }

    if os.path.exists("orders.json") and os.path.getsize("orders.json") != 0:
        with open("orders.json", "r", encoding="utf-8") as f:
            load_data = json.load(f)
            load_data.append(dict_data)
            orders.extend(load_data)
    else:
        orders.append(dict_data)

    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4)


write_order_to_json("apple", "3", "12.5", "woman", "12.05.2023")
write_order_to_json("tv", "1", "1200", "man", "15.06.2023")
write_order_to_json("phone", "1", "120", "man", "15.07.2023")
