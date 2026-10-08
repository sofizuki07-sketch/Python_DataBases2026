from math import *
import configparser
from pathlib import Path

def calculate(op1: int | float, op2: int | float, epsilon: float = 0.0001) -> float:
    """ Функция деления двух чисел с заданной точностью

    :param int | float op1: операнд 1 (делимое)
    :param int | float op2: операнд 2 (делитель)
    :param float epsilon: точность вычислений (=0.0001 по умолчанию)
    :return: кортеж из результата вычислений с необходимой точностью и кол-во знаков после запятой в точности

    >>> calculate(10, 3, 0.1)
    3.3
    """
    power = len(str(epsilon).split('.')[1]) # необходимое кол-во цифр после запятой
    return round((op1/op2), power)


def load_params(path=None):
    """ Функция считывает точность из файла settings.ini

    :param path: путь к файлу конфигурации
    :return:
    """

    if path is None:
        path = Path(__file__).resolve().parent / 'settings.ini' # ищет файл именно в папке с текущим файлом
    config = configparser.ConfigParser()
    read_files = config.read(path)

    # print("Прочитанные файлы:", read_files)  # отладка
    # print("Секции в конфиге:", config.sections())  # отладка

    return config.getfloat('DEFAULT', 'epsilon')

    
eps = load_params()
print(calculate(10, 3, eps))    



