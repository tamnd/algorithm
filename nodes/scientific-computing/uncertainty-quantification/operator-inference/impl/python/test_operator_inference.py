# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operator-inference/. The authors are listed in prov/094ATM.jsonl.
import math
import random

import pytest

from operator_inference import (
    burgers_step,
    intrusive_rom,
    learn,
    lift,
    lstsq_qr,
    opinf,
    pod_basis,
    restrict,
    rom_step,
    rom_trajectory,
    sq,
    trajectory,
)

N, NU, DT, K = 32, 0.05, 0.002, 200
F = burgers_step(N, NU, DT)
XG = [(i + 1) / (N + 1) for i in range(N)]
X0S = [
    [math.sin(math.pi * x) for x in XG],
    [0.8 * math.sin(2 * math.pi * x) + 0.3 * math.sin(math.pi * x) for x in XG],
    [2 * x * (1 - x) * (1 + x) for x in XG],
]
TEST_X0 = [0.6 * math.sin(math.pi * x) + 0.4 * math.sin(3 * math.pi * x) for x in XG]


def norm(v):
    return math.sqrt(sum(t * t for t in v))


def max_diff(p, q):
    return max(abs(x - y) for ra, rb in zip(p, q) for x, y in zip(ra, rb))


def rel_traj_err(v, a_hat, h_hat, x0):
    full = trajectory(F, x0, K)
    red = rom_trajectory(a_hat, h_hat, restrict(v, x0), K)
    return max(norm([p - q for p, q in zip(lift(v, a), x)]) for a, x in zip(red, full)) / max(norm(x) for x in full)


def normal_equations(d, rhs):
    """Reference least squares: solve (D^T D) X = D^T rhs by Gaussian elimination."""
    p = len(d[0])
    g = [[sum(row[i] * row[j] for row in d) for j in range(p)] for i in range(p)]
    out = []
    for col in range(len(rhs[0])):
        b = [sum(row[i] * rr[col] for row, rr in zip(d, rhs)) for i in range(p)]
        m = [list(gr) + [bi] for gr, bi in zip(g, b)]
        for k in range(p):
            piv = max(range(k, p), key=lambda i: abs(m[i][k]))
            m[k], m[piv] = m[piv], m[k]
            for i in range(k + 1, p):
                fct = m[i][k] / m[k][k]
                for j in range(k, p + 1):
                    m[i][j] -= fct * m[k][j]
        x = [0.0] * p
        for i in range(p - 1, -1, -1):
            x[i] = (m[i][p] - sum(m[i][j] * x[j] for j in range(i + 1, p))) / m[i][i]
        out.append(x)
    return [[out[c][j] for c in range(len(rhs[0]))] for j in range(p)]


def test_quadratic_terms():
    assert sq([2.0, 3.0, 5.0]) == [4.0, 6.0, 10.0, 9.0, 15.0, 25.0]
    assert len(sq([1.0] * 6)) == 21


def test_least_squares_against_normal_equations():
    rng = random.Random(1)
    d = [[rng.gauss(0, 1) for _ in range(5)] for _ in range(30)]
    rhs = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(30)]
    got, ref = lstsq_qr(d, rhs), normal_equations(d, rhs)
    assert max_diff(got, ref) < 1e-10


def test_planted_quadratic_model_is_recovered():
    rng = random.Random(2)
    r = 3
    a_true = [[0.9 * (i == j) + 0.05 * rng.gauss(0, 1) for j in range(r)] for i in range(r)]
    h_true = [[0.05 * rng.gauss(0, 1) for _ in range(6)] for _ in range(r)]
    # 40 one-step trajectories from random states
    trajs = [rom_trajectory(a_true, h_true, [rng.uniform(-1, 1) for _ in range(r)], 1) for _ in range(40)]
    a_hat, h_hat = opinf(trajs, r)
    assert max_diff(a_hat, a_true) < 1e-10 and max_diff(h_hat, h_true) < 1e-10


def test_intrusive_reference_is_the_galerkin_step():
    rng = random.Random(3)
    v, _ = pod_basis([x for x0 in X0S for x in trajectory(F, x0, 40)], 4)
    a_i, h_i = intrusive_rom(F, v)
    for _ in range(5):
        a = [rng.gauss(0, 1) for _ in range(4)]
        assert rom_step(a_i, h_i, a) == pytest.approx(restrict(v, F(lift(v, a))), abs=1e-10)


def test_reprojection_recovers_the_intrusive_model():
    for r in (3, 4, 5):
        v, a_hat, h_hat = learn(F, X0S, K, r, reproject=True)
        a_i, h_i = intrusive_rom(F, v)
        assert max_diff(a_hat + h_hat, a_i + h_i) < 1e-9


def test_plain_projection_has_a_closure_error():
    v, a_hat, h_hat = learn(F, X0S, K, 4, reproject=False)
    a_i, h_i = intrusive_rom(F, v)
    assert max_diff(a_hat + h_hat, a_i + h_i) > 1e-3


def test_example_errors():
    snaps = [x for x0 in X0S for x in trajectory(F, x0, K)]
    _, sig = pod_basis(snaps, 4)
    assert sig[0] == pytest.approx(66.33, rel=1e-3) and sig[4] == pytest.approx(0.7232, rel=1e-3)
    v, a_hat, h_hat = learn(F, X0S, K, 4, reproject=True)
    assert rel_traj_err(v, a_hat, h_hat, X0S[0]) == pytest.approx(1.13e-2, rel=1e-2)
    assert rel_traj_err(v, a_hat, h_hat, TEST_X0) == pytest.approx(0.102, rel=1e-2)
