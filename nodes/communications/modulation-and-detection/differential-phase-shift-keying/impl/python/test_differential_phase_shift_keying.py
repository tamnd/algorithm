# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-phase-shift-keying/. The authors are listed in prov/3Q2A6K.jsonl.

import math
import random

import cbb
from differential_phase_shift_keying import (
    asymptotic_loss_db,
    detect,
    detect_coherent,
    encode,
    gray,
    gray_inverse,
    rotate,
)


def close(a: list[complex], b: list[complex]) -> bool:
    return len(a) == len(b) and all(abs(x - y) < 1e-12 for x, y in zip(a, b))


def test_dbpsk_worked_example() -> None:
    bits = [1, 0, 1, 1, 0]
    s = encode(bits, 2)
    assert close(s, [1, -1, -1, 1, -1, -1])
    # An unknown phase of 0.7 rad changes every symbol and no decision.
    r = rotate(s, 0.7)
    z = [cur * prev.conjugate() for prev, cur in zip(r, r[1:])]
    assert close(z, [-1, 1, -1, -1, 1])
    assert detect(r, 2) == bits


def test_dqpsk_worked_example() -> None:
    # 00, 01, 11, 10 give the steps 0, 90, 180 and 270 degrees.
    s = encode([0, 0, 0, 1, 1, 1, 1, 0], 4)
    assert close(s, [1, 1, 1j, -1j, -1])
    assert [gray_inverse(u) for u in range(4)] == [0, 1, 3, 2]
    assert all(gray(gray_inverse(u)) == u for u in range(64))


def test_round_trip_with_unknown_phase_and_drift() -> None:
    rng = random.Random(5)
    for m in (2, 4, 8, 16):
        k = m.bit_length() - 1
        bits = [rng.randrange(2) for _ in range(600 * k)]
        s = encode(bits, m)
        assert all(abs(abs(v) - 1) < 1e-9 for v in s)
        # A frequency offset of 0.005/T turns 1.8 degrees per symbol, inside the margin 180/M.
        r = rotate(s, rng.uniform(-math.pi, math.pi), 0.005)
        assert detect(r, m) == bits


def test_coherent_detection_needs_the_phase() -> None:
    rng = random.Random(6)
    bits = [rng.randrange(2) for _ in range(800)]
    r = rotate(encode(bits, 4), 0.3, 0.005)
    # The drift reaches 45 degrees after 25 symbols, and the coherent decisions slip.
    wrong = sum(a != b for a, b in zip(detect_coherent(r, 4, 0.3), bits))
    assert wrong > 0
    assert detect(r, 4) == bits
    # With the exact phase, coherent detection and differential decoding recover the bits.
    assert detect_coherent(rotate(encode(bits, 4), 0.3), 4, 0.3) == bits


def test_differential_detector_is_the_two_symbol_noncoherent_rule() -> None:
    # For DBPSK, Re(r_k conj r_(k-1)) > 0 exactly when |r_k + r_(k-1)| > |r_k - r_(k-1)|.
    rng = random.Random(8)
    for _ in range(2000):
        a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        lhs = abs(a + b) ** 2 - abs(a - b) ** 2
        assert abs(lhs - 4 * (a * b.conjugate()).real) < 1e-9


def test_dbpsk_bit_error_rate() -> None:
    # Eb/N0 = 4 (6.02 dB): Pb = exp(-4)/2 = 0.009158. n = 20000 bits, seed 21, about 183 errors.
    ebn0, n = 4.0, 20000
    rng = random.Random(21)
    bits = [rng.randrange(2) for _ in range(n)]
    s = encode(bits, 2)
    r = [v + cbb.cn(rng, 1 / ebn0) for v in rotate(s, 1.1)]
    errors = sum(a != b for a, b in zip(detect(r, 2), bits))
    want = 0.5 * math.exp(-ebn0)
    assert n * want >= 100
    lo, hi = cbb.wilson(errors, n)
    assert lo <= want <= hi, (errors, n, lo, hi, want)


def test_coherent_differentially_encoded_bpsk_doubles_the_errors() -> None:
    # Eb/N0 = 4: p = Q(sqrt(8)) = 0.002339 per decision, Pb = 2p(1 - p) = 0.004667.
    # n = 40000 bits, seed 22, about 187 errors.
    ebn0, n = 4.0, 40000
    rng = random.Random(22)
    bits = [rng.randrange(2) for _ in range(n)]
    r = [v + cbb.cn(rng, 1 / ebn0) for v in encode(bits, 2)]
    errors = sum(a != b for a, b in zip(detect_coherent(r, 2), bits))
    p = cbb.qfunc(math.sqrt(2 * ebn0))
    want = 2 * p * (1 - p)
    assert n * want >= 100
    lo, hi = cbb.wilson(errors, n)
    assert lo <= want <= hi, (errors, n, lo, hi, want)


def test_numbers_on_the_page() -> None:
    # DBPSK at 10 dB, and the Eb/N0 for 1e-5 with DBPSK and with coherent BPSK.
    assert abs(0.5 * math.exp(-10) - 2.270e-5) < 1e-8
    assert abs(10 * math.log10(math.log(5e4)) - 10.34) < 5e-3
    assert abs(10 * math.log10(cbb.qinv(1e-5) ** 2 / 2) - 9.59) < 5e-3
    # The high-SNR loss of M-DPSK against M-PSK.
    assert abs(asymptotic_loss_db(2)) < 1e-12
    assert abs(asymptotic_loss_db(4) - 2.32) < 5e-3
    assert abs(asymptotic_loss_db(8) - 2.84) < 5e-3
    assert abs(asymptotic_loss_db(16) - 2.97) < 5e-3
    assert abs(asymptotic_loss_db(1024) - 10 * math.log10(2)) < 1e-4
