# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distance-based-formation-control/. The authors are listed in prov/W2E44J.jsonl.

import math
import random

from distance_based_formation_control import (
    control,
    is_infinitesimally_rigid_2d,
    potential,
    rank,
    rigidity_matrix,
    rk4_step,
    run_formation,
)

TRI = [(0, 1), (1, 2), (0, 2)]
SQUARE = [(0, 1), (1, 2), (2, 3), (3, 0)]
SQUARE_DIAG = SQUARE + [(0, 2)]


def dists(p, edges):
    return [math.dist(p[i], p[j]) for i, j in edges]


def centroid(p):
    n = len(p)
    return [sum(q[c] for q in p) / n for c in range(len(p[0]))]


def test_control_is_minus_gradient() -> None:
    rng = random.Random(1)
    h = 1e-6
    for _ in range(20):
        n = rng.randrange(3, 6)
        p = [[rng.uniform(-2, 2), rng.uniform(-2, 2)] for _ in range(n)]
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.7]
        if not edges:
            edges = [(0, 1)]
        d = [rng.uniform(0.5, 2) for _ in edges]
        u = control(p, edges, d)
        for i in range(n):
            for c in range(2):
                pp = [list(q) for q in p]
                pm = [list(q) for q in p]
                pp[i][c] += h
                pm[i][c] -= h
                g = (potential(pp, edges, d) - potential(pm, edges, d)) / (2 * h)
                assert abs(u[i][c] + g) < 1e-6 * max(1.0, abs(g))


def test_hand_value() -> None:
    p = [(0.0, 0.0), (2.0, 0.0), (0.0, 1.0)]
    u = control(p, [(0, 1), (0, 2)], [1.0, 1.0])
    # e_01 = 4 - 1 = 3, e_02 = 1 - 1 = 0, so u_0 = -3 (0 - 2, 0) = (6, 0)
    assert u[0] == [6.0, 0.0]
    assert u[1] == [-6.0, 0.0]
    assert u[2] == [0.0, 0.0]
    assert potential(p, [(0, 1), (0, 2)], [1.0, 1.0]) == 2.25


def test_centroid_and_equivariance() -> None:
    rng = random.Random(2)
    p = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(4)]
    d = [1.0] * 5
    u = control(p, SQUARE_DIAG, d)
    assert all(abs(sum(ui[c] for ui in u)) < 1e-12 for c in range(2))
    th, tx, ty = 0.7, 3.0, -1.0
    cs, sn = math.cos(th), math.sin(th)
    q = [[cs * x - sn * y + tx, sn * x + cs * y + ty] for x, y in p]
    uq = control(q, SQUARE_DIAG, d)
    for a, b in zip(u, uq):
        assert abs(cs * a[0] - sn * a[1] - b[0]) < 1e-12
        assert abs(sn * a[0] + cs * a[1] - b[1]) < 1e-12


def test_potential_decreases_and_centroid_is_fixed() -> None:
    rng = random.Random(3)
    p = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(4)]
    d = [1.0, 1.0, 1.0, 1.0, math.sqrt(2)]
    c0 = centroid(p)
    v = potential(p, SQUARE_DIAG, d)
    for _ in range(300):
        p = rk4_step(p, SQUARE_DIAG, d, 0.01)
        nv = potential(p, SQUARE_DIAG, d)
        assert nv <= v + 1e-12
        v = nv
    assert max(abs(a - b) for a, b in zip(centroid(p), c0)) < 1e-9


def test_local_convergence_triangle() -> None:
    rng = random.Random(4)
    target = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)]
    d = [1.0, 1.0, 1.0]
    for _ in range(5):
        p0 = [[x + rng.uniform(-0.2, 0.2), y + rng.uniform(-0.2, 0.2)] for x, y in target]
        p = run_formation(p0, TRI, d, 10.0, 0.01)
        assert max(abs(a - b) for a, b in zip(dists(p, TRI), d)) < 1e-9
        assert max(abs(a - b) for a, b in zip(centroid(p), centroid(p0))) < 1e-9


def test_local_convergence_rigid_square() -> None:
    rng = random.Random(5)
    d = [1.0, 1.0, 1.0, 1.0, math.sqrt(2)]
    target = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert is_infinitesimally_rigid_2d(target, SQUARE_DIAG)
    for _ in range(3):
        p0 = [[x + rng.uniform(-0.15, 0.15), y + rng.uniform(-0.15, 0.15)] for x, y in target]
        p = run_formation(p0, SQUARE_DIAG, d, 15.0, 0.01)
        assert max(abs(a - b) for a, b in zip(dists(p, SQUARE_DIAG), d)) < 1e-8
        # the other diagonal is then also right: the shape is a unit square
        assert abs(math.dist(p[1], p[3]) - math.sqrt(2)) < 1e-7


def test_flexible_square_keeps_sides_but_not_shape() -> None:
    assert not is_infinitesimally_rigid_2d([(0, 0), (1, 0), (1, 1), (0, 1)], SQUARE)
    p0 = [[0.0, 0.0], [1.1, 0.0], [1.5, 0.9], [0.3, 1.0]]
    p = run_formation(p0, SQUARE, [1.0] * 4, 20.0, 0.01)
    assert max(abs(a - 1.0) for a in dists(p, SQUARE)) < 1e-8
    assert abs(math.dist(p[0], p[2]) - math.sqrt(2)) > 0.05


def test_collinear_start_stays_collinear() -> None:
    p0 = [[0.0, 0.0], [1.0, 0.0], [3.0, 0.0]]
    p = run_formation(p0, TRI, [1.0, 1.0, 1.0], 20.0, 0.01)
    assert all(abs(q[1]) < 1e-12 for q in p)
    assert potential(p, TRI, [1.0, 1.0, 1.0]) > 0.1
    u = control(p, TRI, [1.0, 1.0, 1.0])
    assert max(abs(c) for ui in u for c in ui) < 1e-6


def test_rigidity_ranks() -> None:
    tri = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.8)]
    assert rank(rigidity_matrix(tri, TRI)) == 3
    assert rank(rigidity_matrix([(0, 0), (1, 0), (2, 0)], TRI)) == 2
    sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert rank(rigidity_matrix(sq, SQUARE)) == 4
    assert rank(rigidity_matrix(sq, SQUARE_DIAG)) == 5
