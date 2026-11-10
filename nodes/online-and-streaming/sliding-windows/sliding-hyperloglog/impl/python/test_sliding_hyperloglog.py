# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-hyperloglog/. The authors are listed in prov/XQTWXT.jsonl.

import math
import random

from sliding_hyperloglog import (
    SlidingHyperLogLog,
    hll_estimate,
    plain_hll_registers,
    seeded_hash,
    split_hash,
)


def window_items(stream, now, w):
    return [x for t, x in stream if now - w <= t <= now]


def test_split_hash():
    assert split_hash(1 << 63, 4) == (8, 61)
    assert split_hash((3 << 60) | (1 << 59), 4) == (3, 1)
    assert split_hash(0xF << 60, 4) == (15, 61)
    assert split_hash(1, 4) == (0, 60)
    assert seeded_hash("a", 1) == seeded_hash("a", 1) != seeded_hash("a", 2)


def test_registers_equal_hll_on_the_window():
    for seed in range(4):
        rng = random.Random(100 + seed)
        b = rng.choice((4, 6))
        window = rng.choice((5, 20, 60))
        shll = SlidingHyperLogLog(b, window, seed)
        stream = []
        t = 0
        for step in range(400):
            t += rng.choice((0, 0, 1, 1, 2, 5))
            x = rng.randint(0, rng.choice((10, 300)))
            shll.update(t, x)
            stream.append((t, x))
            for lfpm in shll.lists:
                times = [p[0] for p in lfpm]
                ranks = [p[1] for p in lfpm]
                assert times == sorted(times)
                assert all(r1 > r2 for r1, r2 in zip(ranks, ranks[1:]))
                assert len(lfpm) <= 64 - b + 1
            if step % 7 == 0:
                for w in (0, 1, window // 2, window):
                    want = plain_hll_registers(window_items(stream, t, w), b, seed)
                    assert shll.registers(w) == want
        for later in (t + 1, t + window // 2, t + window + 1):
            want = plain_hll_registers(window_items(stream, later, window), b, seed)
            assert shll.registers(window, later) == want


def test_estimate_against_exact_distinct_count():
    b = 10
    m = 1 << b
    tolerance = 4 * 1.04 / math.sqrt(m)
    rng = random.Random(2010)
    window = 8000
    shll = SlidingHyperLogLog(b, window, seed=5)
    stream = []
    for t in range(1, 24001):
        x = rng.randint(0, 6000) if t < 12000 else rng.randint(0, 60000)
        shll.update(t, x)
        stream.append((t, x))
        if t % 6000 == 0:
            for w in (50, 500, 4000, window):
                exact = len(set(window_items(stream, t, w)))
                est = shll.query(w)
                assert abs(est - exact) <= tolerance * exact, (t, w, est, exact)
    assert hll_estimate(shll.registers()) == shll.query()


def test_list_length_stays_small():
    b = 6
    shll = SlidingHyperLogLog(b, 5000, seed=9)
    for t in range(1, 20001):
        shll.update(t, t)
    mean = shll.pairs() / shll.m
    distinct_per_register = 5000 / shll.m
    assert mean <= 1 + math.log(distinct_per_register) + 1


def test_repeated_items_keep_one_pair():
    shll = SlidingHyperLogLog(4, 100, seed=0)
    for t in range(50):
        shll.update(t, "same")
    assert shll.pairs() == 1
    assert shll.registers(0)[split_hash(seeded_hash("same", 0), 4)[0]] > 0
    assert shll.query(10) < 2


def test_bad_arguments():
    for b, window in ((3, 10), (17, 10), (4, 0)):
        try:
            SlidingHyperLogLog(b, window)
        except ValueError:
            pass
        else:
            raise AssertionError("bad arguments must be rejected")
    shll = SlidingHyperLogLog(4, 10)
    shll.update(5, "a")
    try:
        shll.update(4, "b")
    except ValueError:
        pass
    else:
        raise AssertionError("decreasing times must be rejected")
