# Лабораторная работа № 4

### Постановка задачи:
1. Напишите функцию (calculate), которая принимает на вход 2 операнда, возможно целые, возможно дробные , выполняет деление операнда 1 на операнд 2 и точность (epsilon, ключевой аргумент) по умолчанию 0.0001 (диапазон: 10**-1 < epsilon < 10**-9). 
2. Напишите функцию (load_params), которая считывает значение точности из конфигурационного файла settings.ini и задает точность для функции 1. 
3. Напишите тесты для тестирования работы функции 1 ( 1/2, epsilon = 0.1 = 0.5, 1/1000 = 0.001 epsilon = 0.001, деление на ноль) и функции 2 (виды тестов: проверить ситуацию открытия файла на чтение, epsilon входит в диапазон значений, формат числа в конф. файле). 

### Решение задачи:
1) Функция calculate
```python
def calculate(op1: int | float, op2: int | float, epsilon: float = 0.0001) -> float:
    """ Функция деления двух чисел с заданной точностью

    :param int | float op1: операнд 1 (делимое)
    :param int | float op2: операнд 2 (делитель)
    :param float epsilon: точность вычислений
    :return: кортеж из результата вычислений с необходимой точностью и кол-во знаков после запятой в точности

    >>> calculate(10, 3, 0.1)
    (3.3, 1)
    """
    power = int(fabs(log10(epsilon))) # необходимое кол-во цифр после запятой
    return round((op1/op2), power)

```
1) Функция load_params
```python
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
```

*********
Полное решение в файле [Lab_5.py](Lab_5.py)

### Тестирование:
Тесты в файле [tests_division.py](tests_division.py)
Результат написанных тестов:
![](res_test.png)



