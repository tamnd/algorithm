# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crew-pram/. The authors are listed in prov/RA6DW1.jsonl.

import math
import random

import pytest

from crew_pram import AccessError, broadcast, merge_by_ranking, run_step, tree_or


def sorted_list(rng, k, top):
    return sorted(rng.randint(0, top) for _ in range(k))


def test_merge_matches_sorted():
    rng = random.Random(1)
    sizes = list(range(0, 9)) + [15, 16, 17, 40]
    for m in sizes:
        for n in sizes:
            for top in (3, 1000):  # many ties, and few ties
                a, b = sorted_list(rng, m, top), sorted_list(rng, n, top)
                merged, pram = merge_by_ranking(a, b)  # a write conflict would raise
                assert merged == sorted(a + b)
                if m + n:
                    k = max(m, n).bit_length()  # ceil(lg(max(m, n) + 1))
                    assert pram.time <= 2 + k
                    assert pram.work <= (m + n) * (2 + k)


def test_tie_rule_gives_distinct_positions():
    # all items equal: a-items take positions 0..m-1 and b-items take m..m+n-1
    merged, pram = merge_by_ranking([5] * 4, [5] * 3)
    assert merged == [5] * 7
    _, writers = pram.trace[-1]
    owner = {cell[1]: ps[0] for cell, ps in writers.items()}
    assert [owner[k][0] for k in range(7)] == ["a"] * 4 + ["b"] * 3


def test_merge_uses_concurrent_reads():
    rng = random.Random(2)
    for _ in range(50):
        m, n = rng.randint(2, 30), rng.randint(1, 30)
        a, b = sorted_list(rng, m, 100), sorted_list(rng, n, 100)
        _, pram = merge_by_ranking(a, b)
        assert pram.max_readers() >= 2  # the first probe of every a-processor reads the middle of b
        with pytest.raises(AccessError):
            merge_by_ranking(a, b, exclusive_read=True)


def test_one_step_broadcast():
    for p in range(0, 40):
        out, pram = broadcast(p, "v")
        assert out == ["v"] * p and pram.time == 1
        if p >= 2:
            with pytest.raises(AccessError):
                broadcast(p, "v", exclusive_read=True)


def test_exclusive_write_is_enforced():
    step = {0: ((), lambda v: [("x", 1)]), 1: ((), lambda v: [("x", 1)])}
    with pytest.raises(AccessError):
        run_step({}, step)


def test_tree_or():
    rng = random.Random(3)
    for n in list(range(0, 40)) + [64, 65]:
        for density in (0.0, 0.05, 0.5):
            bits = [1 if rng.random() < density else 0 for _ in range(n)]
            value, pram = tree_or(bits)
            assert value == (1 if any(bits) else 0)
            assert pram.time == (math.ceil(math.log2(n)) if n > 1 else 0)
            assert pram.max_readers() <= 1
