# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schmidl-cox-synchronization/. The authors are listed in prov/HGVMCQ.jsonl.

import cmath
import math
import random

import cbb
from schmidl_cox_synchronization import (
    apply_cfo,
    fractional_offset,
    synchronize,
    timing_estimate,
    timing_metric,
    training_symbols,
)


def with_prefix(xf: list[complex], ncp: int) -> list[complex]:
    x = cbb.uidft(xf)
    return x[len(x) - ncp:] + x


def frame(rng: random.Random, n: int, ncp: int, lead: int) -> tuple[list[complex], list[complex]]:
    """lead zero samples, the two training symbols with prefixes, one data symbol."""
    x1, x2, v = training_symbols(n, rng)
    data = [cbb.cn(rng, 1.0) for _ in range(n)]
    s = [0j] * lead + with_prefix(x1, ncp) + with_prefix(x2, ncp) + with_prefix(data, ncp)
    return s, v


def test_first_training_symbol_has_two_equal_halves() -> None:
    rng = random.Random(1)
    for n in (8, 64, 256):
        x1, _, _ = training_symbols(n, rng)
        x = cbb.uidft(x1)
        assert max(abs(x[m] - x[m + n // 2]) for m in range(n // 2)) < 1e-12
        assert abs(cbb.norm2(x) - n) < 1e-9


def test_recursive_metric_matches_the_direct_sums() -> None:
    rng = random.Random(2)
    r = [cbb.cn(rng, 1.0) for _ in range(100)]
    half = 16
    ps, rs, ms = timing_metric(r, half)
    for d in (0, 7, 40, 68):
        p = sum(r[d + m].conjugate() * r[d + m + half] for m in range(half))
        e = sum(abs(r[d + m + half]) ** 2 for m in range(half))
        assert abs(ps[d] - p) < 1e-9
        assert abs(rs[d] - e) < 1e-9
        assert abs(ms[d] - abs(p) ** 2 / e ** 2) < 1e-9


def test_plateau_without_noise() -> None:
    # Channel of 3 taps, prefix 8: M(d) = 1 for the ncp - L + 2 = 7 starts d with an ISI-free window.
    rng = random.Random(3)
    n, ncp, lead = 64, 8, 20
    s, _ = frame(rng, n, ncp, lead)
    r = cbb.conv(s, [0.9, 0.4j, -0.2])
    _, _, ms = timing_metric(r, n // 2)
    ones = [d for d, m in enumerate(ms) if abs(m - 1) < 1e-9]
    assert ones == list(range(lead + 2, lead + ncp + 1))
    # R(d) is the energy of the second half only, so M(d) can pass 1 next to the plateau.
    assert max(ms) > 1.01
    assert lead + 2 <= timing_estimate(ms, "plateau") <= lead + ncp


def test_offsets_without_noise() -> None:
    rng = random.Random(4)
    n, ncp, lead = 64, 8, 20
    for eps in (0.12, -0.45, 0.83, 4.3, -1.7, -6.25):
        s, v = frame(rng, n, ncp, lead)
        r = apply_cfo(cbb.conv(s, [0.9, 0.4j, -0.2]), eps, n)
        d, e = synchronize(r, n, ncp, v, method="plateau")
        assert lead + 2 <= d <= lead + ncp
        assert abs(e - eps) < 1e-9


def test_fractional_part_wraps() -> None:
    assert abs(fractional_offset(cmath.exp(1j * math.pi * 4.3)) - 0.3) < 1e-12
    assert abs(fractional_offset(cmath.exp(-1j * math.pi * 1.7)) - 0.3) < 1e-12


def test_timing_and_offset_at_moderate_snr() -> None:
    # AWGN, SNR = 10 dB per sample, N = 64, ncp = 8, epsilon = 2.12, 100 frames, seed 5.
    # The ISI-free starts are lead, ..., lead + ncp, with the middle at lead + 4.
    # The plateau estimate spreads by a few samples around the middle (a measurement).
    rng = random.Random(5)
    n, ncp, lead, n0, eps = 64, 8, 30, 0.1, 2.12
    good_t = good_f = 0
    total = 0
    trials = 100
    for _ in range(trials):
        s, v = frame(rng, n, ncp, lead)
        r = cbb.awgn(rng, apply_cfo(s, eps, n), n0)
        d, e = synchronize(r, n, ncp, v, method="plateau", gmax=3)
        good_t += lead <= d <= lead + ncp
        good_f += abs(e - eps) < 0.05
        total += d - lead
    assert good_t >= 0.9 * trials
    assert 3 <= total / trials <= 5
    assert good_f == trials


def test_variance_of_the_fractional_estimate() -> None:
    # At the true timing, var(eps_f) is about (1 / (pi^2 L SNR)) (1 + 1 / (2 SNR)), L = N / 2.
    # N = 64, SNR = 10 dB: 3.3245e-4. 2000 trials, seed 6, ratio within 0.85 to 1.15.
    rng = random.Random(6)
    n, ncp, n0, eps = 64, 8, 0.1, 0.12
    snr, half = 1 / n0, n // 2
    expect = (1 + 1 / (2 * snr)) / (math.pi ** 2 * half * snr)
    assert abs(expect - 3.3245e-4) < 1e-7
    acc = 0.0
    trials = 2000
    x1, _, _ = training_symbols(n, rng)
    x = apply_cfo(with_prefix(x1, ncp), eps, n)
    for _ in range(trials):
        r = cbb.awgn(rng, x, n0)
        ps, _, _ = timing_metric(r[ncp:ncp + n], half)
        acc += (fractional_offset(ps[0]) - eps) ** 2
    ratio = acc / trials / expect
    assert 0.85 < ratio < 1.15
