# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-order-observer/. The authors are listed in prov/3BXD4W.jsonl.

"""Reduced-order (minimal-order) observer for x' = A x + B u, y = C x.

C is p by n with full row rank p < n. The outputs give p combinations of
the state exactly, so only n - p numbers are estimated. In the coordinates
T x = [y; w], with T = [C; V],

    y' = A11 y + A12 w + B1 u,
    w' = A21 y + A22 w + B2 u.

The observer state z estimates w - L y:

    z' = F z + G y + H u,   w_hat = z + L y,   x_hat = T^(-1) [y; w_hat],
    F = A22 - L A12,  G = F L + A21 - L A11,  H = B2 - L B1.

Its error w - w_hat obeys e' = F e, and L places the eigenvalues of F.
(A12, A22) is observable if (C, A) is, so this is always possible then.
The same formulas hold in discrete time (z_(k+1) = F z_k + G y_k + H u_k).

Exact (Fraction) for int and Fraction data.
"""

from fractions import Fraction

from ctlmat import add, inv, matvec, mul, solve, sub, transpose

__all__ = ["place", "reduced_order_observer", "observer_rhs", "observer_step", "estimate"]


def _rank(vectors, tol):
    rows = [list(v) for v in vectors]
    if not rows:
        return 0
    exact = all(isinstance(x, (int, Fraction)) for r in rows for x in r)
    if exact:
        rows = [[Fraction(x) for x in r] for r in rows]
    big = 1 if exact else max([abs(x) for r in rows for x in r] + [1.0])
    rank = 0
    for c in range(len(rows[0])):
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
        q = solve(cols, [0] * (n - 1) + [1])
    except ValueError:
        raise ValueError("the pair is not controllable") from None
    At = transpose(A)
    K = [0] * n
    for c in p:
        K = [x + c * y for x, y in zip(matvec(At, K), q)]
    return K


def place(A, B, p, tol=1e-10):
    """Return K with det(s I - (A - B K)) = p(s); Heymann's lemma, then Ackermann.

    Raises ValueError if (A, B) is not controllable.
    """
    n = len(A)
    m = len(B[0])
    if len(p) != n + 1 or p[0] != 1:
        raise ValueError("p must be monic of degree n")
    cols = [[B[i][j] for i in range(n)] for j in range(m)]
    lead = next((j for j in range(m) if _rank([cols[j]], tol) == 1), None)
    if lead is None:
        raise ValueError("the pair is not controllable (B = 0)")
    xs, us = [cols[lead]], []
    while len(xs) < n:
        ax = matvec(A, xs[-1])
        for j in [None] + list(range(m)):
            cand = ax if j is None else [a + c for a, c in zip(ax, cols[j])]
            if _rank(xs + [cand], tol) > len(xs):
                break
        else:
            raise ValueError("the pair is not controllable")
        u = [0] * m
        if j is not None:
            u[j] = 1
        us.append(u)
        xs.append(cand)
    us.append([0] * m)
    F = transpose(solve(xs, us))
    AF = add(A, mul(B, F))
    k1 = _ackermann(AF, cols[lead], p)
    return [[-F[j][k] + (k1[k] if j == lead else 0) for k in range(n)] for j in range(m)]


def reduced_order_observer(A, B, C, alpha, tol=1e-10):
    """Return (F, G, H, L, Tinv) of the reduced-order observer.

    alpha is the monic characteristic polynomial wanted for F, of degree
    n - p. Raises ValueError if C does not have full row rank p < n or if
    (C, A) is not observable.
    """
    n, p = len(A), len(C)
    if _rank(C, tol) != p:
        raise ValueError("C must have full row rank")
    if p >= n:
        raise ValueError("p < n is needed; for p = n, x = C^(-1) y")
    V = []
    for i in range(n):  # @line L1
        e = [1 if j == i else 0 for j in range(n)]
        if _rank(C + V + [e], tol) > p + len(V):
            V.append(e)
    T = [list(r) for r in C] + V
    Tinv = inv(T)
    Ab = mul(mul(T, A), Tinv)  # @line L2
    Bb = mul(T, B) if B is not None else None
    A11 = [r[:p] for r in Ab[:p]]
    A12 = [r[p:] for r in Ab[:p]]
    A21 = [r[:p] for r in Ab[p:]]
    A22 = [r[p:] for r in Ab[p:]]
    try:
        L = transpose(place(transpose(A22), transpose(A12), alpha, tol))  # @line L3
    except ValueError:
        raise ValueError("(C, A) is not observable") from None
    F = sub(A22, mul(L, A12))  # @line L4
    G = add(mul(F, L), sub(A21, mul(L, A11)))
    H = None
    if Bb is not None:
        H = sub(Bb[p:], mul(L, Bb[:p]))
    return F, G, H, L, Tinv  # @line L5


def observer_rhs(F, G, H):
    """Return f(t, z, (u, y)) = F z + G y + H u."""
    def f(t, z, uy):
        u, y = uy
        out = [a + b for a, b in zip(matvec(F, z), matvec(G, y))]  # @line L6
        if H is not None and u is not None:
            out = [a + b for a, b in zip(out, matvec(H, u))]
        return out
    return f


def observer_step(F, G, H, z, u, y):
    """Return the discrete-time update F z + G y + H u."""
    return observer_rhs(F, G, H)(0, z, (u, y))


def estimate(L, Tinv, z, y):
    """Return x_hat = T^(-1) [y; z + L y]."""
    w = [a + b for a, b in zip(z, matvec(L, y))]
    return matvec(Tinv, list(y) + w)  # @line L7
