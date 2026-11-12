# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-replacement/. The authors are listed in prov/TVHW25.jsonl.

import random
from collections import Counter
from fractions import Fraction

from random_replacement import RandomReplacement, random_hits


def exact_miss_distribution(trace, k):
    """Exact law of the number of misses: a walk over all cache states with exact weights."""
    states = {(frozenset(), 0): Fraction(1)}
    for p in trace:
        nxt = {}
        for (cache, m), w in states.items():
            if p in cache:
                outs = [((cache, m), w)]
            elif len(cache) < k:
                outs = [((cache | {p}, m + 1), w)]
            else:
                outs = [(((cache - {q}) | {p}, m + 1), w / k) for q in cache]
            for key, x in outs:
                nxt[key] = nxt.get(key, Fraction(0)) + x
        states = nxt
    law = {}
    for (_, m), w in states.items():
        law[m] = law.get(m, Fraction(0)) + w
    return law


def min_misses(trace, k):
    cache, misses = set(), 0
    for t, p in enumerate(trace):
        if p in cache:
            continue
        misses += 1
        if len(cache) == k:
            def next_use(q):
                for u in range(t + 1, len(trace)):
                    if trace[u] == q:
                        return u
                return len(trace)
            cache.remove(max(cache, key=next_use))
        cache.add(p)
    return misses


def test_fixed_seed_run():
    trace = [0, 1, 2, 3] * 5
    assert random_hits(trace, 3, random.Random(2024)) == random_hits(trace, 3, random.Random(2024))
    c = RandomReplacement(3, random.Random(5))
    for p in trace:
        c.access(p)
        assert len(c) <= 3 and p in c


def test_victim_is_uniform():
    rng = random.Random(31)
    counts = Counter()
    for _ in range(6000):
        c = RandomReplacement(3, rng)
        for p in "abcd":
            c.access(p)
        counts[c.evicted] += 1
    assert set(counts) == {"a", "b", "c"}
    for v in counts.values():
        assert abs(v - 2000) < 200


def test_law_matches_simulation():
    trace = [0, 1, 2, 0, 3, 1, 0, 2, 3, 0, 1, 2]
    law = exact_miss_distribution(trace, 3)
    assert sum(law.values()) == 1
    rng = random.Random(32)
    runs = 20000
    seen = Counter(len(trace) - sum(random_hits(trace, 3, rng)) for _ in range(runs))
    for m, p in law.items():
        assert abs(seen[m] / runs - float(p)) < 0.015


def test_loop_rate_is_two_over_k_plus_one():
    for k in (2, 3, 4, 6):
        trace = list(range(k + 1)) * (60000 // (k + 1))
        hits = random_hits(trace, k, random.Random(33 + k))
        rate = (len(trace) - sum(hits)) / len(trace)
        assert abs(rate - 2 / (k + 1)) < 0.01


def test_loop_exact_expectation_tends_to_the_rate():
    k = 3
    trace = list(range(k + 1)) * 30
    law = exact_miss_distribution(trace, k)
    mean = sum(m * p for m, p in law.items())
    # k + 1 cold misses, then about 2/(k + 1) misses per request
    assert abs(mean - (k + 1) - Fraction(2, k + 1) * (len(trace) - k - 1)) < 1


def test_expected_misses_at_most_k_times_min():
    rng = random.Random(34)
    for _ in range(60):
        k = rng.randint(1, 3)
        trace = [rng.randrange(5) for _ in range(rng.randint(1, 12))]
        law = exact_miss_distribution(trace, k)
        mean = sum(m * p for m, p in law.items())
        assert mean <= k * min_misses(trace, k)
