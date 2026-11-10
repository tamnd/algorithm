# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/misra-gries-summary/. The authors are listed in prov/6P4C0W.jsonl.

import random
from collections import Counter

import pytest

from misra_gries_summary import MisraGries


def check(mg: MisraGries, freq: Counter, universe, direct: bool = False) -> None:
    m, k = mg.m, mg.k
    assert len(mg.counters) <= k - 1
    assert all(v > 0 for v in mg.counters.values())
    slack = m - sum(mg.counters.values())
    if direct:
        assert slack % k == 0  # each decrement step removes exactly k units
    for x in set(universe) | set(freq):
        est = mg.estimate(x)
        assert est <= freq[x]
        assert k * (freq[x] - est) <= slack <= m  # f - est <= (m - sum)/k <= m/k
        if k * freq[x] > m:
            assert x in mg.heavy_candidates()


def run_and_check(stream, k):
    mg = MisraGries(k)
    freq = Counter()
    universe = set(stream)
    for x in stream:
        mg.update(x)
        freq[x] += 1
        check(mg, freq, universe, direct=True)
    return mg, freq


def test_example() -> None:
    mg, _ = run_and_check(list("abacabdab"), 3)
    assert mg.counters == {"a": 2, "b": 1}
    assert mg.m == 9


def test_edges() -> None:
    with pytest.raises(ValueError):
        MisraGries(1)
    mg = MisraGries(2)
    assert mg.estimate("x") == 0
    run_and_check([], 4)
    run_and_check([5], 2)
    run_and_check([5] * 30, 2)
    run_and_check(list(range(30)), 5)


def adversarial_streams(k):
    yield list(range(k)) * 10  # round robin over k items: each round wipes all counters
    yield list(range(k - 1)) + [k] * 20  # full table, then a new item many times
    yield [i % (k + 3) for i in range(60)]
    yield [0] * 15 + list(range(1, 40))  # heavy item first, then many distinct items
    yield list(range(1, 40)) + [0] * 15  # heavy item last
    yield [0 if i % k == 0 else i for i in range(80)]  # item 0 exactly every k-th place


def test_adversarial_streams() -> None:
    for k in range(2, 7):
        for s in adversarial_streams(k):
            run_and_check(s, k)


def test_seeded_streams_every_query() -> None:
    rng = random.Random(2024)
    for _ in range(300):
        k = rng.randrange(2, 8)
        n = rng.randrange(1, 15)
        m = rng.randrange(0, 60)
        weights = [rng.random() ** 3 for _ in range(n)]
        s = rng.choices(range(n), weights=weights, k=m)
        run_and_check(s, k)


def test_merge_against_concatenation() -> None:
    rng = random.Random(99)
    for _ in range(400):
        k = rng.randrange(2, 7)
        n = rng.randrange(1, 12)
        s1 = [rng.randrange(n) for _ in range(rng.randrange(0, 40))]
        s2 = [rng.randrange(n) for _ in range(rng.randrange(0, 40))]
        a, _ = run_and_check(s1, k)
        b, _ = run_and_check(s2, k)
        merged = a.merge(b)
        direct, freq = run_and_check(s1 + s2, k)
        assert merged.m == direct.m == len(s1) + len(s2)
        check(merged, freq, range(n))
        # A merge is not equal to a direct run, but when no counter was ever
        # decremented both are exact and they agree.
        if len(set(s1 + s2)) < k:
            assert merged.counters == direct.counters == dict(freq)


def test_merge_tree_of_many_parts() -> None:
    rng = random.Random(3)
    k = 4
    parts = [[rng.randrange(10) for _ in range(rng.randrange(0, 15))] for _ in range(16)]
    summaries = [run_and_check(p, k)[0] for p in parts]
    while len(summaries) > 1:
        summaries = [summaries[i].merge(summaries[i + 1]) for i in range(0, len(summaries), 2)]
    freq = Counter(x for p in parts for x in p)
    check(summaries[0], freq, range(10))


def test_space_and_time_amortized() -> None:
    # The total number of counter decrements is at most the number of increments.
    rng = random.Random(8)
    k = 10
    mg = MisraGries(k)
    for _ in range(3000):
        mg.update(rng.randrange(50))
    assert len(mg.counters) <= k - 1
    assert mg.m - sum(mg.counters.values()) <= mg.m
