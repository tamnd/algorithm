# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/level-set-topology-optimization/. The authors are listed in prov/H8FVX0.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from fem2d import node, q4_stiffness
from level_set_topology_optimization import (cantilever, compliance_of, hj_step, holes_start, level_set_topology,
                                             reinitialize, solid_count, upwind_gradients_sq)

KE = [[float(v) for v in row] for row in q4_stiffness(F(3, 10))]


def exact_sqrt(q):
    q = F(q)
    a, b = math.isqrt(q.numerator), math.isqrt(q.denominator)
    assert a * a == q.numerator and b * b == q.denominator
    return F(a, b)


def test_upwind_step_is_exact_on_a_linear_function():
    nelx, nely = 6, 5
    for a, b in ((3, 4), (-3, 4), (F(-5, 2), -6), (0, F(7, 3))):
        phi = [a * i + b * j + F(1, 7) for i in range(nelx) for j in range(nely)]
        norm_sq = F(a) ** 2 + F(b) ** 2
        for i in range(1, nelx - 1):
            for j in range(1, nely - 1):
                assert upwind_gradients_sq(phi, nelx, nely, i, j) == (norm_sq, norm_sq)
        speed = [F(random.Random(5).choice([-2, 1, 3]))] * (nelx * nely)
        out = hj_step(phi, nelx, nely, speed, F(1, 4), sqrt=exact_sqrt)
        for i in range(1, nelx - 1):
            for j in range(1, nely - 1):
                e = i * nely + j
                assert out[e] == phi[e] - F(1, 4) * speed[e] * exact_sqrt(norm_sq)


def test_circle_grows_with_unit_speed():
    n, r0 = 30, 4
    phi = [math.hypot(i + 0.5 - 15, j + 0.5 - 15) - r0 for i in range(n) for j in range(n)]
    counts = [solid_count(phi)]
    for _ in range(8):  # 8 steps of dt = 0.5 at speed 1: the radius should grow to 8
        phi = hj_step(phi, n, n, [1.0] * (n * n), 0.5)
        counts.append(solid_count(phi))
    assert counts == sorted(counts)
    radius = math.sqrt(counts[-1] / math.pi)
    assert abs(radius - 8) < 0.5  # measured 7.74: first order upwind lags a little


def test_reinitialize_keeps_signs_and_gives_distances_to_a_line():
    nelx, nely = 20, 7
    phi = [3 * (i + 0.5 - 10.3) for i in range(nelx) for j in range(nely)]
    out = reinitialize(phi, nelx, nely)
    for e, (a, b) in enumerate(zip(phi, out)):
        assert (a < 0) == (b < 0)
        i = e // nely
        assert abs(b - (i + 0.5 - 10.3)) < 1e-12  # the true signed distance to the line x = 10.3
    rng = random.Random(6)
    phi = [rng.uniform(-1, 1) for _ in range(nelx * nely)]
    out = reinitialize(phi, nelx, nely)
    assert all((a < 0) == (b < 0) for a, b in zip(phi, out))


def test_solid_volume_is_monotone_in_the_multiplier():
    rng = random.Random(7)
    nelx, nely = 8, 6
    for _ in range(20):
        phi = [rng.uniform(-2, 2) for _ in range(nelx * nely)]
        w = [rng.random() for _ in range(nelx * nely)]
        counts = [solid_count(hj_step(phi, nelx, nely, [x - lam / 20 for x in w], 0.5)) for lam in range(21)]
        assert counts == sorted(counts, reverse=True)
        assert counts[-1] <= solid_count(phi)  # with l = 1 the speed is at most 0, so nothing grows


def test_never_below_the_brute_force_optimum_on_5x2():
    nelx, nely, eps = 5, 2, 1e-3
    force = {2 * node(nely, nelx, 0) + 1: -1.0}
    fixed = [k for j in range(nely + 1) for k in (2 * node(nely, 0, j), 2 * node(nely, 0, j) + 1)]
    best = min(compliance_of(nelx, nely, KE, [e in s for e in range(10)], force, fixed, eps)[0]
               for k in range(6) for s in itertools.combinations(range(10), k))
    for kx, ky in ((1, 1), (2, 1), (1, 2)):
        phi0 = holes_start(nelx, nely, 0.5, kx, ky)
        phi, hist = level_set_topology(nelx, nely, 0.5, phi0, force, fixed, iters=30, eps=eps)
        assert solid_count(phi) <= 5
        assert min(hist) >= best * (1 - 1e-9)  # every design has at most 5 solid elements
    assert abs(best - 344.52) < 0.01  # the bottom row, with void stiffness 1e-3


def test_cantilever_improves_and_keeps_the_volume():
    nelx, nely, vf = 24, 12, 0.5
    force, fixed = cantilever(nelx, nely)
    phi0 = holes_start(nelx, nely, vf, kx=3, ky=2)
    assert solid_count(phi0) == 144
    phi, hist = level_set_topology(nelx, nely, vf, phi0, force, fixed, iters=40)
    assert solid_count(phi) <= 144
    assert hist[-1] < 0.4 * hist[0]  # measured 237.4 to 72.0
    assert max(hist) > hist[0]  # measured: the compliance is not monotone (2637 at iteration 2)
