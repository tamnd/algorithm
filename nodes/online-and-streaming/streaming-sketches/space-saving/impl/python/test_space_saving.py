# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-saving/. The authors are listed in prov/3PR4D2.jsonl.

import random
from collections import Counter

import pytest

from space_saving import SpaceSaving


class ReferenceMisraGries:
    """A plain Misra-Gries summary with k - 1 counters, used as a reference."""

    def __init__(self, k: int) -> None:
        self.k = k
        self.c: dict = {}

    def update(self, x) -> None:
        if x in self.c:
            self.c[x] += 1
        elif len(self.c) < self.k - 1:
            self.c[x] = 1
        else:
            for y in list(self.c):
                self.c[y] -= 1
                if self.c[y] == 0:
                    del self.c[y]


def check(ss: SpaceSaving, freq: Counter, universe) -> None:
    m, k = ss.m, ss.k
    mu = ss.min_count()
    assert len(ss.count) <= k
    assert ss.delta_bound <= m / k
    if not ss._merged:
        assert sum(ss.count.values()) == m  # every update adds exactly 1
        assert mu == ss.delta_bound
        assert all(c >= mu for c in ss.count.values())
    for x in set(universe) | set(freq):
        est = ss.estimate(x)
        assert freq[x] <= est <= freq[x] + ss.delta_bound
        assert ss.guaranteed(x) <= freq[x]
        if k * freq[x] > m:
            assert x in ss.count


def run_and_check(stream, k, with_mg=True):
    ss = SpaceSaving(k)
    mg = ReferenceMisraGries(k) if with_mg else None  # k - 1 counters
    freq = Counter()
    universe = set(stream)
    decrements = 0
    for x in stream:
        before = ss.min_count()
        ss.update(x)
        freq[x] += 1
        check(ss, freq, universe)
        if mg is not None:
            size = len(mg.c)
            had = x in mg.c
            mg.update(x)
            if not had and size == k - 1:
                decrements += 1
                assert ss.min_count() == before + 1  # a decrement step raises mu by one
            else:
                assert ss.min_count() == before
            # The isomorphism: MG with k - 1 counters equals SS with k counters minus mu.
            assert ss.to_misra_gries() == mg.c
            assert decrements == ss.min_count()
    return ss, freq


def test_example() -> None:
    ss, _ = run_and_check(list("abacabdab"), 3)
    assert ss.count == {"a": 4, "b": 3, "d": 2}
    assert ss.err == {"a": 0, "b": 0, "d": 1}
    assert ss.min_count() == 2
    assert ss.estimate("c") == 2
    assert ss.to_misra_gries() == {"a": 2, "b": 1}


def test_edges() -> None:
    with pytest.raises(ValueError):
        SpaceSaving(0)
    ss = SpaceSaving(1)
    assert ss.estimate("x") == 0
    run_and_check([], 3)
    run_and_check([7], 1)
    run_and_check(list(range(20)), 1)
    run_and_check([5] * 30, 2)
    run_and_check(list(range(30)), 5)


def adversarial_streams(k):
    yield list(range(k + 1)) * 10  # round robin over k + 1 items
    yield list(range(k)) + [k + 5] * 20  # full table, then one new item many times
    yield [i % (k + 3) for i in range(60)]
    yield [0] * 15 + list(range(1, 40))  # heavy item first, then many new items
    yield list(range(1, 40)) + [0] * 15  # heavy item last
    yield [0 if i % (k + 1) == 0 else i for i in range(80)]  # item 0 at every (k+1)-th place


def test_adversarial_streams() -> None:
    for k in range(1, 7):
        for s in adversarial_streams(k):
            run_and_check(s, k)


def test_seeded_streams_every_query() -> None:
    rng = random.Random(2025)
    for _ in range(300):
        k = rng.randrange(1, 8)
        n = rng.randrange(1, 15)
        m = rng.randrange(0, 60)
        weights = [rng.random() ** 3 for _ in range(n)]
        s = rng.choices(range(n), weights=weights, k=m)
        run_and_check(s, k)


def test_top_contains_heavy_items() -> None:
    rng = random.Random(5)
    k = 10
    s = [rng.randrange(3) if rng.random() < 0.6 else rng.randrange(3, 500) for _ in range(3000)]
    ss, freq = run_and_check(s, k, with_mg=False)
    top = [x for x, _ in ss.top(3)]
    assert sorted(top) == [0, 1, 2]


def test_merge_against_concatenation() -> None:
    rng = random.Random(77)
    for _ in range(400):
        k = rng.randrange(1, 7)
        n = rng.randrange(1, 12)
        s1 = [rng.randrange(n) for _ in range(rng.randrange(0, 40))]
        s2 = [rng.randrange(n) for _ in range(rng.randrange(0, 40))]
        a, _ = run_and_check(s1, k, with_mg=False)
        b, _ = run_and_check(s2, k, with_mg=False)
        merged = a.merge(b)
        _, freq = run_and_check(s1 + s2, k, with_mg=False)
        assert merged.m == len(s1) + len(s2)
        check(merged, freq, range(n))
        with pytest.raises(ValueError):
            merged.update(0)


def test_merge_tree_of_many_parts() -> None:
    rng = random.Random(4)
    k = 4
    parts = [[rng.randrange(10) for _ in range(rng.randrange(0, 15))] for _ in range(16)]
    summaries = [run_and_check(p, k, with_mg=False)[0] for p in parts]
    while len(summaries) > 1:
        summaries = [summaries[i].merge(summaries[i + 1]) for i in range(0, len(summaries), 2)]
    freq = Counter(x for p in parts for x in p)
    check(summaries[0], freq, range(10))
