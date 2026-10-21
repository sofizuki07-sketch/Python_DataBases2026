# Лабораторная работа № 4(3)

### Постановка задачи:
1. Напишите функцию (calculate), которая принимает на вход 2 операнда, возможно целые, возможно дробные , выполняет деление операнда 1 на операнд 2 и точность (epsilon, ключевой аргумент) по умолчанию 0.0001 (диапазон: 10**-1 < epsilon < 10**-9). 
2. Напишите функцию (load_params), которая считывает значение точности из конфигурационного файла settings.ini и задает точность для функции 1. 
3. Напишите тесты для тестирования работы функции 1 ( 1/2, epsilon = 0.1 = 0.5, 1/1000 = 0.001 epsilon = 0.001, деление на ноль) и функции 2 (виды тестов: проверить ситуацию открытия файла на чтение, epsilon входит в диапазон значений, формат числа в конф. файле). 

### Решение задачи:
Сначала решение было упрощённым, потом добавилась работа с исключениями через логирование. Поэтому в решении 2 версии основных функций
**!Важно!** Здесь представлены только 2 функции, для полного решения перейти в файл с основной программой V V V

**1)** Функция calculate
**ДО добавления logger:**
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
**ПОСЛЕ добавления logger:**
```python
ef calculate(op1: int | float, op2: int | float, *, epsilon: float = 0.0001) -> float:
    """ Функция деления двух чисел с заданной точностью

    :param int | float op1: операнд 1 (делимое)
    :param int | float op2: операнд 2 (делитель)
    :param float epsilon: точность вычислений (=0.0001 по умолчанию)
    :return: кортеж из результата вычислений с необходимой точностью и кол-во знаков после запятой в точности

    >>> calculate(10, 3, epsilon=0.1)
    3.3
    """
    # ловим ОШИБКУ при делении на ноль
    if op2 == 0:
        error_text = "Деление на ноль"
        logger.error(error_text)
        raise ZeroDivisionError(error_text)

    power = len(str(epsilon).split('.')[1]) # необходимое кол-во цифр после запятой для round
    return round((op1/op2), power)
```

**2)** Функция load_params

**ДО добавления logger:**
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

**ПОСЛЕ добавления logger:**
```python
def load_params(path: str | Path | None = None, section: str = "DEFAULT", option: str = "epsilon") -> float:
    """ Функция считывает точность из файла settings.ini

    :param path: путь к файлу конфигурации
    :param section: имя секции в filename
    :param option: имя параметра в секции section, равного требуемой точности
    :return: точность вычислений epsilon из конфигурационного файла
    """
    # ищет файл именно в папке с текущим файлом
    if path is None:
        path = Path(__file__).resolve().parent / 'settings.ini'

    parser = configparser.ConfigParser()

    # ручная обработка CRITICAL при ошибке ФИЗИЧЕСКОГО чтения файла
    try:
        read_files = parser.read(path, encoding="utf-8")
    except OSError as exc:
        msg = f"Ошибка чтения файла {path}:{exc}"
        logger.critical(msg)
        raise

    # обработка CRITICAL при ошибке в названии/пути файла
    if not read_files:
        msg = f"Файл {str(path)!r} не найден или недоступен"
        logger.critical(msg)
        raise FileNotFoundError(msg)

    if section != parser.default_section and not parser.has_section(section):
        raise KeyError(f"В файле нет секции [{section}]")

    if not parser.has_option(section, option):
        raise KeyError(f"В секции [{section}] нет параметра {option!r}")

    raw_value = parser.get(section, option)

    try:
        epsilon = parser.getfloat(section, option)
    except ValueError as exc:
        raise ValueError(
            f"Параметр {option!r} должен быть числом, получено {raw_value!r}"
        ) from exc

    validate_epsilon(epsilon)

    # Меняем значение по умолчанию для calculate
    calculate.__defaults__ = (epsilon,)

    return epsilon
```

*********
Полное решение в файле [Lab_3.py](Lab_3.py)

### Тестирование:
Тесты в файле [tests_division.py](tests_division.py)
Результат написанных тестов:
![](res_test.png)



