# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-way-radix-quicksort/. The authors are listed in prov/PC1TJR.jsonl.
import random
import unittest

from three_way_radix_quicksort import three_way_radix_quicksort


class TestThreeWayRadixQuicksort(unittest.TestCase):
    def test_page_example(self):
        a = ["cab", "add", "dad", "bad", "cad", "ace", "ad"]
        want = ["ace", "ad", "add", "bad", "cab", "cad", "dad"]
        self.assertEqual(three_way_radix_quicksort(list(a), cutoff=1, shuffle=False), want)
        self.assertEqual(three_way_radix_quicksort(list(a)), want)

    def test_in_place(self):
        a = ["b", "a", "c"]
        self.assertIs(three_way_radix_quicksort(a, cutoff=1), a)
        self.assertEqual(a, ["a", "b", "c"])

    def test_edges(self):
        self.assertEqual(three_way_radix_quicksort([]), [])
        self.assertEqual(three_way_radix_quicksort([""]), [""])
        self.assertEqual(three_way_radix_quicksort(["", "a", ""], cutoff=1), ["", "", "a"])
        self.assertEqual(three_way_radix_quicksort(["ab", "b", "abc", "a", "ba"], cutoff=1), ["a", "ab", "abc", "b", "ba"])
        self.assertEqual(three_way_radix_quicksort(["zz"] * 40, cutoff=1), ["zz"] * 40)
        with self.assertRaises(ValueError):
            three_way_radix_quicksort(["a"], cutoff=0)

    def test_long_common_prefix(self):
        p = "q" * 5000
        a = [p + "c", p, p + "a", p + "ab", p + "b"]
        self.assertEqual(three_way_radix_quicksort(a, cutoff=1), sorted(a))

    def test_unicode(self):
        a = ["ñu", "nu", "中", "", "Zeta", "zeta"]
        self.assertEqual(three_way_radix_quicksort(list(a), cutoff=1), sorted(a))

    def test_random(self):
        rng = random.Random(1997)
        for _ in range(600):
            n = rng.randint(0, 60)
            k = rng.choice([1, 2, 4, 26])
            a = ["".join(chr(97 + rng.randrange(k)) for _ in range(rng.randint(0, 7))) for _ in range(n)]
            m = rng.choice([1, 2, 15])
            self.assertEqual(three_way_radix_quicksort(list(a), cutoff=m, seed=rng.randrange(10**6)), sorted(a))


if __name__ == "__main__":
    unittest.main()
