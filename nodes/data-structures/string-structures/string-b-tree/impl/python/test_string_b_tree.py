# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-b-tree/. The authors are listed in prov/EZGPK7.jsonl.

import bisect
import random

import pytest

from string_b_tree import StringBTree

WORDS = ["abaa", "abab", "abba", "abbb", "abc", "bab", "baba", "bb", "bbaa", "bbab", "c", "caa"]


def test_example() -> None:
    t = StringBTree(4)
    for w in WORDS:
        assert t.insert(w)
        t.check_invariant()
    assert t.height() == 3 and t.sorted_strings() == sorted(WORDS)
    assert not t.insert("abc")
    assert t.with_prefix("ab") == ["abaa", "abab", "abba", "abbb", "abc"]
    assert t.with_prefix("bab") == ["bab", "baba"]
    assert t.with_prefix("bba") == ["bbaa", "bbab"]
    assert t.with_prefix("d") == [] and t.prefix_range("d") == (12, 12)
    assert t.contains("bb") and not t.contains("ba")
    t.chars_read = 0
    t.prefix_range("bbab")
    assert t.chars_read <= 2 * (len("bbab") + 1 + t.height() + 1)


def test_edges() -> None:
    t = StringBTree(4)
    assert t.prefix_range("a") == (0, 0) and not t.contains("")
    assert t.insert("")
    t.check_invariant()
    assert t.contains("") and t.with_prefix("") == [""]
    assert t.insert("a") and t.insert("aa") and t.insert("aaa")
    t.check_invariant()
    assert t.with_prefix("a") == ["a", "aa", "aaa"]
    with pytest.raises(ValueError):
        t.insert("\U0010ffff")
    with pytest.raises(ValueError):
        StringBTree(3)


def test_random_against_sorted_list() -> None:
    rng = random.Random(1999)
    for case in range(500):
        b = rng.choice([4, 5, 8])
        t = StringBTree(b)
        model: list[str] = []
        for _ in range(rng.randint(0, 60)):
            w = "".join(rng.choice("ab" if case % 2 else "abc") for _ in range(rng.randint(0, 6)))
            new = w not in model
            assert t.insert(w) == new
            if new:
                bisect.insort(model, w)
        t.check_invariant()
        assert t.sorted_strings() == model
        for _ in range(8):
            p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
            want = [w for w in model if w.startswith(p)]
            lo = bisect.bisect_left(model, p)
            assert t.prefix_range(p) == (lo, lo + len(want))
            assert t.contains(p) == (p in model)
            # the lcp carried down the tree bounds the symbols read by one search
            t.chars_read = 0
            t._rank(p)
            assert t.chars_read <= len(p) + t.height()
