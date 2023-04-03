"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode).
"""

var_1 = 'разработка'
var_2 = 'администрирование'
var_3 = 'protocol'
var_4= 'standard'

words = [var_1, var_2, var_3, var_4]

words_encode = [i.encode('utf-8') for i in words]
words_decode = [i.decode('utf-8') for i in words_encode]

print(words_encode)
print(words_decode)
