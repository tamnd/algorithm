# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefetching/. The authors are listed in prov/P6H46Y.jsonl.

import random

import pytest

from prefetching import (
    NO_PRED,
    STEADY,
    ReferencePredictionTable,
    aggressive,
    conservative,
    demand_min,
    lru_fetches,
    min_fetches,
    optimal,
    sequential,
    stride_prefetch,
)


def test_sequential_scan() -> None:
    scan = list(range(1000))
    assert sequential(scan, 64, "none").misses == 1000
    assert sequential(scan, 64, "miss").misses == 500  # every other block
    for mode in ("always", "tagged"):
        c = sequential(scan, 64, mode)
        assert c.misses == 1 and c.useful == 999


def test_sequential_runs() -> None:
    # runs of 1 to 16 consecutive blocks from random places
    rng = random.Random(2)
    trace = []
    while len(trace) < 20_000:
        s = rng.randrange(10**6)
        trace += range(s, s + rng.randint(1, 16))
    none = sequential(trace, 256, "none")
    miss = sequential(trace, 256, "miss")
    tagged = sequential(trace, 256, "tagged")
    # measured: 20001 misses with no prefetch, 10585 on miss, 2314 tagged
    assert none.misses == len(trace)
    assert tagged.misses < 0.15 * none.misses < miss.misses < 0.6 * none.misses
    assert tagged.prefetches - tagged.useful < 0.15 * tagged.prefetches  # some prefetches run past a run's end


def test_rpt_states() -> None:
    rpt = ReferencePredictionTable()
    assert rpt.access("pc", 100) is None  # a new entry: initial, stride 0
    assert rpt.access("pc", 104) == 108  # incorrect: transient, stride 4
    assert rpt.access("pc", 108) == 112  # correct: steady
    assert rpt.table["pc"][2] == STEADY
    assert rpt.access("pc", 200) == 204  # incorrect in steady: initial, the stride stays 4
    assert rpt.table["pc"][1] == 4
    assert rpt.access("pc", 7) == 7 - 193  # incorrect in initial: transient, stride -193
    assert rpt.access("pc", 1000) is None  # incorrect in transient: no prediction
    assert rpt.table["pc"][2] == NO_PRED
    assert rpt.access("pc", 2000) is None


def test_stride_prefetcher_on_interleaved_loads() -> None:
    rng = random.Random(3)
    loads = []
    for i in range(5000):
        loads += [("A", 1000 + 3 * i), ("B", 10**6 + 7 * i), ("C", rng.randrange(10**7))]
    blocks = [b for _, b in loads]
    plain = sequential(blocks, 256, "none")
    tagged = sequential(blocks, 256, "tagged")
    rpt = stride_prefetch(loads, 256)
    assert plain.misses == 15_000
    assert tagged.misses == 15_000  # next-block prefetching does not help strides of 3 and 7
    assert rpt.misses <= 5000 + 6  # only the random loads and the first loads of A and B miss
    assert rpt.useful >= 9990


def test_cao_example_abca() -> None:
    # k = 2, F = 4, A and B in the cache at the start
    assert demand_min("ABCA", 2, 4, "AB") == (8, 1)
    assert aggressive("ABCA", 2, 4, "AB") == (10, 2)
    assert optimal("ABCA", 2, 4, "AB") == 8
    # on ABCB the prefetch of C, replacing A, hides one unit of latency
    assert demand_min("ABCB", 2, 4, "AB") == (8, 1)
    assert aggressive("ABCB", 2, 4, "AB") == (7, 1)
    assert optimal("ABCB", 2, 4, "AB") == 7


def test_rules_and_bounds_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n, m, k, F = rng.randint(1, 8), rng.randint(1, 4), rng.randint(1, 3), rng.randint(1, 4)
        refs = [rng.randrange(m) for _ in range(n)]
        start = rng.sample(range(m), min(k, m, rng.randint(0, k)))
        opt = optimal(refs, k, F, start)
        # rules 1 to 3 lose nothing: the search over schedules that obey them finds the optimum
        assert optimal(refs, k, F, start, rules=True) == opt
        a, a_fetches = aggressive(refs, k, F, start)
        c, c_fetches = conservative(refs, k, F, start)
        d, d_fetches = demand_min(refs, k, F, start)
        assert opt <= min(a, c, d)
        assert a <= min(1 + F / k, 2) * opt
        assert c <= 2 * opt
        assert c_fetches == d_fetches == len(min_fetches(refs, k, start))
        if not start:
            assert a_fetches <= lru_fetches(refs, k)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        sequential([1, 2], 4, "sometimes")
    with pytest.raises(ValueError):
        aggressive("AB", 1, 2, "AB")
