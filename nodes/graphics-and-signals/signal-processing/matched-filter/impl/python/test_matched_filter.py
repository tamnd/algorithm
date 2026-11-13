# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matched-filter/. The authors are listed in prov/3Q26KM.jsonl.

import math
import random
from fractions import Fraction

import pytest

from matched_filter import (
    colored_snr,
    detect,
    detection_probability,
    fir,
    matched_filter,
    output_snr,
    q_function,
    q_inverse,
    threshold,
    whitened_template,
)


def rand_frac(rng, lo=-6, hi=6):
    return Fraction(rng.randint(lo, hi), rng.randint(1, 4))


def test_page_example() -> None:
    s = [1, 2, 2, -1]
    h = matched_filter(s)
    assert h == [-1, 2, 2, 1]
    x = [0, 0, 1, 2, 2, -1, 0, 0]
    y = fir(h, x)
    assert y == [0, 0, -1, 0, 4, 10, 4, 0]
    assert max(range(len(y)), key=lambda n: y[n]) == 5
    assert output_snr(h, s, 1) == 10
    assert output_snr([1, 1, 1, 1], s, 1) == 4
    assert output_snr([1, 0, 0, 0], s, 1) == 1
    # sigma^2 = 1, P_FA = 1e-3: gamma = sqrt(10) * 3.0902 = 9.772, so only the peak crosses.
    assert abs(threshold(s, 1.0, 1e-3) - 9.7722) < 1e-4
    assert detect(x, s, 1.0, 1e-3) == [2]
    # A tiny threshold also fires on the side lobes y[4] = y[6] = 4.
    assert detect(x, s, 1e-6, 1e-3) == [1, 2, 3]
    assert matched_filter([1j, 2]) == [2, -1j]


def test_matched_filter_maximizes_snr_exactly() -> None:
    # Cauchy-Schwarz: for every h, SNR(h) <= E / sigma^2, with equality for h = c s reversed.
    rng = random.Random(5101)
    for _ in range(500):
        n = rng.randint(1, 8)
        s = [rand_frac(rng) for _ in range(n)]
        if all(v == 0 for v in s):
            s[0] = Fraction(1)
        sigma2 = Fraction(rng.randint(1, 9), rng.randint(1, 4))
        energy = sum(v * v for v in s)
        best = output_snr(matched_filter(s), s, sigma2)
        assert best == energy / sigma2
        c = rand_frac(rng, 1, 9)
        assert output_snr(matched_filter(s, c), s, sigma2) == best
        h = [rand_frac(rng) for _ in range(n)]
        if all(v == 0 for v in h):
            continue
        snr = output_snr(h, s, sigma2)
        assert snr <= best
        ratio = None
        proportional = True
        for hv, sv in zip(h, reversed(s)):
            if sv == 0:
                proportional = proportional and hv == 0
            else:
                ratio = hv / sv if ratio is None else ratio
                proportional = proportional and hv == ratio * sv
        assert (snr == best) == proportional


def test_whitened_filter_is_optimal_in_colored_noise() -> None:
    rng = random.Random(5102)
    for _ in range(300):
        n = rng.randint(1, 5)
        b = [[rand_frac(rng) for _ in range(n)] for _ in range(n)]
        cov = [[sum(b[i][k] * b[j][k] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
        s = [rand_frac(rng) for _ in range(n)]
        if all(v == 0 for v in s):
            s[0] = Fraction(1)
        w = whitened_template(s, cov)
        best = colored_snr(w, s, cov)
        assert best == sum(wi * si for wi, si in zip(w, s))
        for _ in range(3):
            v = [rand_frac(rng) for _ in range(n)]
            if any(t != 0 for t in v):
                assert colored_snr(v, s, cov) <= best


def test_q_function_and_inverse() -> None:
    assert q_function(0) == 0.5
    assert abs(q_inverse(1e-3) - 3.090232306167813) < 1e-9
    assert abs(q_inverse(0.1) - 1.2815515655446004) < 1e-9
    for p in (1e-9, 1e-4, 0.3, 0.5, 0.9):
        assert abs(q_function(q_inverse(p)) - p) < 1e-12 * max(1, p / 1e-9)
    with pytest.raises(ValueError):
        q_inverse(0)


def test_neyman_pearson_false_alarm_and_detection_rates() -> None:
    # Pulse of 16 samples, energy E = 16 * 0.25 = 4, sigma^2 = 1, P_FA = 0.01, 20000 trials each.
    s = [0.5 if (n * 7) % 3 else -0.5 for n in range(16)]
    energy = sum(v * v for v in s)
    sigma2, pfa, trials = 1.0, 0.01, 20000
    gamma = threshold(s, sigma2, pfa)
    rng = random.Random(5103)
    false_alarms = hits = 0
    for trial in range(trials):
        noise = [rng.gauss(0, 1) for _ in s]
        t0 = sum(a * b for a, b in zip(s, noise))
        t1 = sum(a * (a + b) for a, b in zip(s, noise))
        false_alarms += t0 > gamma
        hits += t1 > gamma
        if trial < 300:
            assert (detect(noise, s, sigma2, pfa) == [0]) == (t0 > gamma)
    pd = detection_probability(energy, sigma2, pfa)
    for count, p in ((false_alarms, pfa), (hits, pd)):
        assert abs(count / trials - p) < 4 * math.sqrt(p * (1 - p) / trials)


def test_edges() -> None:
    assert matched_filter([]) == []
    assert fir([1], [3, 4]) == [3, 4]
    assert detect([0.0] * 5, [1.0, 1.0], 1.0, 0.4) == []
    # y = (0, 1, 2) and gamma = sqrt(0.02) * 2.326 = 0.329: the half overlap at t = 0 also crosses.
    assert detect([0.0, 1.0, 1.0], [1.0, 1.0], 0.01, 0.01) == [0, 1]
