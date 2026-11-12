# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inclusion-property/. The authors are listed in prov/4SP6AS.jsonl.

import itertools
import random

from inclusion_property import fifo_contents, first_violation, lru_contents, min_contents, misses

CLASSIC = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def brute_lru(seq, k):
    """LRU from the definition: after request t, the k distinct items with the latest last use."""
    out = []
    for t in range(len(seq)):
        last = {}
        for s in range(t + 1):
            last[seq[s]] = s
        out.append(frozenset(sorted(last, key=lambda p: -last[p])[:k]))
    return out


def test_lru_matches_definition() -> None:
    rng = random.Random(8)
    for _ in range(200):
        seq = [rng.randrange(6) for _ in range(rng.randrange(25))]
        for k in range(1, 6):
            assert lru_contents(seq, k) == brute_lru(seq, k)


def test_lru_inclusion_exhaustive() -> None:
    for n in range(1, 8):
        for seq in itertools.product(range(4), repeat=n):
            assert first_violation(lru_contents, seq, 4) is None
            assert first_violation(brute_lru, seq, 4) is None


def test_lru_inclusion_random() -> None:
    rng = random.Random(21)
    for _ in range(200):
        seq = [rng.randrange(10) for _ in range(rng.randrange(80))]
        assert first_violation(lru_contents, seq, 10) is None


def test_min_inclusion() -> None:
    for seq in itertools.product(range(4), repeat=7):
        assert first_violation(min_contents, seq, 3) is None
    rng = random.Random(4)
    for _ in range(100):
        seq = [rng.randrange(8) for _ in range(rng.randrange(50))]
        assert first_violation(min_contents, seq, 8) is None


def test_fifo_violates_inclusion() -> None:
    assert first_violation(fifo_contents, CLASSIC, 3) == (3, 6)
    assert fifo_contents(CLASSIC, 3)[6] == frozenset({1, 2, 5})
    assert fifo_contents(CLASSIC, 4)[6] == frozenset({2, 3, 4, 5})


def test_inclusion_gives_monotone_misses() -> None:
    rng = random.Random(6)
    for _ in range(200):
        seq = [rng.randrange(7) for _ in range(rng.randrange(40))]
        for policy in (lru_contents, min_contents):
            m = [misses(policy, seq, k) for k in range(1, 9)]
            assert all(a >= b for a, b in zip(m, m[1:]))
    assert [misses(fifo_contents, CLASSIC, k) for k in (3, 4)] == [9, 10]
