# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/explicit-mpc/. The authors are listed in prov/6TK6XY.jsonl.

import itertools
import random

from explicit_mpc import chebyshev_radius, evaluate, explicit_mpc, mpc_to_mpqp

# Double integrator with h = 1, Q = I, R = 1, P from the DARE (P_12 = sqrt(5)/2).
A = [[1.0, 1.0], [0.0, 1.0]]
B = [[0.5], [1.0]]
Q = [[1.0, 0.0], [0.0, 1.0]]
R = [[1.0]]


def dare(iters=400):
    p = [[1.0, 0.0], [0.0, 1.0]]
    for _ in range(iters):
        pb = [p[0][0] * 0.5 + p[0][1], p[1][0] * 0.5 + p[1][1]]  # P B
        s = 1.0 + 0.5 * pb[0] + pb[1]  # R + B^T P B
        bpa = [pb[0], pb[0] + pb[1]]  # B^T P A
        apa = [[p[0][0], p[0][0] + p[0][1]], [p[0][0] + p[1][0], p[0][0] + p[0][1] + p[1][0] + p[1][1]]]
        p = [[Q[i][j] + apa[i][j] - bpa[i] * bpa[j] / s for j in range(2)] for i in range(2)]
    return p, [bpa[0] / s, bpa[1] / s]


P, K = dare()
XBOX = [10.0, 10.0]
H, F, G, W, E = mpc_to_mpqp(A, B, Q, R, P, 3, [-1.0], [1.0])
REGIONS = explicit_mpc(H, F, G, W, E, XBOX)


def lin_solve(a, b):
    n = len(a)
    m = [list(r) + [v] for r, v in zip(a, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-12:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def brute_qp(x):
    """Solve the QP at x by trying every active set (H > 0, so the KKT point is unique)."""
    nz = len(H)
    f = [sum(F[i][j] * x[j] for j in range(len(x))) for i in range(nz)]
    b = [W[i] + sum(E[i][j] * x[j] for j in range(len(x))) for i in range(len(G))]
    for size in range(nz + 1):
        for S in itertools.combinations(range(len(G)), size):
            kkt = [H[i] + [G[j][i] for j in S] for i in range(nz)] + [G[j] + [0.0] * size for j in S]
            sol = lin_solve(kkt, [-v for v in f] + [b[j] for j in S])
            if sol is None:
                continue
            z, lam = sol[:nz], sol[nz:]
            if all(v >= -1e-9 for v in lam) and all(
                    sum(g * zi for g, zi in zip(G[i], z)) <= b[i] + 1e-9 for i in range(len(G))):
                return z
    raise AssertionError("no KKT point")


def horizon_cost(x, U):
    J, xk = 0.0, list(x)
    for u in U:
        J += xk[0] ** 2 + xk[1] ** 2 + u ** 2
        xk = [xk[0] + xk[1] + 0.5 * u, xk[1] + u]
    return J + sum(xk[i] * P[i][j] * xk[j] for i in range(2) for j in range(2))


def test_region_count_and_unconstrained_region():
    assert len(REGIONS) == 19  # of the 27 candidate sets with independent rows
    free = [r for r in REGIONS if r.active == ()]
    assert len(free) == 1 and free[0].contains([0.0, 0.0])
    assert abs(free[0].K[0][0] + K[0]) < 1e-9 and abs(free[0].K[0][1] + K[1]) < 1e-9


def test_law_matches_brute_force_qp():
    rng = random.Random(21)
    for _ in range(300):
        x = [rng.uniform(-10, 10), rng.uniform(-10, 10)]
        z, idx = evaluate(REGIONS, x)
        assert idx is not None
        zb = brute_qp(x)
        assert max(abs(a - b) for a, b in zip(z, zb)) < 1e-7


def test_example_points():
    z, idx = evaluate(REGIONS, [-5.0, 3.0])
    assert REGIONS[idx].active == (3,)  # u_1 >= -1 is active
    assert max(abs(a - b) for a, b in zip(z, [-0.9516, -1.0, -0.6753])) < 5e-5
    z, idx = evaluate(REGIONS, [3.0, 2.0])
    assert z == [-1.0, -1.0, -1.0] or max(abs(v + 1.0) for v in z) < 1e-12


def test_multipliers_and_kkt_inside_regions():
    rng = random.Random(22)
    for reg in REGIONS:
        for _ in range(20):
            x = [rng.uniform(-10, 10), rng.uniform(-10, 10)]
            if not reg.contains(x, 0.0):
                continue
            z, lam = reg.law(x), reg.multipliers(x)
            assert all(v >= -1e-9 for v in lam)
            grad = [sum(H[i][j] * z[j] for j in range(3)) + sum(F[i][j] * x[j] for j in range(2))
                    + sum(lam[a] * G[reg.active[a]][i] for a in range(len(lam))) for i in range(3)]
            assert max(abs(v) for v in grad) < 1e-9


def test_interiors_do_not_overlap():
    rng = random.Random(23)
    for _ in range(500):
        x = [rng.uniform(-10, 10), rng.uniform(-10, 10)]
        strict = [i for i, r in enumerate(REGIONS) if r.contains(x, -1e-9)]
        assert len(strict) <= 1


def test_law_is_continuous():
    rng = random.Random(24)
    for _ in range(300):
        x = [rng.uniform(-9.9, 9.9), rng.uniform(-9.9, 9.9)]
        y = [x[0] + rng.uniform(-1e-6, 1e-6), x[1] + rng.uniform(-1e-6, 1e-6)]
        zx, _ = evaluate(REGIONS, x)
        zy, _ = evaluate(REGIONS, y)
        assert max(abs(a - b) for a, b in zip(zx, zy)) < 1e-4


def test_value_function_is_convex():
    rng = random.Random(25)
    for _ in range(200):
        x = [rng.uniform(-10, 10), rng.uniform(-10, 10)]
        y = [rng.uniform(-10, 10), rng.uniform(-10, 10)]
        mid = [(a + b) / 2 for a, b in zip(x, y)]
        v = [horizon_cost(p, evaluate(REGIONS, p)[0]) for p in (x, y, mid)]
        assert v[2] <= (v[0] + v[1]) / 2 + 1e-8


def test_outside_the_box_is_not_covered():
    z, idx = evaluate(REGIONS, [10.5, 0.0])
    assert z is None and idx is None


def test_chebyshev_radius():
    box = [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]
    assert abs(chebyshev_radius(box, [1.0, 1.0, 1.0, 1.0]) - 1.0) < 1e-12
    assert abs(chebyshev_radius(box + [[1.0, 1.0]], [1.0, 1.0, 1.0, 1.0, 0.0]) - (2 - 2 ** 0.5)) < 1e-9
    assert chebyshev_radius(box, [1.0, -2.0, 1.0, 1.0]) is None


def test_state_constraints_shrink_the_covered_set():
    Hs, Fs, Gs, Ws, Es = mpc_to_mpqp(A, B, Q, R, P, 2, [-1.0], [1.0], [-5.0, -5.0], [5.0, 5.0])
    regs = explicit_mpc(Hs, Fs, Gs, Ws, Es, [5.0, 5.0])
    assert evaluate(regs, [4.0, 2.0])[1] is None  # infeasible: x_1 >= 5.5 for every u
    z, idx = evaluate(regs, [0.1, -0.1])
    assert idx is not None and abs(z[0] + K[0] * 0.1 - K[1] * 0.1) < 1e-9
