# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-n-body-summation/. The authors are listed in prov/14GKBC.jsonl.
import math
import random

import pytest

from direct_n_body_summation import accelerations, direct_sum, kinetic_energy, leapfrog, potential_energy


def brute(m, x, eps=0.0, G=1.0):
    """Independent reference: for each body, loop over every other body (no third law)."""
    n, dim = len(m), len(x[0])
    acc = []
    for i in range(n):
        ai = [0.0] * dim
        for j in range(n):
            if j != i:
                d = [x[j][k] - x[i][k] for k in range(dim)]
                r2 = sum(c * c for c in d) + eps * eps
                for k in range(dim):
                    ai[k] += G * m[j] * d[k] / r2 ** 1.5
        acc.append(ai)
    u = -0.5 * sum(G * m[i] * m[j] / math.sqrt(sum((x[i][k] - x[j][k]) ** 2 for k in range(dim)) + eps * eps)
                   for i in range(n) for j in range(n) if i != j)
    return acc, u


def random_bodies(n, seed):
    rng = random.Random(seed)
    m = [rng.uniform(0.5, 2.0) for _ in range(n)]
    x = [tuple(rng.uniform(-1.0, 1.0) for _ in range(3)) for _ in range(n)]
    return m, x


def test_hand_example_345():
    m = [1.0, 2.0, 3.0]
    x = [(0.0, 0.0, 0.0), (3.0, 0.0, 0.0), (0.0, 4.0, 0.0)]
    a, u = direct_sum(m, x)
    want = [(2 / 9, 3 / 16, 0.0), (-1 / 9 - 9 / 125, 12 / 125, 0.0), (6 / 125, -1 / 16 - 8 / 125, 0.0)]
    for ai, wi in zip(a, want):
        for c, w in zip(ai, wi):
            assert c == pytest.approx(w, abs=1e-15)
    assert u == pytest.approx(-157 / 60, rel=1e-15)


@pytest.mark.parametrize("eps", [0.0, 0.05])
def test_against_brute_force(eps):
    m, x = random_bodies(60, 7)
    a, u = direct_sum(m, x, eps)
    b, ub = brute(m, x, eps)
    scale = max(math.sqrt(sum(c * c for c in bi)) for bi in b)
    for ai, bi in zip(a, b):
        for c, w in zip(ai, bi):
            assert abs(c - w) <= 1e-12 * scale
    assert u == pytest.approx(ub, rel=1e-12)


def test_total_force_is_zero():
    m, x = random_bodies(80, 3)
    a = accelerations(m, x)
    big = max(mi * math.sqrt(sum(c * c for c in ai)) for mi, ai in zip(m, a))
    for k in range(3):
        assert abs(sum(mi * ai[k] for mi, ai in zip(m, a))) <= 1e-12 * big * len(m)


def test_force_is_minus_gradient_of_energy():
    m, x = random_bodies(12, 11)
    eps, hstep = 0.1, 1e-6
    a = accelerations(m, x, eps)
    for i in range(len(m)):
        for k in range(3):
            xp = [list(p) for p in x]
            xm = [list(p) for p in x]
            xp[i][k] += hstep
            xm[i][k] -= hstep
            grad = (potential_energy(m, xp, eps) - potential_energy(m, xm, eps)) / (2 * hstep)
            assert -grad / m[i] == pytest.approx(a[i][k], rel=1e-6, abs=1e-8)


def test_circular_orbit_period_two_pi():
    # Two bodies of mass 1/2 at distance 1: G M = 1, relative speed 1, period 2 pi.
    m = [0.5, 0.5]
    x = [(-0.5, 0.0, 0.0), (0.5, 0.0, 0.0)]
    v = [(0.0, -0.5, 0.0), (0.0, 0.5, 0.0)]
    steps = 2000
    h = 2 * math.pi / steps
    x1, v1 = leapfrog(m, x, v, h, steps)
    for p, q in zip(x1, x):
        assert math.dist(p, q) < 1e-4
    e0 = kinetic_energy(m, v) + potential_energy(m, x)
    e1 = kinetic_energy(m, v1) + potential_energy(m, x1)
    assert e0 == pytest.approx(-0.125, rel=1e-15)
    assert abs(e1 - e0) / abs(e0) < 1e-10


def test_coincident_bodies_need_softening():
    m = [1.0, 1.0]
    x = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
    with pytest.raises(ValueError):
        direct_sum(m, x)
    a, u = direct_sum(m, x, eps=0.5)
    assert a == [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    assert u == pytest.approx(-2.0)
