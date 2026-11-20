# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coherence-factor/. The authors are listed in prov/BGW13T.jsonl.

import math
import random

from coherence_factor import cf_weighted, coherence_factor, triangle_coherence_cf


def _cgauss(rng):
    return complex(rng.gauss(0, 1), rng.gauss(0, 1)) / math.sqrt(2)


def test_page_examples() -> None:
    assert coherence_factor([1.0, 1.0, 1.0, 1.0]) == 1.0
    assert coherence_factor([1.0, 0.0, 0.0, 0.0]) == 0.25
    assert coherence_factor([1.0, -1.0, 1.0, -1.0]) == 0.0
    assert abs(coherence_factor([3.0, 1.0, 1.0, 1.0]) - 36 / 48) < 1e-15
    assert coherence_factor([0.0, 0.0]) == 0.0


def test_range_and_equality_case() -> None:
    rng = random.Random(6601)
    for _ in range(500):
        m = rng.randint(1, 20)
        s = [_cgauss(rng) for _ in range(m)]
        v = coherence_factor(s)
        assert -1e-15 <= v <= 1 + 1e-12
    c = 0.3 - 2.0j
    assert abs(coherence_factor([c] * 9) - 1) < 1e-12
    # a phase ramp that is not constant lowers CF below 1
    assert coherence_factor([complex(math.cos(0.4 * k), math.sin(0.4 * k)) for k in range(9)]) < 0.9


def test_scale_invariance() -> None:
    rng = random.Random(6602)
    s = [_cgauss(rng) for _ in range(12)]
    for a in (5.0, -0.01, 2 - 3j):
        assert abs(coherence_factor([a * v for v in s]) - coherence_factor(s)) < 1e-12


def test_independent_channels_have_mean_one_over_m() -> None:
    rng = random.Random(6603)
    m, trials = 8, 3000
    mean = sum(coherence_factor([_cgauss(rng) for _ in range(m)]) for _ in range(trials)) / trials
    assert abs(mean - 1 / m) < 0.01


def test_triangle_coherence_closed_form() -> None:
    for m in (1, 2, 5, 16, 64):
        direct = sum(1 - abs(i - j) / m for i in range(m) for j in range(m)) / (m * m)
        assert abs(direct - triangle_coherence_cf(m)) < 1e-12


def test_triangle_coherence_by_simulation() -> None:
    # s_i = (g_i + ... + g_{i+M-1}) / sqrt(M) has the correlation 1 - |i - j| / M
    rng = random.Random(6604)
    m, trials = 8, 3000
    num = den = 0.0
    for _ in range(trials):
        g = [_cgauss(rng) for _ in range(2 * m - 1)]
        s = [sum(g[i:i + m]) / math.sqrt(m) for i in range(m)]
        num += abs(sum(s)) ** 2
        den += m * sum(abs(v) ** 2 for v in s)
    assert abs(num / den - triangle_coherence_cf(m)) < 0.03


def test_weighting() -> None:
    s = [3.0, 1.0, 1.0, 1.0]
    assert abs(cf_weighted(s) - 6 * 0.75) < 1e-12
    assert abs(cf_weighted(s, 2.0) - 6 * 0.75 ** 2) < 1e-12
    assert cf_weighted(s, 0.0) == 6.0
