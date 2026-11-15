# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/infinite-horizon-lqr/. The authors are listed in prov/G9RNJT.jsonl.

import math
import random

import pytest

import ctlmat as cm
import ctlsim as cs
from infinite_horizon_lqr import care_residual, closed_loop_eigs, dare_residual, dlqr, lqr

R3 = math.sqrt(3.0)


def quad(m, v):
    return sum(v[i] * m[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


def close(a, b, tol):
    return all(abs(x - y) <= tol for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def data_norm(A, B, Q, R, P):
    g = cm.mul(B, cm.solve(R, cm.transpose(B)))
    return cm.norm2(Q) + 2 * cm.norm2(A) * cm.norm2(P) + cm.norm2(g) * cm.norm2(P) ** 2


def check_solution(A, B, Q, R, P, K, discrete):
    res = dare_residual(A, B, Q, R, P) if discrete else care_residual(A, B, Q, R, P)
    assert cm.norm2(res) <= 1e-9 * data_norm(A, B, Q, R, P)
    assert cm.is_symmetric(P, 1e-12 * cm.norm2(P))
    lam = [v.real for v in cm.polyroots(cm.charpoly(P))]
    assert min(lam) >= -1e-9 * cm.norm2(P)
    eig = closed_loop_eigs(A, B, K)
    if discrete:
        assert max(abs(z) for z in eig) < 1
    else:
        assert max(z.real for z in eig) < 0


def test_double_integrator_continuous():
    A, B, Q, R = [[0, 1], [0, 0]], [[0], [1]], [[1, 0], [0, 1]], [[1]]
    P, K, _ = lqr(A, B, Q, R)
    assert close(P, [[R3, 1.0], [1.0, R3]], 1e-9)
    assert close(K, [[1.0, R3]], 1e-9)
    check_solution(A, B, Q, R, P, K, False)


def test_scalar_care_and_dare():
    P, K, _ = lqr([[1]], [[1]], [[1]], [[1]])
    assert abs(P[0][0] - (1 + math.sqrt(2))) < 1e-9 and abs(K[0][0] - (1 + math.sqrt(2))) < 1e-9
    P, K, _ = dlqr([[1]], [[1]], [[1]], [[1]])
    phi = (1 + math.sqrt(5)) / 2
    assert abs(P[0][0] - phi) < 1e-12 and abs(K[0][0] - (phi - 1)) < 1e-12


def test_sampled_double_integrator():
    A, B, Q, R = [[1, 1], [0, 1]], [[0.5], [1]], [[1, 0], [0, 1]], [[1]]
    P, K, _ = dlqr(A, B, Q, R)
    check_solution(A, B, Q, R, P, K, True)
    assert abs(P[0][1] - math.sqrt(5) / 2) < 1e-12


def random_problem(rng, n, m):
    A = [[rng.uniform(-1.5, 1.5) for _ in range(n)] for _ in range(n)]
    B = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
    C = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    Q = cm.add(cm.mul(cm.transpose(C), C), cm.scale(0.1, cm.eye(n)))
    D = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(m)]
    R = cm.add(cm.mul(cm.transpose(D), D), cm.scale(0.5, cm.eye(m)))
    return A, B, Q, R


@pytest.mark.parametrize("seed", [1, 2, 3, 4])
def test_random_continuous(seed):
    rng = random.Random(seed)
    A, B, Q, R = random_problem(rng, 3, rng.choice([1, 2]))
    P, K, _ = lqr(A, B, Q, R)
    check_solution(A, B, Q, R, P, K, False)


@pytest.mark.parametrize("seed", [5, 6, 7, 8])
def test_random_discrete(seed):
    rng = random.Random(seed)
    A, B, Q, R = random_problem(rng, 3, rng.choice([1, 2]))
    P, K, _ = dlqr(A, B, Q, R)
    check_solution(A, B, Q, R, P, K, True)


def test_discrete_cost_by_simulation_and_other_gains():
    A, B, Q, R = [[1, 1], [0, 1]], [[0.5], [1]], [[1, 0], [0, 1]], [[1]]
    P, K, _ = dlqr(A, B, Q, R)

    def cost(gain, x0):
        def step(k, x, u):
            return [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
        xs, us = cs.simulate_discrete(step, x0, 400, lambda k, x: [-v for v in cm.matvec(gain, x)])
        return sum(quad(Q, x) + quad(R, u) for x, u in zip(xs, us))

    rng = random.Random(3)
    for _ in range(3):
        x0 = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        best = cost(K, x0)
        assert abs(best - quad(P, x0)) < 1e-10 * quad(P, x0)
        for _ in range(5):
            other = [[K[0][0] + rng.uniform(-0.1, 0.1), K[0][1] + rng.uniform(-0.1, 0.1)]]
            if max(abs(z) for z in closed_loop_eigs(A, B, other)) < 0.95:
                assert cost(other, x0) >= best


def test_scalar_gain_grid_search():
    # Cost of the constant gain k for a = 2, b = 1, q = r = 1, from x0 = 1:
    # sum of (1 + k^2)(2 - k)^(2j) = (1 + k^2) / (1 - (2 - k)^2) for |2 - k| < 1.
    P, K, _ = dlqr([[2]], [[1]], [[1]], [[1]])
    grid = [1.0 + 2.0 * i / 20000 for i in range(1, 20000)]
    best = min(grid, key=lambda k: (1 + k * k) / (1 - (2 - k) ** 2))
    assert abs(best - K[0][0]) < 2e-4
    assert abs((1 + K[0][0] ** 2) / (1 - (2 - K[0][0]) ** 2) - P[0][0]) < 1e-12


def test_continuous_cost_by_simulation():
    A, B, Q, R = [[0, 1], [0, 0]], [[0], [1]], [[1, 0], [0, 1]], [[1]]
    P, K, _ = lqr(A, B, Q, R)

    def f(t, xa, u):
        x = xa[:2]
        uu = [-v for v in cm.matvec(K, x)]
        dx = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, uu))]
        return dx + [quad(Q, x) + quad(R, uu)]

    x0 = [1.0, 0.5]
    _, xs, _ = cs.simulate(f, x0 + [0.0], 0.0, 40.0, 0.01)
    assert abs(xs[-1][2] - quad(P, x0)) < 1e-8


def test_not_detectable_start_from_zero_fails():
    # Q = 0: P = 0 is a fixed point, and A - B K = A is not stable.
    with pytest.raises(ValueError):
        dlqr([[2]], [[1]], [[0]], [[1]])
    with pytest.raises(ValueError):
        lqr([[1]], [[1]], [[0]], [[1]])
    # The stabilizing solutions exist: p = 3 (discrete) and p = 2 (continuous).
    P, K, _ = dlqr([[2]], [[1]], [[0]], [[1]], P0=[[1]])
    assert abs(P[0][0] - 3) < 1e-12 and abs(K[0][0] - 1.5) < 1e-12
    P, K, _ = lqr([[1]], [[1]], [[0]], [[1]], P0=[[1]])
    assert abs(P[0][0] - 2) < 1e-9


def test_not_stabilizable_fails():
    with pytest.raises(ValueError):
        dlqr([[1]], [[0]], [[1]], [[1]], max_iter=500)
