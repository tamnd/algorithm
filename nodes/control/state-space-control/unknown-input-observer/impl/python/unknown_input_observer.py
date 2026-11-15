# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unknown-input-observer/. The authors are listed in prov/A7P4SP.jsonl.

"""Full-order unknown input observer (Darouach, Zasadzinski and Xu, 1994).

System: x' = A x + B u + E d, y = C x, with u known and d unknown. E is n by
q with full column rank q. The observer

    z' = F z + G u + K y,   x_hat = z + H y,

has the error e = x - x_hat with e' = F e for every d, if

    H = E (C E)^+,  T = I - H C,  G = T B,  F = T A - K1 C,  K = K1 + F H.

This needs rank(C E) = rank(E) (so that H C E = E and T E = 0). K1 places
the eigenvalues of F as for a Luenberger observer of the pair (C, T A). The
eigenvalues of T A that no K1 can move are the invariant zeros of (A, E, C);
all must be stable for the error to converge (strong detectability). This
module places all eigenvalues, so it needs (C, T A) observable, that is,
no invariant zeros at all.

The same formulas hold in discrete time. Exact (Fraction) for int and
Fraction data.
"""

from fractions import Fraction

from ctlmat import add, eye, inv, matvec, mul, solve, sub, transpose

__all__ = ["place", "uio_matrices", "unknown_input_observer", "observer_rhs", "observer_step", "estimate"]


def _rank(vectors, tol):
    rows = [list(v) for v in vectors]
    if not rows or not rows[0]:
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
    """Return K with det(s I - (A - B K)) = p(s); Heymann's lemma, then Ackermann."""
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
    k1 = _ackermann(add(A, mul(B, F)), cols[lead], p)
    return [[-F[j][k] + (k1[k] if j == lead else 0) for k in range(n)] for j in range(m)]


def uio_matrices(A, B, C, E, tol=1e-10):
    """Return (H, T, A1, G) with H C E = E, T = I - H C, A1 = T A, G = T B.

    Raises ValueError if E does not have full column rank or if
    rank(C E) < rank(E).
    """
    n, q = len(A), len(E[0])
    if _rank(transpose(E), tol) != q:
        raise ValueError("E must have full column rank")
    CE = mul(C, E)
    if _rank(transpose(CE), tol) != q:  # @line L1
        raise ValueError("rank(C E) < rank(E): no unknown input observer exists")
    CEt = transpose(CE)
    H = mul(E, mul(inv(mul(CEt, CE)), CEt))  # @line L2
    T = sub(eye(n), mul(H, C))  # @line L3
    A1 = mul(T, A)
    G = mul(T, B) if B is not None else None
    return H, T, A1, G


def unknown_input_observer(A, B, C, E, alpha, tol=1e-10):
    """Return (F, G, K, H) with det(s I - F) = alpha(s).

    Raises ValueError if the rank condition fails or if (C, T A) is not
    observable (then (A, E, C) has invariant zeros, which stay eigenvalues
    of F for every gain).
    """
    H, T, A1, G = uio_matrices(A, B, C, E, tol)
    try:
        K1 = transpose(place(transpose(A1), transpose(C), alpha, tol))  # @line L4
    except ValueError:
        raise ValueError("(C, T A) is not observable: (A, E, C) has invariant zeros") from None
    F = sub(A1, mul(K1, C))  # @line L5
    K = add(K1, mul(F, H))
    return F, G, K, H  # @line L6


def observer_rhs(F, G, K):
    """Return f(t, z, (u, y)) = F z + G u + K y."""
    def f(t, z, uy):
        u, y = uy
        out = [a + b for a, b in zip(matvec(F, z), matvec(K, y))]  # @line L7
        if G is not None and u is not None:
            out = [a + b for a, b in zip(out, matvec(G, u))]
        return out
    return f


def observer_step(F, G, K, z, u, y):
    """Return the discrete-time update F z + G u + K y."""
    return observer_rhs(F, G, K)(0, z, (u, y))


def estimate(H, z, y):
    """Return x_hat = z + H y."""
    return [a + b for a, b in zip(z, matvec(H, y))]  # @line L8
