# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meshless-shape-matching/. The authors are listed in prov/CV2R4Y.jsonl.

"""Tests of shape matching against an angle scan, closed forms and conservation laws."""

import cmath
import math
import random

from anim import rot2
import meshless_shape_matching as sm


def random_body(rng, count):
    x0 = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(count)]
    m = [rng.uniform(0.5, 2.0) for _ in range(count)]
    return x0, m


def apply(f, t, pts):
    return [(f[0][0] * p[0] + f[0][1] * p[1] + t[0], f[1][0] * p[0] + f[1][1] * p[1] + t[1]) for p in pts]


def test_example_square():
    x0 = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
    rest = sm.RestShape(x0, [1.0] * 4)
    x = [(2.0 * p[0], p[1]) for p in x0]
    g = sm.goals(rest, x)
    assert max(math.dist(a, b) for a, b in zip(g, x0)) < 1e-15
    x1, v1 = sm.step(rest, x, [(0.0, 0.0)] * 4, 0.5, 0.1, gravity=(0.0, 0.0))
    assert math.dist(x1[2], (1.5, 1.0)) < 1e-14 and math.dist(v1[2], (-5.0, 0.0)) < 1e-13
    gl = sm.goals(rest, x, "linear", 1.0)
    assert math.dist(gl[2], (math.sqrt(2.0), 1.0 / math.sqrt(2.0))) < 1e-14


def test_rotation_is_the_best_rigid_fit():
    """The polar rotation of A_pq beats every angle of a fine scan."""
    rng = random.Random(21)
    for _ in range(30):
        x0, m = random_body(rng, 6)
        rest = sm.RestShape(x0, m)
        x = [(p[0] + rng.gauss(0, 0.5), p[1] + rng.gauss(0, 0.5)) for p in x0]
        r, _ = sm.match(rest, x)
        best = sm.fit_error(rest, x, r)
        assert abs(r[0][0] * r[1][1] - r[0][1] * r[1][0] - 1.0) < 1e-12
        for k in range(720):
            assert best <= sm.fit_error(rest, x, rot2(2.0 * math.pi * k / 720)) + 1e-12


def test_rigid_pose_has_no_pull():
    rng = random.Random(22)
    for _ in range(50):
        x0, m = random_body(rng, 5)
        rest = sm.RestShape(x0, m)
        x = apply(rot2(rng.uniform(-math.pi, math.pi)), (rng.uniform(-3, 3), rng.uniform(-3, 3)), x0)
        for mode in ("rigid", "linear"):
            g = sm.goals(rest, x, mode, rng.uniform(0.0, 1.0))
            assert max(math.dist(a, b) for a, b in zip(g, x)) < 1e-12


def test_linear_mode_recovers_the_affine_map():
    """For x = F x0 + t with det F > 0, A = F and A~ = F / sqrt(det F)."""
    rng = random.Random(23)
    for _ in range(50):
        x0, m = random_body(rng, 5)
        rest = sm.RestShape(x0, m)
        f = [[rng.uniform(0.5, 2.0), rng.uniform(-0.5, 0.5)], [rng.uniform(-0.5, 0.5), rng.uniform(0.5, 2.0)]]
        d = f[0][0] * f[1][1] - f[0][1] * f[1][0]
        x = apply(f, (rng.uniform(-1, 1), rng.uniform(-1, 1)), x0)
        g, _ = sm.match(rest, x, "linear", 1.0)
        for i in range(2):
            for j in range(2):
                assert abs(g[i][j] - f[i][j] / math.sqrt(d)) < 1e-10


def test_momentum_is_kept_exactly():
    rng = random.Random(24)
    for mode, beta in (("rigid", 0.0), ("linear", 0.5), ("linear", 1.0)):
        x0, m = random_body(rng, 8)
        rest = sm.RestShape(x0, m)
        x = [(p[0] + rng.gauss(0, 0.3), p[1] + rng.gauss(0, 0.3)) for p in x0]
        v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in x0]
        p0 = sm.momentum(x, v, m)
        for _ in range(200):
            x, v = sm.step(rest, x, v, 0.3, 0.02, mode, beta, gravity=(0.0, 0.0))
        p1 = sm.momentum(x, v, m)
        scale = sum(mi * math.hypot(*u) for mi, u in zip(m, v)) * (1.0 + max(math.hypot(*p) for p in x))
        assert max(abs(a - b) for a, b in zip(p0, p1)) < 1e-10 * scale


def test_alpha_one_reaches_the_goals():
    rng = random.Random(25)
    x0, m = random_body(rng, 6)
    rest = sm.RestShape(x0, m)
    x = [(p[0] + rng.gauss(0, 0.3), p[1] + rng.gauss(0, 0.3)) for p in x0]
    g = sm.goals(rest, x)
    x1, _ = sm.step(rest, x, [(0.0, 0.0)] * 6, 1.0, 0.05, gravity=(0.0, 0.0))
    assert max(math.dist(a, b) for a, b in zip(x1, g)) < 1e-14


def test_fixed_goal_amplification_has_unit_eigenvalues():
    for alpha in (0.01, 0.1, 0.5, 0.9, 1.0):
        for dt in (1e-3, 0.01, 0.1, 1.0):
            a = sm.amplification(alpha, dt)
            tr = a[0][0] + a[1][1]
            dt_ = a[0][0] * a[1][1] - a[0][1] * a[1][0]
            disc = cmath.sqrt(tr * tr - 4.0 * dt_)
            for lam in ((tr + disc) / 2.0, (tr - disc) / 2.0):
                assert abs(abs(lam) - 1.0) < 1e-12


def test_oscillation_neither_grows_nor_decays():
    """A stretched square keeps the size of its oscillation over 2000 steps (measured)."""
    x0 = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
    rest = sm.RestShape(x0, [1.0] * 4)
    x = [(2.0 * p[0], p[1]) for p in x0]
    v = [(0.0, 0.0)] * 4
    amp = []
    for n in range(2000):
        x, v = sm.step(rest, x, v, 0.2, 0.01, gravity=(0.0, 0.0))
        amp.append(max(math.dist(a, b) for a, b in zip(x, sm.goals(rest, x))))
    first = max(amp[:200])
    last = max(amp[-200:])
    assert 0.95 < last / first < 1.05


def test_center_of_mass_falls_as_symplectic_euler():
    rng = random.Random(26)
    x0, m = random_body(rng, 5)
    rest = sm.RestShape(x0, m)
    x = [(p[0] + rng.gauss(0, 0.2), p[1] + rng.gauss(0, 0.2)) for p in x0]
    c0 = sm.center(x, m)
    v = [(0.0, 0.0)] * 5
    for _ in range(10):
        x, v = sm.step(rest, x, v, 0.4, 0.1)
    c1 = sm.center(x, m)
    assert abs(c1[1] - c0[1] + 5.3955) < 1e-12 and abs(c1[0] - c0[0]) < 1e-12
