# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-sampling-lsh/. The authors are listed in prov/PZGBBJ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from bit_sampling_lsh import BitSamplingLSH, hamming


def to_int(s: str) -> int:
    """Bit i of the result is character i of s."""
    return sum(1 << i for i, ch in enumerate(s) if ch == "1")


P = [to_int(s) for s in ["00010111", "11100000", "11010010", "01011011", "00111100", "10110100"]]
Q = to_int("10110001")


def test_example() -> None:
    idx = BitSamplingLSH(P, 8, 3, 2, positions=[[0, 2, 5], [4, 6, 7]])
    assert idx.key(0, Q) == (1, 1, 0)
    assert idx.tables[0][(1, 1, 0)] == [1]
    assert idx.key(1, Q) not in idx.tables[1]
    assert idx.query(Q, 2, 1) is None
    assert idx.query(Q, 2, 2) == 1


def test_collision_probability_exact() -> None:
    d = 6
    for x, y in itertools.product(range(1 << d), repeat=2):
        if (x * 7 + y) % 37:
            continue
        same = sum(((x >> i) & 1) == ((y >> i) & 1) for i in range(d))
        assert Fraction(same, d) == 1 - Fraction(hamming(x, y), d)


def test_rho_at_most_one_over_c() -> None:
    for d in range(2, 60):
        for r in range(1, d):
            for c in (1.1, 1.5, 2, 3, 4.5):
                if c * r < d:
                    rho = math.log(1 / (1 - r / d)) / math.log(1 / (1 - c * r / d))
                    assert rho <= 1 / c + 1e-12


def test_answers_are_valid_against_brute_force() -> None:
    rng = random.Random(31337)
    for _ in range(500):
        d = rng.randint(1, 20)
        pts = [rng.randrange(1 << d) for _ in range(rng.randint(0, 25))]
        q = rng.randrange(1 << d)
        idx = BitSamplingLSH(pts, d, rng.randint(1, 4), rng.randint(1, 4), rng)
        r, c = rng.randint(0, 3), 2
        got = idx.query(q, c, r)
        if got is not None:
            assert hamming(q, pts[got]) <= c * r
        if not pts or min(hamming(q, p) for p in pts) > c * r:
            assert got is None


def test_success_rate() -> None:
    rng = random.Random(5)
    d, n, r, c = 32, 60, 2, 2
    p1, p2 = 1 - r / d, 1 - c * r / d
    k = math.ceil(math.log(n) / math.log(1 / p2))
    L = math.ceil(n ** (math.log(1 / p1) / math.log(1 / p2)) / p1)
    ok = 0
    for _ in range(300):
        pts = [rng.randrange(1 << d) for _ in range(n)]
        q = pts[0] ^ (1 << rng.randrange(d)) ^ (1 << rng.randrange(d))
        got = BitSamplingLSH(pts, d, k, L, rng).query(q, c, r)
        ok += got is not None
    assert ok / 300 >= 2 / 3 - 1 / math.e
