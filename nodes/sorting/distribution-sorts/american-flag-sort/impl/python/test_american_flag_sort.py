# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/american-flag-sort/. The authors are listed in prov/GW15GA.jsonl.
import random
import unittest

from american_flag_sort import american_flag_sort


class TestAmericanFlagSort(unittest.TestCase):
    def test_page_example(self):
        a = "she sells sea shells by the sea shore".split()
        self.assertEqual(american_flag_sort(a), ["by", "sea", "sea", "sells", "she", "shells", "shore", "the"])

    def test_in_place(self):
        a = ["c", "a", "b"]
        self.assertIs(american_flag_sort(a), a)
        self.assertEqual(a, ["a", "b", "c"])

    def test_edges(self):
        self.assertEqual(american_flag_sort([]), [])
        self.assertEqual(american_flag_sort(["only"]), ["only"])
        self.assertEqual(american_flag_sort(["", "b", "", "a"]), ["", "", "a", "b"])
        self.assertEqual(american_flag_sort(["ab", "b", "abc", "a", "ba"]), ["a", "ab", "abc", "b", "ba"])
        self.assertEqual(american_flag_sort(["same"] * 9), ["same"] * 9)
        with self.assertRaises(ValueError):
            american_flag_sort(["Ā"])

    def test_small_alphabet(self):
        a = ["10", "0", "1", "01", "", "00"]
        self.assertEqual(american_flag_sort(list(a), r=50), sorted(a))

    def test_long_common_prefix(self):
        p = "k" * 4000
        a = [p + "z", p + "a", p, p + "m"]
        self.assertEqual(american_flag_sort(a), sorted(a))

    def test_random(self):
        rng = random.Random(1993)
        for _ in range(600):
            n = rng.randint(0, 50)
            k = rng.choice([1, 2, 5, 26])
            a = ["".join(chr(97 + rng.randrange(k)) for _ in range(rng.randint(0, 6))) for _ in range(n)]
            self.assertEqual(american_flag_sort(list(a)), sorted(a))


if __name__ == "__main__":
    unittest.main()
