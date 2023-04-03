"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""


words = ['сетевое программирование', 'сокет', 'декоратор']

with open('file.txt', 'w') as f:
    for elem in words:
        f.write(elem +'\n')
    file_encoding = f.encoding

with open('file.txt', 'r', encoding=file_encoding, errors='replace') as \
        f:
    for elem in f:
        print(elem)
        