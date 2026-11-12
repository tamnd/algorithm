# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belady-optimal/. The authors are listed in prov/WA9T1Y.jsonl.

import itertools
import random

from belady_optimal import belady_optimal, min_misses, min_variable_size, next_uses


def brute_force_misses(seq, k):
    """Least misses over every demand-paging choice of eviction, by dynamic programming over cache states."""
    states = {frozenset(): 0}
    for x in seq:
        new = {}
        for c, m in states.items():
            if x in c:
                options = [(c, m)]
            elif len(c) < k:
                options = [(c | {x}, m + 1)]
            else:
                options = [((c - {y}) | {x}, m + 1) for y in c]
            for s, v in options:
                if v < new.get(s, v + 1):
                    new[s] = v
        states = new
    return min(states.values())


def brute_force_variable(seq, size, capacity):
    """Least misses with item sizes over every choice of which items to keep (the request must stay)."""
    states = {frozenset(): 0}
    for x in seq:
        new = {}
        for c, m in states.items():
            cost = m if x in c else m + 1
            others = sorted(c - {x})
            for r in range(len(others) + 1):
                for keep in itertools.combinations(others, r):
                    s = frozenset(keep) | {x}
                    if sum(size[p] for p in s) <= capacity and cost < new.get(s, cost + 1):
                        new[s] = cost
        states = new
    return min(states.values())


def test_next_uses() -> None:
    assert next_uses([1, 2, 1, 3, 2]) == [2, 4, 5, 5, 5]
    assert next_uses([]) == []


def test_classic_sequence() -> None:
    s = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    assert [min_misses(s, k) for k in range(1, 6)] == [12, 9, 7, 6, 5]
    evicted = [e for hit, e in belady_optimal(s, 3) if e is not None]
    assert evicted == [3, 4, 1, 2]


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randrange(0, 13)
        pages = rng.randrange(1, 6)
        seq = [rng.randrange(pages) for _ in range(n)]
        for k in range(1, 5):
            assert min_misses(seq, k) == brute_force_misses(seq, k)


def test_cache_never_too_big_and_request_kept() -> None:
    rng = random.Random(11)
    for _ in range(200):
        seq = [rng.randrange(8) for _ in range(rng.randrange(40))]
        k = rng.randrange(1, 5)
        cache = set()
        for x, (hit, ev) in zip(seq, belady_optimal(seq, k)):
            assert hit == (x in cache)
            if ev is not None:
                assert not hit and len(cache) == k
                cache.remove(ev)
            cache.add(x)
            assert len(cache) <= k


def test_misses_never_grow_with_k() -> None:
    rng = random.Random(3)
    for _ in range(200):
        seq = [rng.randrange(7) for _ in range(rng.randrange(30))]
        m = [min_misses(seq, k) for k in range(1, 8)]
        assert all(a >= b for a, b in zip(m, m[1:]))


def test_not_optimal_with_sizes() -> None:
    size = {"a": 3, "b": 1, "c": 1, "d": 1}
    seq = ["a", "b", "c", "d", "c", "a", "b"]
    assert min_variable_size(seq, size, 4) == 6
    assert brute_force_variable(seq, size, 4) == 5


def test_unit_sizes_agree() -> None:
    rng = random.Random(5)
    for _ in range(100):
        seq = [rng.randrange(5) for _ in range(rng.randrange(12))]
        size = {p: 1 for p in range(5)}
        for k in range(1, 4):
            assert min_variable_size(seq, size, k) == min_misses(seq, k)
