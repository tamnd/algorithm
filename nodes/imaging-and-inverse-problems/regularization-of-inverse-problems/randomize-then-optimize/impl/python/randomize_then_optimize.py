# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomize-then-optimize/. The authors are listed in prov/27EKVH.jsonl.
"""Randomize-then-optimize (RTO) with a Metropolis-Hastings correction.

The posterior is written as pi(x) proportional to exp(-||F(x) - ybar||^2 / 2),
where F stacks the whitened forward map and the whitened prior:
F(x) = [Gamma^{-1/2} G(x); L (x - m0)], ybar = [Gamma^{-1/2} y; 0], with
L^T L = C^{-1} for a Gaussian prior N(m0, C). F maps R^n to R^M, M >= n.

RTO fixes Q, an M x n matrix with orthonormal columns that span the range of
the Jacobian J(xbar) at the MAP point xbar. A proposal is the solution x of
Q^T F(x) = Q^T (ybar + eps), eps ~ N(0, I_M). If x -> Q^T F(x) is one-to-one
and smooth, the proposal has density
    q(x) proportional to |det(Q^T J(x))| exp(-||Q^T (F(x) - ybar)||^2 / 2),
and the importance weight pi / q is
    w(x) = |det(Q^T J(x))|^{-1} exp(-||F(x) - ybar||^2 / 2 + ||Q^T (F(x) - ybar)||^2 / 2).
An independence Metropolis-Hastings step with ratio w(x') / w(x) makes the
chain exact. For a linear F the weight is constant and every proposal is an
exact posterior sample.
"""

import math

from imgla import matvec, solve, transpose


def det(a):
    """Determinant of a square matrix by Gaussian elimination with pivoting."""
    n = len(a)
    m = [list(map(float, row)) for row in a]
    d = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0.0:
            return 0.0
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for j in range(c, n):
                m[r][j] -= f * m[c][j]
    return d


def thin_qr_q(j):
    """Q with orthonormal columns spanning the columns of the M x n matrix j
    (modified Gram-Schmidt, applied twice). Raises ValueError if the rank is
    below n."""
    mrows, n = len(j), len(j[0])
    cols = [[j[i][k] for i in range(mrows)] for k in range(n)]
    q = []
    for c in cols:
        v = list(c)
        for _ in range(2):
            for e in q:
                h = sum(a * b for a, b in zip(e, v))
                v = [a - h * b for a, b in zip(v, e)]
        nrm = math.sqrt(sum(a * a for a in v))
        if nrm <= 1e-13 * max(1.0, math.sqrt(sum(a * a for a in c))):
            raise ValueError("Jacobian does not have full column rank")
        q.append([a / nrm for a in v])
    return [[q[k][i] for k in range(n)] for i in range(mrows)]


def gauss_newton_map(f, jac, ybar, x0, iters=100, tol=1e-12):
    """Minimize ||F(x) - ybar||^2 / 2 by Gauss-Newton with step halving."""
    x = list(x0)
    r = [a - b for a, b in zip(f(x), ybar)]
    val = 0.5 * sum(t * t for t in r)
    for _ in range(iters):
        jx = jac(x)
        jt = transpose(jx)
        g = matvec(jt, r)
        if math.sqrt(sum(t * t for t in g)) <= tol:
            break
        jtj = [[sum(a * b for a, b in zip(ri, rk)) for rk in jt] for ri in jt]
        step = solve(jtj, g)
        t = 1.0
        while t > 1e-10:
            xn = [a - t * s for a, s in zip(x, step)]
            rn = [a - b for a, b in zip(f(xn), ybar)]
            vn = 0.5 * sum(e * e for e in rn)
            if vn <= val:
                break
            t *= 0.5
        else:
            break
        x, r, val = xn, rn, vn
    return x


def solve_projected(f, jac, q, target, x0, iters=50, tol=1e-11):
    """Solve Q^T F(x) = target by Newton's method from x0. Returns x, or None
    if Newton does not reach the tolerance."""
    qt = transpose(q)
    x = list(x0)
    for _ in range(iters):
        res = [a - b for a, b in zip(matvec(qt, f(x)), target)]
        if math.sqrt(sum(t * t for t in res)) <= tol * (1.0 + math.sqrt(sum(t * t for t in target))):
            return x
        jq = [matvec(qt, col) for col in transpose(jac(x))]  # columns of Q^T J
        try:
            step = solve(transpose(jq), res)
        except ValueError:
            return None
        x = [a - s for a, s in zip(x, step)]
    res = [a - b for a, b in zip(matvec(qt, f(x)), target)]
    if math.sqrt(sum(t * t for t in res)) <= tol * (1.0 + math.sqrt(sum(t * t for t in target))):
        return x
    return None


def log_weight(f, jac, q, ybar, x):
    """log w(x) = -log|det(Q^T J(x))| - ||F(x) - ybar||^2 / 2 + ||Q^T (F(x) - ybar)||^2 / 2."""
    qt = transpose(q)
    r = [a - b for a, b in zip(f(x), ybar)]
    qr = matvec(qt, r)
    qtj = [matvec(qt, col) for col in transpose(jac(x))]
    d = abs(det(qtj))
    if d == 0.0:
        return -math.inf
    return -math.log(d) - 0.5 * sum(t * t for t in r) + 0.5 * sum(t * t for t in qr)


def rto_mh(f, jac, ybar, x0, steps, rng):
    """RTO-MH. Returns (chain, acceptance_rate, xbar)."""
    xbar = gauss_newton_map(f, jac, ybar, x0)  # @line L1
    q = thin_qr_q(jac(xbar))  # @line L2
    qt = transpose(q)
    x, lw = xbar, log_weight(f, jac, q, ybar, xbar)  # @line L3
    chain = []
    accepted = 0
    for _ in range(steps):  # @line L4
        eps = [rng.gauss(0.0, 1.0) for _ in ybar]  # @line L5
        target = matvec(qt, [a + e for a, e in zip(ybar, eps)])
        xp = solve_projected(f, jac, q, target, xbar)  # @line L6
        if xp is not None:
            lwp = log_weight(f, jac, q, ybar, xp)  # @line L7
            if math.log(1.0 - rng.random()) < lwp - lw:  # @line L8
                x, lw = xp, lwp
                accepted += 1
        chain.append(x)  # @line L9
    return chain, accepted / steps, xbar  # @line L10


def linear_problem(a, y, sigma, prior_sd, m0=None):
    """F and its Jacobian for G(x) = A x, noise N(0, sigma^2 I) and prior
    N(m0, prior_sd^2 I)."""
    n = len(a[0])
    if m0 is None:
        m0 = [0.0] * n
    h = [[v / sigma for v in row] for row in a] + [[(1.0 / prior_sd if i == k else 0.0) for k in range(n)] for i in range(n)]
    ybar = [v / sigma for v in y] + [0.0] * n

    def f(x):
        return [sum(v * xk for v, xk in zip(row, x)) / sigma for row in a] + [(xi - mi) / prior_sd for xi, mi in zip(x, m0)]

    def jac(x):
        return h

    return f, jac, ybar
