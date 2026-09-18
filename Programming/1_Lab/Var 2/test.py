from main import two_sum, two_sum_hashed, two_sum_hashed_2, two_sum_all
import unittest

class TestIndex(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(two_sum([1, 2, 3, 4, 5, 6, 7, 8, 9], 8), (0, 6))
        self.assertEqual(two_sum_hashed([1, 2, 3, 4, 5, 6, 7, 8, 9], 8), (0, 6))
        self.assertEqual(two_sum_hashed_2([1, 2, 3, 4, 5, 6, 7, 8, 9], 8), (0, 6))
        self.assertEqual(two_sum_all([1, 2, 3, 4, 5, 6, 7, 8, 9], 8), [(0, 6), (1, 5), (2, 4)])

    def test_empty(self):
        self.assertEqual(two_sum([], 8), None)
        self.assertEqual(two_sum_hashed([], 8), None)
        self.assertEqual(two_sum_hashed_2([], 8), None)
        self.assertEqual(two_sum_all([], 8), None)

    def test_no_answer(self):
        self.assertEqual(two_sum([1, 3, 4, 20, 1], 8), None)
        self.assertEqual(two_sum_hashed([1, 3, 4, 20, 1], 8), None)
        self.assertEqual(two_sum_hashed_2([1, 3, 4, 20, 1], 8), None)
        self.assertEqual(two_sum_all([1, 3, 4, 20, 1], 8), None)

    def test_equal(self):
        self.assertEqual(two_sum([1, 1, 3, 1, 3], 4), (0, 2))
        self.assertEqual(two_sum_hashed([1, 1, 3, 1, 3], 4), (0, 2))
        self.assertEqual(two_sum_hashed_2([1, 1, 3, 1, 3], 4), (0, 2))
        self.assertEqual(two_sum_all([1, 1, 3, 1, 3], 4),  [(0, 2), (0, 4), (1, 2), (1, 4), (2, 3), (3, 4)])

if __name__ == '__main__':
    unittest.main()

