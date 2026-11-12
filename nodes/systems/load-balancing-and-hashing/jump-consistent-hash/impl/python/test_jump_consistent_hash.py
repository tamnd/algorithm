# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-consistent-hash/. The authors are listed in prov/F8JS2K.jsonl.

import math
import random
from collections import Counter

import pytest

from jump_consistent_hash import iterations, jump_consistent_hash, jump_trace


def test_regression_values():
    # Values of this implementation. The C++ code printed in the paper,
    # compiled with clang, gives the same values for these inputs.
    cases = [
        (0, 10, 0),
        (1, 10, 6),
        (42, 10, 2),
        (256, 1000, 520),
        (123456789, 100, 34),
        ((1 << 64) - 1, 1000, 313),
        (0xDEADBEEF, 1000000, 479362),
    ]
    for key, n, want in cases:
        assert jump_consistent_hash(key, n) == want


def test_trace_of_worked_example():
    assert jump_trace(256, 1000) == [1, 2, 3, 16, 137, 520, 3906]


def test_one_bucket_and_bad_input():
    for k in range(100):
        assert jump_consistent_hash(k, 1) == 0
    with pytest.raises(ValueError):
        jump_consistent_hash(5, 0)


def test_range():
    rng = random.Random(1)
    for _ in range(2000):
        k = rng.getrandbits(64)
        n = rng.randrange(1, 5000)
        assert 0 <= jump_consistent_hash(k, n) < n


def test_monotonicity_exhaustive():
    # Going from n to n + 1 buckets, a key either stays or moves to bucket n.
    rng = random.Random(2)
    keys = [rng.getrandbits(64) for _ in range(1000)] + list(range(200))
    for k in keys:
        prev = jump_consistent_hash(k, 1)
        for n in range(2, 101):
            cur = jump_consistent_hash(k, n)
            assert cur == prev or cur == n - 1
            prev = cur


def test_moved_fraction_on_growth():
    rng = random.Random(3)
    keys = [rng.getrandbits(64) for _ in range(30000)]
    for n in [1, 7, 10, 50]:
        moved = sum(jump_consistent_hash(k, n) != jump_consistent_hash(k, n + 1) for k in keys)
        p = 1 / (n + 1)
        sd = math.sqrt(len(keys) * p * (1 - p))
        assert abs(moved - len(keys) * p) < 5 * sd


def test_balance_chi_square():
    rng = random.Random(4)
    keys = [rng.getrandbits(64) for _ in range(50000)]
    for n in [10, 37]:
        c = Counter(jump_consistent_hash(k, n) for k in keys)
        e = len(keys) / n
        chi2 = sum((c[b] - e) ** 2 / e for b in range(n))
        # mean n - 1; the bound is about 6 standard deviations above it
        assert chi2 < (n - 1) + 6 * math.sqrt(2 * (n - 1))


def test_expected_iterations_close_to_harmonic_number():
    rng = random.Random(5)
    keys = [rng.getrandbits(64) for _ in range(5000)]
    for n in [10, 1000, 1000000]:
        mean = sum(iterations(k, n) for k in keys) / len(keys)
        h = sum(1.0 / i for i in range(1, n + 1))
        assert abs(mean - h) < 0.15
