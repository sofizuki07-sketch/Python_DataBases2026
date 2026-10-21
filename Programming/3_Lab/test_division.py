from Lab_5 import calculate
import unittest
import configparser
import os
import tempfile

class TestBase(unittest.TestCase):
    """ Тест разворачивает временную директорию, создаёт settings.ini,
    читает epsilon из конфига. В итоге классы TestCalculate и TestLoadParams получат наследование атрибута self.epsilon
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "settings.ini")

        with open(self.path, 'w', encoding='utf-8') as f:
            f.write("[DEFAULT]\nepsilon = 0.0001\n")

        self._config = configparser.ConfigParser()
        self._config.read(self.path, encoding='utf-8')
        self.epsilon = float(self._config['DEFAULT']['epsilon'])

        # Сохраняем "оригинальные" значения по умолчанию
        self.old_kwdefaults = calculate.__kwdefaults__

    def tearDown(self):
        calculate.__kwdefaults__ = self.old_kwdefaults
        self.tmp.cleanup()


class TestCalculate(TestBase):
    def test_division1(self):
        self.assertAlmostEqual(calculate(1, 2, 0.1), 0.5, places=9)

    def test_division2(self):
        self.assertAlmostEqual(calculate(1, 1000, 0.001), 0.001, places=9)

    def test_division_by_zero_raises(self):
        with self.assertLogs('myapp', level='ERROR') as cm:
            with self.assertRaises(ZeroDivisionError): # проверка появления исключения деления на 0
                calculate(1, 0, 0.1)

        self.assertTrue(any("Деление на ноль" in msg for msg in cm.output),
                        f"Ожидалось 'Деление на ноль', получено: {cm.output}")
    def test_with_epsilon_from_config(self):
        result = calculate(10, 3, self.epsilon)
        self.assertAlmostEqual(result, 3.3333, places=4)


class TestLoadParams(TestBase):

    # проверка на открытие файла для чтения
    def test_config_file_can_be_opened(self):
        self.assertTrue(os.path.isfile(self.path), f"A")
        try:
            with open(self.path, mode='r', encoding='utf-8') as f:
                self._config.read_file(f)

        except OSError as e:
            self.fail(f"Не удалось открыть файл на чтение: {e}")

    # проверка на пустой файл
    def test_file_is_empty(self):
        with open(self.path, mode='r') as f:
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
