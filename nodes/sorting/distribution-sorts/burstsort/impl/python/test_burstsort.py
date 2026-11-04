# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burstsort/. The authors are listed in prov/QN966N.jsonl.
import random
import unittest

from burstsort import burstsort


class TestBurstsort(unittest.TestCase):
    def test_page_example(self):
        a = "she sells sea shells by the sea shore".split()
        self.assertEqual(burstsort(a, threshold=2), ["by", "sea", "sea", "sells", "she", "shells", "shore", "the"])

    def test_in_place(self):
        a = ["b", "a"]
        self.assertIs(burstsort(a), a)
        self.assertEqual(a, ["a", "b"])

    def test_edges(self):
        self.assertEqual(burstsort([]), [])
        self.assertEqual(burstsort(["x"]), ["x"])
        self.assertEqual(burstsort(["", "", "a", ""], threshold=1), ["", "", "", "a"])
        self.assertEqual(burstsort(["dup"] * 20, threshold=1), ["dup"] * 20)
        self.assertEqual(burstsort(["ab", "b", "abc", "a", "ba"], threshold=1), ["a", "ab", "abc", "b", "ba"])
        with self.assertRaises(ValueError):
            burstsort(["a"], threshold=0)
        with self.assertRaises(ValueError):
            burstsort(["Ā"])

    def test_long_common_prefix(self):
        p = "u" * 300
        a = [p + c for c in "zyxwvutsrq"] + [p]
        self.assertEqual(burstsort(list(a), threshold=2), sorted(a))

    def test_random(self):
        rng = random.Random(2003)
        for _ in range(600):
            n = rng.randint(0, 60)
            k = rng.choice([1, 2, 3, 26])
            a = ["".join(chr(97 + rng.randrange(k)) for _ in range(rng.randint(0, 6))) for _ in range(n)]
            t = rng.choice([1, 2, 4, 64])
            self.assertEqual(burstsort(list(a), threshold=t, seed=rng.randrange(1000)), sorted(a))


if __name__ == "__main__":
    unittest.main()
