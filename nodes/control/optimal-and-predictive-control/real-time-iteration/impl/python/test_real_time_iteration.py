# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-iteration/. The authors are listed in prov/RM47HC.jsonl.

import itertools
import random

from real_time_iteration import (PENDULUM, box_qp, feedback, prepare, rk4, rti_loop, shift, simulate_cost,
                                 solve_nmpc)

# The example of the page.
H_STEP = 0.1
N = 20
Q = [[10.0, 0.0], [0.0, 1.0]]
R = [[0.1]]
P = [[50.0, 10.0], [10.0, 10.0]]


def zero_guess():
    return [[0.0, 0.0] for _ in range(N + 1)], [[0.0] for _ in range(N)]


def test_rk4_derivatives_match_finite_differences():
    rng = random.Random(1)
    eps = 1e-6
    for _ in range(10):
        x = [rng.uniform(-3, 3), rng.uniform(-3, 3)]
        u = [rng.uniform(-2, 2)]
        _, A, B = rk4(PENDULUM, x, u, 0.2)
        for j in range(2):
            xp, xm = list(x), list(x)
            xp[j] += eps
            xm[j] -= eps
            col = [(a - b) / (2 * eps) for a, b in zip(rk4(PENDULUM, xp, u, 0.2)[0], rk4(PENDULUM, xm, u, 0.2)[0])]
            assert all(abs(col[i] - A[i][j]) < 1e-7 for i in range(2))
        col = [(a - b) / (2 * eps) for a, b in zip(rk4(PENDULUM, x, [u[0] + eps], 0.2)[0],
                                                    rk4(PENDULUM, x, [u[0] - eps], 0.2)[0])]
        assert all(abs(col[i] - B[i][0]) < 1e-7 for i in range(2))


def test_rk4_is_the_fourth_order_taylor_step_on_a_linear_model():
    lam = -1.7
    model = (lambda x, u: [lam * x[0] + u[0]], lambda x, u: [[lam]], lambda x, u: [[1.0]])
    for h in (0.1, 0.5):
        z = lam * h
        xn, A, B = rk4(model, [1.0], [0.0], h)
        assert abs(xn[0] - (1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24)) < 1e-14
        assert abs(A[0][0] - xn[0]) < 1e-14


def test_box_qp_against_kkt_enumeration():
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(1, 4)
        L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        H = [[sum(L[i][k] * L[j][k] for k in range(n)) + (0.1 if i == j else 0.0) for j in range(n)] for i in range(n)]
        g = [rng.uniform(-2, 2) for _ in range(n)]
        lo = [rng.uniform(-1.5, 0.2) for _ in range(n)]
        hi = [v + rng.uniform(0.1, 2) for v in lo]
        x = box_qp(H, g, lo, hi)
        found = 0
        for pattern in itertools.product((-1, 0, 1), repeat=n):
            fixed = {i: (lo[i] if p < 0 else hi[i]) for i, p in enumerate(pattern) if p}
            free = [i for i in range(n) if i not in fixed]
            y = [fixed.get(i, 0.0) for i in range(n)]
            if free:
                # Solve H_FF y_F = -(g_F + H_FB y_B) by Cramer-free elimination.
                M = [[H[i][j] for j in free] + [-(g[i] + sum(H[i][j] * y[j] for j in fixed))] for i in free]
                k = len(free)
                for c in range(k):
                    p = max(range(c, k), key=lambda r: abs(M[r][c]))
                    M[c], M[p] = M[p], M[c]
                    for r in range(k):
                        if r != c:
                            f = M[r][c] / M[c][c]
                            M[r] = [a - f * b for a, b in zip(M[r], M[c])]
                for c, i in enumerate(free):
                    y[i] = M[c][k] / M[c][c]
            grad = [sum(H[i][j] * y[j] for j in range(n)) + g[i] for i in range(n)]
            ok = all(lo[i] - 1e-12 <= y[i] <= hi[i] + 1e-12 for i in free)
            ok = ok and all((grad[i] >= -1e-12) if fixed[i] == lo[i] else (grad[i] <= 1e-12) for i in fixed)
            if ok:
                found += 1
                assert max(abs(a - b) for a, b in zip(x, y)) < 1e-9
        assert found >= 1


def test_condensed_qp_is_the_linearized_cost():
    rng = random.Random(3)
    n_int = 4
    s = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(n_int + 1)]
    q = [[rng.uniform(-1, 1)] for _ in range(n_int)]
    prep = prepare(PENDULUM, s, q, H_STEP, Q, R, P)

    def lin_cost(ds0, dq):
        ds, J = ds0, 0.0
        for k in range(n_int + 1):
            x = [a + b for a, b in zip(s[k], ds)]
            W = P if k == n_int else Q
            J += sum(x[i] * W[i][j] * x[j] for i in range(2) for j in range(2))
            if k < n_int:
                u = q[k][0] + dq[k]
                J += R[0][0] * u * u
                ds = [sum(prep["A"][k][i][j] * ds[j] for j in range(2)) + prep["B"][k][i][0] * dq[k] + prep["c"][k][i]
                      for i in range(2)]
        return J

    for _ in range(5):
        ds0 = [rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]
        dq = [rng.uniform(-1, 1) for _ in range(n_int)]
        gx = [gi + sum(Gi[j] * ds0[j] for j in range(2)) for gi, Gi in zip(prep["g"], prep["G"])]
        model = 0.5 * sum(dq[i] * prep["H"][i][j] * dq[j] for i in range(n_int) for j in range(n_int))
        model += sum(a * b for a, b in zip(gx, dq))
        assert abs(lin_cost(ds0, dq) - lin_cost(ds0, [0.0] * n_int) - model) < 1e-9


def test_sqp_converges_to_a_local_minimum():
    s0, q0 = zero_guess()
    x0 = [1.0, 0.0]
    s, q, it = solve_nmpc(PENDULUM, x0, s0, q0, H_STEP, Q, R, P, [10.0])
    assert it <= 10
    # No gaps: the nodes are the simulated trajectory.
    for k in range(N):
        assert max(abs(a - b) for a, b in zip(rk4(PENDULUM, s[k], q[k], H_STEP)[0], s[k + 1])) < 1e-9
    J = simulate_cost(PENDULUM, x0, q, H_STEP, Q, R, P)
    rng = random.Random(4)
    for _ in range(20):
        d = [[rng.uniform(-1e-3, 1e-3)] for _ in range(N)]
        assert simulate_cost(PENDULUM, x0, [[a[0] + b[0]] for a, b in zip(q, d)], H_STEP, Q, R, P) >= J - 1e-12
    assert abs(q[0][0] + 8.4348) < 1e-4


def test_rti_follows_the_converged_solution():
    s0, q0 = zero_guess()
    x0 = [1.0, 0.0]
    xs, us = rti_loop(PENDULUM, x0, s0, q0, 20, H_STEP, Q, R, P, [10.0])
    s, q, diffs = s0, q0, []
    for k in range(6):
        # The fully converged NMPC input at the same state as the RTI loop.
        s, q, _ = solve_nmpc(PENDULUM, xs[k], s, q, H_STEP, Q, R, P, [10.0])
        diffs.append(abs(q[0][0] - us[k][0]))
        s, q = shift(s, q)
    assert 0.1 < diffs[0] < 0.2
    assert diffs[1] < 1e-4 and max(diffs[2:]) < 1e-5
    assert max(abs(v) for v in xs[-1]) < 1e-2


def test_saturated_loop_keeps_bounds_and_stabilizes():
    s0, q0 = zero_guess()
    xs, us = rti_loop(PENDULUM, [2.5, 0.0], s0, q0, 35, H_STEP, Q, R, P, [2.0])
    assert all(abs(u[0]) <= 2.0 + 1e-12 for u in us)
    assert max(abs(v) for v in xs[-1]) < 1e-2
    # The plant alone falls: without input the angle grows from 0.1 to almost 1 in 3 seconds.
    x = [0.1, 0.0]
    for _ in range(30):
        x = rk4(PENDULUM, x, [0.0], H_STEP)[0]
    assert x[0] > 0.9


def test_preparation_does_not_use_the_state():
    # The feedback for two different measured states uses the same prepared data.
    s0, q0 = zero_guess()
    prep = prepare(PENDULUM, s0, q0, H_STEP, Q, R, P)
    u1, _, _ = feedback(prep, s0, q0, [0.2, 0.0], [10.0])
    u2, _, _ = feedback(prep, s0, q0, [0.4, 0.0], [10.0])
    # Linearized at 0 and unconstrained, the first input is linear in x0.
    u4, _, _ = feedback(prep, s0, q0, [0.0, 0.0], [10.0])
    assert abs(u4[0]) < 1e-12 and abs(u2[0] - 2 * u1[0]) < 1e-9
