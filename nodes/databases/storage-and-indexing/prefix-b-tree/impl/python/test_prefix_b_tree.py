# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefix-b-tree/. The authors are listed in prov/AJZDXP.jsonl.

import itertools
import random
import unittest

from prefix_b_tree import PrefixBTree, common_prefix, shortest_separator


def all_strings(alphabet, max_len):
    out = [""]
    for n in range(1, max_len + 1):
        out.extend("".join(t) for t in itertools.product(alphabet, repeat=n))
    return out


def random_key(rng, alphabet="abc", max_len=6):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(1, max_len)))


class TestShortestSeparator(unittest.TestCase):
    def test_against_brute_force(self):
        strings = sorted(set(all_strings("abc", 3)))
        candidates = all_strings("abc", 4)
        for a in strings:
            for b in strings:
                if not a < b:
                    continue
                s = shortest_separator(a, b)
                self.assertTrue(a < s <= b)
                best = min(len(t) for t in candidates if a < t <= b)
                self.assertEqual(len(s), best)

    def test_examples(self):
        self.assertEqual(shortest_separator("Smith", "Smyth"), "Smy")
        self.assertEqual(shortest_separator("cat", "catalog"), "cata")
        self.assertEqual(shortest_separator("apple", "banana"), "b")
        with self.assertRaises(ValueError):
            shortest_separator("b", "a")

    def test_common_prefix_is_shared_by_the_interval(self):
        strings = all_strings("ab", 4)
        for low in strings:
            for high in strings:
                if not low < high:
                    continue
                p = common_prefix(low, high)
                for k in strings:
                    if low <= k < high:
                        self.assertTrue(k.startswith(p))


class TestPrefixBTree(unittest.TestCase):
    def test_against_a_sorted_set(self):
        for seed in range(12):
            rng = random.Random(seed)
            t = PrefixBTree(capacity=rng.choice([3, 4, 5, 8]), d=rng.choice([0, 1, 2]))
            ref = set()
            for _ in range(rng.randint(1, 200)):
                k = random_key(rng)
                self.assertEqual(t.insert(k), k not in ref)
                ref.add(k)
            t.check()
            self.assertEqual(t.keys(), sorted(ref))
            for _ in range(60):
                k = random_key(rng)
                self.assertEqual(t.contains(k), k in ref)
            for _ in range(30):
                lo, hi = sorted([random_key(rng), random_key(rng)])
                self.assertEqual(t.range(lo, hi), sorted(x for x in ref if lo <= x <= hi))

    def test_sorted_and_reverse_inserts(self):
        keys = sorted(set(all_strings("abcd", 3)) - {""})
        for order in (keys, keys[::-1]):
            t = PrefixBTree(capacity=4, d=1)
            for k in order:
                t.insert(k)
            t.check()
            self.assertEqual(t.keys(), keys)
            self.assertTrue(all(t.contains(k) for k in keys))
            self.assertFalse(t.contains("e"))

    def test_prefix_truncation_saves_characters(self):
        rng = random.Random(7)
        t = PrefixBTree(capacity=4, d=1)
        for _ in range(200):
            t.insert("customer-" + random_key(rng, "abcdef", 5))
        t.check()
        stored, full = t.stored_chars()
        self.assertLess(stored, full)

    def test_split_interval_shortens_separators(self):
        keys = ["aaaa", "aaab", "aaac", "aaad", "b"]
        mid = PrefixBTree(capacity=4, d=0)
        wide = PrefixBTree(capacity=4, d=1)
        for k in keys:
            mid.insert(k)
            wide.insert(k)
        self.assertEqual(mid.root.full_keys(), ["aaad"])
        self.assertEqual(wide.root.full_keys(), ["b"])
        mid.check()
        wide.check()

    def test_hand_cases(self):
        t = PrefixBTree(capacity=3)
        self.assertFalse(t.contains("a"))
        self.assertEqual(t.range("a", "z"), [])
        self.assertTrue(t.insert("a"))
        self.assertFalse(t.insert("a"))
        with self.assertRaises(TypeError):
            t.insert(3)
        with self.assertRaises(ValueError):
            PrefixBTree(capacity=2)


if __name__ == "__main__":
    unittest.main()
