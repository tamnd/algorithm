# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/front-tracking-method/. The authors are listed in prov/7VRC33.jsonl.
import math
import random

from front_tracking_method import (
    circle_front,
    enclosed_area,
    front_track,
    grid_field,
    interpolate,
    peskin_phi,
    regrid,
    spread,
    tension_forces,
)


def frozen(u, v, fx, fy, dt):
    return u, v


def test_peskin_kernel_moments():
    rng = random.Random(1)
    for _ in range(200):
        r = rng.uniform(-3.0, 3.0)
        w = [peskin_phi(r - j) for j in range(-6, 7)]
        assert abs(sum(w) - 1.0) < 1e-14
        assert abs(sum((r - j) * peskin_phi(r - j) for j in range(-6, 7))) < 1e-14
        assert abs(sum(a * a for a in w) - 0.375) < 1e-14
    assert peskin_phi(2.0) == 0.0 and abs(peskin_phi(0.0) - 0.5) < 1e-15


def test_tension_forces_hand_and_balance():
    sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    F = tension_forces(sq, 1.0)
    assert F[1] == (-1.0, 1.0)  # inward at the corner (1, 0), length sqrt(2) = 2 sin(pi/4)
    rng = random.Random(2)
    for _ in range(50):
        m = rng.randrange(5, 40)
        X = [(0.5 + (0.2 + 0.1 * rng.random()) * math.cos(2 * math.pi * k / m),
              0.5 + (0.2 + 0.1 * rng.random()) * math.sin(2 * math.pi * k / m)) for k in range(m)]
        F = tension_forces(X, 0.7)
        assert abs(sum(f[0] for f in F)) < 1e-14 and abs(sum(f[1] for f in F)) < 1e-14
        torque = sum(x * f[1] - y * f[0] for (x, y), f in zip(X, F))
        assert abs(torque) < 1e-14
        fx, fy = spread(X, F, 16)
        assert abs(sum(map(sum, fx)) / 256) < 1e-13 and abs(sum(map(sum, fy)) / 256) < 1e-13


def test_spread_and_interpolate():
    n = 16
    fx, fy = spread([(0.3141, 0.2718)], [(2.0, -1.0)], n)
    assert abs(sum(map(sum, fx)) / n ** 2 - 2.0) < 1e-14 and abs(sum(map(sum, fy)) / n ** 2 + 1.0) < 1e-14
    u = grid_field(n, lambda x, y: 1.5 * x - 0.5 * y + 0.25)
    v = grid_field(n, lambda x, y: -0.3 * x + 2.0 * y)
    for (a, b), (x, y) in zip(interpolate(u, v, [(0.3, 0.4), (0.55, 0.61), (0.5, 0.5)]), [(0.3, 0.4), (0.55, 0.61), (0.5, 0.5)]):
        assert abs(a - (1.5 * x - 0.5 * y + 0.25)) < 1e-14 and abs(b - (-0.3 * x + 2.0 * y)) < 1e-14


def test_laplace_pressure_jump():
    n, m, r, sigma = 32, 128, 0.25, 1.0
    c = (n // 2 + 0.5) / n
    fx, fy = spread(circle_front(c, c, r, m), tension_forces(circle_front(c, c, r, m), sigma), n)
    dp = -sum(fx[i][n // 2] for i in range(n // 2, n)) / n  # integral of grad p = f across the front
    assert abs(dp - sigma / r) < 0.01 * sigma / r  # measured 3.9957 against 4


def test_rotation_second_order():
    w = 2 * math.pi
    n = 32
    u = grid_field(n, lambda x, y: -w * (y - 0.5))
    v = grid_field(n, lambda x, y: w * (x - 0.5))
    X0 = circle_front(0.5, 0.75, 0.15, 64)
    errs = []
    for steps in (50, 100):
        X, _, _ = front_track(X0, u, v, 1.0 / steps, steps, 0.0, frozen, 0.002, 0.03)
        assert len(X) == 64
        errs.append(max(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(X, X0)))
    assert errs[1] < 1.8e-3 and 3.8 < errs[0] / errs[1] < 4.2


def test_shear_regrid():
    n = 32
    u = grid_field(n, lambda x, y: y - 0.5)
    v = grid_field(n, lambda x, y: 0.0)
    X0 = circle_front(0.5, 0.5, 0.2, 40)
    X, _, _ = front_track(X0, u, v, 0.05, 40, 0.0, frozen, 0.01, 0.03)
    m = len(X)
    lengths = [math.hypot(X[(k + 1) % m][0] - X[k][0], X[(k + 1) % m][1] - X[k][1]) for k in range(m)]
    assert m > 40 and min(lengths) >= 0.01 and max(lengths) <= 0.04
    assert abs(enclosed_area(X) / enclosed_area(X0) - 1.0) < 2e-3
    sq = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert enclosed_area(regrid(sq, 0.1, 0.3)) == 1.0 and len(regrid(sq, 0.1, 0.3)) == 16


def test_bad_input():
    for f in (lambda: tension_forces([(0.0, 0.0), (1.0, 0.0)], 1.0),
              lambda: tension_forces([(0.0, 0.0), (0.0, 0.0), (1.0, 1.0)], 1.0),
              lambda: regrid(circle_front(0.5, 0.5, 0.2, 8), 0.2, 0.3),
              lambda: front_track(circle_front(0.5, 0.5, 0.2, 8), [[0.0]], [[0.0]], 0.0, 1, 1.0, frozen, 0.01, 0.03)):
        try:
            f()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
