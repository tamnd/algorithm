# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ehrlich-loopless-combinations/. The authors are listed in prov/3PVRP2.jsonl.

import itertools
import math
import random

from ehrlich_loopless_combinations import revolving_door, revolving_door_rank


def gray_reference(n: int, k: int) -> list[tuple[int, ...]]:
    """The weight-k words of the binary reflected Gray code, as decreasing tuples."""
    out = []
    for r in range(1 << n):
        g = r ^ (r >> 1)
        if bin(g).count("1") == k:
            out.append(tuple(j for j in range(n - 1, -1, -1) if g >> j & 1))
    return out


def key(c: tuple[int, ...]) -> tuple[int, ...]:
    """Sort key of the revolving door order: c_k, -c_(k-1), c_(k-2), ..."""
    return tuple(v if p % 2 == 0 else -v for p, v in enumerate(c))


def test_example() -> None:
    assert list(revolving_door(5, 3)) == [
        (2, 1, 0), (3, 2, 0), (3, 2, 1), (3, 1, 0), (4, 3, 0),
        (4, 3, 1), (4, 3, 2), (4, 2, 0), (4, 2, 1), (4, 1, 0),
    ]
    tests: list[int] = []
    got = list(revolving_door(6, 4, tests))
    assert [int("".join(map(str, c))) for c in got] == [
        3210, 4310, 4321, 4320, 4210, 5410, 5421, 5420,
        5432, 5431, 5430, 5310, 5321, 5320, 5210,
    ]
    assert tests == [1, 1, 0, 2, 3, 1, 0, 1, 0, 0, 2, 1, 0, 2, 3]


def test_edges() -> None:
    assert list(revolving_door(0, 0)) == [()]
    assert list(revolving_door(4, 0)) == [()]
    assert list(revolving_door(4, 4)) == [(3, 2, 1, 0)]
    assert list(revolving_door(3, 4)) == []
    assert list(revolving_door(4, -1)) == []
    assert list(revolving_door(4, 1)) == [(0,), (1,), (2,), (3,)]
    assert list(revolving_door(3, 2)) == [(1, 0), (2, 1), (2, 0)]


def test_order_and_cover() -> None:
    for n in range(0, 12):
        for k in range(0, n + 1):
            got = list(revolving_door(n, k))
            assert got == gray_reference(n, k)
            assert got == sorted(got, key=key)
            assert len(got) == math.comb(n, k)
            want = {tuple(sorted(s, reverse=True)) for s in itertools.combinations(range(n), k)}
            assert set(got) == want


def test_revolving_door_and_cycle() -> None:
    for n in range(2, 12):
        for k in range(1, n):
            got = [set(c) for c in revolving_door(n, k)]
            for a, b in zip(got, got[1:] + got[:1]):
                assert len(a - b) == 1 and len(b - a) == 1


def test_rank() -> None:
    for n in range(0, 11):
        for k in range(0, n + 1):
            got = list(revolving_door(n, k))
            assert [revolving_door_rank(c) for c in got] == list(range(len(got)))


def test_loopless_bound() -> None:
    for n in range(3, 16):
        for k in range(2, n):
            tests: list[int] = []
            count = sum(1 for _ in revolving_door(n, k, tests))
            assert count == math.comb(n, k)
            assert len(tests) == count
            assert max(tests) <= 4
    tests = []
    assert sum(1 for _ in revolving_door(20, 10, tests)) == 184756
    assert max(tests) <= 4


def test_random_rank() -> None:
    rng = random.Random(1979)
    for _ in range(200):
        n = rng.randint(2, 14)
        k = rng.randint(1, n - 1)
        got = list(revolving_door(n, k))
        r = rng.randrange(len(got))
        assert revolving_door_rank(got[r]) == r
