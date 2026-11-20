# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclostationary-feature-detection/. The authors are listed in prov/XYTR6D.jsonl.

import cmath
import math
import random

import pytest

from cbb import cn, undb, wilson
from cyclostationary_feature_detection import (
    _ncx_tail,
    cyclic_autocorrelation,
    cyclic_detect,
    cyclic_scan,
    cyclic_statistic,
    pd_bpsk,
    scan_detect,
    scan_threshold,
)


def bpsk(rng: random.Random, n: int, power: float, fc: float) -> list[complex]:
    """BPSK symbols, one per sample, on carrier fc with a random phase."""
    ph = rng.uniform(0.0, 2.0 * math.pi)
    return [math.sqrt(power) * rng.choice((-1, 1)) * cmath.exp(1j * (2 * math.pi * fc * i + ph)) for i in range(n)]


def simpson(f, a: float, b: float, steps: int = 4000) -> float:
    h = (b - a) / steps
    s = f(a) + f(b)
    for i in range(1, steps):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def test_page_example() -> None:
    # eight noiseless BPSK samples on carrier 1/8: y[n]^2 e^(-j 2 pi n / 4) = 1 for every n
    y = [(1 if i % 3 else -1) * cmath.exp(1j * math.pi * i / 4) for i in range(8)]
    assert cyclic_autocorrelation(y, 0.25, 0) == pytest.approx(1.0)
    present, t, lam = cyclic_detect(y, 0.25, 0, 0.05)
    assert t == pytest.approx(4.0)
    assert lam == pytest.approx(-math.log(0.05))
    assert present
    # at the wrong cycle frequency 1/8 the rotations cancel over the eight samples
    assert cyclic_statistic(y, 0.125, 0) == pytest.approx(0.0, abs=1e-20)


def test_scan_matches_direct_sum() -> None:
    rng = random.Random(3)
    y = [cn(rng, 1.0) for _ in range(16)]
    rs = cyclic_scan(y, 0)
    for k in range(16):
        assert rs[k] == pytest.approx(cyclic_autocorrelation(y, k / 16, 0), abs=1e-12)
    rs = cyclic_scan(y, 2, conjugate=False)
    assert len(rs) == 14
    for k in range(14):
        assert rs[k] == pytest.approx(cyclic_autocorrelation(y, k / 14, 2, conjugate=False), abs=1e-12)


def test_no_noise_power_needed() -> None:
    rng = random.Random(4)
    y = [cn(rng, 1.0) for _ in range(40)]
    for c in (1e-3, 3.7j, 250.0):
        z = [c * v for v in y]
        assert cyclic_statistic(z, 0.2, 0) == pytest.approx(cyclic_statistic(y, 0.2, 0), rel=1e-9)
        assert cyclic_statistic(z, 0.1, 3, conjugate=False) == pytest.approx(
            cyclic_statistic(y, 0.1, 3, conjugate=False), rel=1e-9
        )


def test_false_alarm_rate() -> None:
    rng = random.Random(5)
    n, pfa, trials = 128, 0.1, 1500
    lam = -math.log(pfa)
    # the conjugate test at tau = 0, noise power 1
    hits = sum(cyclic_statistic([cn(rng, 1.0) for _ in range(n)], 0.2, 0) > lam for _ in range(trials))
    lo, hi = wilson(hits, trials)
    assert lo <= pfa <= hi
    # the non-conjugate test at tau = 3, noise power 4, with the same threshold
    hits = sum(
        cyclic_statistic([cn(rng, 4.0) for _ in range(n)], 0.13, 3, conjugate=False) > lam for _ in range(trials)
    )
    lo, hi = wilson(hits, trials)
    assert lo <= pfa <= hi


def test_bpsk_detection() -> None:
    rng = random.Random(6)
    n, pfa, trials, fc = 64, 0.1, 1000, 0.1
    snr = undb(-5.0)
    p = pd_bpsk(n, snr, pfa)
    assert p == pytest.approx(0.5074, abs=1e-4)
    hits = 0
    for _ in range(trials):
        y = [v + cn(rng, 1.0) for v in bpsk(rng, n, snr, fc)]
        hits += cyclic_detect(y, 2 * fc, 0, pfa)[0]
    lo, hi = wilson(hits, trials)
    assert lo <= p <= hi


def test_qpsk_has_no_conjugate_feature() -> None:
    # QPSK symbols squared are +-j with mean 0, so a strong QPSK signal does not raise T like BPSK does
    rng = random.Random(7)
    n, pfa, trials, fc = 128, 0.1, 1000, 0.1
    power = undb(10.0)
    hits_qpsk = hits_bpsk = 0
    for _ in range(trials):
        q = [
            math.sqrt(power) * cmath.exp(1j * (math.pi / 4 * (2 * rng.randrange(4) + 1) + 2 * math.pi * fc * i))
            for i in range(n)
        ]
        hits_qpsk += cyclic_detect([v + cn(rng, 1.0) for v in q], 2 * fc, 0, pfa)[0]
    for _ in range(100):
        hits_bpsk += cyclic_detect([v + cn(rng, 1.0) for v in bpsk(rng, n, power, fc)], 2 * fc, 0, pfa)[0]
    lo, hi = wilson(hits_qpsk, trials)
    assert hi < pfa
    assert hits_bpsk == 100


def test_cyclic_prefix_feature() -> None:
    # blocks of 16 Gaussian samples with a cyclic prefix of 4: y[n + 16] conj(y[n]) has period 20
    rng = random.Random(8)
    body, cp, blocks, trials = 16, 4, 20, 300
    hits = 0
    for _ in range(trials):
        x = []
        for _ in range(blocks):
            b = [cn(rng, 1.0) for _ in range(body)]
            x += b[body - cp :] + b
        y = [v + cn(rng, 1.0) for v in x]
        hits += cyclic_detect(y, 1 / (body + cp), body, 0.05, conjugate=False)[0]
    lo, hi = wilson(hits, trials)
    assert lo > 0.5


def test_scan() -> None:
    assert scan_threshold(0.1, 1) == pytest.approx(-math.log(0.1))
    lam = scan_threshold(0.05, 64)
    assert 1 - (1 - math.exp(-lam)) ** 64 == pytest.approx(0.05, rel=1e-12)
    rng = random.Random(9)
    # unknown carrier 5/64: the feature is at alpha = 10/64
    y = [v + cn(rng, 1.0) for v in bpsk(rng, 64, undb(3.0), 5 / 64)]
    present, k, t, lam = scan_detect(y, 0, 0.05)
    assert present and k == 10
    # under noise only, the max over 64 bins keeps the rate at or below P_fa
    trials, hits = 400, 0
    for _ in range(trials):
        hits += scan_detect([cn(rng, 1.0) for _ in range(64)], 0, 0.1)[0]
    lo, hi = wilson(hits, trials)
    assert lo <= 0.1


def test_noncentral_tail_and_sample_count() -> None:
    mu, x = 3.0, 4.0
    dens = lambda t: math.exp(-t - mu) * sum((mu * t) ** j / math.factorial(j) ** 2 for j in range(60))
    assert _ncx_tail(mu, x) == pytest.approx(simpson(dens, x, 60.0, 6000), rel=1e-8)
    assert _ncx_tail(0.0, 2.0) == pytest.approx(math.exp(-2.0))
    assert pd_bpsk(100, 0.0, 0.05) == pytest.approx(0.05)
    snr = undb(-10.0)
    assert pd_bpsk(1263, snr, 0.1) >= 0.9 > pd_bpsk(1262, snr, 0.1)


def test_errors() -> None:
    y = [1 + 0j, 1j, -1 + 0j]
    with pytest.raises(ValueError):
        cyclic_statistic(y, 0.1, 0, conjugate=False)
    with pytest.raises(ValueError):
        cyclic_statistic(y, 0.1, 3)
    with pytest.raises(ValueError):
        cyclic_detect(y, 0.1, 0, 1.0)
