from Lab_5 import load_params, calculate
import unittest
import configparser
from pathlib import Path

class TestMath(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import configparser
        cls._config = configparser.ConfigParser()

        cls._config.read('settings.ini')
        cls._epsilon = float(cls._config['DEFAULT']['epsilon'])


    def test_division(self):
        self.assertAlmostEqual(calculate(1, 2, 0.1), 0.5, places=9)
        self.assertAlmostEqual(calculate(1, 1000, 0.001), 0.001, places=9)
        with self.assertRaises(ZeroDivisionError):
            calculate(1, 0, 0.1)

    def test_check_epsilon_range(self):
        self.epsilon = float(self._config['DEFAULT']['epsilon'])

        self.assertGreaterEqual(self.epsilon, 10 ** -9)
        self.assertLessEqual(self.epsilon, 10 ** -1)

    def test_config_file_can_be_opened(self):
        config_path = Path(__file__).resolve().parent / 'settings.ini'
        self.assertTrue(config_path.is_file(), f"Файл не найден: {config_path}") # файл существует и это именно файл

        try: # файл можно открыть на чтение
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except OSError as e:
            self.fail(f"Не удалось открыть файл на чтение: {e}")

        self.assertGreater(len(content), 0, "Файл пустой")

    def test_epsilon_format_is_number(self):
        raw_value = self._config['DEFAULT']['epsilon']

        self.assertNotEqual(raw_value.strip(), "", "Значение epsilon пустое") # строка не пустая

        try: # преобразуется в float без ошибок
            parsed = float(raw_value)
        except ValueError:
            self.fail(f"epsilon = {raw_value!r} не является числом")

    @classmethod
    def tearDownClass(cls):
        cls._config = None