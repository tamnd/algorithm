# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-estimator/. The authors are listed in prov/NDP0HX.jsonl.
import math
import random

import pytest

from collision_estimator import collision_estimator, move, uniform_isotropic_source


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def expint(order, z, steps=2000):
    """E_n(z) = integral over u in (0, 1] of exp(-z/u) u^(n-2) du, by Simpson's rule (n >= 2)."""
    if z == 0.0:
        return 1.0 / (order - 1)
    h = 1.0 / steps
    total = 0.0
    for k in range(steps + 1):
        u = k * h
        f = 0.0 if u == 0.0 else math.exp(-z / u) * u ** (order - 2)
        total += f * (1 if k in (0, steps) else (4 if k % 2 else 2))
    return total * h / 3.0


def test_one_history_by_hand():
    # Beam on a slab of 2 cm, sigma_t = 2, sigma_s = 1, two bins of 1 cm.
    # r = 0.5: flight ln 2 / 2 = 0.3466, collision in bin 0, score 1/2.
    # r = 0.7: scatter; r = 1.0: mu = 1. r = 0.9: flight ln 10 / 2 = 1.1513, x = 1.4979.
    # Bin 1 scores 1/2. r = 0.1: absorbed.
    # The second history collides in bin 0 (score 1/2) and is absorbed there.
    # With N = 2 and dx = 1 cm: phi_0 = 1.0 / 2 and phi_1 = 0.5 / 2.
    rng = FixedRng([0.5, 0.7, 1.0, 0.9, 0.1, 0.5, 0.1])
    phi, se = collision_estimator(2, 2.0, 2.0, 1.0, 2, rng)
    assert phi == pytest.approx([(0.5 + 0.5) / 2, 0.5 / 2])


def test_pure_absorber_beam_exact():
    sig, length, nb, n = 1.0, 2.0, 4, 20000
    phi, se = collision_estimator(n, length, sig, 0.0, nb, random.Random(1))
    dx = length / nb
    for j in range(nb):
        exact = (math.exp(-sig * j * dx) - math.exp(-sig * (j + 1) * dx)) / (sig * dx)
        assert abs(phi[j] - exact) < 4.0 * se[j]


def test_reflecting_slab_is_infinite_medium():
    # Source 1 per history spread over L, so Q = 1 / L; then phi = Q / sigma_a everywhere.
    length, sig_t, sig_s, n = 2.0, 1.0, 0.5, 6000
    phi, se = collision_estimator(n, length, sig_t, sig_s, 4, random.Random(2), uniform_isotropic_source, "reflect")
    exact = (1.0 / length) / (sig_t - sig_s)
    for p, e in zip(phi, se):
        assert abs(p - exact) < 4.0 * e


def test_pure_absorber_volume_source_against_e3():
    # phi(x) = (Q / (2 sigma)) (2 - E2(sigma x) - E2(sigma (L - x))) with Q = 1 / L.
    length, sig, nb, n = 2.0, 1.0, 4, 30000
    phi, se = collision_estimator(n, length, sig, 0.0, nb, random.Random(3), uniform_isotropic_source)
    q, dx = 1.0 / length, length / nb
    for j in range(nb):
        a, b = j * dx, (j + 1) * dx
        left = (expint(3, sig * a) - expint(3, sig * b)) / sig
        right = (expint(3, sig * (length - b)) - expint(3, sig * (length - a))) / sig
        exact = q / (2.0 * sig * dx) * (2.0 * dx - left - right)
        assert abs(phi[j] - exact) < 4.0 * se[j]


def test_mirror_move():
    x, mu, inside = move(0.5, 1.0, 1.0, 1.0, "reflect")  # one reflection at x = 1
    assert inside and x == pytest.approx(0.5) and mu == -1.0
    x, mu, inside = move(0.5, 1.0, 2.0, 1.0, "reflect")  # reflections at x = 1 and x = 0
    assert inside and x == pytest.approx(0.5) and mu == 1.0
    x, mu, inside = move(0.5, -1.0, 0.75, 1.0, "reflect")
    assert x == pytest.approx(0.25) and mu == 1.0
    assert move(0.5, 1.0, 0.75, 1.0, "vacuum")[2] is False
