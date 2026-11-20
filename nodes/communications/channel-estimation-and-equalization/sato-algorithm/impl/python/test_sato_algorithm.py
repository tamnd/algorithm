# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sato-algorithm/. The authors are listed in prov/2220NN.jsonl.

import cmath
import itertools
import math
import random
from fractions import Fraction

import pytest

import cbb
from sato_algorithm import csgn, sato, sato_gamma

PAM4 = [v / math.sqrt(5) for v in (-3, -1, 1, 3)]
QAM16 = [complex(a, b) / math.sqrt(10) for a in (-3, -1, 1, 3) for b in (-3, -1, 1, 3)]


def test_gamma_check_values() -> None:
    assert sato_gamma([-1, 1]) == 1.0
    assert sato_gamma([-3, -1, 1, 3]) == 2.5
    assert sato_gamma([-7, -5, -3, -1, 1, 3, 5, 7]) == 5.25
    assert abs(sato_gamma(PAM4) - math.sqrt(5) / 2) < 1e-12  # 1.1180 for unit-energy 4-PAM


def mean_error_times_symbols(g, levels, gamma):
    # E[e a_j] for each j, with z = sum_j g_j a_j and e = z - gamma sgn(z), by exact enumeration
    acc = [Fraction(0)] * len(g)
    count = 0
    for a in itertools.product(levels, repeat=len(g)):
        z = sum(gi * ai for gi, ai in zip(g, a))
        e = z - gamma * (1 if z > 0 else (-1 if z < 0 else 0))
        for j in range(len(g)):
            acc[j] += e * a[j]
        count += 1
    return [v / count for v in acc]


def test_the_perfect_equalizer_is_a_stationary_point() -> None:
    levels = [-3, -1, 1, 3]
    gamma = Fraction(5, 2)
    # g = e_1: the mean update E[e conj(u)] = H^* E[e a] is zero
    assert mean_error_times_symbols([0, 1, 0], levels, gamma) == [0, 0, 0]
    assert mean_error_times_symbols([0, -1, 0], levels, gamma) == [0, 0, 0]
    # a wrong gain or a residual tap is not stationary
    assert mean_error_times_symbols([0, Fraction(9, 10), 0], levels, gamma)[1] == Fraction(-1, 2)
    assert any(v != 0 for v in mean_error_times_symbols([Fraction(1, 5), 1, 0], levels, gamma))


def test_error_is_the_derivative_of_the_cost() -> None:
    # J(z) = |z|^2 / 2 - gamma (|Re z| + |Im z|); dJ / d conj(z) = e / 2 away from the axes
    gamma = 0.8
    rng = random.Random(1)
    for _ in range(20):
        z = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        cost = lambda v: abs(v) ** 2 / 2 - gamma * (abs(v.real) + abs(v.imag))
        eps = 1e-6
        dx = (cost(z + eps) - cost(z - eps)) / (2 * eps)
        dy = (cost(z + 1j * eps) - cost(z - 1j * eps)) / (2 * eps)
        assert abs(0.5 * complex(dx, dy) - (z - gamma * csgn(z)) / 2) < 1e-8


def run(h, points, n, mu, k, n0, seed, rot=1):
    rng = random.Random(seed)
    x = [rng.choice(points) for _ in range(k)]
    y = [rot * v for v in cbb.conv(x, h)[:k]]
    if n0 > 0:
        y = cbb.awgn(rng, y, n0)
    gamma = sato_gamma([p.real for p in points])
    c, z = sato(y, n, mu, gamma)
    g = cbb.conv(c, [rot * v for v in h])
    return x, c, z, g


def test_4pam_through_a_known_channel() -> None:
    n = 11
    x, c, z, g = run([1, 0.5], PAM4, n, 0.002, 8000, 0.0, 2)
    p = [abs(v) ** 2 for v in g]
    d = max(range(len(g)), key=lambda i: p[i])
    assert (sum(p) - p[d]) / p[d] < 0.01
    sign = 1 if g[d].real > 0 else -1
    errors = sum(min(PAM4, key=lambda q: abs(z[t] * sign - q)) != x[t + n - 1 - d] for t in range(len(z) - 2000, len(z)))
    assert errors == 0


def test_sign_flip_gives_the_same_taps() -> None:
    rng = random.Random(3)
    x = [rng.choice(PAM4) for _ in range(500)]
    y = cbb.conv(x, [1, 0.4])[:500]
    c1, z1 = sato(y, 7, 0.003, sato_gamma(PAM4))
    c2, z2 = sato([-v for v in y], 7, 0.003, sato_gamma(PAM4))
    assert max(abs(u - v) for u, v in zip(c1, c2)) < 1e-12
    assert max(abs(u + v) for u, v in zip(z1, z2)) < 1e-12


def test_qam_form_removes_a_carrier_phase_up_to_90_degrees() -> None:
    # unlike CMA, the per-axis sign brings the output back to the axes of the grid
    for rot_deg in (25, 70):
        rot = cmath.exp(1j * math.radians(rot_deg))
        x, c, z, g = run([1, 0.3 + 0.2j], QAM16, 11, 0.0005, 12000, 0.0, 4, rot)
        d = max(range(len(g)), key=lambda i: abs(g[i]))
        ph = math.degrees(cmath.phase(g[d])) % 90
        assert min(ph, 90 - ph) < 3


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        sato([1, 2], 0, 0.01, 1.0)
    with pytest.raises(ValueError):
        sato([1, 2], 2, 0.01, 0.0)
    with pytest.raises(ValueError):
        sato_gamma([0, 0])
