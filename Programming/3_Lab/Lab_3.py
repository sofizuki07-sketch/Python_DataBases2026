import configparser
from pathlib import Path
import logging

def log() -> logging.Logger:
    """ Настраивает базовое логирование и возвращает логгер

    :return: объект логгера с именем 'myapp'
    """
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger('myapp')

logger = log()

def calculate(op1: int | float, op2: int | float, *, epsilon: float = 0.0001) -> float:
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

def validate_epsilon(epsilon: int | float) -> None:
    """ Функция проверки epsilon на числовой тип и диапазон

    :param epsilon: полученная из конфига точность вычислений
    """
    if not isinstance(epsilon, (int, float)):
        raise TypeError("epsilon должен быть числом")

    if not (0.1 >= epsilon >= pow(10, -9)):
        raise ValueError(
            f"epsilon должен быть в диапазоне "
            f"{0.1} >= epsilon >= {pow(10, -9)}"
        )

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


# запуск ТОЛЬКО напрямую, не через методы и т.д.
if __name__ == '__main__':
    eps = load_params()
    print(calculate(10, 3, epsilon=eps))



