# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-aggregation/. The authors are listed in prov/ET3B5B.jsonl.

import random
from fractions import Fraction

from hash_aggregation import hash_aggregate

ALL = ["count", "sum", "min", "max", "avg"]


def sort_based(rows, key, aggs):
    """Reference: sort on the key, then aggregate each run of equal keys."""
    kf = lambda r: tuple(r[i] for i in key)
    srt = sorted(rows, key=kf)
    out, i = {}, 0
    while i < len(srt):
        j = i
        while j < len(srt) and kf(srt[j]) == kf(srt[i]):
            j += 1
        res = []
        for a, c in aggs:
            vals = [r[c] for r in srt[i:j]]
            res.append({"count": len(vals), "sum": sum(vals), "min": min(vals), "max": max(vals),
                        "avg": Fraction(sum(vals), len(vals))}[a])
        out[kf(srt[i])] = tuple(res)
        i = j
    return out


SALES = [("east", 10), ("west", 5), ("east", 7), ("north", 3), ("west", 5), ("east", 1)]


def test_example() -> None:
    st = {}
    got = hash_aggregate(SALES, [0], [(a, 1) for a in ALL], mem_groups=2, fanout=2, stats=st)
    assert got == {("east",): (3, 18, 1, 10, Fraction(6)), ("west",): (2, 10, 5, 5, Fraction(5)),
                   ("north",): (1, 3, 3, 3, Fraction(3))}
    assert st == {"spilled": 1, "levels": 2}


def test_edges() -> None:
    assert hash_aggregate([], [0], [("sum", 0)], 1) == {}
    assert hash_aggregate([(4,)], [], [("avg", 0)], 1) == {(): (Fraction(4),)}
    try:
        hash_aggregate([(1,)], [0], [("sum", 0)], 0)
        assert False
    except ValueError:
        pass


def test_against_sort_based() -> None:
    rng = random.Random(11)
    for _ in range(400):
        g = rng.randrange(1, 30)
        rows = [(rng.randrange(g), rng.randrange(3), rng.randrange(-9, 10)) for _ in range(rng.randrange(60))]
        key = rng.choice([[0], [0, 1], [1]])
        aggs = [(a, 2) for a in ALL]
        mem = rng.randrange(1, 8)
        assert hash_aggregate(rows, key, aggs, mem, rng.randrange(2, 5)) == sort_based(rows, key, aggs)


def test_one_pass_when_groups_fit() -> None:
    rng = random.Random(5)
    rows = [(rng.randrange(20), rng.randrange(100)) for _ in range(2000)]
    st = {}
    hash_aggregate(rows, [0], [("sum", 1)], mem_groups=20, stats=st)
    assert st == {"spilled": 0, "levels": 1}


def test_spill_count_level_zero() -> None:
    # Level 0 spills exactly the rows whose key is not among the first
    # mem_groups distinct keys; deeper levels may spill more.
    rng = random.Random(9)
    for _ in range(100):
        rows = [(rng.randrange(12), 1) for _ in range(rng.randrange(80))]
        mem = rng.randrange(1, 12)
        first = set()
        for r in rows:
            if r[0] not in first and len(first) < mem:
                first.add(r[0])
        outside = sum(1 for r in rows if r[0] not in first)
        st = {}
        hash_aggregate(rows, [0], [("count", 1)], mem, fanout=2, stats=st)
        assert st["spilled"] >= outside
        if outside == 0:
            assert st["levels"] == 1
