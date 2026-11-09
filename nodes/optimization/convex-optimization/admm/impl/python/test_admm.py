# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/admm/. The authors are listed in prov/N7GCD0.jsonl.

import itertools
import random
from fractions import Fraction

from admm import admm, box_qp_steps, matvec, solve, standard_lp_steps


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def sq(v):
    return dot(v, v)


def sub(u, v):
    return [p - q for p, q in zip(u, v)]


def eye(n, s=1):
    return [[Fraction(s) if i == j else Fraction(0) for j in range(n)] for i in range(n)]


def check_run(res, a, bm, c, z0, u0, rho, fval, xstar, zstar, ystar, rng):
    """Checks the Lyapunov decrease and the ergodic O(1/K) bounds, exactly."""
    y0 = [rho * v for v in u0]
    pstar = fval(xstar)

    def lyap(y, z):
        return sq(sub(y, ystar)) / rho + rho * sq(matvec(bm, sub(z, zstar)))

    v_prev, z_prev = lyap(y0, z0), z0
    sx = [Fraction(0)] * len(xstar)
    sz = [Fraction(0)] * len(zstar)
    for k, (x, z, u, r) in enumerate(res.steps, start=1):
        y = [rho * v for v in u]
        v = lyap(y, z)
        drop = rho * sq(r) + rho * sq(matvec(bm, sub(z, z_prev))) if k >= 2 else 0
        assert v <= v_prev - drop
        v_prev, z_prev = v, z
        # ergodic averages of the first k iterates
        sx = [p + q for p, q in zip(sx, x)]
        sz = [p + q for p, q in zip(sz, z)]
        xb, zb = [p / k for p in sx], [p / k for p in sz]
        rb = [p + q - ci for p, q, ci in zip(matvec(a, xb), matvec(bm, zb), c)]
        gap = fval(xb) - pstar
        assert gap + dot(ystar, rb) >= 0  # the saddle point inequality
        for lam in ([0] * len(ystar), ystar, [p + q for p, q in zip(ystar, rb)], [Fraction(rng.randint(-3, 3)) for _ in ystar]):
            bound = sq(sub(lam, y0)) / (2 * rho) + rho * sq(matvec(bm, sub(z0, zstar))) / 2
            assert gap + dot(lam, rb) <= bound / k


def box_oracle(p, q, lo, hi):
    """Exact minimizer of x^T P x / 2 + q^T x on a box, by enumeration of the active bounds."""
    n = len(q)
    for state in itertools.product((0, 1, 2), repeat=n):  # 0 at lo, 1 at hi, 2 free
        x = [lo[i] if s == 0 else hi[i] if s == 1 else None for i, s in enumerate(state)]
        free = [i for i in range(n) if state[i] == 2]
        if free:
            mat = [[p[i][j] for j in free] for i in free]
            rhs = [-q[i] - sum(p[i][j] * x[j] for j in range(n) if state[j] != 2) for i in free]
            try:
                xf = solve(mat, rhs)
            except ValueError:
                continue
            for i, v in zip(free, xf):
                x[i] = v
        if any(x[i] < lo[i] or x[i] > hi[i] for i in range(n)):
            continue
        grad = [dot(p[i], x) + q[i] for i in range(n)]
        if all((grad[i] >= 0 if s == 0 else grad[i] <= 0 if s == 1 else grad[i] == 0) for i, s in enumerate(state)):
            return x, grad
    return None


def lp_oracle(a, b, c):
    """An optimal basic pair (x*, s*) of min c^T x, A x = b, x >= 0, with s* = c - A^T w*."""
    m, n = len(b), len(c)
    for basis in itertools.combinations(range(n), m):
        ab = [[a[i][j] for j in basis] for i in range(m)]
        try:
            xb = solve(ab, list(b))
            w = solve([list(col) for col in zip(*ab)], [c[j] for j in basis])
        except ValueError:
            continue
        s = [c[j] - sum(a[i][j] * w[i] for i in range(m)) for j in range(n)]
        if min(xb) >= 0 and min(s) >= 0:
            x = [Fraction(0)] * n
            for j, v in zip(basis, xb):
                x[j] = v
            return x, s
    return None


def test_page_example() -> None:
    # minimize (x - 3)^2 / 2 subject to 0 <= x <= 1, split as x - z = 0; x* = z* = 1, y* = 2
    p, q, lo, hi = [[Fraction(1)]], [Fraction(-3)], [Fraction(0)], [Fraction(1)]
    xs, zs = box_qp_steps(p, q, lo, hi)
    a, bm, c = eye(1), eye(1, -1), [Fraction(0)]
    res = admm(xs, zs, a, bm, c, [Fraction(1)], [Fraction(0)], Fraction(1), max_iter=8)
    for k, (x, z, u, r) in enumerate(res.steps, start=1):
        e = Fraction(2, 2**k)
        assert x == [1 + e] and z == [1] and u == [2 - e] and r == [e]
    fval = lambda x: (x[0] - 3) ** 2 / 2
    check_run(res, a, bm, c, [Fraction(1)], [Fraction(0)], Fraction(1), fval, [Fraction(1)], [Fraction(1)], [Fraction(2)], random.Random(0))


def test_random_box_qp() -> None:
    rng = random.Random(3)
    done = 0
    while done < 500:
        n = rng.randint(1, 3)
        rows = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(rng.randint(0, n))]
        p = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]  # PSD, often singular
        q = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        lo = [Fraction(rng.randint(-2, 0)) for _ in range(n)]
        hi = [l + rng.randint(0, 3) for l in lo]
        sol = box_oracle(p, q, lo, hi)
        assert sol is not None  # a convex QP on a nonempty box always has a KKT point
        xstar, grad = sol
        ystar = [-g for g in grad]
        rho = Fraction(rng.choice([1, 2, 3]), rng.choice([1, 2]))
        z0 = [Fraction(rng.randint(-2, 2)) for _ in range(n)]
        u0 = [Fraction(rng.randint(-2, 2)) for _ in range(n)]
        xs, zs = box_qp_steps(p, q, lo, hi)
        a, bm, c = eye(n), eye(n, -1), [Fraction(0)] * n
        res = admm(xs, zs, a, bm, c, z0, u0, rho, max_iter=8)
        assert all(lo[i] <= z[i] <= hi[i] for _, z, _, _ in res.steps for i in range(n))
        fval = lambda x: dot(x, matvec(p, x)) / 2 + dot(q, x)
        check_run(res, a, bm, c, z0, u0, rho, fval, xstar, xstar, ystar, rng)
        done += 1


def test_random_standard_lp() -> None:
    rng = random.Random(4)
    done = 0
    while done < 500:
        m = rng.randint(1, 2)
        n = rng.randint(m + 1, 4)
        a = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(m)]
        x0 = [Fraction(rng.randint(0, 2)) for _ in range(n)]
        b = matvec(a, x0)
        w0 = [Fraction(rng.randint(-2, 2)) for _ in range(m)]
        c = [sum(a[i][j] * w0[i] for i in range(m)) + rng.randint(0, 2) for j in range(n)]
        sol = lp_oracle(a, b, c)
        if sol is None:
            continue  # A does not have full row rank
        xstar, sstar = sol
        ystar = [-v for v in sstar]
        rho = Fraction(rng.choice([1, 2]), rng.choice([1, 2]))
        z0 = [Fraction(rng.randint(0, 2)) for _ in range(n)]
        u0 = [Fraction(rng.randint(-1, 1)) for _ in range(n)]
        xs, zs = standard_lp_steps(a, b, c)
        ai, bm, cz = eye(n), eye(n, -1), [Fraction(0)] * n
        res = admm(xs, zs, ai, bm, cz, z0, u0, rho, max_iter=6)
        assert all(matvec(a, x) == b and min(z) >= 0 for x, z, _, _ in res.steps)
        check_run(res, ai, bm, cz, z0, u0, rho, lambda x: dot(c, x), xstar, xstar, ystar, rng)
        done += 1


def test_float_stop_rule() -> None:
    # minimize (x1 - 2)^2 / 2 + (x2 + 1)^2 subject to 0 <= x <= 1; x* = (1, 0), y* = (1, -2)
    p, q = [[1.0, 0.0], [0.0, 2.0]], [-2.0, 2.0]
    xs, zs = box_qp_steps(p, q, [0.0, 0.0], [1.0, 1.0])
    a, bm, c = [[1.0, 0.0], [0.0, 1.0]], [[-1.0, 0.0], [0.0, -1.0]], [0.0, 0.0]
    res = admm(xs, zs, a, bm, c, [0.0, 0.0], [0.0, 0.0], 1.0, eps=1e-10)
    assert len(res.steps) < 1000
    assert all(abs(u - v) < 1e-9 for u, v in zip(res.z, [1.0, 0.0]))
    assert all(abs(u - v) < 1e-9 for u, v in zip(res.y, [1.0, -2.0]))
