# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-pole-placement/. The authors are listed in prov/PCC8GC.jsonl.

"""Robust pole placement by the Kautsky-Nichols-Van Dooren method 0.

Given x' = A x + B u with m inputs (rank B = m) and n wanted closed-loop
eigenvalues, find K with u = -K x so that A - B K has these eigenvalues and
a well conditioned matrix X of eigenvectors.

Steps:
- QR of B: B = U0 Z with [U0, U1] orthogonal and Z invertible.
- For each eigenvalue lambda_j, S_j is an orthonormal basis of the null
  space of U1^T (A - lambda_j I). Every eigenvector of A - B K for lambda_j
  lies in range S_j, and every vector of range S_j is such an eigenvector
  for a suitable K.
- Method 0: sweep over j. Replace x_j by the normalized projection onto
  range S_j of a unit vector y_j orthogonal to all other columns of X. For
  real eigenvalues each such step does not decrease |det X| when the
  columns have unit length.
- K = Z^(-1) U0^T (A - X Lambda X^(-1)).

This implementation needs distinct eigenvalues, closed under complex
conjugation. For a complex pair it updates the member with positive
imaginary part and sets the other column to its conjugate, so K is real.
It is a plain version of method 0 for teaching; it is not the full KNV
algorithm with repeated eigenvalues and the real treatment of complex
pairs. Computation is in floating point (complex where needed).
"""

import random

from ctlmat import inv, mul, norm2, solve, transpose

__all__ = ["input_qr", "eigvec_subspace", "knv0", "eigvec_condition", "eigenvectors"]


def _cdot(x, y):
    """Return x^H y."""
    return sum(complex(a).conjugate() * b for a, b in zip(x, y))


def _cnorm(x):
    return sum(abs(v) ** 2 for v in x) ** 0.5


def _orthonormal_extend(vectors, n, total):
    """Gram-Schmidt the given vectors, then add unit vectors up to `total`.

    Returns (Q, R): Q is the orthonormal basis of the span of `vectors`
    (vectors with a tiny residual are dropped), R are the added vectors
    (orthonormal and orthogonal to Q). Two passes of orthogonalization keep
    the result orthonormal to rounding error.
    """
    basis = []

    def residual(v):
        r = [complex(a) for a in v]
        for _ in range(2):
            for q in basis:
                c = _cdot(q, r)
                r = [a - c * b for a, b in zip(r, q)]
        return r

    scale = max([_cnorm(v) for v in vectors] + [1.0])
    for v in vectors:
        r = residual(v)
        nr = _cnorm(r)
        if nr > 1e-10 * scale:
            basis.append([a / nr for a in r])
    q_count = len(basis)
    while len(basis) < total:
        best, best_norm = None, -1.0
        for i in range(n):
            e = [0.0] * n
            e[i] = 1.0
            r = residual(e)
            nr = _cnorm(r)
            if nr > best_norm:
                best, best_norm = r, nr
        basis.append([a / best_norm for a in best])
    return basis[:q_count], basis[q_count:]


def _real_if_close(vectors):
    out = []
    for v in vectors:
        if all(abs(complex(a).imag) <= 1e-14 for a in v):
            out.append([complex(a).real for a in v])
        else:
            out.append(v)
    return out


def input_qr(B):
    """Return (U0, U1, Z) with B = U0 Z, [U0, U1] orthogonal, Z m by m.

    U0 and U1 are lists of columns (each a flat list). Raises ValueError if
    B does not have full column rank.
    """
    n = len(B)
    m = len(B[0])
    cols = [[float(B[i][j]) for i in range(n)] for j in range(m)]
    q, rest = _orthonormal_extend(cols, n, n)
    if len(q) != m:
        raise ValueError("B must have full column rank")
    U0 = _real_if_close(q)
    U1 = _real_if_close(rest)
    Z = [[sum(U0[i][k] * cols[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
    return U0, U1, Z


def eigvec_subspace(A, U1, lam):
    """Return an orthonormal basis (list of columns) of null(U1^T (A - lam I))."""
    n = len(A)
    rows = []
    for u in U1:
        row = [sum(u[k] * (A[k][j] - (lam if k == j else 0)) for k in range(n)) for j in range(n)]
        rows.append(row)
    conj_rows = [[complex(v).conjugate() for v in r] for r in rows]
    q, null = _orthonormal_extend(conj_rows, n, n)
    return null


def _orth_to_others(X, j, n):
    others = [X[i] for i in range(len(X)) if i != j]
    _, rest = _orthonormal_extend(others, n, len(others) + 1)
    return rest[0]


def _project(S, y):
    coeffs = [_cdot(s, y) for s in S]
    x = [sum(c * s[i] for c, s in zip(coeffs, S)) for i in range(len(y))]
    return x


def eigvec_condition(X):
    """Return the 2-norm condition number of the matrix with columns X."""
    M = transpose(X)
    return norm2(M) * norm2(inv(M))


def _pairs(poles):
    """Return the indices of the poles to update and the partner index of each."""
    n = len(poles)
    used = [False] * n
    leaders = []
    partner = [None] * n
    for i, p in enumerate(poles):
        if used[i]:
            continue
        p = complex(p)
        if abs(p.imag) <= 1e-14 * (1 + abs(p)):
            used[i] = True
            leaders.append(i)
            continue
        best = None
        for j in range(n):
            if not used[j] and j != i and abs(complex(poles[j]) - p.conjugate()) <= 1e-12 * (1 + abs(p)):
                best = j
                break
        if best is None:
            raise ValueError("complex poles must come in conjugate pairs")
        used[i] = used[best] = True
        lead, other = (i, best) if p.imag > 0 else (best, i)
        leaders.append(lead)
        partner[lead] = other
    return leaders, partner


def knv0(A, B, poles, sweeps=50, seed=0):
    """Return (K, X, cond): the gain, the eigenvector columns and cond_2(X).

    A is n by n, B is n by m with rank m, and poles is a list of n distinct
    numbers closed under conjugation. Raises ValueError if the poles are
    not distinct, if a complex pole has no partner, or if no independent
    eigenvectors are found (then (A, B) is not controllable at some pole).
    """
    n = len(A)
    if len(poles) != n:
        raise ValueError("give exactly n poles")
    for i in range(n):
        for j in range(i + 1, n):
            if abs(complex(poles[i]) - complex(poles[j])) <= 1e-12 * (1 + abs(complex(poles[i]))):
                raise ValueError("this implementation needs distinct poles")
    leaders, partner = _pairs(poles)
    lam = [complex(p) if abs(complex(p).imag) > 0 else float(complex(p).real) for p in poles]
    U0, U1, Z = input_qr(B)  # @line L1
    S = [eigvec_subspace(A, U1, l) for l in lam]  # @line L2
    rng = random.Random(seed)
    X = [None] * n
    for j in leaders:  # @line L3
        y = [rng.uniform(-1, 1) for _ in range(n)]
        x = _project(S[j], y)
        nx = _cnorm(x)
        X[j] = [v / nx for v in x]
        if partner[j] is not None:
            X[partner[j]] = [complex(v).conjugate() for v in X[j]]
    best, best_X = eigvec_condition(X), [list(c) for c in X]
    for _ in range(sweeps):  # @line L4
        for j in leaders:
            y = _orth_to_others(X, j, n)  # @line L5
            x = _project(S[j], y)  # @line L6
            nx = _cnorm(x)
            if nx < 1e-12:
                continue
            X[j] = [v / nx for v in x]
            if partner[j] is not None:
                X[partner[j]] = [complex(v).conjugate() for v in X[j]]
        c = eigvec_condition(X)
        if c >= best * (1 - 1e-9):
            if c < best:
                best, best_X = c, [list(col) for col in X]
            break
        best, best_X = c, [list(col) for col in X]
    X, cond = best_X, best
    if cond > 1e12:
        raise ValueError("no independent eigenvectors found; (A, B) may be uncontrollable")
    Xm = transpose(X)
    XL = [[Xm[i][j] * lam[j] for j in range(n)] for i in range(n)]
    # M = X Lambda X^(-1), computed as the solution of X^T M^T = (X Lambda)^T.
    M = transpose(solve(transpose(Xm), transpose(XL)))  # @line L7
    D = [[A[i][j] - M[i][j] for j in range(n)] for i in range(n)]
    # U0, a list of columns, read as a list of rows is the matrix U0^T.
    Kc = solve(Z, mul(U0, D))  # @line L8
    big = max(1.0, max(abs(v) for row in Kc for v in row))
    if any(abs(complex(v).imag) > 1e-8 * big for row in Kc for v in row):
        raise ValueError("the gain is not real; check the conjugate pairs")
    K = [[complex(v).real for v in row] for row in Kc]
    return K, X, cond


def eigenvectors(Acl, poles, iters=3):
    """Return unit eigenvectors (columns) of Acl for the given simple poles.

    Uses inverse iteration with a small shift. For use on a closed loop from
    any method, so that conditions can be compared.
    """
    n = len(Acl)
    rng = random.Random(1)
    cols = []
    for lam in poles:
        lam = complex(lam)
        shift = lam + 1e-9 * (1 + abs(lam))
        M = [[complex(Acl[i][j]) - (shift if i == j else 0) for j in range(n)] for i in range(n)]
        x = [complex(rng.uniform(-1, 1)) for _ in range(n)]
        for _ in range(iters):
            x = solve(M, x)
            nx = _cnorm(x)
            x = [v / nx for v in x]
        cols.append(x)
    return cols
