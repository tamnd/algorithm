# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-horizon-lqr/. The authors are listed in prov/6S5J80.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
import ctlsim as cs
from finite_horizon_lqr import lqr_cost, rde_rhs, riccati_backward, riccati_ode


def quad(m, v):
    return sum(v[i] * m[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


def batch_value_matrix(A, B, Q, R, Qf, N):
    """Minimum of J over all input sequences, as x0^T W x0, by stacking the inputs.

    x_k = Phi_k x0 + Gamma_k U with U = (u_0, ..., u_(N-1)). J is a quadratic
    form in (x0, U), and the minimum over U is x0^T (M - G^T H^(-1) G) x0.
    This is the brute force reference: one linear solve of size N m, no recursion.
    """
    n, m = len(A), len(B[0])
    phi = cm.eye(n)
    gam = cm.zeros(n, N * m)
    H = cm.zeros(N * m)
    for k in range(N):
        for i in range(m):
            H[k * m + i][k * m:(k + 1) * m] = list(R[i])
    G = cm.zeros(N * m, n)
    M = cm.zeros(n)
    for k in range(N + 1):
        w = Qf if k == N else Q
        gtw = cm.mul(cm.transpose(gam), w)
        H = cm.add(H, cm.mul(gtw, gam))
        G = cm.add(G, cm.mul(gtw, phi))
        M = cm.add(M, cm.mul(cm.transpose(phi), cm.mul(w, phi)))
        if k < N:
            gam = cm.mul(A, gam)
            for i in range(n):
                for j in range(m):
                    gam[i][k * m + j] += B[i][j]
            phi = cm.mul(A, phi)
    return cm.sub(M, cm.mul(cm.transpose(G), cm.solve(H, G))), H


def closed_loop(A, B, Ks):
    def step(k, x, u):
        return [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]

    def control(k, x):
        return [-v for v in cm.matvec(Ks[k], x)]
    return step, control


def test_scalar_fibonacci():
    Ps, Ks = riccati_backward([[1]], [[1]], [[1]], [[1]], [[0]], 5)
    assert [p[0][0] for p in Ps] == [Fraction(55, 34), Fraction(21, 13), Fraction(8, 5),
                                     Fraction(3, 2), 1, 0]
    assert [k[0][0] for k in Ks] == [Fraction(21, 34), Fraction(8, 13), Fraction(3, 5),
                                     Fraction(1, 2), 0]


def test_scalar_limit_is_golden_ratio():
    Ps, Ks = riccati_backward([[1.0]], [[1.0]], [[1.0]], [[1.0]], [[0.0]], 40)
    phi = (1 + math.sqrt(5)) / 2
    assert abs(Ps[0][0][0] - phi) < 1e-12
    assert abs(Ks[0][0][0] - (phi - 1)) < 1e-12


def test_double_integrator_steps_exact():
    A = [[1, 1], [0, 1]]
    B = [[Fraction(1, 2)], [1]]
    Q = [[1, 0], [0, 0]]
    Ps, Ks = riccati_backward(A, B, Q, [[1]], Q, 3)
    assert Ps[2] == [[Fraction(9, 5), Fraction(4, 5)], [Fraction(4, 5), Fraction(4, 5)]]
    assert Ks[2] == [[Fraction(2, 5), Fraction(2, 5)]]
    assert Ps[0] == [[Fraction(1817, 949), Fraction(900, 949)], [Fraction(900, 949), Fraction(1388, 949)]]


def random_problem(rng, n, m):
    A = [[Fraction(rng.randint(-4, 4), 2) for _ in range(n)] for _ in range(n)]
    B = [[Fraction(rng.randint(-3, 3), 2) for _ in range(m)] for _ in range(n)]
    C = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(n)]
    Q = cm.mul(cm.transpose(C), C)
    D = [[Fraction(rng.randint(-2, 2)) for _ in range(m)] for _ in range(m)]
    R = cm.add(cm.mul(cm.transpose(D), D), cm.eye(m))
    E = [[Fraction(rng.randint(-1, 1)) for _ in range(n)] for _ in range(n)]
    Qf = cm.mul(cm.transpose(E), E)
    return A, B, Q, R, Qf


@pytest.mark.parametrize("seed", [1, 2, 3, 4, 5])
def test_matches_batch_minimum_exactly(seed):
    rng = random.Random(seed)
    n, m = rng.choice([(2, 1), (3, 1), (3, 2)])
    N = rng.randint(1, 4)
    A, B, Q, R, Qf = random_problem(rng, n, m)
    Ps, Ks = riccati_backward(A, B, Q, R, Qf, N)
    W, _ = batch_value_matrix(A, B, Q, R, Qf, N)
    assert Ps[0] == W
    for p in Ps:
        assert cm.is_symmetric(p)


@pytest.mark.parametrize("seed", [11, 12, 13])
def test_feedback_cost_and_perturbations(seed):
    rng = random.Random(seed)
    n, m, N = 3, 2, 4
    A, B, Q, R, Qf = random_problem(rng, n, m)
    Ps, Ks = riccati_backward(A, B, Q, R, Qf, N)
    step, control = closed_loop(A, B, Ks)
    x0 = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
    xs, us = cs.simulate_discrete(step, x0, N, control)
    best = lqr_cost(A, B, Q, R, Qf, xs, us)
    assert best == quad(Ps[0], x0)
    for _ in range(10):
        vs = [[u[i] + Fraction(rng.randint(-2, 2), 3) for i in range(m)] for u in us]
        if vs == us:
            continue
        ys, _ = cs.simulate_discrete(step, x0, N, lambda k, x: vs[k])
        assert lqr_cost(A, B, Q, R, Qf, ys, vs) > best


def test_long_horizon_solves_the_dare():
    A = [[1.0, 1.0], [0.0, 1.0]]
    B = [[0.5], [1.0]]
    Q = [[1.0, 0.0], [0.0, 1.0]]
    R = [[1.0]]
    Ps, Ks = riccati_backward(A, B, Q, R, [[0.0, 0.0], [0.0, 0.0]], 80)
    P = Ps[0]
    pb = cm.mul(P, B)
    s = cm.add(R, cm.mul(cm.transpose(B), pb))
    rhs = cm.sub(cm.add(Q, cm.mul(cm.transpose(A), cm.mul(P, A))),
                 cm.mul(cm.mul(cm.transpose(A), pb), cm.solve(s, cm.mul(cm.transpose(pb), A))))
    assert cm.norm2(cm.sub(rhs, P)) < 1e-12 * cm.norm2(P)
    acl = cm.sub(A, cm.mul(B, Ks[0]))
    assert max(abs(z) for z in cm.polyroots(cm.charpoly(acl))) < 1


def test_zero_horizon():
    Ps, Ks = riccati_backward([[2]], [[1]], [[1]], [[1]], [[3]], 0)
    assert Ps == [[[3]]] and Ks == []
    with pytest.raises(ValueError):
        riccati_backward([[2]], [[1]], [[1]], [[1]], [[3]], -1)


def test_scalar_riccati_ode_closed_form():
    T = 1.0
    ts, Ps = riccati_ode([[1.0]], [[1.0]], [[1.0]], [[1.0]], [[0.0]], T, 200)
    s = math.sqrt(2.0)
    pp, pm = 1 + s, 1 - s
    for t, P in zip(ts[::20], Ps[::20]):
        w = (pp / pm) * math.exp(-2 * s * (T - t))
        assert abs(P[0][0] - (pp - w * pm) / (1 - w)) < 1e-9


def test_riccati_ode_long_horizon_tends_to_care():
    A = [[0.0, 1.0], [0.0, 0.0]]
    B = [[0.0], [1.0]]
    Q = [[1.0, 0.0], [0.0, 1.0]]
    _, Ps = riccati_ode(A, B, Q, [[1.0]], [[0.0, 0.0], [0.0, 0.0]], 30.0, 3000)
    r3 = math.sqrt(3.0)
    want = [[r3, 1.0], [1.0, r3]]
    assert max(abs(Ps[0][i][j] - want[i][j]) for i in range(2) for j in range(2)) < 1e-9
    assert cm.norm2(rde_rhs(A, B, Q, [[1.0]], Ps[0])) < 1e-9


def test_continuous_simulated_cost_equals_value():
    A = [[0.0, 1.0], [-1.0, 0.5]]
    B = [[0.0], [1.0]]
    Q = [[2.0, 0.0], [0.0, 1.0]]
    R = [[0.5]]
    Qf = [[1.0, 0.0], [0.0, 3.0]]
    T, S = 2.0, 400
    _, Ps = riccati_ode(A, B, Q, R, Qf, T, 2 * S)
    half = T / (2 * S)

    def f(t, xa, u):
        x = xa[:2]
        P = Ps[round(t / half)]
        k = cm.solve(R, cm.mul(cm.transpose(B), P))
        uu = [-v for v in cm.matvec(k, x)]
        dx = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, uu))]
        return dx + [quad(Q, x) + quad(R, uu)]

    x0 = [1.0, -0.5]
    _, xs, _ = cs.simulate(f, x0 + [0.0], 0.0, T, T / S)
    cost = xs[-1][2] + quad(Qf, xs[-1][:2])
    assert abs(cost - quad(Ps[0], x0)) < 1e-8 * quad(Ps[0], x0)
