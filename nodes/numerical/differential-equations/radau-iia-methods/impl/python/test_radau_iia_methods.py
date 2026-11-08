# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radau-iia-methods/. The authors are listed in prov/SBC09Y.jsonl.

import math
from fractions import Fraction as F

import pytest

from radau_iia_methods import (pade_exp, radau_iia, radau_nodes, radau_polynomial, radau_tableau,
                               stability_function)


def B(tab, k):
    return sum(bi * ci ** (k - 1) for bi, ci in zip(tab.b, tab.c)) - F(1, k)


def C(tab, k):
    return [sum(a * cj ** (k - 1) for a, cj in zip(row, tab.c)) - ci ** k / k for row, ci in zip(tab.A, tab.c)]


def D(tab, k):
    s = tab.stages
    return [sum(tab.b[i] * tab.c[i] ** (k - 1) * tab.A[i][j] for i in range(s)) - tab.b[j] * (1 - tab.c[j] ** k) / k
            for j in range(s)]


def test_tableau_exact_small():
    t1 = radau_tableau(1)
    assert (t1.A, t1.b, t1.c) == ([[1]], [1], [1])  # backward Euler
    t2 = radau_tableau(2)
    assert t2.c == [F(1, 3), F(1)]
    assert t2.A == [[F(5, 12), F(-1, 12)], [F(3, 4), F(1, 4)]]
    assert t2.b == [F(3, 4), F(1, 4)]


def test_order_conditions_exact_s2():
    t = radau_tableau(2)
    assert all(B(t, k) == 0 for k in (1, 2, 3)) and B(t, 4) != 0
    assert all(x == 0 for k in (1, 2) for x in C(t, k))
    assert all(x == 0 for x in D(t, 1))
    # the four trees of order <= 3 directly
    s = 2
    assert sum(t.b[i] * t.A[i][j] * t.c[j] for i in range(s) for j in range(s)) == F(1, 6)


@pytest.mark.parametrize("s", [3, 4, 5])
def test_simplifying_conditions_float(s):
    t = radau_tableau(s)
    assert t.c[-1] == 1 and t.A[-1] == t.b  # stiffly accurate
    assert all(abs(B(t, k)) < 1e-12 for k in range(1, 2 * s))
    assert abs(B(t, 2 * s)) > 1e-6
    assert all(abs(x) < 1e-12 for k in range(1, s + 1) for x in C(t, k))
    assert all(abs(x) < 1e-12 for k in range(1, s) for x in D(t, k))
    p = radau_polynomial(s)
    assert all(abs(sum(float(a) * c ** i for i, a in enumerate(p))) < 1e-10 for c in t.c)


def test_stability_function_is_pade():
    for s in (1, 2):
        t = radau_tableau(s)
        for z in (F(-7), F(3, 7), F(-1, 3), F(10 ** 6)):
            assert stability_function(t, z) == pade_exp(s - 1, s, z)
    for s in (3, 4, 5):
        t = radau_tableau(s)
        for z in (-0.5, 0.37, -20.0, 3.0):
            assert abs(stability_function(t, z) - float(pade_exp(s - 1, s, F(z)))) < 1e-11
        assert abs(stability_function(t, -1e9)) < 1e-7  # R(-inf) = 0: L-stable
        assert all(abs(stability_function(t, complex(-x, y))) <= 1 + 1e-12
                   for x in (0.0, 0.5, 5.0) for y in (0.1, 1.0, 3.0, 30.0))


def test_observed_orders():
    f = lambda t, y: y * math.cos(t)
    exact = math.exp(math.sin(2.0))
    for s, p in ((1, 1), (2, 3), (3, 5)):
        errs = [abs(radau_iia(f, 0, 1.0, 2.0, h, s, jac=lambda t, y: math.cos(t)).y - exact)
                for h in (0.2, 0.1, 0.05)]
        orders = [math.log2(errs[i] / errs[i + 1]) for i in range(2)]
        assert all(abs(q - p) < 0.15 for q in orders), (s, orders)


def test_stiff_large_steps():
    g = lambda t, y: -50 * (y - math.cos(t))
    exact = (2500 * math.cos(1.2) + 50 * math.sin(1.2)) / 2501 - 2500 / 2501 * math.exp(-60)
    r = radau_iia(g, 0, 0.0, 1.2, 0.2, 3, jac=lambda t, y: -50.0)
    assert abs(r.y - exact) < 1e-6  # z = -10, far outside every explicit stability region
    lam = -1e6
    pr = lambda t, y: lam * (y - math.sin(t)) + math.cos(t)
    r = radau_iia(pr, 0, 0.0, 1.0, 0.1, 3, jac=lambda t, y: lam)
    assert abs(r.y - math.sin(1.0)) < 1e-9


def test_edge_cases_and_vector():
    f = lambda t, y: -y
    r = radau_iia(f, 1.0, 2.0, 1.0, 0.1)
    assert (r.steps, r.y, r.t) == (0, 2.0, 1.0)
    r = radau_iia(f, 0.0, 1.0, 0.3, 5.0, 1)  # h larger than the interval: one step of 0.3
    assert r.steps == 1 and abs(r.y - 1 / 1.3) < 1e-12
    r = radau_iia(f, 0.0, 1.0, 1.0, 0.3, 3, keep_path=True)  # off-grid final step
    assert r.steps == 4 and r.t == 1.0 and abs(r.path[-2][0] - 0.9) < 1e-15
    assert abs(r.y - math.exp(-1)) < 1e-5
    osc = lambda t, y: [y[1], -y[0]]
    rv = radau_iia(osc, 0.0, [1.0, 0.0], 1.0, 0.3, 3)
    assert abs(rv.y[0] - math.cos(1)) < 1e-5 and abs(rv.y[1] + math.sin(1)) < 1e-5
    with pytest.raises(ValueError):
        radau_iia(f, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        radau_nodes(0)


def test_dissipative_not_symplectic():
    osc = lambda t, y: [y[1], -y[0]]
    r = radau_iia(osc, 0.0, [1.0, 0.0], 50.0, 0.5, 2, keep_path=True)
    energy = [y[0] ** 2 + y[1] ** 2 for _, y in r.path]
    assert all(b < a for a, b in zip(energy, energy[1:]))
    assert abs(energy[-1] - abs(stability_function(radau_tableau(2), 0.5j)) ** (2 * 100)) < 1e-10


def test_costs():
    f = lambda t, y: [-y[0] + y[1] ** 2, -2 * y[1]]
    r = radau_iia(f, 0.0, [1.0, 1.0], 1.0, 0.25, 3,
                  jac=lambda t, y: [[-1.0, 2 * y[1]], [0.0, -2.0]])
    assert r.jac_evals == r.lu_factorizations == r.steps == 4
    assert r.f_evals == 3 * r.newton_iterations
    r2 = radau_iia(f, 0.0, [1.0, 1.0], 1.0, 0.25, 3)
    assert r2.f_evals == 3 * r2.newton_iterations + 3 * r2.steps
    exact = [math.exp(-1) + (math.exp(-1) - math.exp(-4)) / 3, math.exp(-2)]
    assert max(abs(a - b) for a, b in zip(r2.y, exact)) < 1e-5


def test_newton_failure_reported():
    vdp = lambda t, y: [y[1], 100.0 * ((1 - y[0] ** 2) * y[1] - y[0])]
    with pytest.raises(RuntimeError):
        radau_iia(vdp, 0.0, [2.0, 0.0], 1.0, 0.05, 3)
    r = radau_iia(vdp, 0.0, [2.0, 0.0], 1.0, 0.01, 3, tol=1e-10, max_iter=50)
    assert r.steps == 100 and -2.1 < r.y[0] < -1.8
