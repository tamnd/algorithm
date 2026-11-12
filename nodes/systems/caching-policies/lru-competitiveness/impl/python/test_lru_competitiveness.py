# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru-competitiveness/. The authors are listed in prov/JZN82D.jsonl.

import random
from fractions import Fraction

from lru_competitiveness import fifo_faults, lru_faults, opt_faults, phases


def random_cases(seed, count):
    rng = random.Random(seed)
    for _ in range(count):
        pages = rng.randrange(1, 7)
        yield [rng.randrange(pages) for _ in range(rng.randrange(1, 16))]


def test_k_competitive_from_empty_caches() -> None:
    for seq in random_cases(1, 500):
        for k in range(1, 5):
            opt = opt_faults(seq, k)
            assert lru_faults(seq, k) <= k * opt
            assert fifo_faults(seq, k) <= k * opt


def test_resource_augmented_bound() -> None:
    for seq in random_cases(2, 300):
        for k in range(1, 5):
            lru, fifo = lru_faults(seq, k), fifo_faults(seq, k)
            for h in range(1, k + 1):
                bound = Fraction(k, k - h + 1) * opt_faults(seq, h) + k
                assert lru <= bound and fifo <= bound


def test_phase_lemmas() -> None:
    for seq in random_cases(3, 400):
        for k in range(1, 5):
            starts = phases(seq, k)
            bounds = starts[1:] + [len(seq)]
            for a, b in zip(starts, bounds):
                assert len(set(seq[a:b])) <= k
            assert lru_faults(seq, k) <= k * len(starts)
            assert fifo_faults(seq, k) <= k * len(starts)
            for h in range(1, k + 1):
                assert opt_faults(seq, h) >= (len(starts) - 1) * (k - h + 1) + 1


def test_cycle_reaches_ratio_k() -> None:
    for k in range(1, 5):
        seq = list(range(k + 1)) * 6
        assert lru_faults(seq, k) == len(seq)
        assert fifo_faults(seq, k) == len(seq)
        opt = opt_faults(seq, k)
        assert opt == k + (len(seq) - 1) // k


def test_adversary_against_lru() -> None:
    # Always request the page of 0 .. k that LRU does not hold: LRU faults every time.
    for k in range(1, 5):
        cache = []
        seq = []
        for _ in range(20):
            x = next(p for p in range(k + 1) if p not in cache)
            seq.append(x)
            if len(cache) == k:
                cache.pop(0)
            cache.append(x)
        assert lru_faults(seq, k) == 20
        assert opt_faults(seq, k) <= k + (20 - k + k - 1) // k
