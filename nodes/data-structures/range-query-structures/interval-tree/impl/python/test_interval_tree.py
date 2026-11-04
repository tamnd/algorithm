# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-tree/. The authors are listed in prov/8H8C9B.jsonl.

import random

import pytest

from interval_tree import IntervalTree

EXAMPLE = [(16, 21), (8, 9), (25, 30), (5, 10), (15, 23), (17, 19), (26, 26), (0, 3), (6, 7), (19, 20)]


def overlaps(iv: tuple[int, int], a: int, b: int) -> bool:
    return iv[0] <= b and a <= iv[1]


def test_example() -> None:
    t = IntervalTree(seed=1)
    for lo, hi in EXAMPLE:
        t.insert(lo, hi)
    t.check_invariant()
    assert t.report(22, 25) == [(15, 23), (25, 30)]
    assert t.report(9, 9) == [(5, 10), (8, 9)]
    found = t.search(22, 25)
    assert found in {(15, 23), (25, 30)}
    assert t.search(11, 14) is None
    assert t.report(11, 14) == []
    assert t.root is not None and t.root.max == 30


def test_edges() -> None:
    t = IntervalTree()
    assert t.search(0, 0) is None and t.report(-5, 5) == []
    assert not t.delete(1, 2)
    with pytest.raises(ValueError):
        t.insert(3, 2)
    t.insert(4, 4)
    t.insert(4, 4)
    t.insert(4, 9)
    assert t.report(4, 4) == [(4, 4), (4, 4), (4, 9)]
    assert t.report(5, 5) == [(4, 9)]
    assert t.delete(4, 4)
    assert t.report(0, 10) == [(4, 4), (4, 9)]
    assert t.delete(4, 4) and not t.delete(4, 4)
    assert t.report(0, 10) == [(4, 9)]
    t.check_invariant()
    sorted_tree = IntervalTree()
    for i in range(2000):
        sorted_tree.insert(i, i + 1)
    assert sorted_tree.report(999, 999) == [(998, 999), (999, 1000)]
    sorted_tree.check_invariant()


def test_random_against_brute_force() -> None:
    rng = random.Random(4242)
    for trial in range(500):
        t = IntervalTree(seed=trial)
        bag: list[tuple[int, int]] = []
        for _ in range(rng.randint(0, 40)):
            r = rng.random()
            if r < 0.45:
                lo = rng.randint(-20, 20)
                hi = lo + rng.randint(0, 10)
                t.insert(lo, hi)
                bag.append((lo, hi))
            elif r < 0.6:
                if bag and rng.random() < 0.8:
                    iv = rng.choice(bag)
                else:
                    iv = (rng.randint(-20, 20), rng.randint(20, 30))
                expected = iv in bag
                assert t.delete(*iv) == expected
                if expected:
                    bag.remove(iv)
            else:
                a = rng.randint(-25, 25)
                b = a + rng.randint(0, 8)
                want = sorted(iv for iv in bag if overlaps(iv, a, b))
                assert t.report(a, b) == want
                got = t.search(a, b)
                if want:
                    assert got is not None and overlaps(got, a, b) and got in bag
                else:
                    assert got is None
        t.check_invariant()
