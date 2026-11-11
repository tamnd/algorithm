# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birthday-attack/. The authors are listed in prov/4ZQ3BQ.jsonl.

import hashlib
import math
import random

from birthday_attack import (
    birthday_attack,
    collision_probability,
    lower_bound,
    queries_for,
    upper_bound,
)


def trunc_sha256(n: int):
    """SHA-256 cut down to its first n bits: the toy target."""

    def h(x: bytes) -> int:
        return int.from_bytes(hashlib.sha256(x).digest()[:4], "big") >> (32 - n)

    return h


def test_finds_real_collision_24_bits() -> None:
    h = trunc_sha256(24)
    x1, x2, q = birthday_attack(h, b"hf1-24:")
    assert x1 != x2
    assert h(x1) == h(x2)
    assert q < 1 << 15  # 2^12 expected, 8 times that is very unlikely


def test_finds_real_collision_32_bits() -> None:
    h = trunc_sha256(32)
    x1, x2, q = birthday_attack(h, b"hf1-32:")
    assert x1 != x2
    d1 = hashlib.sha256(x1).digest()
    d2 = hashlib.sha256(x2).digest()
    assert d1[:4] == d2[:4] and d1 != d2
    assert q < 1 << 19


def test_average_cost_matches_sqrt_pi_n_over_2() -> None:
    # Mean number of queries to the first collision is about sqrt(pi 2^n / 2).
    n = 16
    h = trunc_sha256(n)
    qs = [birthday_attack(h, b"run%d:" % r)[2] for r in range(300)]
    mean = sum(qs) / len(qs)
    want = math.sqrt(math.pi * (1 << n) / 2) + 2 / 3
    assert abs(mean - want) / want < 0.08


def test_formulas_against_simulation() -> None:
    rng = random.Random(20240611)
    n = 16
    big_n = 1 << n
    for q in (100, 302, 500):
        hits = 0
        trials = 3000
        for _ in range(trials):
            seen = set()
            for _ in range(q):
                v = rng.randrange(big_n)
                if v in seen:
                    hits += 1
                    break
                seen.add(v)
        p_sim = hits / trials
        p = collision_probability(q, n)
        assert abs(p_sim - p) < 4 * math.sqrt(p * (1 - p) / trials) + 0.005
        assert lower_bound(q, n) <= p <= upper_bound(q, n) + 1e-12
        # Katz and Lindell lower bound q(q-1)/(4N) for q <= sqrt(2N)
        if q <= math.sqrt(2 * big_n):
            assert p >= q * (q - 1) / (4 * big_n)


def test_half_point() -> None:
    n = 32
    q = queries_for(0.5, n)
    assert abs(q / 2 ** (n / 2) - 1.1774) < 1e-4
    assert abs(collision_probability(round(q), n) - 0.5) < 1e-3


def test_edges() -> None:
    assert collision_probability(0, 8) == 0.0
    assert collision_probability(1, 8) == 0.0
    assert collision_probability(257, 8) == 1.0
    assert upper_bound(2, 8) == 1 / 256
