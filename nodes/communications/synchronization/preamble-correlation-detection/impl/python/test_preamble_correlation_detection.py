# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preamble-correlation-detection/. The authors are listed in prov/31P2YC.jsonl.

import cmath
import math
import random

from cbb import cn, wilson
from preamble_correlation_detection import (
    detect,
    normalized_correlation,
    phase_of,
    recompute_energy,
    threshold_for_pfa,
)

BARKER13 = [complex(v) for v in (1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1)]


def rho_direct(y, s, n):
    """|sum conj(s) y|^2 / (E_s E(n)) with every sum taken afresh."""
    c = sum(si.conjugate() * y[n + i] for i, si in enumerate(s))
    es = sum(abs(v) ** 2 for v in s)
    return abs(c) ** 2 / (es * recompute_energy(y, n, len(s)))


def test_threshold_formula():
    lam = threshold_for_pfa(1e-6, 13)
    assert abs(lam - (1 - 10 ** -0.5)) < 1e-12
    assert abs((1 - lam) ** 12 - 1e-6) < 1e-18


def test_finds_clean_preamble_with_unknown_gain():
    rng = random.Random(1)
    gain = 0.5 * cmath.exp(0.7j)
    y = [cn(rng, 1.0) for _ in range(37)] + [gain * v for v in BARKER13] + [cn(rng, 1.0) for _ in range(30)]
    found = detect(y, BARKER13, threshold_for_pfa(1e-6, 13))
    assert found is not None
    n, r, g = found
    assert n == 37
    assert abs(r - 1.0) < 1e-12
    assert abs(g - gain) < 1e-12
    assert abs(phase_of(g) - 0.7) < 1e-12


def test_running_energy_matches_direct_sums():
    rng = random.Random(2)
    y = [cn(rng, 2.0) for _ in range(300)]
    rho = normalized_correlation(y, BARKER13)
    assert len(rho) == 300 - 13 + 1
    for n, r in enumerate(rho):
        assert abs(r - rho_direct(y, BARKER13, n)) < 1e-9
        assert 0.0 <= r <= 1.0 + 1e-12


def test_scale_invariance():
    rng = random.Random(3)
    y = [cn(rng, 1.0) for _ in range(100)]
    c = 3.0 * cmath.exp(1.3j)
    r1 = normalized_correlation(y, BARKER13)
    r2 = normalized_correlation([c * v for v in y], BARKER13)
    assert max(abs(a - b) for a, b in zip(r1, r2)) < 1e-12


def test_false_alarm_rate_on_noise():
    # P(rho >= lambda) = (1 - lambda)^(L - 1) for any noise level. lambda = 0.25
    # and L = 13 give 0.0317, so 5000 trials expect 158 false alarms.
    rng = random.Random(4)
    lam, trials, hits = 0.25, 5000, 0
    for _ in range(trials):
        var = rng.uniform(0.01, 100.0)
        y = [cn(rng, var) for _ in range(13)]
        hits += normalized_correlation(y, BARKER13)[0] >= lam
    p = (1 - lam) ** 12
    assert trials * p >= 100
    lo, hi = wilson(hits, trials)
    assert lo <= p <= hi


def test_no_detection_on_noise_with_low_false_alarm_rate():
    rng = random.Random(5)
    y = [cn(rng, 1.0) for _ in range(1000)]
    assert detect(y, BARKER13, threshold_for_pfa(1e-6, 13)) is None


def test_detects_noisy_preamble():
    # Es/N0 = 10 dB per symbol and a random carrier phase. At the true start rho is
    # about SNR / (1 + SNR) = 0.91, well above lambda = 0.684.
    rng = random.Random(6)
    lam = threshold_for_pfa(1e-6, 13)
    good = 0
    for _ in range(100):
        start = rng.randrange(20, 60)
        g = cmath.exp(1j * rng.uniform(-math.pi, math.pi))
        y = [cn(rng, 0.1) for _ in range(start)] + [g * v + cn(rng, 0.1) for v in BARKER13] + [cn(rng, 0.1) for _ in range(20)]
        found = detect(y, BARKER13, lam)
        good += found is not None and found[0] == start
    assert good >= 95
