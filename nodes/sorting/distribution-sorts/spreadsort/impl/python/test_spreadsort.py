# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spreadsort/. The authors are listed in prov/ER6NF4.jsonl.
import random
import unittest

from spreadsort import integer_key, spreadsort


class TestSpreadsort(unittest.TestCase):
    def test_page_example(self):
        a = [37, 12, 58, 3, 45, 21, 60, 9, 33, 50]
        self.assertEqual([(x - 3) >> 3 for x in a], [4, 1, 6, 0, 5, 2, 7, 0, 3, 5])
        spreadsort(a, small=4, log_bin=0)
        self.assertEqual(a, [3, 9, 12, 21, 33, 37, 45, 50, 58, 60])

    def test_edges(self):
        for a in ([], [1], [2, 1], [5, 5, 5], [0, -5, 3, -1, -5, 2], [2**63 - 1, -(2**63), 0, -1, 1]):
            b = list(a)
            spreadsort(b, small=2, log_bin=0)
            self.assertEqual(b, sorted(a))

    def test_key_map_order(self):
        for a in (["b", "", "a", "ab", "ba"], [-1.5, 0.0, 2.25, -1e308, 1e308]):
            f, _ = integer_key(a)
            self.assertEqual(sorted(a, key=f), sorted(a))

    def test_floats_and_mixed(self):
        a = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68, 1e308, -1e308] * 3
        b = list(a)
        spreadsort(b)
        self.assertEqual(b, sorted(a))
        c = [3, 1.5, -2, 0.25, 2**63, 2**63 - 1] * 5
        d = list(c)
        spreadsort(d, small=2)
        self.assertEqual(d, sorted(c))

    def test_strings(self):
        for a in (["pear", "fig", "apple"] * 9, ["b", "", "a", "ab", ""] * 7, ["same"] * 40, ["xxxxxxb", "xxxxxxa", "xxxxxx"] * 8):
            b = list(a)
            spreadsort(b, small=2)
            self.assertEqual(b, sorted(a))

    def test_skewed_and_patterns(self):
        for a in ([10**18] + list(range(500, 0, -1)), [i % 7 for i in range(400)], [2**k for k in range(62)] * 3):
            b = list(a)
            spreadsort(b)
            self.assertEqual(b, sorted(a))

    def test_random(self):
        rng = random.Random(2002)
        for _ in range(600):
            n = rng.randint(0, 120)
            kind = rng.randrange(4)
            if kind == 0:
                a = [rng.randint(-1000, 1000) for _ in range(n)]
            elif kind == 1:
                a = [rng.random() for _ in range(n)]
            elif kind == 2:
                a = [rng.randint(-(2**63), 2**63 - 1) for _ in range(n)]
            else:
                a = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 5))) for _ in range(n)]
            b = list(a)
            spreadsort(b, small=rng.choice([2, 4, 16]), log_bin=rng.choice([0, 2]))
            self.assertEqual(b, sorted(a))


if __name__ == "__main__":
    unittest.main()
