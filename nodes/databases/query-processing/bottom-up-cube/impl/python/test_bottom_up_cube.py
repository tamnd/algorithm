# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottom-up-cube/. The authors are listed in prov/78FNHM.jsonl.
"""Tests of BUC against the iceberg cube by definition: all 2^D group-bys with dbrel.aggregate."""

import random
from collections import Counter
from itertools import combinations, product

import pytest

import dbrel
from bottom_up_cube import ALL, buc, cube_size

SALES = [
    ("tea", "Hanoi", 2023, 4), ("tea", "Hue", 2023, 3), ("coffee", "Hanoi", 2023, 5),
    ("tea", "Hanoi", 2024, 2), ("coffee", "Hanoi", 2024, 6), ("coffee", "Hue", 2024, 1),
    ("tea", "Hanoi", 2024, 7), ("juice", "Hue", 2023, 8),
]


def reference(rows, ncols, dims, aggs, minsup):
    """Every group-by of every subset of dims, by definition, with HAVING COUNT(*) >= minsup."""
    schema = ["c%d" % i for i in range(ncols)]
    rel = dbrel.Relation(schema, rows)
    spec = [("count_star", None, "n")] + [
        (f, None if c is None else schema[c], "a%d" % i) for i, (f, c) in enumerate(aggs)]
    out = Counter()
    for k in range(len(dims) + 1):
        for subset in combinations(range(len(dims)), k):
            g = [schema[dims[i]] for i in subset]
            res = dbrel.aggregate(rel, g, spec)
            for t in res.rows:
                if t[len(g)] < minsup:
                    continue
                cell = [ALL] * len(dims)
                for pos, i in enumerate(subset):
                    cell[i] = t[pos]
                out[tuple(cell) + t[len(g) + 1:]] += 1
    return out


def test_worked_example():
    st = {}
    got = buc(SALES, [0, 1, 2], [("count_star", None), ("sum", 3)], minsup=3, stats=st)
    assert got == [
        (ALL, ALL, ALL, 8, 36),
        ("coffee", ALL, ALL, 3, 12),
        ("tea", ALL, ALL, 4, 16),
        ("tea", "Hanoi", ALL, 3, 13),
        (ALL, "Hanoi", ALL, 5, 24),
        (ALL, "Hanoi", 2024, 3, 15),
        (ALL, "Hue", ALL, 3, 12),
        (ALL, ALL, 2023, 4, 20),
        (ALL, ALL, 2024, 4, 16),
    ]
    assert st == {"calls": 9, "sorted": 49, "pruned": 13}
    full = buc(SALES, [0, 1, 2], [("count_star", None)], minsup=1)
    assert len(full) == 29
    assert len(buc(SALES, [0, 1, 2], [("count_star", None)], minsup=2)) == 16


def test_against_definition_random():
    rng = random.Random(1999)
    funcs = ["count_star", "count", "sum", "avg", "min", "max"]
    for _ in range(150):
        D = rng.randint(1, 4)
        ncols = D + 1
        n = rng.randint(0, 25)
        doms = [rng.randint(1, 4) for _ in range(D)]
        rows = []
        for _ in range(n):
            t = [None if rng.random() < 0.15 else rng.randrange(c) for c in doms]
            t.append(None if rng.random() < 0.2 else rng.randint(-5, 9))
            rows.append(tuple(t))
        dims = list(range(D))
        rng.shuffle(dims)
        aggs = [(f, None if f == "count_star" else D) for f in rng.sample(funcs, rng.randint(1, 4))]
        minsup = rng.randint(1, 5)
        st = {}
        got = buc(rows, dims, aggs, minsup, st)
        assert Counter(got) == reference(rows, ncols, dims, aggs, minsup)
        assert st["calls"] == len(got)
        if minsup == 1:
            assert st["sorted"] == n * (2 ** D - 1)


def test_input_is_not_changed():
    rows = list(SALES)
    buc(rows, [2, 1, 0], [("max", 3)], minsup=2)
    assert rows == SALES


def test_full_cube_size():
    cards = [2, 3, 2]
    rows = [t + (1,) for t in product(*[range(c) for c in cards])]
    got = buc(rows, [0, 1, 2], [("count_star", None)], minsup=1)
    assert len(got) == cube_size(cards) == 3 * 4 * 3
    assert len(set(got)) == len(got)


def test_pruning_is_monotone_and_saves_work():
    rng = random.Random(42)
    rows = [(rng.randrange(6), rng.randrange(6), i, rng.randrange(3)) for i in range(60)]
    dims = [0, 1, 2]
    prev = None
    work = []
    for minsup in range(1, 8):
        st = {}
        cells = set(buc(rows, dims, [("count_star", None)], minsup, st))
        if prev is not None:
            assert cells <= prev
        prev = cells
        work.append(st["sorted"])
    assert work == sorted(work, reverse=True)
    # Dimension 2 is unique per row, so with minsup = 2 no cell fixes it.
    assert all(c[2] is ALL for c in buc(rows, dims, [("count_star", None)], 2))
    assert work[1] < work[0]


def test_edge_cases():
    assert buc([], [0, 1], [("count_star", None)], minsup=1) == []
    one = buc([(1, 2, 5)], [0, 1], [("count_star", None), ("sum", 2)], minsup=1)
    assert len(one) == 4 and all(c[2:] == (1, 5) for c in one)
    same = [(7, "a", i) for i in range(5)]
    cells = buc(same, [0, 1], [("count_star", None), ("avg", 2), ("min", 2)], minsup=5)
    assert cells == [(ALL, ALL, 5, 2, 0), (7, ALL, 5, 2, 0), (7, "a", 5, 2, 0), (ALL, "a", 5, 2, 0)]
    assert buc(same, [0, 1], [("count_star", None)], minsup=6) == []
    nulls = [(None, 1, None), (None, 2, 3), (0, 1, None)]
    got = buc(nulls, [0], [("count_star", None), ("count", 2), ("sum", 2)], minsup=1)
    assert got == [(ALL, 3, 1, 3), (None, 2, 1, 3), (0, 1, 0, None)]
    assert buc(SALES, [], [("count_star", None)], minsup=1) == [(8,)]
    with pytest.raises(ValueError):
        buc(SALES, [0], [("count_star", None)], minsup=0)
    with pytest.raises(ValueError):
        buc(SALES, [0], [("median", 3)], minsup=1)
