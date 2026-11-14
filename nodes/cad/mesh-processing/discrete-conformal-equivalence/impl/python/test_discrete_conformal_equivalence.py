# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-conformal-equivalence/. The authors are listed in prov/VG00WC.jsonl.

import math
import random

import pytest

from discrete_conformal_equivalence import (
    angle_sums,
    conformal_scale_factors,
    edge_lengths,
    energy,
    gradient_and_hessian,
    layout,
    lobachevsky,
    new_lengths,
)
from mx2geom import boundary_loop, exact_orient2d


def hex_disk(r, rng, bend, jitter=0.15):
    """A hexagonal patch of the triangular lattice, jittered and lifted to z = a x^2 + b y^2 + c x y."""
    pts, index = [], {}
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            if abs(i + j) <= r:
                index[(i, j)] = len(pts)
                pts.append((i + 0.5 * j + rng.uniform(-jitter, jitter), j * math.sqrt(3) / 2 + rng.uniform(-jitter, jitter)))
    a, b, c = [rng.uniform(-bend, bend) for _ in range(3)]
    verts = [(x, y, a * x * x + b * y * y + c * x * y) for x, y in pts]
    faces = []
    for (i, j), v in index.items():
        if (i + 1, j) in index and (i, j + 1) in index:
            faces.append((v, index[(i + 1, j)], index[(i, j + 1)]))
        if (i + 1, j) in index and (i + 1, j - 1) in index:
            faces.append((v, index[(i + 1, j - 1)], index[(i + 1, j)]))
    return verts, faces


def disk_problem(seed, r=3, bend=0.5):
    rng = random.Random(seed)
    v, f = hex_disk(r, rng, bend)
    lengths = edge_lengths(v, f)
    loop = boundary_loop(f)
    inner = [x for x in range(len(v)) if x not in loop]
    return v, f, lengths, loop, inner


PYRAMID_V = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (0, 0, 1)]
PYRAMID_F = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
OCTA_V = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
OCTA_F = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]


def lob_quadrature(x, n=2000):
    """-integral_0^x log(2 sin t) dt for 0 < x < pi: the log(2 t) part exactly, log(sin t / t) by Simpson."""
    h = x / n

    def smooth(t):
        return math.log(math.sin(t) / t) if t > 0 else 0.0

    s = smooth(0.0) + smooth(x) + sum((4 if k % 2 else 2) * smooth(k * h) for k in range(1, n))
    return -(x * math.log(2 * x) - x) - s * h / 3


def test_lobachevsky_function():
    # Lob(pi/6) = Cl2(pi/3) / 2 and Lob(pi/4) = G / 2 (Catalan's constant).
    assert abs(lobachevsky(math.pi / 6) - 0.5 * 1.0149416064096536) < 1e-15
    assert abs(lobachevsky(math.pi / 4) - 0.5 * 0.915965594177219) < 1e-15
    for x in (0.3, 1.0, 1.5, 2.0, 3.0):
        assert abs(lobachevsky(x) - lob_quadrature(x)) < 1e-10
        assert abs(lobachevsky(-x) + lobachevsky(x)) < 1e-15
        assert abs(lobachevsky(x + math.pi) - lobachevsky(x)) < 1e-12
    assert lobachevsky(0.0) == 0.0 and abs(lobachevsky(math.pi / 2)) < 1e-15


def test_gradient_and_hessian_match_finite_differences():
    for seed in range(3):
        v, f, lengths, loop, inner = disk_problem(seed, r=2)
        rng = random.Random(100 + seed)
        theta = {i: 2 * math.pi + rng.uniform(-0.3, 0.3) for i in inner}
        u = [rng.uniform(-0.2, 0.2) for _ in v]
        g, h = gradient_and_hessian(f, lengths, u, theta, inner)
        eps = 1e-5
        for k, i in enumerate(inner):
            up, um = list(u), list(u)
            up[i] += eps
            um[i] -= eps
            fd = (energy(f, lengths, up, theta) - energy(f, lengths, um, theta)) / (2 * eps)
            assert abs(g[k] - fd) < 1e-7
            gp, _ = gradient_and_hessian(f, lengths, up, theta, inner)
            gm, _ = gradient_and_hessian(f, lengths, um, theta, inner)
            # g is the gradient of E, so its derivative is the Hessian H.
            for c in range(len(inner)):
                assert abs(h[c][k] - (gp[c] - gm[c]) / (2 * eps)) < 1e-6


def test_energy_is_convex_along_lines_through_degenerate_triangles():
    v, f, lengths, loop, inner = disk_problem(5, r=2)
    theta = {i: 2 * math.pi for i in inner}
    rng = random.Random(7)
    for _ in range(10):
        d = [rng.uniform(-1, 1) if i in theta else 0.0 for i in range(len(v))]
        values = [energy(f, lengths, [s * x for x in d], theta) for s in [k / 10 for k in range(-40, 41)]]
        for a, b, c in zip(values, values[1:], values[2:]):
            assert a - 2 * b + c > -1e-9


def test_target_angle_sums_are_met_on_disks():
    for seed in range(5):
        v, f, lengths, loop, inner = disk_problem(seed)
        theta = {i: 2 * math.pi for i in inner}
        u, steps = conformal_scale_factors(f, lengths, theta, len(v))
        s = angle_sums(f, lengths, u, len(v))
        assert max(abs(s[i] - 2 * math.pi) for i in inner) < 1e-11
        assert all(u[b] == 0.0 for b in loop)
        assert steps <= 10


def test_rectangle_target_lays_out_as_a_rectangle_without_flips():
    for seed in range(3):
        v, f, lengths, loop, inner = disk_problem(seed)
        m = len(loop)
        corners = {loop[(c * m) // 4] for c in range(4)}
        theta = {i: 2 * math.pi for i in inner}
        for b in loop:
            theta[b] = math.pi / 2 if b in corners else math.pi
        fixed = loop[1]
        del theta[fixed]
        u, _ = conformal_scale_factors(f, lengths, theta, len(v))
        s = angle_sums(f, lengths, u, len(v))
        # The fixed vertex gets its angle for free, by the discrete Gauss-Bonnet theorem.
        assert abs(s[fixed] - math.pi) < 1e-10
        pos = layout(f, lengths, u)
        nl = new_lengths(lengths, u)
        for (i, j), l in nl.items():
            assert abs(math.dist(pos[i], pos[j]) - l) < 1e-9
        for x, y, z in f:
            assert exact_orient2d(pos[x], pos[y], pos[z]) > 0
        for t in range(m):
            p0, p1, p2 = pos[loop[t - 1]], pos[loop[t]], pos[loop[(t + 1) % m]]
            d0 = (p1[0] - p0[0], p1[1] - p0[1])
            d1 = (p2[0] - p1[0], p2[1] - p1[1])
            turn = math.atan2(d0[0] * d1[1] - d0[1] * d1[0], d0[0] * d1[0] + d0[1] * d1[1])
            assert abs(turn - (math.pi / 2 if loop[t] in corners else 0.0)) < 1e-9


def test_closed_octahedron_reaches_targets_that_satisfy_gauss_bonnet():
    for seed in range(3):
        rng = random.Random(seed)
        v = [tuple(c * rng.uniform(0.6, 1.5) for c in p) for p in OCTA_V]
        lengths = edge_lengths(v, OCTA_F)
        theta = {i: 4 * math.pi / 3 for i in range(1, 6)}
        u, _ = conformal_scale_factors(OCTA_F, lengths, theta, 6)
        s = angle_sums(OCTA_F, lengths, u, 6)
        assert max(abs(x - 4 * math.pi / 3) for x in s) < 1e-11


def test_minimum_is_unique_from_different_starts():
    v, f, lengths, loop, inner = disk_problem(2)
    theta = {i: 2 * math.pi for i in inner}
    u1, _ = conformal_scale_factors(f, lengths, theta, len(v))
    rng = random.Random(9)
    for _ in range(3):
        start = [rng.uniform(-0.5, 0.5) if i in theta else 0.0 for i in range(len(v))]
        u2, _ = conformal_scale_factors(f, lengths, theta, len(v), u0=start)
        assert max(abs(a - b) for a, b in zip(u1, u2)) < 1e-10


def test_pyramid_example():
    lengths = edge_lengths(PYRAMID_V, PYRAMID_F)
    u, steps = conformal_scale_factors(PYRAMID_F, lengths, {4: 2 * math.pi}, 5)
    assert abs(u[4] - math.log(2 / 3)) < 1e-12
    assert steps == 5  # five Newton steps, then the stop test passes
    pos = layout(PYRAMID_F, lengths, u)
    for i in range(4):
        assert abs(math.dist(pos[i], pos[(i + 1) % 4]) - 2) < 1e-12
        assert abs(math.dist(pos[i], pos[4]) - math.sqrt(2)) < 1e-12


def test_targets_without_a_valid_solution_raise():
    lengths = edge_lengths(PYRAMID_V, PYRAMID_F)
    # 3.9 pi is reached with valid triangles, after gradient steps through degenerate ones.
    u, _ = conformal_scale_factors(PYRAMID_F, lengths, {4: 3.9 * math.pi}, 5)
    assert abs(angle_sums(PYRAMID_F, lengths, u, 5)[4] - 3.9 * math.pi) < 1e-11
    # 4 pi needs all four apex angles equal to pi: only degenerate triangles reach it.
    with pytest.raises(ValueError):
        conformal_scale_factors(PYRAMID_F, lengths, {4: 4 * math.pi}, 5)
    # Above 4 pi the angle sum is never reached and E has no minimum.
    with pytest.raises(ValueError):
        conformal_scale_factors(PYRAMID_F, lengths, {4: 4.5 * math.pi}, 5)
