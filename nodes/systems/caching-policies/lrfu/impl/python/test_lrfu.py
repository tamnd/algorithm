# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lrfu/. The authors are listed in prov/ETPAQ6.jsonl.

import random
from collections import OrderedDict

import pytest

from lrfu import LRFU, lrfu_hits


def run(trace, k, lam):
    c = LRFU(k, lam)
    out, victims = [], []
    for x in trace:
        out.append(c.access(x))
        if c.evicted is not None:
            victims.append(c.evicted)
        assert x in c and len(c) <= k and len(c.heap) <= 2 * k + 16
    return out, victims


def naive_lrfu(trace, k, lam):
    """Sum F(t - t_i) over all references since the load, for each block."""
    refs, out, victims = {}, [], []
    for t, x in enumerate(trace, 1):
        if x in refs:
            refs[x].append(t)
            out.append(True)
            continue
        if len(refs) == k:

            def crf(y):
                return sum(0.5 ** (lam * (t - s)) for s in refs[y])

            v = min(refs, key=lambda y: (crf(y), refs[y][-1]))
            victims.append(v)
            del refs[v]
        refs[x] = [t]
        out.append(False)
    return out, victims


def lru(trace, k):
    c, out, victims = OrderedDict(), [], []
    for x in trace:
        if x in c:
            c.move_to_end(x)
            out.append(True)
            continue
        if len(c) == k:
            victims.append(c.popitem(last=False)[0])
        c[x] = None
        out.append(False)
    return out, victims


def lfu(trace, k):
    """In-cache LFU: least count since the load, ties to the older last use."""
    count, last, out, victims = {}, {}, [], []
    for t, x in enumerate(trace):
        if x in count:
            count[x] += 1
            last[x] = t
            out.append(True)
            continue
        if len(count) == k:
            v = min(count, key=lambda y: (count[y], last[y]))
            victims.append(v)
            del count[v], last[v]
        count[x], last[x] = 1, t
        out.append(False)
    return out, victims


def test_example_of_the_page():
    trace = list("ccbbadebd")
    out, victims = run(trace, 3, 0.5)
    assert victims == ["c", "a"] and out.count(False) == 5
    assert run(trace, 3, 1.0) == lru(trace, 3)
    assert lru(trace, 3)[1] == ["c", "b", "a"]
    assert run(trace, 3, 0.0) == lfu(trace, 3)
    assert lfu(trace, 3)[1] == ["a", "d", "e"]
    c = LRFU(3, 0.5)
    for x in trace[:5]:
        c.access(x)
    c.t += 1  # look at the values at t = 6, before the request to d
    assert round(c.value("c"), 3) == 0.427
    assert round(c.value("b"), 3) == 0.854
    assert round(c.value("a"), 3) == 0.707


def test_lambda_one_is_lru():
    rng = random.Random(111)
    for _ in range(300):
        k = rng.randint(1, 6)
        trace = [rng.randrange(10) for _ in range(rng.randint(0, 120))]
        assert run(trace, k, 1.0) == lru(trace, k)


def test_lambda_zero_is_lfu():
    rng = random.Random(112)
    for _ in range(300):
        k = rng.randint(1, 6)
        trace = [rng.randrange(10) for _ in range(rng.randint(0, 120))]
        assert run(trace, k, 0.0) == lfu(trace, k)


def test_long_runs_at_lambda_one():
    # 80 references in a row push C to 2.0 in floating point; ties still go
    # to the older block, so the order stays that of LRU.
    trace = ["a"] * 80 + ["b", "c", "a", "d", "b"] * 3
    assert run(trace, 2, 1.0) == lru(trace, 2)


def test_matches_naive_sum():
    rng = random.Random(113)
    for _ in range(300):
        k = rng.randint(1, 5)
        lam = rng.choice([0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0])
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        assert run(trace, k, lam) == naive_lrfu(trace, k, lam)


def test_middle_lambda_differs_from_both_ends():
    trace = list("ccbbadebd")
    misses = [lrfu_hits(trace, 3, lam).count(False) for lam in (0.0, 0.5, 1.0)]
    assert misses == [6, 5, 6]


def test_bad_arguments():
    with pytest.raises(ValueError):
        LRFU(0, 0.5)
    with pytest.raises(ValueError):
        LRFU(2, 1.5)
    with pytest.raises(ValueError):
        LRFU(2, -0.1)
