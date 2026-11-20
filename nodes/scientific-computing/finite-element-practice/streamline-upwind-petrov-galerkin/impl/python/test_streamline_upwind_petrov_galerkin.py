# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/streamline-upwind-petrov-galerkin/. The authors are listed in prov/CZJ24B.jsonl.

import math
import random
from fractions import Fraction as F

import scisparse
from streamline_upwind_petrov_galerkin import cell_peclet, exact, optimal_tau, supg


def max_nodal_error(U, u, m):
    return max(abs(U[j] - u(j / m)) for j in range(m + 1))


def test_cell_peclet_and_tau() -> None:
    assert cell_peclet(0.01, 1.0, 0.1) == 5.0
    h, eps = 0.1, 0.01
    pe = cell_peclet(eps, 1.0, h)
    expected = h / 2 * (1 / math.tanh(pe) - 1 / pe)
    assert abs(optimal_tau(eps, 1.0, h) - expected) < 1e-15
    # the sign of a does not change tau
    assert optimal_tau(eps, -1.0, h) == optimal_tau(eps, 1.0, h)
    # small Pe: tau = h^2 / (12 eps) to first order
    t = optimal_tau(1.0, 1.0, 1e-6)
    assert abs(t / (1e-12 / 12) - 1) < 1e-6
    # large Pe: tau tends to h / (2 |a|)
    assert abs(optimal_tau(1e-8, 2.0, 0.1) - 0.1 / 4) < 1e-8


def test_nodally_exact_for_constant_source() -> None:
    rng = random.Random(7)
    # oracle: the closed-form solution, sampled at the nodes
    for _ in range(500):
        eps = 10 ** rng.uniform(-3, 0)
        a = rng.choice([-1, 1]) * rng.uniform(0.5, 2.0)
        c = rng.uniform(-2, 2)
        g0, g1 = rng.uniform(-1, 1), rng.uniform(-1, 1)
        m = rng.randint(2, 20)
        U = supg(eps, a, lambda x: c, m, g0, g1)
        err = max_nodal_error(U, lambda x: exact(eps, a, c, g0, g1, x), m)
        assert err < 1e-9, (eps, a, m, err)


def test_galerkin_oscillates_supg_does_not() -> None:
    eps, a, m = 0.01, 1.0, 10  # Pe_h = 5
    gal = supg(eps, a, lambda x: 0.0, m, 0.0, 1.0, tau=0)
    st = supg(eps, a, lambda x: 0.0, m, 0.0, 1.0)
    assert min(gal) < -0.5  # negative values although 0 <= u <= 1
    assert any(gal[j + 1] < gal[j] for j in range(m))
    assert all(st[j] <= st[j + 1] for j in range(m))
    assert all(-1e-12 <= v <= 1 + 1e-12 for v in st)


def test_exact_fraction_equivalence_with_extra_diffusion() -> None:
    # P1, constant data: SUPG with tau equals Galerkin with eps + tau a^2
    for eps, a, tau, c, m in [(F(1, 50), F(1), F(1, 25), F(1), 10),
                              (F(1, 3), F(-2), F(1, 7), F(-3, 2), 7)]:
        s = supg(eps, a, lambda x: c, m, F(0), F(1), tau=tau)
        g = supg(eps + tau * a * a, a, lambda x: c, m, F(0), F(1), tau=F(0))
        assert s == g
        assert all(isinstance(v, F) for v in s)


def test_linear_solution_reproduced_for_any_tau() -> None:
    # u = 2 x + 1 solves -eps u'' + a u' = 2 a; the residual is zero on every cell
    for tau in (F(0), F(1, 9), F(3)):
        U = supg(F(1, 10), F(3), lambda x: F(6), 9, F(1), F(3), tau=tau)
        assert U == [1 + 2 * F(j, 9) for j in range(10)]


def test_thomas_solves_the_assembled_rows() -> None:
    # residual check of the helper on a diagonally dominant system
    rng = random.Random(3)
    n = 12
    a = [rng.uniform(-1, 0) for _ in range(n)]
    c = [rng.uniform(-1, 0) for _ in range(n)]
    b = [abs(a[i]) + abs(c[i]) + rng.uniform(0.1, 1) for i in range(n)]
    d = [rng.uniform(-1, 1) for _ in range(n)]
    x = scisparse.thomas(a, b, c, d)
    for i in range(n):
        r = b[i] * x[i] - d[i]
        if i > 0:
            r += a[i] * x[i - 1]
        if i < n - 1:
            r += c[i] * x[i + 1]
        assert abs(r) < 1e-12


def test_refinement_rates() -> None:
    a = 1.0
    for eps, lo in ((1.0, 3.8), (0.01, 3.0)):
        def f(x, eps=eps):
            return eps * math.pi ** 2 * math.sin(math.pi * x) + a * math.pi * math.cos(math.pi * x)

        def u(x):
            return math.sin(math.pi * x)

        e = [max_nodal_error(supg(eps, a, f, m), u, m) for m in (16, 32, 64)]
        assert math.log2(e[1] / e[2]) > lo, (eps, e)
        g = [max_nodal_error(supg(eps, a, f, m, tau=0), u, m) for m in (16, 32, 64)]
        assert abs(math.log2(g[1] / g[2]) - 2) < 0.1
        assert e[2] < g[2]
