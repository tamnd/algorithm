# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/root-sum-of-squares-coil-combination/. The authors are listed in prov/4R76FY.jsonl.

import cmath
import math
import random

from imgla import cho_solve, cholesky
from root_sum_of_squares_coil_combination import optimal_combination, rss, rss_prewhitened

PSI = [
    [1.0, 0.3 + 0.1j, 0.1, 0.0],
    [0.3 - 0.1j, 1.5, 0.2j, 0.1],
    [0.1, -0.2j, 0.8, 0.25],
    [0.0, 0.1, 0.25, 1.2],
]


def random_case(rng, n=6, c=4):
    maps = [[[complex(rng.uniform(0.2, 1.0), rng.uniform(-0.5, 0.5)) for _ in range(n)] for _ in range(n)] for _ in range(c)]
    rho = [[cmath.rect(rng.uniform(0.5, 2.0), rng.uniform(-3, 3)) for _ in range(n)] for _ in range(n)]
    coils = [[[s * p for s, p in zip(sr, pr)] for sr, pr in zip(m, rho)] for m in maps]
    return maps, rho, coils


def correlated_noise(rng, low, count):
    """count noise vectors n = L z with E[z z^H] = I, so E[n n^H] = L L^H."""
    c = len(low)
    out = []
    for _ in range(count):
        z = [complex(rng.gauss(0, math.sqrt(0.5)), rng.gauss(0, math.sqrt(0.5))) for _ in range(c)]
        out.append([sum(low[i][k] * z[k] for k in range(i + 1)) for i in range(c)])
    return out


def test_hand_values():
    assert rss([[[3.0]], [[4j]], [[12.0]]]) == [[13.0]]
    assert rss([[[1.0, 0.0]], [[0.0, -2.0]]]) == [[1.0, 2.0]]


def test_noiseless_value_and_phase_invariance():
    rng = random.Random(2)
    maps, rho, coils = random_case(rng)
    out = rss(coils)
    turned = [[[v * cmath.exp(1j * (0.7 * k + 0.2)) for v in row] for row in m] for k, m in enumerate(coils)]
    again = rss(turned)
    low = cholesky(PSI)
    pw = rss_prewhitened(coils, PSI)
    for i in range(6):
        for j in range(6):
            s = [m[i][j] for m in maps]
            assert abs(out[i][j] - abs(rho[i][j]) * math.sqrt(sum(abs(v) ** 2 for v in s))) < 1e-12
            assert abs(again[i][j] - out[i][j]) < 1e-12
            q = sum(a.conjugate() * b for a, b in zip(s, cho_solve(low, s))).real
            assert abs(pw[i][j] - abs(rho[i][j]) * math.sqrt(q)) < 1e-12


def test_identity_covariance_gives_plain_rss():
    rng = random.Random(4)
    _, _, coils = random_case(rng)
    a, b = rss(coils), rss_prewhitened(coils)
    assert all(abs(x - y) < 1e-12 for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_noise_only_mean():
    # E[RSS] = Gamma(c + 1/2) / Gamma(c) for c coils of unit noise power, also after whitening.
    rng = random.Random(7)
    expect = math.gamma(4.5) / math.gamma(4.0)
    eye = [[1.0 if a == b else 0.0 for b in range(4)] for a in range(4)]
    for psi in (eye, PSI):
        noise = correlated_noise(rng, cholesky(psi), 8000)
        coils = [[[v[k] for v in noise]] for k in range(4)]
        vals = rss_prewhitened(coils, psi)[0]
        assert abs(sum(vals) / len(vals) / expect - 1.0) < 0.015


def test_optimal_combination_is_unbiased_with_least_variance():
    rng = random.Random(11)
    maps, rho, coils = random_case(rng, n=1)
    s = [m[0][0] for m in maps]
    assert abs(optimal_combination(coils, maps, PSI)[0][0] - rho[0][0]) < 1e-12
    low = cholesky(PSI)
    q = sum(a.conjugate() * b for a, b in zip(s, cho_solve(low, s))).real
    noise = correlated_noise(rng, low, 6000)
    noisy = [[[coils[k][0][0] + v[k] for v in noise]] for k in range(4)]
    wide = [[[s[k]] * len(noise)] for k in range(4)]
    est = optimal_combination(noisy, wide, PSI)[0]
    var = sum(abs(e - rho[0][0]) ** 2 for e in est) / len(est)
    assert abs(var * q - 1.0) < 0.05
    # The prewhitened RSS of the noiseless data is |rho| sqrt(q) = |rho| / (noise std of the optimal estimate).
    assert abs(rss_prewhitened(coils, PSI)[0][0] - abs(rho[0][0]) / math.sqrt(1.0 / q)) < 1e-12
