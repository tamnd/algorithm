# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multigrid-method/. The authors are listed in prov/ZXX910.jsonl.

import math
import random
from fractions import Fraction

import pytest

from multigrid_method import (
    apply_a, jacobi_damping, level_of, multigrid, prolong, restrict, smooth, v_cycle,
)


def exact_solve(f, h2inv):
    """Thomas algorithm for tridiag(-1, 2, -1) h^-2 u = f in exact arithmetic."""
    n = len(f)
    d = [Fraction(v) / h2inv for v in f]
    c, dd = [Fraction(0)] * n, [Fraction(0)] * n
    piv = Fraction(2)
    c[0], dd[0] = Fraction(-1) / piv, d[0] / piv
    for i in range(1, n):
        piv = 2 + c[i - 1]
        c[i] = Fraction(-1) / piv
        dd[i] = (d[i] + dd[i - 1]) / piv
    u = [Fraction(0)] * n
    u[-1] = dd[-1]
    for i in range(n - 2, -1, -1):
        u[i] = dd[i] - c[i] * u[i + 1]
    return u


def kappa(n):
    return (math.sin(n * math.pi / (2 * (n + 1))) / math.sin(math.pi / (2 * (n + 1)))) ** 2


def norm(v):
    return math.sqrt(sum(float(x) ** 2 for x in v))


def test_level_of():
    assert [level_of(n) for n in (1, 3, 7, 1023)] == [1, 2, 3, 10]
    for bad in (0, 2, 6, 8):
        with pytest.raises(ValueError):
            level_of(bad)


def test_single_unknown_is_solved_exactly():
    u, k, conv = multigrid([Fraction(3)], tol=0)
    assert u == [Fraction(3, 8)] and k == 1 and conv
    u, k, conv = multigrid([3.0])
    assert conv and k == 1 and u == [3.0 / 8]


def test_galerkin_property_exact():
    # R A_h P = A_2h for full weighting and linear interpolation
    for L in (2, 3, 4):
        nc = 2 ** (L - 1) - 1
        for j in range(nc):
            e = [Fraction(int(i == j)) for i in range(nc)]
            lhs = restrict(apply_a(prolong(e), 4 ** L))
            rhs = apply_a(e, 4 ** (L - 1))
            assert lhs == rhs


def test_exact_solution_is_a_fixed_point():
    rng = random.Random(3)
    f = [Fraction(rng.randint(-9, 9)) for _ in range(15)]
    u = exact_solve(f, 4 ** 4)
    assert v_cycle(u, f) == u
    assert v_cycle(u, f, 1, 1, "gs") == u


def test_exact_two_grid_contraction():
    rng = random.Random(4)
    for _ in range(5):
        f = [Fraction(rng.randint(-9, 9)) for _ in range(15)]
        x = exact_solve(f, 4 ** 4)
        u = [Fraction(0)] * 15
        e0 = norm([a - b for a, b in zip(u, x)])
        for _ in range(3):
            u = v_cycle(u, f)
        e3 = norm([a - b for a, b in zip(u, x)])
        assert e3 <= 0.2 ** 3 * e0


def test_iteration_count_independent_of_n():
    for kind, nu, cap in (("jacobi", (2, 1), 13), ("gs", (1, 1), 14)):
        counts = []
        for L in range(3, 12):
            n = 2 ** L - 1
            rng = random.Random(100 + L)
            f = [rng.uniform(-1, 1) for _ in range(n)]
            u, k, conv = multigrid(f, tol=1e-10, nu1=nu[0], nu2=nu[1], kind=kind)
            assert conv and k <= cap
            if L >= 6:
                counts.append(k)
        assert max(counts) - min(counts) <= 2  # h-independent once past small grids


def test_random_rhs_error_bound():
    for seed in range(12):
        rng = random.Random(seed)
        L = rng.randint(2, 8)
        n = 2 ** L - 1
        f = [rng.uniform(-5, 5) for _ in range(n)]
        u, k, conv = multigrid(f, tol=1e-9)
        x = [float(v) for v in exact_solve(f, 4 ** L)]
        rel = norm([a - b for a, b in zip(f, apply_a(u, 4 ** L))]) / norm(f)
        err = norm([a - b for a, b in zip(u, x)]) / norm(x)
        assert conv and rel <= 1e-9
        assert err <= kappa(n) * rel * 1.001 + 1e-14


def test_jacobi_smoothing_factor():
    n, w = 63, 2 / 3
    for k in range((n + 1) // 2, n + 1):
        assert abs(jacobi_damping(n, k, w)) <= 1 / 3 + 1e-12
    assert jacobi_damping(n, 1, w) > 0.998  # smooth modes are barely touched
    for k in (1, 17, 40, 63):
        mode = [math.sin(k * math.pi * (i + 1) / (n + 1)) for i in range(n)]
        out = smooth(mode, [0.0] * n, 4 ** 6, 1, "jacobi", w)
        g = jacobi_damping(n, k, w)
        assert max(abs(a - g * b) for a, b in zip(out, mode)) <= 1e-12


def test_divergence_with_bad_relaxation():
    h = []
    u, k, conv = multigrid([1.0] * 63, omega=1.5, maxiter=30, history=h)
    assert not conv and h[-1] > 1e10


def test_stagnation_at_rounding_level():
    rng = random.Random(8)
    f = [rng.uniform(-1, 1) for _ in range(255)]
    h = []
    u, k, conv = multigrid(f, tol=1e-18, maxiter=25, history=h)
    assert not conv
    assert 1e-18 < min(h) < 1e-12
    assert max(h[-5:]) / min(h[-5:]) < 100
