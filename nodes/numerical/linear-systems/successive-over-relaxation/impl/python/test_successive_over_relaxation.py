# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-over-relaxation/. The authors are listed in prov/MJSE1P.jsonl.

import math
import random
from fractions import Fraction

import pytest

from successive_over_relaxation import (
    ZeroDiagonal, from_dense, optimal_omega, residual, sor, sor_radius, sor_sweep,
)

U = 2.0 ** -53


def model(n):
    return [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]


def exact_solve(a, b):
    n = len(b)
    g = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if g[i][k] != 0)
        g[k], g[p] = g[p], g[k]
        piv = g[k][k]
        g[k] = [v / piv for v in g[k]]
        for i in range(n):
            if i != k and g[i][k] != 0:
                f = g[i][k]
                g[i] = [vi - f * vk for vi, vk in zip(g[i], g[k])]
    return [row[n] for row in g]


def inf_norm_inverse(a):
    n = len(a)
    cols = [exact_solve(a, [1 if i == j else 0 for i in range(n)]) for j in range(n)]
    return max(sum(abs(cols[j][i]) for j in range(n)) for i in range(n))


def random_spd(rng, n):
    b = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    return [[sum(b[k][i] * b[k][j] for k in range(n)) + (n if i == j else 0) for j in range(n)] for i in range(n)]


def gauss_seidel_sweep(a, b, x):
    n = len(b)
    for i in range(n):
        x[i] = (b[i] - sum(a[i][j] * x[j] for j in range(n) if j != i)) / a[i][i]


def test_one_by_one():
    x, k, ok = sor(from_dense([[5.0]]), [10.0], 1.0)
    assert ok and k == 1 and x == [2.0]


def test_diagonal_exact_in_one_sweep():
    d = [3.0, -2.0, 0.5, 8.0]
    a = [[d[i] if i == j else 0.0 for j in range(4)] for i in range(4)]
    x, k, ok = sor(from_dense(a), [6.0, 4.0, 1.0, 16.0], 1.0)
    assert ok and k == 1 and x == [2.0, -2.0, 2.0, 2.0]


def test_hand_sweep():
    a = [[Fraction(v) for v in r] for r in [[4, -1, 0], [-1, 4, -1], [0, -1, 4]]]
    x = [Fraction(0)] * 3
    sor_sweep(from_dense(a), [Fraction(3), Fraction(2), Fraction(3)], x, Fraction(6, 5), [Fraction(4)] * 3)
    assert x == [Fraction(9, 10), Fraction(87, 100), Fraction(1161, 1000)]


def test_omega_one_is_gauss_seidel_exactly():
    rng = random.Random(1)
    for _ in range(30):
        n = rng.randint(2, 6)
        a = [[Fraction(rng.randint(-4, 4)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] = Fraction(rng.choice([-1, 1]) * rng.randint(1, 9))
        b = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        x = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        y = list(x)
        diag = [a[i][i] for i in range(n)]
        for _ in range(3):
            sor_sweep(from_dense(a), b, x, Fraction(1), diag)
            gauss_seidel_sweep(a, b, y)
        assert x == y


def test_solution_is_a_fixed_point():
    rng = random.Random(2)
    for _ in range(30):
        n = rng.randint(1, 6)
        a = random_spd(rng, n)
        b = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        xs = exact_solve(a, b)
        x = list(xs)
        omega = Fraction(rng.randint(1, 19), 10)
        sor_sweep(from_dense(a), b, x, omega, [a[i][i] for i in range(n)])
        assert x == xs


def test_random_spd_converges_and_error_is_bounded_by_kappa_times_residual():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(2, 7)
        a = random_spd(rng, n)
        b = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        if all(v == 0 for v in b):
            b[0] = Fraction(1)
        omega = rng.choice([0.4, 1.0, 1.3, 1.8])
        af = [[float(v) for v in row] for row in a]
        x, k, ok = sor(from_dense(af), [float(v) for v in b], omega, tol=1e-12, maxiter=20000)
        assert ok, (n, omega)
        xs = exact_solve(a, b)
        r = [b[i] - sum(a[i][j] * Fraction(x[j]) for j in range(n)) for i in range(n)]
        norm_a = max(sum(abs(v) for v in row) for row in a)
        kappa = norm_a * inf_norm_inverse(a)
        err = max(abs(Fraction(x[i]) - xs[i]) for i in range(n)) / max(abs(v) for v in xs)
        relres = max(abs(v) for v in r) / max(abs(v) for v in b)
        assert err <= kappa * relres  # exact: ||e||/||x|| <= kappa ||r||/||b||


def predicted(rho, tol):
    return math.log(tol) / math.log(rho)


def test_iteration_counts_match_young_theory():
    n, tol = 20, 1e-8
    rows, b = from_dense(model(n)), [1.0] * n
    mu = math.cos(math.pi / (n + 1))
    counts = {}
    for omega in (1.0, 1.5, 1.9):
        _, k, ok = sor(rows, b, omega, tol=tol)
        assert ok
        ratio = k / predicted(sor_radius(mu, omega), tol)
        assert 0.85 <= ratio <= 1.2, (omega, k, ratio)
        counts[omega] = k
    wopt = optimal_omega(mu)
    _, kopt, ok = sor(rows, b, wopt, tol=tol)
    assert ok and kopt < min(counts.values())
    assert kopt <= 1.5 * predicted(wopt - 1, tol)  # a Jordan block at omega_opt slows it a little


def test_optimal_sor_scales_like_n_gauss_seidel_like_n_squared():
    tol = 1e-8
    gs, opt = [], []
    for n in (10, 20, 40):
        rows, b = from_dense(model(n)), [1.0] * n
        mu = math.cos(math.pi / (n + 1))
        opt.append(sor(rows, b, optimal_omega(mu), tol=tol)[1])
        if n < 40:
            gs.append(sor(rows, b, 1.0, tol=tol)[1])
    assert 3.3 <= gs[1] / gs[0] <= 4.2
    for p, q in zip(opt, opt[1:]):
        assert 1.7 <= q / p <= 2.3


def test_radius_formula_against_observed_contraction():
    n = 10
    a = model(n)
    rows = from_dense(a)
    mu = math.cos(math.pi / (n + 1))
    assert sor_radius(mu, 1.0) == pytest.approx(mu * mu)
    w = optimal_omega(mu)
    assert sor_radius(mu, w) == pytest.approx(w - 1)
    rng = random.Random(4)
    for omega in (0.8, 1.0, 1.3):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        zero = [0.0] * n
        for _ in range(150):
            sor_sweep(rows, zero, x, omega, [2.0] * n)
        before = math.sqrt(sum(v * v for v in x))
        sor_sweep(rows, zero, x, omega, [2.0] * n)
        after = math.sqrt(sum(v * v for v in x))
        assert after / before == pytest.approx(sor_radius(mu, omega), rel=0.02)


def test_omega_outside_zero_two_diverges():
    n = 20
    rows, b = from_dense(model(n)), [1.0] * n
    for omega in (2.0, 2.2, -0.5):
        x, k, ok = sor(rows, b, omega, maxiter=300)
        assert not ok
    x, _, _ = sor(rows, b, 2.2, maxiter=60)
    assert max(abs(v) for v in residual(rows, b, x)) > 1e3


def test_symmetric_indefinite_diverges_for_every_omega():
    rows = from_dense([[1.0, 2.0], [2.0, 1.0]])
    for omega in (0.5, 1.0, 1.5):
        x, k, ok = sor(rows, [1.0, 1.0], omega, maxiter=100)
        assert not ok
        assert not max(abs(v) for v in x) <= 1e3  # grows without bound (or overflows to inf, nan)


def test_nonsymmetric_gauss_seidel_divergence():
    rows = from_dense([[1.0, 2.0, -2.0], [1.0, 1.0, 1.0], [2.0, 2.0, 1.0]])  # rho(G_1) = 2
    x, k, ok = sor(rows, [1.0, 3.0, 5.0], 1.0, maxiter=100)
    assert not ok


def test_zero_diagonal_raises():
    with pytest.raises(ZeroDiagonal):
        sor(from_dense([[0.0, 1.0], [1.0, 0.0]]), [1.0, 1.0], 1.0)


def test_stagnation_at_rounding_level():
    n = 20
    rows, b = from_dense(model(n)), [1.0] * n
    x, k, ok = sor(rows, b, 1.74, tol=1e-18, maxiter=1500)
    assert not ok  # the tolerance is below what rounding allows
    r = max(abs(v) for v in residual(rows, b, x))
    xn = max(abs(v) for v in x)
    assert r <= n * U * 4.0 * xn  # observed: about 0.4 u ||A|| ||x||, not a proved bound
    exact = [(i + 1) * (n - i) / 2 for i in range(n)]
    assert max(abs(p - q) for p, q in zip(x, exact)) <= 1e-12
