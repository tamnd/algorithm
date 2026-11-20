# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-strength-exchange/. The authors are listed in prov/0HQEAM.jsonl.
import math
import random

import pytest

from particle_strength_exchange import diffuse, exchange_pairs, exchange_rates, lattice, pse_step, stable_step


def gaussian(x, y, s2):
    # the Lamb-Oseen vorticity with circulation 1 and s2 = 4 nu t
    return math.exp(-(x * x + y * y) / s2) / (math.pi * s2)


def test_page_example_two_particles():
    pairs = exchange_pairs([0.0, 1.0], [0.0, 0.0], 1.0, 1.0)
    w = 4 / math.pi * math.exp(-1)
    assert pairs[0][2] == pytest.approx(w, abs=1e-15)
    assert exchange_rates([1.0, 0.0], [1.0, 1.0], pairs) == pytest.approx([-w, w], abs=1e-15)
    om = pse_step([1.0, 0.0], [1.0, 1.0], pairs, 0.5)
    assert om == pytest.approx([0.765801, 0.234199], abs=1e-6)
    assert sum(om) == 1.0


def test_total_circulation_is_conserved_exactly():
    rng = random.Random(1)
    n = 120
    xs = [rng.uniform(0, 1) for _ in range(n)]
    ys = [rng.uniform(0, 1) for _ in range(n)]
    vol = [rng.uniform(0.005, 0.02) for _ in range(n)]
    om = [rng.uniform(-5, 5) for _ in range(n)]
    pairs = exchange_pairs(xs, ys, 0.3, 0.12)
    c0 = sum(v * o for v, o in zip(vol, om))
    h = stable_step(vol, pairs)
    for _ in range(50):
        om = pse_step(om, vol, pairs, h)
    assert sum(v * o for v, o in zip(vol, om)) == pytest.approx(c0, abs=1e-12)


def test_laplacian_of_a_quadratic_is_exact_on_a_fine_lattice():
    xs, ys, vol = lattice(0.1, 1.0)
    pairs = exchange_pairs(xs, ys, 1.0, 0.15)
    om = [3 * x * x - x * y + 2 * y * y + x for x, y in zip(xs, ys)]
    rate = exchange_rates(om, vol, pairs)
    for p in range(len(xs)):
        if abs(xs[p]) < 0.2 and abs(ys[p]) < 0.2:
            assert rate[p] == pytest.approx(10.0, abs=1e-6)


def test_rate_on_a_gaussian_matches_the_integral_operator():
    # for the Gaussian kernel, L_eps g_s = (4 / eps^2) (g_{s + eps^2} - g_s) exactly, and L_eps -> Laplacian
    xs, ys, vol = lattice(0.1, 1.0)
    s2 = 0.16
    om = [gaussian(x, y, s2) for x, y in zip(xs, ys)]
    centre = len(xs) // 2
    assert xs[centre] == 0.0 and ys[centre] == 0.0
    laplacian = -4 / s2 * gaussian(0, 0, s2)
    last = math.inf
    for eps in (0.25, 0.2, 0.15):
        rate = exchange_rates(om, vol, exchange_pairs(xs, ys, 1.0, eps))[centre]
        operator = 4 / eps ** 2 * (gaussian(0, 0, s2 + eps * eps) - gaussian(0, 0, s2))
        assert rate == pytest.approx(operator, rel=1e-6)
        assert abs(rate - laplacian) < last
        last = abs(rate - laplacian)


def test_stable_step_keeps_the_maximum_principle():
    rng = random.Random(2)
    n = 100
    xs = [rng.uniform(0, 1) for _ in range(n)]
    ys = [rng.uniform(0, 1) for _ in range(n)]
    vol = [0.01] * n
    om = [rng.uniform(0, 1) for _ in range(n)]
    pairs = exchange_pairs(xs, ys, 0.5, 0.1)
    h = stable_step(vol, pairs)
    lo, hi = min(om), max(om)
    for _ in range(100):
        om = pse_step(om, vol, pairs, h)
        assert lo - 1e-12 <= min(om) and max(om) <= hi + 1e-12
    # spread is reduced: diffusion smooths the data
    assert max(om) - min(om) < hi - lo


def test_lamb_oseen_vortex_diffuses_at_the_right_rate():
    nu, xs, ys, vol = 1.0, *lattice(0.1, 1.0)
    assert len(xs) <= 500
    om = [gaussian(x, y, 0.16) for x, y in zip(xs, ys)]
    pairs = exchange_pairs(xs, ys, nu, 0.15)
    om = diffuse(om, vol, pairs, 0.01)
    exact = [gaussian(x, y, 0.16 + 4 * nu * 0.01) for x, y in zip(xs, ys)]
    assert max(abs(a - b) for a, b in zip(om, exact)) < 0.01 * max(exact)
