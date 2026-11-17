# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-by-aggregation/. The authors are listed in prov/KFFKTB.jsonl.

import random
from fractions import Fraction

from group_by_aggregation import (AGGREGATES, aggregate_values, combine_partitions,
                                  sort_aggregate_io, sort_group_by)

SALES = [("east", 10), ("west", 5), ("east", 7), ("north", 3), ("west", 5), ("east", 1)]
ALL = [(a, 1) for a in ("count", "sum", "min", "max", "avg", "median", "count_distinct")]


def naive(rows, key, aggs):
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r[i] for i in key), []).append(r)
    return sorted((k, tuple(aggregate_values(a, [r[c] for r in g]) for a, c in aggs))
                  for k, g in groups.items())


def test_example() -> None:
    assert sort_group_by(SALES, [0], ALL) == [
        (("east",), (3, 18, 1, 10, Fraction(6), 7, 3)),
        (("north",), (1, 3, 3, 3, Fraction(3), 3, 1)),
        (("west",), (2, 10, 5, 5, Fraction(5), 5, 1)),
    ]


def test_edges() -> None:
    assert sort_group_by([], [0], ALL) == []
    assert sort_group_by([(1, 2)], [], [("sum", 1)]) == [((), (2,))]
    assert sort_group_by([(1, 2), (1, 2)], [0, 1], [("count", 0)]) == [((1, 2), (2,))]


def test_against_naive() -> None:
    rng = random.Random(7)
    for _ in range(300):
        rows = [(rng.randrange(4), rng.randrange(3), rng.randrange(-5, 6))
                for _ in range(rng.randrange(25))]
        key = rng.choice([[0], [1], [0, 1], [1, 0], []])
        if not rows and not key:
            continue
        assert sort_group_by(rows, key, [(a, 2) for a, _ in ALL]) == naive(rows, key, [(a, 2) for a, _ in ALL])


def test_partial_states() -> None:
    rng = random.Random(3)
    for _ in range(300):
        vals = [rng.randrange(10) for _ in range(rng.randrange(1, 15))]
        cuts = sorted(rng.randrange(len(vals) + 1) for _ in range(rng.randrange(4)))
        parts = [vals[a:b] for a, b in zip([0] + cuts, cuts + [len(vals)])]
        for name in AGGREGATES:
            assert combine_partitions(parts, name) == aggregate_values(name, vals)


def test_median_is_holistic() -> None:
    a, b = [[1, 2, 3], [4, 5]], [[2, 2, 2], [4, 5]]
    for p, q in zip(a, b):
        assert aggregate_values("median", p) == aggregate_values("median", q)
        assert len(p) == len(q)
    assert aggregate_values("median", a[0] + a[1]) == 3
    assert aggregate_values("median", b[0] + b[1]) == 2


def test_io() -> None:
    assert sort_aggregate_io(10, 10) == (1, 10)
    assert sort_aggregate_io(1000, 100) == (2, 3000)
    assert sort_aggregate_io(1000, 10) == (4, 7000)
    for n in range(1, 400):
        passes, io = sort_aggregate_io(n, 5)
        assert io == (n if passes == 1 else 2 * n * passes - n)
