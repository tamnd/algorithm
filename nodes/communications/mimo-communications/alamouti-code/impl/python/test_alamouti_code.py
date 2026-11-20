# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alamouti-code/. The authors are listed in prov/04NE33.jsonl.

import math
import random

import cbb
import constel
from alamouti_code import combine, decode, encode, transmit


def _rayleigh(rng: random.Random, nr: int, amp: float = 1.0) -> list[list[complex]]:
    return [[amp * cbb.cn(rng, 1.0), amp * cbb.cn(rng, 1.0)] for _ in range(nr)]


def _noisy(rng: random.Random, x, h, n0: float):
    return [cbb.awgn(rng, row, n0) for row in transmit(x, h)]


def _mrc_bpsk(branches: int, snr: float) -> float:
    """The exact BPSK bit error rate of maximal ratio combining over i.i.d. Rayleigh branches of mean SNR snr."""
    mu = math.sqrt(snr / (1 + snr))
    return ((1 - mu) / 2) ** branches * sum(
        math.comb(branches - 1 + k, k) * ((1 + mu) / 2) ** k for k in range(branches))


def test_encoder_is_orthogonal() -> None:
    rng = random.Random(1)
    for _ in range(50):
        s1, s2 = cbb.cn(rng, 1.0), cbb.cn(rng, 1.0)
        x = encode(s1, s2)
        assert x == [[s1, -s2.conjugate()], [s2, s1.conjugate()]]
        gram = cbb.matmul(x, cbb.herm(x))
        e = abs(s1) ** 2 + abs(s2) ** 2
        assert cbb.norm2(cbb.sub(gram, cbb.scale(e, cbb.eye(2)))) < 1e-24


def test_worked_example() -> None:
    h = [[0.6 + 0.8j, -1 + 0.5j]]
    s = 1 / math.sqrt(2)
    s1, s2 = complex(s, s), complex(-s, s)
    y = transmit(encode(s1, s2), h)
    y = [[y[0][0] + (0.1 - 0.2j), y[0][1] + (-0.15 + 0.05j)]]
    z1, z2, g = combine(y, h)
    assert abs(g - 2.25) < 1e-12
    assert abs(z1 - (1.66599026 + 1.36599026j)) < 1e-7
    assert abs(z2 - (-1.74099026 + 1.89099026j)) < 1e-7
    pts = constel.qam(4)
    assert decode(y, h, pts) == (pts.index(min(pts, key=lambda p: abs(p - s1))),
                                 pts.index(min(pts, key=lambda p: abs(p - s2))))


def test_noiseless_round_trip() -> None:
    rng = random.Random(2)
    for pts in (constel.qam(4), constel.qam(16), constel.psk(8)):
        for nr in (1, 2, 3):
            for _ in range(40):
                h = _rayleigh(rng, nr)
                i1, i2 = rng.randrange(len(pts)), rng.randrange(len(pts))
                y = transmit(encode(pts[i1], pts[i2]), h)
                z1, z2, g = combine(y, h)
                assert abs(z1 - g * pts[i1]) < 1e-9 and abs(z2 - g * pts[i2]) < 1e-9
                assert decode(y, h, pts) == (i1, i2)


def test_matches_brute_force_ml() -> None:
    # The stacked real model per receive antenna i:
    # [y_i1; conj(y_i2)] = [[h_i1, h_i2], [conj(h_i2), -conj(h_i1)]] [s1; s2] + noise.
    rng = random.Random(3)
    for pts, n0 in ((constel.qam(4), 0.5), (constel.qam(16), 0.1), (constel.psk(8), 0.2)):
        for nr in (1, 2):
            for _ in range(60):
                h = _rayleigh(rng, nr)
                x = encode(rng.choice(pts), rng.choice(pts))
                y = _noisy(rng, x, h, n0)
                stack_y, stack_h = [], []
                for (a, b), (r1, r2) in zip(h, y):
                    stack_y += [r1, r2.conjugate()]
                    stack_h += [[a, b], [b.conjugate(), -a.conjugate()]]
                assert list(decode(y, h, pts)) == constel.ml_vector(stack_y, stack_h, pts)


def test_combined_noise_variance() -> None:
    # With x = 0, z_k is pure noise of variance g N0 for a fixed channel.
    rng = random.Random(4)
    h = [[0.6 + 0.8j, -1 + 0.5j], [0.3j, 0.9]]
    n0, n = 0.4, 6000
    zero = encode(0, 0)
    acc1 = acc2 = cross = 0.0
    g = 0.0
    for _ in range(n):
        z1, z2, g = combine(_noisy(rng, zero, h, n0), h)
        acc1 += abs(z1) ** 2
        acc2 += abs(z2) ** 2
        cross += (z1 * z2.conjugate()).real
    assert abs(acc1 / n / (g * n0) - 1) < 0.07
    assert abs(acc2 / n / (g * n0) - 1) < 0.07
    assert abs(cross / n) < 0.07 * g * n0


def test_bpsk_bit_error_rate_equals_mrc_of_order_2nr() -> None:
    # Total Es/N0 = gamma, each antenna sends with amplitude sqrt(1/2). The
    # combiner output has the error rate of MRC over 2 Nr branches of mean SNR gamma / 2.
    pts = constel.pam(2)
    for seed, nr, snr_db, blocks in ((5, 1, 10.0, 10000), (6, 2, 4.0, 8000)):
        rng = random.Random(seed)
        gamma = cbb.undb(snr_db)
        n0 = 1 / gamma
        errors = 0
        for _ in range(blocks):
            h = _rayleigh(rng, nr, math.sqrt(0.5))
            i1, i2 = rng.randrange(2), rng.randrange(2)
            y = _noisy(rng, encode(pts[i1], pts[i2]), h, n0)
            d1, d2 = decode(y, h, pts)
            errors += (d1 != i1) + (d2 != i2)
        expect = _mrc_bpsk(2 * nr, gamma / 2)
        assert expect * 2 * blocks >= 100
        lo, hi = cbb.wilson(errors, 2 * blocks)
        assert lo <= expect <= hi
    assert abs(_mrc_bpsk(2, 5.0) - 0.0055282) < 5e-7
    assert abs(_mrc_bpsk(4, cbb.undb(4.0) / 2) - 0.0065994) < 5e-7


def test_rejects_bad_input() -> None:
    try:
        decode([[1, 1]], [[0, 0]], constel.qam(4))
    except ValueError:
        pass
    else:
        raise AssertionError("a zero channel must raise")
    try:
        combine([[1, 1]], [[1, 1], [1, 1]])
    except ValueError:
        pass
    else:
        raise AssertionError("mismatched rows must raise")
