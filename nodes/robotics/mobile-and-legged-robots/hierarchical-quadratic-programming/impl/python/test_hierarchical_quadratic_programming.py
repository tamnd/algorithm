# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-quadratic-programming/. The authors are listed in prov/7BEBTS.jsonl.

import itertools
import math
import random

from hierarchical_quadratic_programming import active_set_lsq, solve_hqp, weighted_qp


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def gauss(a, b):
    """Plain Gaussian elimination with partial pivoting; None if singular."""
    n = len(a)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-11:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                for j in range(c, n + 1):
                    m[r][j] -= f * m[c][j]
    return [m[i][n] / m[i][i] for i in range(n)]


def norm2(v):
    return sum(x * x for x in v)


def test_strict_priority_on_one_variable():
    # Level 1: x <= 1. Level 2: x = 3. The higher level wins.
    x, res = solve_hqp([{"C": [[1.0]], "d": [1.0]}, {"A": [[1.0]], "b": [3.0]}], 1)
    assert abs(x[0] - 1.0) < 1e-9
    assert res[0][1] == [0.0] and abs(res[1][0][0] + 2.0) < 1e-9
    # Swap the levels: now x = 3 and the inequality is violated by 2.
    x, res = solve_hqp([{"A": [[1.0]], "b": [3.0]}, {"C": [[1.0]], "d": [1.0]}], 1)
    assert abs(x[0] - 3.0) < 1e-7
    assert abs(res[1][1][0] - 2.0) < 1e-7


def test_infeasible_level_is_solved_in_least_squares():
    # Level 1 asks x >= 2 and x <= 1: the best compromise is 1.5. Level 2 (x = 0) cannot move it.
    lv1 = {"C": [[-1.0], [1.0]], "d": [-2.0, 1.0]}
    x, res = solve_hqp([lv1, {"A": [[1.0]], "b": [0.0]}], 1)
    assert abs(x[0] - 1.5) < 1e-8
    assert close(res[0][1], [0.5, 0.5], 1e-8)
    assert abs(res[1][0][0] - 1.5) < 1e-8


def test_page_example():
    # Level 1: x1 <= 1. Level 2: x1 + x2 = 3. Level 3: x1 = 0 and x2 = 0.
    levels = [
        {"C": [[1.0, 0.0]], "d": [1.0]},
        {"A": [[1.0, 1.0]], "b": [3.0]},
        {"A": [[1.0, 0.0], [0.0, 1.0]], "b": [0.0, 0.0]},
    ]
    x, res = solve_hqp(levels, 2)
    assert close(x, [1.0, 2.0], 1e-8)
    assert abs(res[1][0][0]) < 1e-8
    assert close(res[2][0], [1.0, 2.0], 1e-8)
    # The weighted QP with weights 100, 10, 1 trades the levels against each other.
    xw = weighted_qp(levels, 2, [100.0, 10.0, 1.0])
    assert abs(xw[0] + xw[1] - 3.0) > 1e-2


def test_active_set_qp_against_vertex_enumeration():
    # min (1/2)|u - c|^2 over a random polygon given by m half-planes, n = 2.
    rng = random.Random(5)
    for _ in range(60):
        m = rng.randint(3, 6)
        rows, rhs = [], []
        for _ in range(m):
            t = rng.uniform(0, 2 * math.pi)
            rows.append([math.cos(t), math.sin(t)])
            rhs.append(rng.uniform(0.2, 1.5))  # u = 0 is feasible
        c = [rng.uniform(-3, 3), rng.uniform(-3, 3)]
        u, _, _ = active_set_lsq([[1.0, 0.0], [0.0, 1.0]], c, rows, rhs, [0.0, 0.0])
        best = None
        cands = [c]
        for i in range(m):
            a, b = rows[i], rhs[i]
            s = (sum(a[j] * c[j] for j in range(2)) - b)
            cands.append([c[j] - s * a[j] for j in range(2)])
            for k in range(i + 1, m):
                p = gauss([rows[i], rows[k]], [rhs[i], rhs[k]])
                if p is not None:
                    cands.append(p)
        for p in cands:
            if all(sum(r[j] * p[j] for j in range(2)) <= bb + 1e-9 for r, bb in zip(rows, rhs)):
                val = norm2([p[j] - c[j] for j in range(2)])
                if best is None or val < best:
                    best = val
        assert abs(norm2([u[j] - c[j] for j in range(2)]) - best) < 1e-9


def null_space_cascade(levels, n):
    """Reference for equality-only stacks: solve the levels one by one in the null space of the higher levels."""
    x = [0.0] * n
    z = [[1.0 if i == j else 0.0 for i in range(n)] for j in range(n)]  # columns
    for lev in levels:
        a, b = lev["A"], lev["b"]
        r = len(z)
        if r == 0:
            break
        m = [[sum(row[i] * col[i] for i in range(n)) for col in z] for row in a]
        res = [b[i] - sum(a[i][j] * x[j] for j in range(n)) for i in range(len(a))]
        if len(a) >= r:  # full column rank: normal equations
            y = gauss([[sum(m[t][i] * m[t][j] for t in range(len(a))) for j in range(r)] for i in range(r)],
                      [sum(m[t][i] * res[t] for t in range(len(a))) for i in range(r)])
        else:  # full row rank: the minimum-norm solution
            lam = gauss([[sum(m[i][t] * m[j][t] for t in range(r)) for j in range(len(a))] for i in range(len(a))], res)
            y = [sum(m[t][i] * lam[t] for t in range(len(a))) for i in range(r)]
        x = [x[i] + sum(z[j][i] * y[j] for j in range(r)) for i in range(n)]
        # New basis: the null space of m in y coordinates, mapped back by z.
        basis = []
        for row in m:
            v = list(row)
            for q in basis:
                c = sum(v[i] * q[i] for i in range(r))
                v = [v[i] - c * q[i] for i in range(r)]
            nv = math.sqrt(norm2(v))
            if nv > 1e-9:
                basis.append([t / nv for t in v])
        nb = []
        for j in range(r):
            v = [1.0 if i == j else 0.0 for i in range(r)]
            for q in basis + nb:
                c = sum(v[i] * q[i] for i in range(r))
                v = [v[i] - c * q[i] for i in range(r)]
            nv = math.sqrt(norm2(v))
            if nv > 1e-6 and len(basis) + len(nb) < r:
                nb.append([t / nv for t in v])
        z = [[sum(z[k][i] * q[k] for k in range(r)) for i in range(n)] for q in nb]
    return x


def test_equality_stacks_match_the_null_space_cascade():
    rng = random.Random(6)
    for sizes, n in [((2, 2, 1), 6), ((1, 3), 3), ((2, 3, 2), 4), ((3, 3), 4)]:
        for _ in range(10):
            levels = [{"A": [[rng.gauss(0, 1) for _ in range(n)] for _ in range(k)],
                       "b": [rng.gauss(0, 1) for _ in range(k)]} for k in sizes]
            x, res = solve_hqp(levels, n, eps=1e-12)
            want = null_space_cascade(levels, n)
            assert close(x, want, 1e-6)


def brute_force_hqp(levels, n, eps):
    """Level by level, enumerate which inequality rows are active, violated or free.

    Uses the slack form of Kanoun et al.: the rows of higher levels stay A x = b + w* and
    C x <= d + v*. Every candidate is the minimizer of a quadratic on an affine set; the
    best feasible candidate is the optimum of the damped level problem.
    """
    x_prev = [0.0] * n
    eq, ineq = [], []
    out = []
    for lev in levels:
        a, b = lev.get("A", []), lev.get("b", [])
        c, d = lev.get("C", []), lev.get("d", [])

        def f(x):
            r = [sum(a[i][j] * x[j] for j in range(n)) - b[i] for i in range(len(a))]
            s = [max(0.0, sum(c[i][j] * x[j] for j in range(n)) - d[i]) for i in range(len(c))]
            return 0.5 * norm2(r) + 0.5 * norm2(s) + 0.5 * eps * norm2([x[i] - x_prev[i] for i in range(n)])

        best = None
        for hard_on in itertools.product((0, 1), repeat=len(ineq)):
            for own in itertools.product((0, 1, 2), repeat=len(c)):  # 0 free, 1 active, 2 violated
                obj = [(row, rhs) for row, rhs in zip(a, b)]
                obj += [(c[i], d[i]) for i in range(len(c)) if own[i] == 2]
                cons = list(eq) + [ineq[i] for i in range(len(ineq)) if hard_on[i]]
                cons += [(c[i], d[i]) for i in range(len(c)) if own[i] == 1]
                if len(cons) > n:
                    continue
                k = len(cons)
                kkt = [[sum(r[i] * r[j] for r, _ in obj) + (eps if i == j else 0.0) for j in range(n)]
                       + [cons[t][0][i] for t in range(k)] for i in range(n)]
                kkt += [list(cons[t][0]) + [0.0] * k for t in range(k)]
                rhs = [sum(r[i] * q for r, q in obj) + eps * x_prev[i] for i in range(n)] + [q for _, q in cons]
                sol = gauss(kkt, rhs)
                if sol is None:
                    continue
                x = sol[:n]
                if any(abs(sum(r[j] * x[j] for j in range(n)) - q) > 1e-7 for r, q in eq):
                    continue
                if any(sum(r[j] * x[j] for j in range(n)) > q + 1e-9 for r, q in ineq):
                    continue
                val = f(x)
                if best is None or val < best[0]:
                    best = (val, x)
        x = best[1]
        w = [sum(a[i][j] * x[j] for j in range(n)) - b[i] for i in range(len(a))]
        v = [max(0.0, sum(c[i][j] * x[j] for j in range(n)) - d[i]) for i in range(len(c))]
        eq += [(a[i], b[i] + w[i]) for i in range(len(a))]
        ineq += [(c[i], d[i] + v[i]) for i in range(len(c))]
        out.append((w, v))
        x_prev = x
    return x_prev, out


def test_inequality_stacks_match_brute_force():
    rng = random.Random(7)
    n = 3
    for trial in range(40):
        levels = []
        for k in range(3):
            ne = rng.choice([0, 1]) if k < 2 else rng.choice([1, 2])
            ni = rng.choice([1, 2])
            levels.append({
                "A": [[rng.gauss(0, 1) for _ in range(n)] for _ in range(ne)],
                "b": [rng.gauss(0, 1) for _ in range(ne)],
                "C": [[rng.gauss(0, 1) for _ in range(n)] for _ in range(ni)],
                "d": [rng.gauss(0, 1) for _ in range(ni)],
            })
        x, res = solve_hqp(levels, n, eps=1e-9)
        xb, resb = brute_force_hqp(levels, n, 1e-9)
        for (w, v), (wb, vb) in zip(res, resb):
            assert abs(norm2(w) + norm2(v) - norm2(wb) - norm2(vb)) < 1e-6
        assert close(x, xb, 1e-5)


def test_lower_levels_never_degrade_higher_levels():
    # Adding a level at the bottom does not change the optimal residuals of the levels above it.
    rng = random.Random(8)
    n = 4
    for _ in range(20):
        levels = [{"A": [[rng.gauss(0, 1) for _ in range(n)]], "b": [rng.gauss(0, 1)],
                   "C": [[rng.gauss(0, 1) for _ in range(n)] for _ in range(2)],
                   "d": [rng.gauss(0, 1) for _ in range(2)]} for _ in range(3)]
        _, res3 = solve_hqp(levels, n)
        extra = {"A": [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)], "b": [rng.gauss(0, 3) for _ in range(n)]}
        _, res4 = solve_hqp(levels + [extra], n)
        for (w, v), (w2, v2) in zip(res3, res4):
            assert abs(norm2(w) + norm2(v) - norm2(w2) - norm2(v2)) < 1e-7
