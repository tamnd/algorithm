# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-stampede/. The authors are listed in prov/WMTKQ5.jsonl.

import math
import random

from cache_stampede import (Clock, TTLStore, early_probability,
                            expected_stampede, simulate, stampede_size,
                            trigger_probability, xfetch,
                            xfetch_should_recompute)

# The fixed scenario: requests every 0.25 time units from 0 to 14.75, the
# entry expires at 10, a recompute takes 1 unit, the new value lives 100.
TIMES = [i / 4 for i in range(60)]
EXPIRY, DELTA, TTL = 10.0, 1.0, 100.0


def test_xfetch_function_with_simulated_clock():
    clock = Clock()
    cache = TTLStore(clock)
    calls = []

    def recompute(key):
        calls.append(clock.now)
        clock.now += 2.0  # the recompute costs 2 time units
        return "v%d" % len(calls)

    rng = random.Random(3)
    assert xfetch(cache, "k", 10.0, recompute, rng) == "v1"
    assert cache.items["k"] == ("v1", 2.0, 12.0)  # delta measured, expiry = 2 + 10
    clock.now = 5.0  # far from expiry: no early recompute with beta = 0
    assert xfetch(cache, "k", 10.0, recompute, rng, beta=0.0) == "v1"
    clock.now = 11.99
    assert xfetch(cache, "k", 10.0, recompute, rng, beta=0.0) == "v1"
    clock.now = 12.0  # expired: recompute
    assert xfetch(cache, "k", 10.0, recompute, rng, beta=0.0) == "v2"
    assert calls == [0.0, 12.0]
    # with beta = 1, the share of early recomputes at 2 units before expiry is e^-1
    hits = 0
    for _ in range(4000):
        cache.items["k"] = ("old", 2.0, 100.0)
        clock.now = 98.0
        hits += xfetch(cache, "k", 10.0, lambda key: "new", rng) == "new"
    assert abs(hits / 4000 - math.exp(-1)) < 4 * math.sqrt(0.2325 / 4000)


def test_plain_and_single_flight():
    starts, done = simulate(TIMES, "plain", EXPIRY, DELTA, TTL)
    assert starts == [10.0, 10.25, 10.5, 10.75] and done == 11.0
    assert stampede_size(starts, done) == 4
    starts, done = simulate(TIMES, "single_flight", EXPIRY, DELTA, TTL)
    assert starts == [10.0] and stampede_size(starts, done) == 1


def test_beta_zero_never_recomputes_early():
    rng = random.Random(1)
    for _ in range(2000):
        t = rng.uniform(0, EXPIRY)
        assert not xfetch_should_recompute(t, DELTA, 0.0, EXPIRY, rng)
    for seed in range(50):
        starts, done = simulate(TIMES, "xfetch", EXPIRY, DELTA, TTL, beta=0.0,
                                rng=random.Random(seed))
        assert starts == [10.0, 10.25, 10.5, 10.75]  # same as plain
    assert expected_stampede(TIMES, EXPIRY, DELTA, 0.0) == 4.0


def test_trigger_frequency_matches_exp():
    rng = random.Random(7)
    n = 40000
    for gap, beta in ((0.5, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 1.0)):
        p = trigger_probability(EXPIRY - gap, EXPIRY, DELTA, beta)
        assert math.isclose(p, math.exp(-gap / beta))
        k = sum(xfetch_should_recompute(EXPIRY - gap, DELTA, beta, EXPIRY, rng)
                for _ in range(n))
        se = math.sqrt(p * (1 - p) / n)
        assert abs(k / n - p) < 4 * se


def test_expected_stampede_matches_simulation():
    for beta, seed in ((1.0, 11), (0.5, 12), (2.0, 13)):
        exact = expected_stampede(TIMES, EXPIRY, DELTA, beta)
        rng = random.Random(seed)
        trials = 20000
        sizes = []
        early = 0
        for _ in range(trials):
            starts, done = simulate(TIMES, "xfetch", EXPIRY, DELTA, TTL, beta, rng)
            sizes.append(stampede_size(starts, done))
            early += starts[0] < EXPIRY
        mean = sum(sizes) / trials
        var = sum((s - mean) ** 2 for s in sizes) / (trials - 1)
        assert abs(mean - exact) < 4 * math.sqrt(var / trials), (beta, mean, exact)
        pe = early_probability(TIMES, EXPIRY, DELTA, beta)
        assert abs(early / trials - pe) < 4 * math.sqrt(pe * (1 - pe) / trials) + 1e-9


def test_exact_formula_by_brute_force_on_small_case():
    # three requests: enumerate all 2^3 outcomes of the independent coin flips
    times, expiry, delta, beta = [8.0, 8.5, 9.6], 10.0, 1.0, 1.0
    p = [trigger_probability(t, expiry, delta, beta) for t in times]
    total = 0.0
    for mask in range(8):
        prob, fired = 1.0, []
        for j in range(3):
            bit = mask >> j & 1
            prob *= p[j] if bit else 1 - p[j]
            if bit:
                fired.append(times[j])
        size = 0
        if fired:
            size = sum(1 for t in fired if t < fired[0] + delta)
        total += prob * size
    assert math.isclose(total, expected_stampede(times, expiry, delta, beta))
