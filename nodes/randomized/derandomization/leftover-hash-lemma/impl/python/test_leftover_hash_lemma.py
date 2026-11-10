# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leftover-hash-lemma/. The authors are listed in prov/T7RZCY.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from leftover_hash_lemma import (
    collision_probability,
    collision_rate,
    extraction_distance,
    flat_source,
    is_universal,
    joint_collision_probability,
    lhl_bound_squared,
    min_entropy_at_least,
    prefix_family,
    toeplitz_family,
    toeplitz_hash,
)


def test_toeplitz_matrix_layout() -> None:
    # n = 3, m = 2, t = 0b0110: T = [[t2, t1, t0], [t3, t2, t1]] = [[1, 1, 0], [0, 1, 1]].
    h = toeplitz_hash(0b0110, 3, 2)
    assert h(0b001) == 0b01
    assert h(0b010) == 0b11
    assert h(0b100) == 0b10


def test_toeplitz_is_exactly_universal() -> None:
    for n in range(1, 5):
        for m in range(1, 4):
            family = toeplitz_family(n, m)
            for x in range(1 << n):
                for y in range(x + 1, 1 << n):
                    assert collision_rate(family, x, y) == Fraction(1, 1 << m)


def test_prefix_family_is_not_universal() -> None:
    assert not is_universal(prefix_family(4, 2), 4, 2)
    assert is_universal(prefix_family(2, 2), 2, 2)


def test_worst_flat_sources_exhaustive() -> None:
    n, k = 4, 2
    want = {1: Fraction(3, 16), 2: Fraction(21, 64)}
    for m in (1, 2):
        family = toeplitz_family(n, m)
        worst = Fraction(0)
        for support in combinations(range(1 << n), 1 << k):
            sd = extraction_distance(family, flat_source(support), m)
            assert sd * sd <= lhl_bound_squared(k, m)
            worst = max(worst, sd)
        assert worst == want[m]
    assert extraction_distance(toeplitz_family(4, 1), flat_source((0, 1, 2, 4)), 1) == Fraction(3, 16)


def test_lhl_bound_on_random_flat_sources() -> None:
    rng = random.Random(1)
    cases = 0
    for _ in range(500):
        n = rng.randrange(2, 6)
        m = rng.randrange(1, 3)
        k = rng.randrange(0, n + 1)
        support = rng.sample(range(1 << n), 1 << k)
        family = toeplitz_family(n, m)
        sd = extraction_distance(family, flat_source(support), m)
        assert sd * sd <= lhl_bound_squared(k, m)
        cases += 1
    assert cases == 500


def test_collision_probability_bound_and_l2_step() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randrange(2, 5)
        m = rng.randrange(1, 3)
        weights = [rng.randrange(0, 5) for _ in range(1 << n)]
        if sum(weights) == 0:
            continue
        total = sum(weights)
        source = {x: Fraction(w, total) for x, w in enumerate(weights) if w}
        family = toeplitz_family(n, m)
        size = len(family)
        cp = joint_collision_probability(family, source)
        # CP(H, H(X)) <= (CP(X) + 2^-m) / |H|.
        assert cp <= (collision_probability(source) + Fraction(1, 1 << m)) / size
        # Statistical distance <= (1/2) sqrt(N * CP - 1) with N = |H| 2^m.
        sd = extraction_distance(family, source, m)
        assert 4 * sd * sd <= size * (1 << m) * cp - 1


def test_lhl_with_min_entropy_on_nonflat_sources() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = 4
        k = rng.randrange(1, 4)
        m = rng.randrange(1, 3)
        cap = Fraction(1, 1 << k)
        support = rng.sample(range(1 << n), (1 << k) + rng.randrange(0, 4))
        probs = [Fraction(rng.randrange(1, 6)) for _ in support]
        total = sum(probs)
        source = {x: p / total for x, p in zip(support, probs)}
        if not min_entropy_at_least(source, k):
            continue
        assert max(source.values()) <= cap
        sd = extraction_distance(toeplitz_family(n, m), source, m)
        assert sd * sd <= lhl_bound_squared(k, m)


def test_non_universal_family_fails() -> None:
    n, m = 4, 2
    # X has its first two bits 0 and the last two bits uniform: min-entropy 2 = m.
    source = flat_source([x for x in range(1 << n) if x & 0b11 == 0])
    assert min_entropy_at_least(source, 2)
    sd = extraction_distance(prefix_family(n, m), source, m)
    assert sd == 1 - Fraction(1, 1 << m)
    assert sd * sd > lhl_bound_squared(2, m)
