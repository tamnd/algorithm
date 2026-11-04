# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/introsort/. The authors are listed in prov/S172EG.jsonl.

import itertools
import random

import introsort as module
from introsort import hoare_partition, introsort


class Key:
    def __init__(self, k: int, tag: int) -> None:
        self.k, self.tag = k, tag

    def __lt__(self, other: "Key") -> bool:
        return self.k < other.k


EXAMPLE = [13, 2, 19, 7, 5, 17, 11, 3, 20, 1, 15, 9, 6, 18, 4, 12, 16, 8, 14, 10]


def test_example() -> None:
    a = list(EXAMPLE)
    introsort(a)
    assert a == list(range(1, 21))


def test_example_partition() -> None:
    a = list(EXAMPLE)
    j = hoare_partition(a, 0, 19)
    assert j == 11
    assert a == [10, 2, 8, 7, 5, 12, 11, 3, 4, 1, 6, 9, 15, 18, 20, 17, 16, 19, 14, 13]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [2**63 - 1, 0, -(2**63), 2**63 - 1]):
        b = list(a)
        introsort(b)
        assert b == sorted(a)


def test_patterns() -> None:
    n = 3000
    for a in (list(range(n)), list(range(n, 0, -1)), [7] * n, [i % 3 for i in range(n)], list(range(n // 2)) + list(range(n // 2, 0, -1))):
        b = list(a)
        introsort(b)
        assert b == sorted(a)


def test_all_permutations_of_small_and_cutoff_sizes() -> None:
    for n in range(7):
        for p in itertools.permutations(range(n)):
            b = list(p)
            introsort(b)
            assert b == list(range(n))
    rng = random.Random(16)
    for n in (16, 17, 18, 33, 34):
        for _ in range(50):
            a = [rng.randint(0, 5) for _ in range(n)]
            b = list(a)
            introsort(b)
            assert b == sorted(a)


def test_heapsort_fallback_on_killer_input() -> None:
    # McIlroy's adversary against median-of-3 quicksort, run lazily.
    n = 600
    val: list[int | None] = [None] * n
    state = {"solid": 0, "cand": -1}

    class Gas:
        def __init__(self, i: int) -> None:
            self.i = i

        def __lt__(self, other: "Gas") -> bool:
            x, y = self.i, other.i
            if val[x] is None and val[y] is None:
                z = x if x == state["cand"] else y
                val[z] = state["solid"]
                state["solid"] += 1
            if val[x] is None:
                state["cand"] = x
            elif val[y] is None:
                state["cand"] = y
            vx = n if val[x] is None else val[x]
            vy = n if val[y] is None else val[y]
            return vx < vy

    used = []
    original = module._heapsort

    def counting_heapsort(a: list, lo: int, hi: int) -> None:
        used.append(hi - lo)
        original(a, lo, hi)

    module._heapsort = counting_heapsort
    try:
        g = [Gas(i) for i in range(n)]
        introsort(g)
    finally:
        module._heapsort = original
    assert all(not g[i + 1] < g[i] for i in range(n - 1))
    assert sum(used) > n // 2


def test_not_stable() -> None:
    v = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1]
    a = [Key(k, i) for i, k in enumerate(v)]
    introsort(a)
    assert [e.k for e in a] == sorted(v)
    assert [e.tag for e in a] == [15, 14, 13, 9, 0, 5, 4, 1, 8, 6, 7, 3, 10, 11, 12, 2, 16]


def test_random_against_sorted() -> None:
    rng = random.Random(1997)
    for _ in range(600):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 120))]
        b = list(a)
        introsort(b)
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"] * 5
    introsort(a)
    assert a == sorted(["pear", "fig", "apple", "fig", "kiwi"] * 5)
