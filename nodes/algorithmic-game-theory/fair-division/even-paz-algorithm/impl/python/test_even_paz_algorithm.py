# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/even-paz-algorithm/. The authors are listed in prov/E1V4HN.jsonl.

import random
from fractions import Fraction

from agtcake import Oracle, normalize, piece_value, random_valuation
from even_paz_algorithm import even_paz, query_count

F = Fraction


def ceil_lg(n: int) -> int:
    return (n - 1).bit_length()


def check_partition(alloc, n) -> None:
    assert sorted(alloc) == list(range(n))
    assert all(len(alloc[i]) == 1 for i in range(n))
    ivs = sorted(alloc[i][0] for i in range(n))
    assert ivs[0][0] == 0 and ivs[-1][1] == 1
    for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
        assert a1 <= b1 == a2 <= b2


def test_example() -> None:
    vals = [normalize(d) for d in ([1, 1, 1, 1], [0, 1, 1, 2], [2, 2, 0, 0], [1, 0, 0, 3])]
    o = Oracle(vals)
    alloc = even_paz(o)
    assert alloc == {
        0: [(0, F(1, 4))],
        2: [(F(1, 4), F(1, 2))],
        1: [(F(1, 2), F(13, 16))],
        3: [(F(13, 16), 1)],
    }
    assert [piece_value(vals[i], alloc[i]) for i in range(4)] == [F(1, 4), F(3, 8), F(1, 2), F(9, 16)]
    assert o.cuts == [2, 2, 2, 2] and o.evals == [1, 1, 1, 1]
    assert o.total() == query_count(4) == 12


def test_query_count_formula() -> None:
    for n in range(2, 65):
        L = ceil_lg(n)
        assert query_count(n) == 2 * n * L - 2 ** (L + 1) + n
        assert query_count(n) <= 2 * n * L - n
        if n == 2**L:
            assert query_count(n) == 2 * n * L - n
    assert query_count(1) == 0


def test_random_valuations() -> None:
    rng = random.Random(31337)
    for _ in range(150):
        n = rng.randint(1, 5)
        vals = [random_valuation(rng, rng.randint(1, 8), 6) for _ in range(n)]
        o = Oracle(vals)
        alloc = even_paz(o)
        check_partition(alloc, n)
        for i in range(n):
            assert piece_value(vals[i], alloc[i]) >= F(1, n)
        assert o.total() == query_count(n)
        assert o.total_cuts() <= n * ceil_lg(n)
        assert o.total_evals() == query_count(n) - o.total_cuts()


def test_more_agents_few_segments() -> None:
    rng = random.Random(4)
    for n in (6, 7, 8):
        vals = [random_valuation(rng, 4, 3) for _ in range(n)]
        o = Oracle(vals)
        alloc = even_paz(o)
        check_partition(alloc, n)
        for i in range(n):
            assert piece_value(vals[i], alloc[i]) >= F(1, n)
        assert o.total() == query_count(n)


def test_identical_valuations() -> None:
    rng = random.Random(6)
    for n in range(1, 6):
        v = random_valuation(rng, 6, 4)
        alloc = even_paz(Oracle([v] * n))
        check_partition(alloc, n)
        for i in range(n):
            assert piece_value(v, alloc[i]) == F(1, n)
