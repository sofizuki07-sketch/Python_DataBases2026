from Lab_5 import load_params, calculate
import unittest
import configparser
from pathlib import Path

class TestMath(unittest.TestCase):

    def setUp(self):
        self._config = configparser.ConfigParser()
        self.config_path = Path(__file__).resolve().parent / 'settings.ini'  # ищет файл именно в папке с текущим файлом
        self._config.read('settings.ini')

    @classmethod
    def tearDownClass(cls):
        cls._config = None


    # тест Функции 1
    def test_division(self):
        self.assertAlmostEqual(calculate(1, 2, 0.1), 0.5, places=9)
        self.assertAlmostEqual(calculate(1, 1000, 0.001), 0.001, places=9)
        with self.assertRaises(ZeroDivisionError): # проверка появления исключения деления на 0
            calculate(1, 0, 0.1)

    # проверка диапазона epsilon
    def test_check_epsilon_range(self):
        self.epsilon = float(self._config['DEFAULT']['epsilon'])

        self.assertGreaterEqual(self.epsilon, 10 ** -9)
        self.assertLessEqual(self.epsilon, 10 ** -1)

    # проверка на открытие файла для чтения
    def test_config_file_can_be_opened(self):

        try:
            with open(self.config_path, mode='r') as f:
                self._config.read(f)

        except OSError as e:
            self.fail(f"Не удалось открыть файл на чтение: {e}")

    # проверка на пустой файл
    def test_file_is_empty(self):
        with open(self.config_path, mode='r') as f:
            self._config.read(f)

    # проверка на формат числа (float) из конфига
    def test_epsilon_format_is_number(self):
        raw_value = self._config['DEFAULT']['epsilon'] # Не делаю сразу getfloat, т.к. сначала нужно проверить на пустую строку

        self.assertNotEqual(raw_value.strip(), "", "Значение epsilon пустое") # строка НЕ равна пустой строке

        # проверка на преобразование в float
        try:
            float(raw_value)
        except ValueError:
            self.fail(f"epsilon = {raw_value!r} не является числом")

if __name__ == '__main__':
    unittest.main()
