# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-exchange-sort/. The authors are listed in prov/Y3DQBZ.jsonl.
import random
import unittest

from radix_exchange_sort import radix_exchange_sort


class TestRadixExchangeSort(unittest.TestCase):
    def test_page_example(self):
        a = [5, 2, 7, 1, 4, 6, 0, 3]
        self.assertEqual(radix_exchange_sort(a, w=3), [0, 1, 2, 3, 4, 5, 6, 7])

    def test_in_place(self):
        a = [3, 1, 2]
        self.assertIs(radix_exchange_sort(a), a)
        self.assertEqual(a, [1, 2, 3])

    def test_edges(self):
        self.assertEqual(radix_exchange_sort([]), [])
        self.assertEqual(radix_exchange_sort([0]), [0])
        self.assertEqual(radix_exchange_sort([0, 0, 0]), [0, 0, 0])
        self.assertEqual(radix_exchange_sort([9] * 7), [9] * 7)
        self.assertEqual(radix_exchange_sort([2**64 - 1, 0, 2**63]), [0, 2**63, 2**64 - 1])
        self.assertEqual(radix_exchange_sort(list(range(50, 0, -1))), list(range(1, 51)))
        with self.assertRaises(ValueError):
            radix_exchange_sort([-1, 2])
        with self.assertRaises(ValueError):
            radix_exchange_sort([8], w=3)

    def test_random(self):
        rng = random.Random(1959)
        for _ in range(700):
            n = rng.randint(0, 60)
            hi = rng.choice([1, 2, 16, 1000, 2**32, 2**64])
            a = [rng.randrange(hi) for _ in range(n)]
            self.assertEqual(radix_exchange_sort(list(a)), sorted(a))


if __name__ == "__main__":
    unittest.main()
