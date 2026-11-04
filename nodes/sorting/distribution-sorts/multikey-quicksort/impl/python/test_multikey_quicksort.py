# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multikey-quicksort/. The authors are listed in prov/36KMJW.jsonl.
import random
import unittest

from multikey_quicksort import multikey_quicksort


class TestMultikeyQuicksort(unittest.TestCase):
    def test_page_example(self):
        a = "she sells sea shells by the sea shore".split()
        self.assertEqual(
            multikey_quicksort(a, seed=1),
            ["by", "sea", "sea", "sells", "she", "shells", "shore", "the"],
        )

    def test_in_place(self):
        a = ["b", "a"]
        r = multikey_quicksort(a)
        self.assertIs(r, a)
        self.assertEqual(a, ["a", "b"])

    def test_edges(self):
        self.assertEqual(multikey_quicksort([]), [])
        self.assertEqual(multikey_quicksort(["x"]), ["x"])
        self.assertEqual(multikey_quicksort(["", "a", ""]), ["", "", "a"])
        self.assertEqual(multikey_quicksort(["ab", "a", "abc", "b"]), ["a", "ab", "abc", "b"])
        self.assertEqual(multikey_quicksort(["aaa"] * 5), ["aaa"] * 5)

    def test_unicode(self):
        a = ["été", "zebra", "中文", "apple", "é"]
        self.assertEqual(multikey_quicksort(a), sorted(a))

    def test_long_common_prefix(self):
        p = "x" * 5000
        a = [p + "b", p, p + "a", p + "ab"]
        self.assertEqual(multikey_quicksort(a), sorted(a))

    def test_random(self):
        rng = random.Random(36)
        for _ in range(600):
            n = rng.randint(0, 40)
            k = rng.choice([1, 2, 3, 26])
            a = ["".join(chr(97 + rng.randrange(k)) for _ in range(rng.randint(0, 6))) for _ in range(n)]
            self.assertEqual(multikey_quicksort(list(a), seed=rng.randrange(10**6)), sorted(a))


if __name__ == "__main__":
    unittest.main()
