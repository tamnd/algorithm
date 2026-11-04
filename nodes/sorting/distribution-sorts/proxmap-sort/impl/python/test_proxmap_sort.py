# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proxmap-sort/. The authors are listed in prov/QTZM0Z.jsonl.
import math
import random
import unittest

from proxmap_sort import proxmap_sort


class TestProxmapSort(unittest.TestCase):
    def test_page_example(self):
        a = [3.4, 0.9, 5.2, 3.1, 7.7, 0.2, 5.9, 3.8, 2.5, 6.0]
        proxmap_sort(a, m=8, key_map=math.floor)
        self.assertEqual(a, [0.2, 0.9, 2.5, 3.1, 3.4, 3.8, 5.2, 5.9, 6.0, 7.7])

    def test_default_map(self):
        a = [3.4, 0.9, 5.2, 3.1, 7.7, 0.2, 5.9, 3.8, 2.5, 6.0]
        b = list(a)
        proxmap_sort(b)
        self.assertEqual(b, sorted(a))

    def test_edges(self):
        for a in ([], [1], [2, 1], [4, 4, 4], [0, -5, 3, -1, -5, 2], [2**63 - 1, -(2**63), 0, 2**63 - 1]):
            b = list(a)
            proxmap_sort(b)
            self.assertEqual(b, sorted(a))
        with self.assertRaises(ValueError):
            proxmap_sort([2, 1], m=0)

    def test_strings(self):
        for a in (["pear", "fig", "apple"], ["b", "", "a", "ab", ""], ["same"] * 4, ["zzzzzzb", "zzzzzz", "zzzzzza"]):
            b = list(a)
            proxmap_sort(b)
            self.assertEqual(b, sorted(a))

    def test_stable(self):
        a = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
        keys = [p[0] for p in a]
        order = list(range(len(a)))
        # sort indices by key with a map on the key value; ties keep input order
        idx = [k * 10 + i for i, k in enumerate(keys)]
        proxmap_sort(idx, m=3, key_map=lambda v: v // 10)
        self.assertEqual([order[v % 10] for v in idx], [1, 3, 0, 2])

    def test_one_subarray(self):
        a = list(range(200, 0, -1))
        proxmap_sort(a, m=1)
        self.assertEqual(a, list(range(1, 201)))

    def test_random(self):
        rng = random.Random(1998)
        for _ in range(600):
            n = rng.randint(0, 80)
            kind = rng.randrange(3)
            if kind == 0:
                a = [rng.randint(-50, 50) for _ in range(n)]
            elif kind == 1:
                a = [rng.random() * 100 for _ in range(n)]
            else:
                a = ["".join(rng.choice("xyz") for _ in range(rng.randint(0, 4))) for _ in range(n)]
            b = list(a)
            proxmap_sort(b, m=rng.choice([None, 1, 2, 7]))
            self.assertEqual(b, sorted(a))


if __name__ == "__main__":
    unittest.main()
