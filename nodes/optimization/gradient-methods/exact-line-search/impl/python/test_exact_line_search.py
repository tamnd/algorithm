# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exact-line-search/. The authors are listed in prov/V5H45Q.jsonl.

import math
import random

import pytest

from exact_line_search import (
    GOLDEN,
    dot,
    exact_line_search,
    exact_step_quadratic,
    matvec,
    steepest_descent_exact,
    steepest_descent_quadratic,
)

TOL = 1e-9
# Golden-section search in double precision can locate a minimizer only to about
# sqrt(2^-53) ~ 1.5e-8 relative to the scale of the problem; allow ten times that.
SQRT_EPS_SLACK = 1.5e-7


def householder(v):
    """The orthogonal matrix I - 2 v v^T / (v^T v)."""
    s = sum(t * t for t in v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


def random_spd(rng, n, lo=0.1, hi=10.0):
    """A = Q diag(lam) Q^T with known eigenvalues lam."""
    lam = [rng.uniform(lo, hi) for _ in range(n)]
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    a = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    return a, lam, q


def test_worked_example():
    """f = 1/2 (x1^2 + 10 x2^2) from (10, 1): the step is 2/11 at every iteration and
    x_k = (9/11)^k (10, (-1)^k), so f drops by the factor (9/11)^2 each step."""
    phi = lambda t: 55.0 - 200.0 * t + 550.0 * t * t
    alpha, lo, hi = exact_line_search(phi, 1.0, 1e-8)
    assert lo <= 2.0 / 11.0 <= hi and hi - lo <= 1e-8
    assert abs(alpha - 2.0 / 11.0) <= 0.5e-8
    a = [[1.0, 0.0], [0.0, 10.0]]
    path = steepest_descent_quadratic(a, [0.0, 0.0], [10.0, 1.0], 30)
    f = lambda x: 0.5 * (x[0] ** 2 + 10.0 * x[1] ** 2)
    for k, x in enumerate(path):
        r = (9.0 / 11.0) ** k
        assert math.isclose(x[0], 10.0 * r, rel_tol=1e-12)
        assert math.isclose(x[1], (-1.0) ** k * r, rel_tol=1e-12)
        if k > 0:
            assert math.isclose(f(x), (81.0 / 121.0) * f(path[k - 1]), rel_tol=1e-12)
    g0 = [10.0, 10.0]
    assert exact_step_quadratic(a, g0, [-10.0, -10.0]) == 2.0 / 11.0
    path = steepest_descent_quadratic(a, [0.0, 0.0], [10.0, 1.0], 1000, tol=1e-6)
    assert len(path) - 1 == 83


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        exact_line_search(lambda t: t, 0.0)
    with pytest.raises(ValueError):
        exact_line_search(lambda t: t, 1.0, 0.0)
    with pytest.raises(ValueError):
        exact_line_search(lambda t: -t, 1.0, 1e-6)
    with pytest.raises(ValueError):
        exact_step_quadratic([[1.0, 0.0], [0.0, -1.0]], [0.0, 1.0], [0.0, -1.0])


def test_bracket_contains_minimizer():
    """For strictly unimodal phi with a known minimizer a*: lo <= a* <= hi, hi - lo <= tau,
    and |alpha - a*| <= tau / 2."""
    rng = random.Random(8201)
    shapes = [
        lambda p, s: (lambda t: p * (t - s) ** 2),
        lambda p, s: (lambda t: p * (math.sqrt(1.0 + (t - s) ** 2) - 1.0)),
        lambda p, s: (lambda t: p * abs(t - s) ** 1.5),
        lambda p, s: (lambda t: -p / (1.0 + (t - s) ** 2)),
    ]
    for _ in range(2000):
        star = rng.choice([0.0, rng.uniform(0, 1), rng.uniform(0, 1000), 1e-7])
        p = rng.uniform(0.1, 10.0)
        q = rng.uniform(-3, 3)
        base = rng.choice(shapes)(p, star)
        phi = lambda t, base=base, q=q: base(t) + q
        h = rng.choice([1.0, 0.01, 50.0])
        tau = rng.choice([1e-4, 1e-6])
        alpha, lo, hi = exact_line_search(phi, h, tau)
        # Near a minimizer phi is flat to second order, so comparisons of phi values in floating
        # point locate the minimizer only to about sqrt(machine epsilon) times the scale.
        slack = SQRT_EPS_SLACK * (1 + star)
        assert lo - slack <= star <= hi + slack
        assert hi - lo <= tau
        assert abs(alpha - star) <= tau / 2 + slack


def test_golden_section_count():
    """Each golden-section pass multiplies hi - lo by GOLDEN, so the number of passes from [0, h]
    is the least j with h * GOLDEN^j <= tau."""
    calls = []
    phi = lambda t: calls.append(t) or (t - 0.3) ** 2
    exact_line_search(phi, 1.0, 1e-6)
    passes = (len(calls) - 2) // 2
    expected = math.ceil(math.log(1e-6) / math.log(GOLDEN))
    assert passes in (expected, expected + 1)


def test_quadratic_closed_form_agrees():
    rng = random.Random(8202)
    for _ in range(500):
        n = rng.randint(1, 5)
        a, lam, _ = random_spd(rng, n)
        b = [rng.uniform(-5, 5) for _ in range(n)]
        x = [rng.uniform(-5, 5) for _ in range(n)]
        g = [gi - bi for gi, bi in zip(matvec(a, x), b)]
        d = [rng.gauss(0, 1) for _ in range(n)]
        if dot(g, d) > 0:
            d = [-t for t in d]
        if abs(dot(g, d)) < 1e-3:
            continue
        exact = exact_step_quadratic(a, g, d)
        f = lambda y: 0.5 * dot(y, matvec(a, y)) - dot(b, y)
        phi = lambda t: f([xi + t * di for xi, di in zip(x, d)])
        alpha, lo, hi = exact_line_search(phi, 1.0, 1e-6)
        assert abs(alpha - exact) <= 0.5e-6 + SQRT_EPS_SLACK * (1 + exact)
        xn = [xi + exact * di for xi, di in zip(x, d)]
        gn = [gi - bi for gi, bi in zip(matvec(a, xn), b)]
        assert abs(dot(gn, d)) <= 1e-9 * (1 + math.sqrt(dot(g, g) * dot(d, d)))


def test_kantorovich_bound_every_step():
    """Steepest descent with exact steps on 1/2 (x - x*)^T A (x - x*):
    E(x_{k+1}) <= ((kappa - 1)/(kappa + 1))^2 E(x_k) and successive gradients are orthogonal."""
    rng = random.Random(8203)
    for _ in range(200):
        n = rng.randint(1, 6)
        a, lam, _ = random_spd(rng, n, 0.1, rng.choice([1.0, 10.0, 100.0]))
        kappa = max(lam) / min(lam)
        factor = ((kappa - 1.0) / (kappa + 1.0)) ** 2
        xstar = [rng.uniform(-5, 5) for _ in range(n)]
        b = matvec(a, xstar)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        path = steepest_descent_quadratic(a, b, x0, 100, tol=1e-6)

        def err(x):
            e = [xi - si for xi, si in zip(x, xstar)]
            return 0.5 * dot(e, matvec(a, e))

        for k in range(1, len(path)):
            assert err(path[k]) <= factor * err(path[k - 1]) + 1e-12 * (1 + err(path[k - 1]))
            g0 = [gi - bi for gi, bi in zip(matvec(a, path[k - 1]), b)]
            g1 = [gi - bi for gi, bi in zip(matvec(a, path[k]), b)]
            assert abs(dot(g0, g1)) <= 1e-8 * (1 + dot(g0, g0))


def test_nonquadratic_strongly_convex_bound():
    """f(x) = sum_i a_i z_i^2 / 2 + b_i log cosh z_i with z = Q x is mu-strongly convex and
    L-smooth with mu = min a_i and L = max (a_i + b_i), and f* = 0 at x = 0.
    With golden-section steps, f(x_{k+1}) <= (1 - mu/L) f(x_k) at every step, up to 1e-12."""
    rng = random.Random(8204)
    for _ in range(60):
        n = rng.randint(1, 4)
        q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
        av = [rng.uniform(0.5, 3.0) for _ in range(n)]
        bv = [rng.uniform(0.0, 5.0) for _ in range(n)]
        mu, big_l = min(av), max(x + y for x, y in zip(av, bv))

        def f(x):
            z = matvec(q, x)
            # log cosh z = log1p(2 sinh^2(z/2)) keeps full relative accuracy for small z.
            return sum(ai * zi * zi / 2 + bi * math.log1p(2.0 * math.sinh(zi / 2) ** 2) for ai, bi, zi in zip(av, bv, z))

        def grad(x):
            z = matvec(q, x)
            w = [ai * zi + bi * math.tanh(zi) for ai, bi, zi in zip(av, bv, z)]
            return [sum(q[t][i] * w[t] for t in range(n)) for i in range(n)]

        x0 = [rng.uniform(-4, 4) for _ in range(n)]
        tau = 1e-6
        path, steps = steepest_descent_exact(f, grad, x0, 60, tau=tau, tol=1e-5)
        for k in range(1, len(path)):
            assert f(path[k]) <= (1.0 - mu / big_l) * f(path[k - 1]) + 1e-12
            g0, g1 = grad(path[k - 1]), grad(path[k])
            # |phi'(alpha)| <= L ||g||^2 |alpha - a*|, and |alpha - a*| <= tau / 2 plus rounding.
            assert abs(dot(g0, g1)) <= big_l * dot(g0, g0) * (tau / 2 + SQRT_EPS_SLACK * (1 + steps[k - 1]))
