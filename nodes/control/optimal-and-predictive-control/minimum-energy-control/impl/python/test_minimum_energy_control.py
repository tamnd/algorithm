# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-energy-control/. The authors are listed in prov/H8NC6E.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
import ctlsim
from minimum_energy_control import gramian, minimum_energy_control, minimum_energy_discrete, reach_matrix


def maxabs(a):
    return max(abs(v) for row in a for v in row)


def rand_mat(rng, n, m, lo=-1.5, hi=1.5):
    return [[rng.uniform(lo, hi) for _ in range(m)] for _ in range(n)]


def simulate_optimal(A, B, x0, eta, t1, dt):
    """RK4 on x' = A x + B B^T z, z' = -A^T z, e' = |B^T z|^2, so u = B^T z."""
    n, m = len(A), len(B[0])
    at = cm.transpose(A)
    z0 = cm.matvec(cm.expm(cm.scale(t1, at)), eta)

    def f(t, s, u):
        x, z = s[:n], s[n:2 * n]
        v = [sum(B[i][j] * z[i] for i in range(n)) for j in range(m)]
        dx = [sum(A[i][k] * x[k] for k in range(n)) + sum(B[i][j] * v[j] for j in range(m)) for i in range(n)]
        dz = [-sum(at[i][k] * z[k] for k in range(n)) for i in range(n)]
        return dx + dz + [sum(vj * vj for vj in v)]

    steps = round(t1 / dt)
    assert abs(steps * dt - t1) <= 1e-12 * t1
    _, xs, _ = ctlsim.simulate(f, list(x0) + z0 + [0.0], 0.0, t1, dt)
    return xs[-1][:n], xs[-1][-1]


def lyapunov_gramian(A, B, t1):
    """Independent oracle: A W + W A^T + B B^T - e^(A t1) B B^T e^(A^T t1) = 0, by Kronecker form."""
    n = len(A)
    phi = cm.expm(cm.scale(t1, A))
    bbt = cm.mul(B, cm.transpose(B))
    rhs = cm.sub(cm.mul(phi, cm.mul(bbt, cm.transpose(phi))), bbt)
    op = cm.add(cm.kron(cm.eye(n), A), cm.kron(A, cm.eye(n)))
    return cm.unvec(cm.solve(op, cm.vec(rhs)), n, n)


def test_double_integrator():
    A, B = [[0, 1], [0, 0]], [[0], [1]]
    W = gramian(A, B, 1.0)
    want = [[1 / 3, 1 / 2], [1 / 2, 1.0]]
    assert maxabs(cm.sub(W, want)) <= 1e-14
    u, energy, eta = minimum_energy_control(A, B, [0, 0], [1, 0], 1.0)
    assert abs(energy - 12.0) <= 1e-12
    assert abs(eta[0] - 12.0) <= 1e-11 and abs(eta[1] + 6.0) <= 1e-11
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        assert abs(u(t)[0] - (6.0 - 12.0 * t)) <= 1e-11


def test_scalar_closed_form():
    for a in [-1.0, 0.5, 2.0]:
        for t1 in [0.3, 1.0, 2.0]:
            W = gramian([[a]], [[1.0]], t1)[0][0]
            want = (math.exp(2 * a * t1) - 1) / (2 * a)
            assert abs(W - want) <= 1e-13 * want
            _, energy, _ = minimum_energy_control([[a]], [[1.0]], [0.0], [1.0], t1)
            assert abs(energy - 1 / want) <= 1e-12 / want
    W = gramian([[-1.0]], [[1.0]], 1.0)[0][0]
    assert abs(W - (1 - math.exp(-2.0)) / 2) <= 1e-15


def test_gramian_against_lyapunov_oracle():
    rng = random.Random(11)
    count = 0
    while count < 500:
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A, B = rand_mat(rng, n, n), rand_mat(rng, n, m)
        sums = [r1 + r2 for r1 in cm.polyroots(cm.charpoly(A)) for r2 in cm.polyroots(cm.charpoly(A))]
        if min(abs(s) for s in sums) < 0.05:
            continue
        t1 = rng.uniform(0.2, 1.5)
        W = gramian(A, B, t1)
        ref = lyapunov_gramian(A, B, t1)
        assert maxabs(cm.sub(W, ref)) <= 1e-9 * (1 + maxabs(ref))
        assert cm.is_symmetric(W, 0)
        count += 1


def test_simulation_reaches_target_with_stated_energy():
    rng = random.Random(5)
    done = 0
    while done < 60:
        n, m = rng.randint(1, 3), rng.randint(1, 2)
        A, B = rand_mat(rng, n, n), rand_mat(rng, n, m)
        W = gramian(A, B, 1.0)
        if min(cm._sym_eigvals(W)) < 1e-3:
            continue
        x0 = [rng.uniform(-1, 1) for _ in range(n)]
        x1 = [rng.uniform(-1, 1) for _ in range(n)]
        u, energy, eta = minimum_energy_control(A, B, x0, x1, 1.0)
        # RK4 with dt = 0.01 over [0, 1]; the global error is O(dt^4).
        xT, eT = simulate_optimal(A, B, x0, eta, 1.0, 0.01)
        scale = 1 + max(abs(v) for v in eta)
        assert max(abs(p - q) for p, q in zip(xT, x1)) <= 1e-6 * scale
        assert abs(eT - energy) <= 1e-6 * (1 + energy)
        z = u(0.5)
        assert len(z) == m
        done += 1


def test_zoh_inputs_cost_more():
    """Least-norm piecewise constant inputs reach x1 too, with energy at least the optimum, tending to it."""
    A, B = [[0.0, 1.0], [-2.0, -0.3]], [[0.0], [1.0]]
    x0, x1, t1 = [1.0, 0.0], [0.0, 0.5], 2.0
    _, best, _ = minimum_energy_control(A, B, x0, x1, t1)
    prev = None
    for N in [5, 10, 20, 40]:
        h = t1 / N
        aug = cm.block([[A, B], [cm.zeros(1, 2), cm.zeros(1, 1)]])
        e = cm.expm(cm.scale(h, aug))
        Ad = [row[:2] for row in e[:2]]
        Bd = [row[2:] for row in e[:2]]
        us, en = minimum_energy_discrete(Ad, Bd, x0, x1, N)
        zoh = h * en
        assert zoh >= best * (1 - 1e-12)
        if prev is not None:
            assert zoh <= prev + 1e-12
        prev = zoh
    assert prev - best <= 0.01 * best


def kkt_oracle(C, d):
    """Least-norm solution of C u = d from the KKT system [[I, C^T], [C, 0]] [u; lam] = [0; d]."""
    n, k = len(C), len(C[0])
    K = cm.block([[cm.eye(k), cm.transpose(C)], [C, cm.zeros(n, n)]])
    sol = cm.solve(K, [0] * k + list(d))
    return sol[:k]


def test_discrete_exact_against_kkt():
    rng = random.Random(23)
    count = 0
    while count < 500:
        n, m, N = rng.randint(1, 3), rng.randint(1, 2), rng.randint(1, 4)
        A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        B = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
        C = reach_matrix(A, B, N)
        if cm.det(cm.mul(C, cm.transpose(C))) == 0:
            with pytest.raises(ValueError):
                minimum_energy_discrete(A, B, [0] * n, [1] * n, N)
            continue
        x0 = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        x1 = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        us, energy = minimum_energy_discrete(A, B, x0, x1, N)
        x = list(x0)
        for uk in us:
            x = [p + q for p, q in zip(cm.matvec(A, x), cm.matvec(B, uk))]
        assert x == x1
        flat = [v for uk in us for v in uk]
        d = [p - q for p, q in zip(x1, cm.matvec(cm.mat_power(A, N), x0))]
        assert flat == kkt_oracle(C, d)
        assert energy == sum(v * v for v in flat)
        count += 1


def test_discrete_scalar_example():
    us, energy = minimum_energy_discrete([[2]], [[1]], [0], [21], 3)
    assert us == [[Fraction(4)], [Fraction(2)], [Fraction(1)]]
    assert energy == 21


def test_uncontrollable_and_bad_input():
    with pytest.raises(ValueError):
        minimum_energy_control([[1.0, 0.0], [0.0, 1.0]], [[1.0], [1.0]], [0.0, 0.0], [1.0, 0.0], 1.0)
    with pytest.raises(ValueError):
        minimum_energy_control([[0.0]], [[1.0]], [0.0], [1.0], 0.0)
    with pytest.raises(ValueError):
        minimum_energy_control([[0.0]], [[0.0]], [0.0], [1.0], 1.0)
    with pytest.raises(ValueError):
        minimum_energy_discrete([[1]], [[1]], [0], [1], 0)
