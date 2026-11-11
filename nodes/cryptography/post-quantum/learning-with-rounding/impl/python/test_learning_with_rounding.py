# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-with-rounding/. The authors are listed in prov/DNQHCE.jsonl.
"""Tests for LWR sampling and the toy BPR direct PRF.

LWR is a problem and the PRF is a research construction, so there are no
official test vectors. The tests check the rounding map, the relation of
the samples, the agreement of rounded LWE with LWR, and basic properties of
the PRF on toy parameters.
"""

import itertools
import random
from collections import Counter

from learning_with_rounding import BPRDirectPRF, lwe_then_round, round_p, sample_lwr


def test_round_small():
    # q = 16, p = 4: (p/q) x = x / 4, rounded to nearest, mod 4.
    got = [round_p(x, 16, 4) for x in range(16)]
    assert got == [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 0, 0]


def test_round_uniform_when_p_divides_q():
    q, p = 1 << 10, 1 << 4
    counts = Counter(round_p(x, q, p) for x in range(q))
    assert set(counts.values()) == {q // p}


def test_round_matches_float():
    rng = random.Random(1)
    for _ in range(500):
        q = rng.randrange(17, 5000)
        p = rng.randrange(2, q)
        x = rng.randrange(q)
        want = int((p * x / q) + 0.5) % p  # nonnegative, so int() floors
        assert round_p(x, q, p) == want or abs(p * x / q - int(p * x / q) - 0.5) < 1e-9


def test_lwr_relation():
    rng = random.Random(2)
    q, p, n = 1 << 12, 1 << 4, 8
    A, b, s = sample_lwr(n, 50, q, p, rng)
    for row, bi in zip(A, b):
        exact = sum(x * y for x, y in zip(row, s)) % q
        assert abs(p * exact / q - bi) <= 0.5 or abs(p * exact / q - p - bi) <= 0.5


def test_rounded_lwe_agrees_with_lwr_when_q_over_p_is_large():
    # An error of size at most B changes the rounding only when <a, s> is
    # within B of a rounding boundary: probability at most 2 B p / q per sample.
    rng = random.Random(3)
    q, p, n, m, B = 1 << 16, 1 << 4, 8, 2000, 2
    A, b, s = sample_lwr(n, m, q, p, rng)
    e = [rng.randint(-B, B) for _ in range(m)]
    rounded = lwe_then_round(A, s, e, q, p)
    differ = sum(x != y for x, y in zip(rounded, b))
    assert differ <= 3  # expected at most 2000 * 2 * 2 * 16 / 65536, about 2
    # With q / p small the two disagree often.
    q2 = 1 << 6
    A2, b2, s2 = sample_lwr(n, m, q2, p, rng)
    e2 = [rng.randint(-B, B) for _ in range(m)]
    differ2 = sum(x != y for x, y in zip(lwe_then_round(A2, s2, e2, q2, p), b2))
    assert differ2 > m // 10


def test_prf_deterministic_and_in_range():
    rng = random.Random(4)
    F = BPRDirectPRF(n=4, k=8, q=1 << 16, p=1 << 4, rng=rng)
    x = [1, 0, 1, 1, 0, 0, 1, 0]
    y = F(x)
    assert y == F(x)
    assert len(y) == 4 and all(0 <= v < 16 for v in y)
    # The empty product: F(0...0) = round_p(a).
    assert F([0] * 8) == [round_p(v, 1 << 16, 16) for v in F.a]


def test_prf_outputs_spread():
    rng = random.Random(5)
    F = BPRDirectPRF(n=4, k=8, q=1 << 16, p=1 << 4, rng=rng)
    outs = [tuple(F(list(x))) for x in itertools.product((0, 1), repeat=8)]
    # 256 inputs, 16^4 = 65536 possible outputs: nearly all distinct.
    assert len(set(outs)) >= 250
    # Each output coordinate is close to uniform over Z_16.
    counts = Counter(v for o in outs for v in o)
    assert all(30 <= c <= 100 for c in counts.values()) and len(counts) == 16


def test_prf_rejects_bad_input():
    F = BPRDirectPRF(n=2, k=3, q=257, p=4, rng=random.Random(6))
    for bad in ([0, 1], [0, 1, 2]):
        try:
            F(bad)
        except ValueError:
            continue
        raise AssertionError("bad input accepted")
