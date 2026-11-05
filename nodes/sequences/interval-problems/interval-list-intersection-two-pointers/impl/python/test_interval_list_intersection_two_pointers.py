# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-list-intersection-two-pointers/. The authors are listed in prov/ZRYF9N.jsonl.

import random

from interval_list_intersection_two_pointers import interval_list_intersection_two_pointers as inter


def oracle(a: list[tuple[int, int]], b: list[tuple[int, int]], closed: bool) -> list[tuple[int, int]]:
    """All pairs, then sort: the definition of the output."""
    out = []
    for x, y in a:
        for u, v in b:
            lo, hi = max(x, u), min(y, v)
            if lo < hi or (closed and lo == hi):
                out.append((lo, hi))
    return sorted(out)


def random_list(rng: random.Random, closed: bool) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    pos = rng.randrange(0, 3)
    for _ in range(rng.randrange(0, 6)):
        lo = pos
        hi = lo + rng.randrange(0 if closed else 1, 4)
        out.append((lo, hi))
        pos = hi + (rng.randrange(1, 3) if closed else rng.randrange(0, 3))
    return out


def test_example() -> None:
    a = [(1, 3), (6, 9), (12, 15), (18, 20)]
    b = [(2, 6), (9, 12), (14, 14), (16, 22)]
    assert inter(a, b) == [(2, 3), (6, 6), (9, 9), (12, 12), (14, 14), (18, 20)]
    b2 = [(2, 6), (9, 12), (16, 22)]
    assert inter(a, b2, closed=False) == [(2, 3), (18, 20)]


def test_edges() -> None:
    assert inter([], [(1, 2)]) == []
    assert inter([(1, 2)], []) == []
    assert inter([(1, 2), (5, 6)], [(1, 2), (5, 6)]) == [(1, 2), (5, 6)]
    assert inter([(0, 10)], [(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]
    assert inter([(1, 3)], [(3, 5)]) == [(3, 3)]
    assert inter([(1, 3)], [(3, 5)], closed=False) == []
    assert inter([(0, 4), (6, 10), (12, 16)], [(2, 8), (9, 14)]) == [(2, 4), (6, 8), (9, 10), (12, 14)]
    big = 2**62
    assert inter([(-big, big)], [(0, big)]) == [(0, big)]


def test_against_oracle() -> None:
    rng = random.Random(986)
    for _ in range(1000):
        closed = rng.random() < 0.5
        a, b = random_list(rng, closed), random_list(rng, closed)
        got = inter(a, b, closed)
        assert got == oracle(a, b, closed)
        assert len(got) <= max(0, len(a) + len(b) - 1)
