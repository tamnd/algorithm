# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luenberger-observer/. The authors are listed in prov/7T6PY4.jsonl.

"""Full-order Luenberger observer for x' = A x + B u, y = C x.

The observer is

    xhat' = A xhat + B u + L (y - C xhat),

so the error e = x - xhat obeys e' = (A - L C) e, whatever u is. The gain L
places the eigenvalues of A - L C. It is the transpose of a state feedback
gain for the dual pair (A^T, C^T): A - L C = (A^T - C^T L^T)^T.

place() handles any number of inputs (here: outputs of the observed
system). It uses Heymann's lemma in the constructive form of Hautus (1977):
a feedback F and one input column b = B e_l make (A + B F, b) controllable,
and then Ackermann's formula places the poles of the single-input pair. The
result is one valid gain, not a well conditioned one; for that, see the
robust pole placement page.

The same formulas hold in discrete time, with
xhat_(k+1) = A xhat_k + B u_k + L (y_k - C xhat_k).
Exact (Fraction) for int and Fraction data.
"""

from fractions import Fraction

from ctlmat import matvec, solve, transpose

__all__ = ["place", "observer_gain", "observer_rhs", "observer_step"]


def _rank(vectors, tol):
    """Rank of a list of flat vectors (exact for int and Fraction data)."""
    rows = [list(v) for v in vectors]
    if not rows:
        return 0
    exact = all(isinstance(x, (int, Fraction)) for r in rows for x in r)
    if exact:
        rows = [[Fraction(x) for x in r] for r in rows]
    big = max([abs(x) for r in rows for x in r] + [1.0]) if not exact else 1
    rank = 0
    ncol = len(rows[0])
    for c in range(ncol):
        p = max(range(rank, len(rows)), key=lambda i: abs(rows[i][c]), default=None)
        if p is None:
            break
        if (rows[p][c] == 0) if exact else (abs(rows[p][c]) <= tol * big):
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for i in range(rank + 1, len(rows)):
            f = rows[i][c] / rows[rank][c]
            rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def _ackermann(A, b, p):
    n = len(A)
    cols = [list(b)]
    for _ in range(n - 1):
        cols.append(matvec(A, cols[-1]))
    try:
        q = solve(cols, [0] * (n - 1) + [1])  # rows of W^T are the columns of W
    except ValueError:
        raise ValueError("the pair is not controllable") from None
    At = transpose(A)
    K = [0] * n
    for c in p:
        K = [x + c * y for x, y in zip(matvec(At, K), q)]
    return K


def place(A, B, p, tol=1e-10):
    """Return K (m by n) with det(s I - (A - B K)) = p(s), p monic of degree n.

    Raises ValueError if (A, B) is not controllable.
    """
    n = len(A)
    m = len(B[0])
    if len(p) != n + 1 or p[0] != 1:
        raise ValueError("p must be monic of degree n")
    cols = [[B[i][j] for i in range(n)] for j in range(m)]
    lead = None
    for j in range(m):
        if _rank([cols[j]], tol) == 1:
            lead = j
            break
    if lead is None:
        raise ValueError("the pair is not controllable (B = 0)")
    # Hautus' construction: x_1 = b, x_(k+1) = A x_k + B u_k not in span(x_1..x_k).
    xs = [cols[lead]]
    us = []
    while len(xs) < n:
        ax = matvec(A, xs[-1])
        chosen = None
        for j in [None] + list(range(m)):
            cand = ax if j is None else [a + c for a, c in zip(ax, cols[j])]
            if _rank(xs + [cand], tol) > len(xs):
                chosen = (j, cand)
                break
        if chosen is None:
            raise ValueError("the pair is not controllable")
        j, cand = chosen
        u = [0] * m
        if j is not None:
            u[j] = 1
        us.append(u)
        xs.append(cand)
    us.append([0] * m)
    # F x_k = u_k for all k, so F = U X^(-1): solve X^T F^T = U^T.
    Ft = solve(xs, us)  # xs as rows is X^T, us as rows is U^T
    F = transpose(Ft)
    AF = [[A[i][k] + sum(B[i][j] * F[j][k] for j in range(m)) for k in range(n)] for i in range(n)]
    k1 = _ackermann(AF, cols[lead], p)
    # A - B K = A + B F - b k1 with K = -F + e_lead k1.
    return [[-F[j][k] + (k1[k] if j == lead else 0) for k in range(n)] for j in range(m)]


def observer_gain(A, C, p, tol=1e-10):
    """Return L (n by p) with det(s I - (A - L C)) = p(s).

    Raises ValueError if (C, A) is not observable.
    """
    try:
        Kd = place(transpose(A), transpose(C), p, tol)  # @line L1
    except ValueError:
        raise ValueError("(C, A) is not observable") from None
    return transpose(Kd)  # @line L2


def observer_rhs(A, B, C, L):
    """Return f(t, xhat, (u, y)) = A xhat + B u + L (y - C xhat)."""
    def f(t, xhat, uy):
        u, y = uy
        r = [yi - ci for yi, ci in zip(y, matvec(C, xhat))]  # @line L3
        out = matvec(A, xhat)  # @line L4
        if B is not None and u is not None:
            out = [o + v for o, v in zip(out, matvec(B, u))]
        return [o + v for o, v in zip(out, matvec(L, r))]
    return f


def observer_step(A, B, C, L, xhat, u, y):
    """Return the discrete-time update A xhat + B u + L (y - C xhat)."""
    return observer_rhs(A, B, C, L)(0, xhat, (u, y))
