# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eytzinger-layout/. The authors are listed in prov/Q8TG36.jsonl.

import bisect
import random

from eytzinger_layout import Eytzinger, eytzinger_layout

A = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


def test_page_example() -> None:
    e = Eytzinger(A)
    e.check_invariant()
    assert eytzinger_layout(A) == [14, 8, 18, 4, 12, 16, 20, 2, 6, 10]
    assert e.rank[1:] == [6, 3, 8, 1, 5, 7, 9, 0, 2, 4]
    assert e.lower_bound_slot(13) == 1 and e.lower_bound(13) == 6
    assert e.lower_bound_slot(21) == 0 and e.lower_bound(21) == 10
    assert e.lower_bound_slot(1) == 8 and e.lower_bound(1) == 0
    assert e.lower_bound_slot(20) == 7 and e.lower_bound(20) == 9
    assert e.find(14) == 6 and e.find(13) == -1
    assert list(e) == A


def test_edges() -> None:
    e: Eytzinger[int] = Eytzinger([])
    e.check_invariant()
    assert len(e) == 0
    assert e.lower_bound_slot(5) == 0 and e.lower_bound(5) == 0
    assert e.find(5) == -1
    one = Eytzinger([7])
    one.check_invariant()
    assert one.lower_bound(6) == 0 and one.lower_bound(7) == 0 and one.lower_bound(8) == 1
    assert one.find(7) == 0 and 7 in one and 8 not in one
    same = Eytzinger([3] * 9)
    same.check_invariant()
    assert same.find(3) == 0 and same.lower_bound(4) == 9


def test_every_size_and_key() -> None:
    for n in range(0, 70):
        a = list(range(0, 2 * n, 2))
        e = Eytzinger(a)
        e.check_invariant()
        for v in range(-1, 2 * n + 1):
            assert e.lower_bound(v) == bisect.bisect_left(a, v)


def test_comparison_count() -> None:
    class Key:
        count = 0

        def __init__(self, v: int) -> None:
            self.v = v

        def __lt__(self, other: "Key") -> bool:
            Key.count += 1
            return self.v < other.v

    for n in range(1, 140):
        e = Eytzinger([Key(2 * i) for i in range(n)])
        lo, hi = (n + 1).bit_length() - 1, n.bit_length()
        for v in range(-1, 2 * n + 1):
            Key.count = 0
            e.lower_bound_slot(Key(v))
            assert lo <= Key.count <= hi


def test_random_ops_against_bisect() -> None:
    rng = random.Random(5150)
    for _ in range(600):
        a = sorted(rng.randint(-10, 10) for _ in range(rng.randint(0, 50)))
        e = Eytzinger(a)
        e.check_invariant()
        assert list(e) == a
        for _ in range(10):
            x = rng.randint(-12, 12)
            i = bisect.bisect_left(a, x)
            assert e.lower_bound(x) == i
            assert e.find(x) == (i if i < len(a) and a[i] == x else -1)
            assert (x in e) == (x in a)


def test_strings() -> None:
    words = ["ant", "bee", "cat", "dog", "eel", "fox", "gnu"]
    e = Eytzinger(words)
    e.check_invariant()
    assert eytzinger_layout(words) == ["dog", "bee", "fox", "ant", "cat", "eel", "gnu"]
    assert e.find("eel") == 4 and e.find("elk") == -1
