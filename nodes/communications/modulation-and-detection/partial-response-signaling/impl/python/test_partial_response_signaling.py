# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-response-signaling/. The authors are listed in prov/HBVC3V.jsonl.

import math
import random

import cbb
from partial_response_signaling import (
    allowed_values,
    controlled_isi,
    decode,
    decode_without_precoder,
    detect,
    levels,
    link,
    precode,
)

DUOBINARY = [1, 1]
DICODE = [1, -1]
MODIFIED = [1, 0, -1]
EPR4 = [1, 1, -1, -1]  # (1 - D)(1 + D)^2


def test_worked_example() -> None:
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    p = precode(bits, DUOBINARY, 2)
    assert p == [1, 1, 0, 1, 1, 1, 0, 0]
    a = levels(p, 2)
    assert a == [1, 1, -1, 1, 1, 1, -1, -1]
    c = controlled_isi(a, DUOBINARY, -1)
    assert c == [0, 2, 0, 0, 2, 2, 0, -2]
    assert [decode(v, DUOBINARY, 2) for v in c] == bits


def test_exercise_three() -> None:
    a = levels(precode([0, 1, 1, 0, 1], DUOBINARY, 2), 2)
    assert controlled_isi(a, DUOBINARY, -1) == [-2, 0, 0, -2, 0]


def test_allowed_values() -> None:
    assert allowed_values(DUOBINARY, 2) == [-2, 0, 2]
    assert allowed_values(MODIFIED, 2) == [-2, 0, 2]
    assert allowed_values(DUOBINARY, 4) == [-6, -4, -2, 0, 2, 4, 6]


def test_round_trip_without_noise() -> None:
    rng = random.Random(3)
    for f, m in ((DUOBINARY, 2), (DICODE, 2), (MODIFIED, 2), (EPR4, 2), (DUOBINARY, 4), (MODIFIED, 4)):
        bits = [rng.randrange(m) for _ in range(500)]
        assert link(bits, f, m) == bits


def test_one_wrong_sample_gives_one_wrong_digit() -> None:
    rng = random.Random(5)
    for f, m in ((DUOBINARY, 2), (MODIFIED, 2), (EPR4, 2), (DUOBINARY, 4)):
        allowed = allowed_values(f, m)
        bits = [rng.randrange(m) for _ in range(200)]
        c = controlled_isi(levels(precode(bits, f, m), m), f, -(m - 1))
        for k in (0, 17, 100, 199):
            bad = list(c)
            i = allowed.index(bad[k])
            bad[k] = allowed[i + 1] if i + 1 < len(allowed) else allowed[i - 1]
            got = [decode(detect(v, allowed), f, m) for v in bad]
            wrong = [j for j in range(len(bits)) if got[j] != bits[j]]
            assert wrong == [k]


def test_error_propagation_without_precoder() -> None:
    # Alternating bits make a_k + a_(k-1) = 0 from the second sample on.
    bits = [1, 0] * 20
    a = [2 * b - 1 for b in bits]
    c = controlled_isi(a, DUOBINARY, -1)
    assert decode_without_precoder(c, DUOBINARY, 2) == bits
    c[3] = 2 if c[3] == 0 else 0
    got = decode_without_precoder(c, DUOBINARY, 2)
    assert sum(g != b for g, b in zip(got, bits)) == len(bits) - 3


def test_duobinary_bit_error_rate() -> None:
    # c = 0 (probability 1/2) fails if |w| > 1; c = +-2 fails if w crosses the threshold at +-1
    # but not the far one at -+3, which gives c = -+2 and the same bit.
    # n = 10000 bits, seed 11, sigma = 0.5: Pb = 1.5 Q(2) - 0.5 Q(6) = 0.034125, about 341 errors.
    sigma, n = 0.5, 10000
    rng = random.Random(11)
    bits = [rng.randrange(2) for _ in range(n)]
    noise = [rng.gauss(0.0, sigma) for _ in range(n)]
    got = link(bits, DUOBINARY, 2, noise)
    errors = sum(g != b for g, b in zip(got, bits))
    want = 1.5 * cbb.qfunc(1 / sigma) - 0.5 * cbb.qfunc(3 / sigma)
    assert n * want >= 100
    lo, hi = cbb.wilson(errors, n)
    assert lo <= want <= hi, (errors, n, lo, hi, want)


def test_symbol_by_symbol_loss() -> None:
    # The equal split of |X(f)| = 2T cos(pi f T) scales energy and noise by its integral 4/pi.
    steps = 100000
    integral = sum(2 * math.cos(math.pi * (-0.5 + (i + 0.5) / steps)) for i in range(steps)) / steps
    assert abs(integral - 4 / math.pi) < 1e-9
    assert abs(20 * math.log10(4 / math.pi) - 2.098) < 5e-4
    # The duobinary pulse at t = T/2.
    x = 2 * math.sin(math.pi / 2) / (math.pi / 2)
    assert abs(x - 4 / math.pi) < 1e-15
