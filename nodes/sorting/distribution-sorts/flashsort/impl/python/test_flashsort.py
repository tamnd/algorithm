# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flashsort/. The authors are listed in prov/GEP1AZ.jsonl.
import random
import unittest

from flashsort import class_map, flashsort


class TestFlashsort(unittest.TestCase):
    def test_page_example(self):
        a = [42, 7, 93, 18, 65, 30, 7, 88, 51, 24]
        k = class_map(a, 7, 93, 4)
        self.assertEqual([k(x) for x in a], [1, 0, 3, 0, 2, 0, 0, 2, 1, 0])
        flashsort(a, m=4)
        self.assertEqual(a, [7, 7, 18, 24, 30, 42, 51, 65, 88, 93])

    def test_edges(self):
        for a in ([], [1], [2, 1], [5, 5, 5], [0, -5, 3, -1, -5, 2], [2**63 - 1, -(2**63), 0, -1, 1]):
            b = list(a)
            flashsort(b)
            self.assertEqual(b, sorted(a))

    def test_floats_and_mixed(self):
        a = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68, 1e308, -1e308]
        b = list(a)
        flashsort(b)
        self.assertEqual(b, sorted(a))
        c = [3, 1.5, -2, 0.25]
        flashsort(c)
        self.assertEqual(c, [-2, 0.25, 1.5, 3])

    def test_strings(self):
        for a in (["pear", "fig", "apple"], ["b", "", "a", "ab", ""], ["same"] * 5, ["xxxxxxb", "xxxxxxa", "xxxxxx"]):
            b = list(a)
            flashsort(b)
            self.assertEqual(b, sorted(a))

    def test_skewed(self):
        a = [10**9] + list(range(300, 0, -1))
        flashsort(a)
        self.assertEqual(a, sorted(a))

    def test_bad_m(self):
        with self.assertRaises(ValueError):
            flashsort([2, 1], m=1)

    def test_random(self):
        rng = random.Random(1998)
        for _ in range(600):
            n = rng.randint(0, 80)
            kind = rng.randrange(3)
            if kind == 0:
                a = [rng.randint(-1000, 1000) for _ in range(n)]
            elif kind == 1:
                a = [rng.random() for _ in range(n)]
            else:
                a = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 5))) for _ in range(n)]
            b = list(a)
            flashsort(b, m=rng.choice([None, 2, 3, 50]))
            self.assertEqual(b, sorted(a))


if __name__ == "__main__":
    unittest.main()
