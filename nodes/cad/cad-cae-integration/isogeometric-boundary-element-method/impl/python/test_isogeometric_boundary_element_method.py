# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeometric-boundary-element-method/. The authors are listed in prov/JQY36Z.jsonl.

import math
import random

from isogeometric_boundary_element_method import (
    flux_at,
    interior_value,
    refined_circle,
    solve_dirichlet,
)


def flux_error(curve, q, grad, samples=400):
    """Largest |q_h - dg/dn| over equally spaced parameters."""
    worst = 0.0
    for k in range(samples):
        t = k / samples
        (x, y), _, n, _ = curve.eval(t)
        gx, gy = grad(x, y)
        worst = max(worst, abs(flux_at(curve, q, t) - (gx * n[0] + gy * n[1])))
    return worst


def test_refined_geometry_is_exact() -> None:
    rng = random.Random(5)
    for per_span in (1, 3, 8):
        c = refined_circle(2.0, per_span)
        for _ in range(200):
            (x, y), _, n, row = c.eval(rng.random())
            assert abs(math.hypot(x, y) - 2.0) < 1e-12
            assert abs(n[0] * x + n[1] * y - 2.0) < 1e-12  # outward unit normal
            assert abs(sum(row) - 1.0) < 1e-12  # partition of unity of the merged basis


def test_single_layer_of_a_constant() -> None:
    """On a circle of radius R, int u*(x, y) ds_y = -R ln R for x on the circle."""
    for radius in (2.0, 0.5):
        c = refined_circle(radius, 4)
        _, _, _, _, _, G = solve_dirichlet(c, lambda x, y: 0.0)
        for row in G:
            assert abs(sum(row) + radius * math.log(radius)) < 1e-7


def test_degenerate_scale_radius_one() -> None:
    """Pitfall: for R = 1 the constant is in the kernel of the single layer, so G is (nearly) singular."""
    c = refined_circle(1.0, 4)
    _, _, _, _, _, G = solve_dirichlet(c, lambda x, y: 0.0)
    assert max(abs(sum(row)) for row in G) < 1e-7
    assert max(abs(v) for row in G for v in row) > 1e-2


def test_constant_data_gives_zero_flux() -> None:
    c = refined_circle(2.0, 4)
    _, q, _, _, _, _ = solve_dirichlet(c, lambda x, y: 1.0)
    assert max(abs(v) for v in q) < 1e-7


def test_exact_when_data_and_flux_are_in_the_space() -> None:
    """u = x + 2 y on the circle of radius 2 has q = (x + 2 y) / 2, and both are NURBS of the basis."""
    for per_span in (1, 2, 4):
        c = refined_circle(2.0, per_span)
        u, q, _, _, _, _ = solve_dirichlet(c, lambda x, y: x + 2 * y)
        for uj, qj, (px, py) in zip(u, q, c.pts):
            assert abs(uj - (px + 2 * py)) < 1e-12
            assert abs(qj - (px + 2 * py) / 2) < 1e-7  # only the quadrature error is left


def test_circle_against_exact_solution() -> None:
    """u = x^2 - y^2 on the circle of radius 2: q = 2 R cos(2 theta)."""
    g = lambda x, y: x * x - y * y
    grad = lambda x, y: (2 * x, -2 * y)
    errs = []
    for per_span in (4, 8, 16):
        c = refined_circle(2.0, per_span)
        u, q, _, _, _, _ = solve_dirichlet(c, g)
        errs.append(flux_error(c, q, grad))
        if per_span == 8:
            assert abs(interior_value(c, u, q, (0.5, 0.3)) - 0.16) < 1e-5
    assert errs[1] < 3e-3
    rates = [math.log2(errs[k] / errs[k + 1]) for k in range(2)]
    assert all(r > 2.7 for r in rates), rates


def test_ellipse_against_exact_solution() -> None:
    g = lambda x, y: x * x - y * y + 0.5 * x * y + x
    grad = lambda x, y: (2 * x + 0.5 * y + 1, -2 * y + 0.5 * x)
    errs = []
    for per_span in (4, 8):
        c = refined_circle(2.0, per_span, 1.0, 0.75)
        u, q, _, _, _, _ = solve_dirichlet(c, g)
        errs.append(flux_error(c, q, grad))
    assert errs[1] < 5e-3 and errs[0] / errs[1] > 6
    assert abs(interior_value(c, u, q, (0.5, 0.3)) - g(0.5, 0.3)) < 1e-4
