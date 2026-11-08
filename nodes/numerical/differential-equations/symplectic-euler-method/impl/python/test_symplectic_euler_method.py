# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symplectic-euler-method/. The authors are listed in prov/B9ZN3M.jsonl.

import math
from fractions import Fraction as F

import pytest

from symplectic_euler_method import (oscillator_matrix, se_step, se_step_general, step_count,
                                     symplectic_euler)

ident = lambda x: x


def pend_H(q, p):
    return p * p / 2 - math.cos(q)


def test_exact_trace_and_matrix():
    r = symplectic_euler(ident, ident, 0, F(1), F(0), F(1), F(1, 2), keep_path=True)
    assert [(q, p) for _, q, p in r.path] == [(1, 0), (F(3, 4), F(-1, 2)), (F(5, 16), F(-7, 8))]
    h = F(1, 3)
    M = oscillator_matrix(h)
    assert M[0][0] * M[1][1] - M[0][1] * M[1][0] == 1
    q, p = F(2), F(1)
    assert se_step(ident, ident, q, p, h) == (M[0][0] * q + M[0][1] * p, M[1][0] * q + M[1][1] * p)


def test_modified_energy_exact():
    h = F(1, 3)
    q, p = F(1), F(0)
    for _ in range(30):
        assert q * q + p * p - h * q * p == 1
        q, p = se_step(ident, ident, q, p, h)


def test_first_order():
    errs = []
    for h in (0.1, 0.05, 0.025, 0.0125):
        r = symplectic_euler(ident, ident, 0.0, 1.0, 0.0, 10.0, h)
        errs.append(max(abs(r.q - math.cos(10)), abs(r.p + math.sin(10))))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(0.95 < x < 1.1 for x in orders)


def test_pendulum_energy_bounded_explicit_euler_drifts():
    q0, p0, h = 0.0, 1.5, 0.1
    r = symplectic_euler(ident, math.sin, 0.0, q0, p0, 100.0, h, keep_path=True)
    err = max(abs(pend_H(q, p) - pend_H(q0, p0)) for _, q, p in r.path)
    assert err < 0.06
    q, p = q0, p0
    for _ in range(1000):
        q, p = q + h * p, p - h * math.sin(q)
    assert pend_H(q, p) - pend_H(q0, p0) > 4.0


def test_stability_limit():
    ok = symplectic_euler(ident, ident, 0.0, 1.0, 0.0, 1990.0, 1.99)
    assert max(abs(ok.q), abs(ok.p)) < 30
    bad = symplectic_euler(ident, ident, 0.0, 1.0, 0.0, 2010.0, 2.01)
    assert abs(bad.q) > 1e80


def test_composition_of_adjoints_is_verlet():
    dV = lambda q: [q[0] / (q[0] ** 2 + q[1] ** 2) ** 1.5, q[1] / (q[0] ** 2 + q[1] ** 2) ** 1.5]
    q, p, h = [0.5, 0.0], [0.0, 1.7], 0.1
    qa, pa = se_step(ident, dV, q, p, h / 2, "A")
    qb, pb = se_step(ident, dV, qa, pa, h / 2, "B")
    # velocity Verlet: half kick, drift, half kick
    v = [pi - h / 2 * g for pi, g in zip(p, dV(q))]
    x = [qi + h * vi for qi, vi in zip(q, v)]
    v = [vi - h / 2 * g for vi, g in zip(v, dV(x))]
    assert max(abs(a - b) for a, b in zip(qb + pb, x + v)) < 1e-15


def test_symplectic_jacobian_and_adjoint_inverse():
    def phi(x, variant="A", h=0.2):
        q, p = x
        for _ in range(5):
            q, p = se_step(ident, math.sin, q, p, h, variant)
        return [q, p]
    x0, eps = [0.3, 1.1], 1e-6
    cols = []
    for k in range(2):
        xp, xm = list(x0), list(x0)
        xp[k] += eps
        xm[k] -= eps
        cols.append([(a - b) / (2 * eps) for a, b in zip(phi(xp), phi(xm))])
    det = cols[0][0] * cols[1][1] - cols[1][0] * cols[0][1]
    assert abs(det - 1) < 1e-8
    # B with -h undoes A with h
    q, p = se_step(ident, math.sin, 0.3, 1.1, 0.2, "A")
    q, p = se_step(ident, math.sin, q, p, -0.2, "B")
    assert abs(q - 0.3) < 1e-15 and abs(p - 1.1) < 1e-15


def test_general_nonseparable():
    # H = p^2 (1 + q^2)/2 + q^2/2: H_p = p (1 + q^2), H_q = p^2 q + q
    Hp = lambda p, q: p * (1 + q * q)
    Hq = lambda p, q: p * p * q + q
    H = lambda q, p: p * p * (1 + q * q) / 2 + q * q / 2
    q, p, h = 0.5, 0.5, 0.01
    H0 = H(q, p)
    worst = 0.0
    for _ in range(2000):
        q, p, it = se_step_general(Hp, Hq, q, p, h)
        worst = max(worst, abs(H(q, p) - H0))
    assert worst < 0.01 and it < 20
    # for separable H the general step agrees with the explicit one
    q1, p1, _ = se_step_general(lambda p, q: p, lambda p, q: math.sin(q), 0.3, 1.1, 0.2)
    assert (q1, p1) == pytest.approx(se_step(ident, math.sin, 0.3, 1.1, 0.2))


def test_edge_cases_and_vectors():
    r = symplectic_euler(ident, ident, 0.0, 1.0, 0.0, 0.0, 0.1)
    assert r.steps == 0 and r.q == 1.0
    r = symplectic_euler(ident, ident, 0.0, 1.0, 0.0, 0.3, 5.0)
    assert r.steps == 1 and r.t == 0.3 and r.p == -0.3 and abs(r.q - 0.91) < 1e-15
    r = symplectic_euler(ident, ident, 0.0, [1.0, 0.0], [0.0, 1.0], 1.05, 0.1)
    assert r.steps == 11 and r.t == 1.05 and abs(r.q[0] - math.cos(1.05)) < 0.05
    assert step_count(0.0, 1.0, 0.1) == 10
    with pytest.raises(ValueError):
        symplectic_euler(ident, ident, 0.0, 1.0, 0.0, 1.0, -0.1)
    with pytest.raises(ValueError):
        se_step(ident, ident, 1.0, 0.0, 0.1, "C")
