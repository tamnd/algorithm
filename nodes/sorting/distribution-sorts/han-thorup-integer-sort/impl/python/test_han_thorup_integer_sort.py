# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/han-thorup-integer-sort/. The authors are listed in prov/B8DZ6B.jsonl.
import random
import unittest

from han_thorup_integer_sort import _split, han_thorup_integer_sort


class TestHanThorupIntegerSort(unittest.TestCase):
    def test_page_example(self):
        a = [41, 7, 93, 18, 65, 30, 7, 88, 51, 24, 76, 3, 59, 12, 97, 35]
        parts, equal = _split(a, [18, 51, 88])
        self.assertEqual(parts, [[7, 7, 3, 12], [41, 30, 24, 35], [65, 76, 59], [93, 97]])
        self.assertEqual(equal, [1, 1, 1])
        for seed in range(20):
            self.assertEqual(han_thorup_integer_sort(a, base=4, seed=seed), sorted(a))

    def test_edges(self):
        for a in ([], [1], [2, 1], [5] * 50, [0, -5, 3, -1, -5, 2], [2**63 - 1, -(2**63), 0, -1, 1] * 4):
            self.assertEqual(han_thorup_integer_sort(a, base=2, seed=1), sorted(a))

    def test_patterns(self):
        for a in (list(range(3000)), list(range(3000, 0, -1)), [i % 17 for i in range(3000)], [2**k for k in range(63)] * 5):
            self.assertEqual(han_thorup_integer_sort(a, seed=7), sorted(a))

    def test_bad_base(self):
        with self.assertRaises(ValueError):
            han_thorup_integer_sort([2, 1], base=1)

    def test_random(self):
        rng = random.Random(2002)
        for _ in range(600):
            n = rng.randint(0, 150)
            hi = rng.choice([3, 1000, 2**64])
            a = [rng.randint(-hi, hi) for _ in range(n)]
            got = han_thorup_integer_sort(a, base=rng.choice([2, 4, 8]), seed=rng.randrange(10**6))
            self.assertEqual(got, sorted(a))


if __name__ == "__main__":
    unittest.main()
