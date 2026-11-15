# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-mpc/. The authors are listed in prov/R448P7.jsonl.

import itertools
import random

import pytest

import ctlmat as cm
from linear_mpc import Infeasible, LinearMPC, condense, kkt_residual, qp_solve

# Double integrator sampled with h = 1 s (zero-order hold), Q = I, R = 1.
A = [[1.0, 1.0], [0.0, 1.0]]
B = [[0.5], [1.0]]
Q = [[1.0, 0.0], [0.0, 1.0]]
R = [[1.0]]


def dare(A, B, Q, R, iters=400):
    P = [row[:] for row in Q]
    for _ in range(iters):
        S = cm.add(R, cm.mul(cm.transpose(B), cm.mul(P, B)))
        K = cm.solve(S, cm.mul(cm.transpose(B), cm.mul(P, A)))
        P = cm.sub(cm.add(Q, cm.mul(cm.transpose(A), cm.mul(P, A))),
                   cm.mul(cm.transpose(A), cm.mul(cm.mul(P, B), K)))
    return P, K


P, K = dare(A, B, Q, R)
AK = cm.sub(A, cm.mul(B, K))
KA = cm.mul(K, AK)
# Terminal set: the maximal admissible set of x+ = (A - B K) x with |x_1| <= 5,
# |x_2| <= 5 and |K x| <= 1 (see the maximal-positively-invariant-set page).
HF = [[1.0, 0.0], [-1.0, 0.0], K[0], [-v for v in K[0]], KA[0], [-v for v in KA[0]]]
HFB = [5.0, 5.0, 1.0, 1.0, 1.0, 1.0]
CONS = dict(umin=[-1.0], umax=[1.0], xmin=[-5.0, -5.0], xmax=[5.0, 5.0], Hf=HF, hf=HFB)


def step(x, u):
    return [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]


def stage(x, u):
    return x[0] ** 2 + x[1] ** 2 + u[0] ** 2


def brute_qp(H, f, G, b, tol=1e-9):
    """Enumerate active sets; return the KKT point (unique because H > 0)."""
    nz = len(H)
    best = None
    for size in range(0, nz + 1):
        for S in itertools.combinations(range(len(G)), size):
            kkt = [H[i] + [G[j][i] for j in S] for i in range(nz)]
            kkt += [G[j] + [0.0] * size for j in S]
            rhs = [-v for v in f] + [b[j] for j in S]
            try:
                sol = cm.solve(kkt, rhs)
            except ValueError:
                continue
            z, lam = sol[:nz], sol[nz:]
            if any(l < -tol for l in lam):
                continue
            if any(sum(g * zi for g, zi in zip(G[i], z)) > b[i] + tol for i in range(len(G))):
                continue
            best = z
            return best
    return best


def test_condensed_prediction_matches_simulation():
    rng = random.Random(1)
    N = 6
    phi, gamma, H, F = condense(A, B, Q, R, P, N)
    for _ in range(20):
        x0 = [rng.uniform(-3, 3) for _ in range(2)]
        U = [rng.uniform(-1, 1) for _ in range(N)]
        X = [a + b for a, b in zip(cm.matvec(phi, x0), cm.matvec(gamma, U))]
        x = x0
        for k in range(N):
            x = step(x, [U[k]])
            assert abs(X[2 * k] - x[0]) < 1e-12 and abs(X[2 * k + 1] - x[1]) < 1e-12


def test_condensed_cost_is_the_horizon_cost():
    rng = random.Random(2)
    N = 4
    mpc = LinearMPC(A, B, Q, R, P, N)
    for _ in range(20):
        x0 = [rng.uniform(-3, 3) for _ in range(2)]
        U = [rng.uniform(-1, 1) for _ in range(N)]
        quad = sum(U[i] * mpc.H[i][j] * U[j] for i in range(N) for j in range(N))
        lin = 2 * sum(u * v for u, v in zip(U, cm.matvec(mpc.F, x0)))
        const = mpc.cost(x0, [0.0] * N, Q, R, P, A, B)
        assert abs(quad + lin + const - mpc.cost(x0, U, Q, R, P, A, B)) < 1e-9


def test_qp_against_brute_force_on_random_problems():
    rng = random.Random(3)
    for _ in range(60):
        nz = rng.randint(1, 3)
        M = [[rng.uniform(-1, 1) for _ in range(nz)] for _ in range(nz)]
        H = cm.add(cm.mul(cm.transpose(M), M), [[0.2 if i == j else 0.0 for j in range(nz)] for i in range(nz)])
        f = [rng.uniform(-2, 2) for _ in range(nz)]
        nc = rng.randint(1, 6)
        G = [[rng.uniform(-1, 1) for _ in range(nz)] for _ in range(nc)]
        b = [rng.uniform(0.0, 1.0) for _ in range(nc)]  # z = 0 is feasible
        z, lam, _ = qp_solve(H, f, G, b)
        assert kkt_residual(H, f, G, b, z, lam) < 1e-9
        zb = brute_qp(H, f, G, b)
        assert zb is not None
        assert max(abs(u - v) for u, v in zip(z, zb)) < 1e-7


def test_qp_detects_infeasible_constraints():
    H = [[1.0, 0.0], [0.0, 1.0]]
    f = [0.0, 0.0]
    G = [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0]]
    b = [-1.0, -1.0, 5.0]  # z_1 <= -1 and z_1 >= 1
    with pytest.raises(Infeasible):
        qp_solve(H, f, G, b)


def test_mpc_equals_lqr_near_the_origin():
    rng = random.Random(4)
    mpc = LinearMPC(A, B, Q, R, P, 5, **CONS)
    for _ in range(20):
        x0 = [rng.uniform(-0.5, 0.5) for _ in range(2)]
        u = mpc.step(x0)[0]
        assert abs(u + K[0][0] * x0[0] + K[0][1] * x0[1]) < 1e-9


def test_example_numbers():
    mpc = LinearMPC(A, B, Q, R, P, 5, **CONS)
    assert len(mpc.H) == 5 and len(mpc.G) == 36
    U, lam = mpc.solve([-5.0, 3.0])
    want = [-0.9516, -1.0, -0.6753, -0.2896, -0.0910]
    assert max(abs(u - w) for u, w in zip(U, want)) < 5e-5
    assert [i for i, l in enumerate(lam) if l > 1e-9] == [3]  # u_1 >= -1 is active
    assert abs(mpc.cost([-5.0, 3.0], U, Q, R, P, A, B) - 48.9369) < 5e-5
    assert abs(P[0][1] - 5 ** 0.5 / 2) < 1e-12


def test_kkt_conditions_at_random_states():
    rng = random.Random(5)
    mpc = LinearMPC(A, B, Q, R, P, 6, **CONS)
    solved = 0
    for _ in range(40):
        x0 = [rng.uniform(-5, 5), rng.uniform(-3, 3)]
        f, b = mpc.qp_data(x0)
        try:
            z, lam, _ = qp_solve(mpc.H, f, mpc.G, b)
        except Infeasible:
            continue
        solved += 1
        assert kkt_residual(mpc.H, f, mpc.G, b, z, lam) < 1e-8
    assert solved >= 20


def test_infeasible_state():
    mpc = LinearMPC(A, B, Q, R, P, 5, **CONS)
    with pytest.raises(Infeasible):
        mpc.step([4.0, 2.0])  # even u = -1 gives x_1 = 5.5 > 5


def test_terminal_set_is_admissible_and_invariant():
    # vertices of the polygon by brute force over pairs of rows
    verts = []
    for i, j in itertools.combinations(range(len(HF)), 2):
        a1, a2 = HF[i], HF[j]
        d = a1[0] * a2[1] - a1[1] * a2[0]
        if abs(d) < 1e-12:
            continue
        v = [(HFB[i] * a2[1] - HFB[j] * a1[1]) / d, (a1[0] * HFB[j] - a2[0] * HFB[i]) / d]
        if all(r[0] * v[0] + r[1] * v[1] <= h + 1e-9 for r, h in zip(HF, HFB)):
            verts.append(v)
    assert len(verts) >= 6
    for v in verts:
        u = -(K[0][0] * v[0] + K[0][1] * v[1])
        assert abs(u) <= 1 + 1e-9 and abs(v[1]) <= 5 + 1e-9
        w = cm.matvec(AK, v)
        assert all(r[0] * w[0] + r[1] * w[1] <= h + 1e-9 for r, h in zip(HF, HFB))


def test_closed_loop_constraints_cost_decrease_and_convergence():
    mpc = LinearMPC(A, B, Q, R, P, 5, **CONS)
    x = [-5.0, 3.0]
    U, _ = mpc.solve(x)
    V = mpc.cost(x, U, Q, R, P, A, B)
    for _ in range(40):
        u = U[:1]
        assert -1 - 1e-9 <= u[0] <= 1 + 1e-9
        xn = step(x, u)
        assert all(abs(v) <= 5 + 1e-9 for v in xn)
        Un, _ = mpc.solve(xn)
        Vn = mpc.cost(xn, Un, Q, R, P, A, B)
        assert Vn <= V - stage(x, u) + 1e-8
        x, U, V = xn, Un, Vn
    assert max(abs(v) for v in x) < 1e-6
