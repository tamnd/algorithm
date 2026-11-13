# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-contours/. The authors are listed in prov/JHEZE1.jsonl.

import math
import random

import pytest

from active_contours import (_bspline, cholesky, edge_strength, energy, internal_matrix, snake, solve,
                             spline_potential)


def circle(cx, cy, r, n):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def zero(x, y):
    return 0.0, 0.0, 0.0


def disk_image(n=33, radius=8):
    return [[200 if (x - 16) ** 2 + (y - 16) ** 2 <= radius * radius else 20 for x in range(n)] for y in range(n)]


def step_and_check(v, potential, alpha, beta, gamma, lip, steps):
    """Run single steps. Check E(new) <= E(old) - (gamma - lip / 2) |new - old|^2 at each one."""
    e = energy(v, potential, alpha, beta)
    for _ in range(steps):
        new = snake(v, potential, alpha, beta, gamma, 1)
        e_new = energy(new, potential, alpha, beta)
        moved = sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in zip(v, new))
        assert e_new <= e - (gamma - lip / 2) * moved + 1e-9
        assert e_new <= e + 1e-12
        v, e = new, e_new
    return v


def test_quadratic_form_matches_internal_energy() -> None:
    rng = random.Random(97)
    for n in (3, 4, 5, 9):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(n)]
        alpha, beta = rng.uniform(0, 2), rng.uniform(0, 2)
        a = internal_matrix(n, alpha, beta)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        q = sum(xs[i] * a[i][j] * xs[j] + ys[i] * a[i][j] * ys[j] for i in range(n) for j in range(n)) / 2
        assert math.isclose(q, energy(pts, zero, alpha, beta), rel_tol=1e-12)


def test_pentadiagonal_row() -> None:
    a = internal_matrix(8, 0.5, 0.25)
    assert a[3][1:6] == [0.25, -1.5, 2.5, -1.5, 0.25]
    assert a[0][7] == -1.5 and a[0][6] == 0.25


def test_cholesky_solve() -> None:
    rng = random.Random(101)
    a = internal_matrix(7, 0.3, 0.2)
    m = [[a[i][j] + (0.5 if i == j else 0.0) for j in range(7)] for i in range(7)]
    b = [rng.uniform(-1, 1) for _ in range(7)]
    x = solve(cholesky(m), b)
    for i in range(7):
        assert math.isclose(sum(m[i][j] * x[j] for j in range(7)), b[i], abs_tol=1e-12)


def test_no_image_energy_shrinks_a_circle_by_the_known_factor() -> None:
    n, alpha, beta, gamma = 24, 0.4, 0.2, 1.0
    mu = 2 - 2 * math.cos(2 * math.pi / n)
    factor = gamma / (gamma + alpha * mu + beta * mu * mu)
    v = snake(circle(10, 7, 5, n), zero, alpha, beta, gamma, 1)
    for (x, y), (x0, y0) in zip(v, circle(10, 7, 5 * factor, n)):
        assert math.isclose(x, x0, abs_tol=1e-12) and math.isclose(y, y0, abs_tol=1e-12)
    step_and_check(circle(10, 7, 5, n), zero, alpha, beta, gamma, 0.0, 20)


def test_smooth_analytic_potential_decreases_energy() -> None:
    w = 3.0

    def wave(x, y):
        return (w * math.sin(x / 3) * math.cos(y / 4), w / 3 * math.cos(x / 3) * math.cos(y / 4),
                -w / 4 * math.sin(x / 3) * math.sin(y / 4))

    lip = w * (1 / 9 + 1 / 12 + 1 / 16)
    step_and_check(circle(0, 0, 6, 30), wave, 0.1, 0.1, 0.6, lip, 60)


def test_spline_potential_gradient_and_bounds() -> None:
    rng = random.Random(103)
    grid = [[rng.random() for _ in range(6)] for _ in range(5)]
    p = spline_potential(grid, 2.0)
    for _ in range(50):
        x, y = rng.uniform(-1, 7), rng.uniform(-1, 6)
        e, ex, ey = p(x, y)
        h = 1e-6
        assert math.isclose(ex, (p(x + h, y)[0] - p(x - h, y)[0]) / (2 * h), abs_tol=1e-5)
        assert math.isclose(ey, (p(x, y + h)[0] - p(x, y - h)[0]) / (2 * h), abs_tol=1e-5)
    flat = spline_potential([[3.0] * 4 for _ in range(4)], 1.0)
    assert math.isclose(flat(1.3, 2.7)[0], -3.0)
    for s in range(101):
        t = s / 100
        assert sum(abs(_bspline(t - i)[1]) for i in range(-2, 4)) <= 1.5 + 1e-12
        assert sum(abs(_bspline(t - i)[2]) for i in range(-2, 4)) <= 4.0 + 1e-12


def test_disk_energy_decreases_and_contour_locks_on() -> None:
    strength = edge_strength(disk_image(), 2.0)
    weight, alpha, beta = 1.0, 0.05, 0.05
    lip = 6.25 * weight * max(max(r) for r in strength)
    gamma = 3.5
    assert gamma > lip / 2
    v = step_and_check(circle(16, 16, 13, 40), spline_potential(strength, weight), alpha, beta, gamma, lip, 300)
    radii = [math.hypot(x - 16, y - 16) for x, y in v]
    assert all(abs(r - 8) <= 1 for r in radii)


def test_result_depends_on_the_start() -> None:
    """Two disks of radius 6. A start around one disk finds that disk; a start around both wraps both."""
    image = [[200 if min((x - 12) ** 2, (x - 36) ** 2) + (y - 16) ** 2 <= 36 else 20 for x in range(48)]
             for y in range(33)]
    p = spline_potential(edge_strength(image, 1.5), 1.0)
    for cx in (12, 36):
        v = snake(circle(cx, 16, 10, 40), p, 0.05, 0.05, 1.0, 200)
        assert all(abs(math.hypot(x - cx, y - 16) - 6) <= 1 for x, y in v)
    both = snake(circle(24, 16, 22, 60), p, 0.05, 0.05, 1.0, 300)
    xs = [x for x, _ in both]
    assert min(xs) < 7 and max(xs) > 41


def test_errors() -> None:
    with pytest.raises(ValueError):
        snake([(0, 0), (1, 0)], zero, 1, 1, 1, 1)
    with pytest.raises(ValueError):
        snake(circle(0, 0, 1, 5), zero, 1, 1, 0, 1)
