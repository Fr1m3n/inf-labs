#!/usr/bin/python3

# Author: Roman Devyatilov
# Group: P3112
# Variant: 4
# License: WTFPL
# Код считывает из файла строки типа:
# <x: исходная СС> <y: СС для результата> <a0..a4: целые положительные числа в СС х>
# Допустимые СС:
# СС с основанием x(x - целое число в десятичной СС),
# факториальная(обозначается как fact),
# фибоначчиева(обозначается как fibb)

FIBBONACCI = 'fibb'
FACTORIAL = 'fact'
ZERO_ASCII_CODE = ord('0')

# Свой int, надеюсь можно было написать...
def _int(q):
    a = 0
    for d in str(q):
        a = a * 10 + ord(d) - ord('0')
    return a

# Функция перевода числа в десятичную СС
# Аргументы:
# source - исходное число
# source_radix - СС исходного числа
def toDec(source, source_radix):

    if(str(type(source)) != "<type 'str'>"):
        source = str(source)

    def getNext(radix, x, y):
        if(radix == FACTORIAL):
            y += 1
            return x * y, y
        elif(radix == FIBBONACCI):
            q = y
            y = x
            return x + q, y
        else:
            return x * _int(radix), radix

    if(source_radix == '10'):
        return source
    source = source[::-1]
    x = 1
    y = 1
    res = 0
    for digit in source:
        digit_code = ord(digit) - ZERO_ASCII_CODE
        # print(digit_code)
        res += (digit_code if digit_code <= 9 else digit_code - 7) * x
        x, y = getNext(source_radix, x, y)
        # print(x, y, res)
    return res
# Функция для перевода числа source из СС десятичной в res_radix СС.
def decTo(source, res_radix):

    if(str(type(source)) != "<type 'int'>"):
        source = _int(source)

    if(res_radix == FIBBONACCI):
        return decToFibb(source)

    def getNext(radix, x):
        return (x + 1 if radix == FACTORIAL else x)

    if(res_radix == 10):
        return source


    x = (2 if res_radix == FACTORIAL else _int(res_radix))
    res = ''
    while(source != 0):
        res += str(source % x)
        source //= x
        x = getNext(res_radix, x)
    return res[::-1]

# Отдельная функция для перевода в фиббоначчиеву СС из десятичной.
# Принимает только исходное десятичное число
def decToFibb(source):
    if(str(type(source)) != "<type 'int'>"):
        source = _int(source)
    _f = [1, 2]
    res = ''
    while(_f[-1] < source):
        _f.append(_f[-1] + _f[-2])
    for fib_num in _f[::-1]:
        if fib_num <= source:
            res += '1'
            source -= fib_num
        else:
            res += '' if res == '' else '0'
    return res.strip()

# Функция для перевода числа source из source_radix СС в res_radix СС
def convert(source, source_radix, res_radix):
    return decTo(toDec(source, source_radix), res_radix)

# Точка входа
if __name__ == "__main__":
    inp = open("input.txt", "r")
    for line in inp:
        words = line.split()
        source_radix = words[0]
        res_radix = words[1]
        s = source_radix + ' -> ' + res_radix + ' : '
        words = words[2:]   
        for num in words:
            source = num
            res = convert(source, source_radix, res_radix)
            s += (' | ' if s[-2] != ':' else '') + source + ' -> ' + res
        print(s)
