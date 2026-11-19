# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/immersed-boundary-method/. The authors are listed in prov/J7JVKP.jsonl.

import math
import random

from immersed_boundary_method import (Grid, circle, divergence, elastic_force, ib_step, interpolate, phi,
                                      polygon_area, project, spread)


def test_four_point_kernel_conditions():
    rng = random.Random(1)
    for r in [0.0, 0.5, 1.0, 1.5, 2.0] + [rng.uniform(-3, 3) for _ in range(200)]:
        js = range(math.floor(r) - 3, math.floor(r) + 4)
        w = [phi(r - j) for j in js]
        assert abs(sum(w) - 1) < 1e-14
        assert abs(sum((r - j) * phi(r - j) for j in js)) < 1e-14
        assert abs(sum(x * x for x in w) - 3 / 8) < 1e-14
        assert abs(sum(phi(r - j) for j in js if j % 2 == 0) - 0.5) < 1e-14
    assert phi(2.0) == 0.0 and abs(phi(0.0) - 0.5) < 1e-15  # continuous, support of width 4


def test_spreading_is_the_adjoint_of_interpolation():
    # sum_x f(x) . u(x) h^2 = sum_l F_l . U(X_l) ds: the power is the same on both sides.
    rng = random.Random(2)
    g = Grid(12)
    u = [rng.uniform(-1, 1) for _ in range(g.N)]
    v = [rng.uniform(-1, 1) for _ in range(g.N)]
    X = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(7)]  # some near the edges, so wrapping is tested
    F = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
    ds = 0.3
    fu, fv = spread(g, F, X, ds)
    U = interpolate(g, u, v, X)
    grid_power = sum(fu[k] * u[k] + fv[k] * v[k] for k in range(g.N)) * g.h**2
    point_power = sum(a * c + b * d for (a, b), (c, d) in zip(F, U)) * ds
    assert abs(grid_power - point_power) < 1e-12


def test_spreading_keeps_total_force_and_torque():
    rng = random.Random(3)
    g = Grid(16)
    X = [(rng.uniform(0.3, 0.7), rng.uniform(0.3, 0.7)) for _ in range(5)]  # support does not wrap
    F = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(5)]
    ds = 0.1
    fu, fv = spread(g, F, X, ds)
    h2 = g.h**2
    assert abs(sum(fu) * h2 - sum(a for a, _ in F) * ds) < 1e-13
    assert abs(sum(fv) * h2 - sum(b for _, b in F) * ds) < 1e-13
    torque_grid = (sum(x * fv[k] for k, (x, _) in enumerate(g.points("v")))
                   - sum(y * fu[k] for k, (_, y) in enumerate(g.points("u")))) * h2
    torque_points = sum(x * b - y * a for (x, y), (a, b) in zip(X, F)) * ds
    assert abs(torque_grid - torque_points) < 1e-13


def test_static_circle_pressure_jump_is_the_laplace_value():
    # Zero rest length springs on a circle: tension kappa R, so the jump is kappa (discrete:
    # kappa (2 - 2 cos ds) / ds^2). The pressure balances the gradient part of the force.
    kappa, R = 1.0, 0.25
    g = Grid(16)
    m = 50
    ds = 2 * math.pi / m
    X = circle(m, 0.5, 0.5, R)
    fu, fv = spread(g, elastic_force(X, kappa, ds), X, ds)
    _, _, p = project(g, fu, fv)
    r = [math.hypot(x - 0.5, y - 0.5) for x, y in g.points("p")]
    pin = [p[k] for k in range(g.N) if r[k] < R - 2 * g.h]
    pout = [p[k] for k in range(g.N) if r[k] > R + 2 * g.h]
    jump = sum(pin) / len(pin) - sum(pout) / len(pout)
    exact = kappa * (2 - 2 * math.cos(ds)) / ds**2
    assert abs(jump - exact) < 1e-3  # measured: 0.998556 against 0.998685
    assert max(pin) - min(pin) < 1e-3  # flat inside


def test_ellipse_relaxes_toward_a_circle_and_keeps_its_area():
    g = Grid(16)
    m = 50
    ds = 2 * math.pi / m
    X = circle(m, 0.5, 0.5, 0.3, 0.2)
    a0 = polygon_area(X)
    u, v = [0.0] * g.N, [0.0] * g.N
    for _ in range(20):
        u, v, p, X = ib_step(g, u, v, X, 1.0, ds, 0.1, 0.005)
        assert max(abs(x) for x in divergence(g, u, v)) < 1e-10
    xs, ys = [x for x, _ in X], [y for _, y in X]
    assert max(xs) - min(xs) < 0.595 and max(ys) - min(ys) > 0.403, (max(xs) - min(xs), max(ys) - min(ys))
    assert abs(polygon_area(X) / a0 - 1) < 1e-3


def test_explicit_step_too_large_blows_up():
    g = Grid(16)
    m = 50
    ds = 2 * math.pi / m
    X = circle(m, 0.5, 0.5, 0.3, 0.2)
    u, v = [0.0] * g.N, [0.0] * g.N
    for _ in range(8):
        u, v, p, X = ib_step(g, u, v, X, 1.0, ds, 0.1, 0.04)  # 4 times the viscous limit h^2 / (4 nu)
    assert max(map(abs, u)) > 10
