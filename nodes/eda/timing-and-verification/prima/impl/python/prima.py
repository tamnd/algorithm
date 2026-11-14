# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prima/. The authors are listed in prov/KQ4G00.jsonl.

import math
from typing import NamedTuple, Sequence


class ReducedModel(NamedTuple):
    G: list  # k x k, X^T G X
    C: list  # k x k, X^T C X
    B: list  # k x p, X^T B
    L: list  # k x r, X^T L
    X: list  # the k orthonormal basis vectors (each of length n)


def lu_factor(A: Sequence[Sequence]) -> tuple:
    """LU factorization with partial pivoting. Works for float and complex entries."""
    n = len(A)
    M = [list(row) for row in A]
    perm = list(range(n))
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            raise ValueError("singular matrix")
        M[c], M[p] = M[p], M[c]
        perm[c], perm[p] = perm[p], perm[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r][c] = f
            if f != 0:
                for k in range(c + 1, n):
                    M[r][k] -= f * M[c][k]
    return M, perm


def lu_solve(factor: tuple, rhs: Sequence) -> list:
    M, perm = factor
    n = len(M)
    y = [rhs[perm[i]] for i in range(n)]
    for i in range(n):
        for k in range(i):
            y[i] -= M[i][k] * y[k]
    for i in range(n - 1, -1, -1):
        for k in range(i + 1, n):
            y[i] -= M[i][k] * y[k]
        y[i] /= M[i][i]
    return y


def dot(u: Sequence, v: Sequence) -> float:
    return sum(a * b for a, b in zip(u, v))


def matvec(A: Sequence[Sequence], x: Sequence) -> list:
    return [dot(row, x) for row in A]


def columns(B: Sequence[Sequence]) -> list:
    return [[row[j] for row in B] for j in range(len(B[0]))]


def project_out(v: list, block: list) -> list:
    """v minus its components along the orthonormal vectors of block, one at a time."""
    for x in block:
        h = dot(x, v)
        v = [a - h * b for a, b in zip(v, x)]
    return v


def orthonormalize(vectors: list, basis: list, scales=None, tol: float = 1e-10) -> list:
    """Modified Gram-Schmidt of vectors against basis and against each other.

    Each vector is orthogonalized twice. A vector whose norm falls below tol
    times its scale (by default its own norm) is dropped (deflation).
    Returns the new unit vectors.
    """
    out = []
    for i, v in enumerate(vectors):
        v = [float(x) for x in v]
        first = math.sqrt(dot(v, v)) if scales is None else scales[i]
        if first == 0.0:
            continue
        for _ in range(2):
            for x in basis + out:
                h = dot(x, v)
                v = [a - h * b for a, b in zip(v, x)]
        norm = math.sqrt(dot(v, v))
        if norm > tol * first:
            out.append([a / norm for a in v])
    return out


def prima(G, C, B, L, q: int) -> ReducedModel:
    """PRIMA: congruence projection of (G + sC) x = B u, y = L^T x onto the block Krylov
    subspace span{R, AR, ..., A^(q-1) R}, with A = -G^{-1} C and R = G^{-1} B.

    G, C are n x n, B is n x p and L is n x r (lists of rows). With L = B,
    G + G^T positive semidefinite and C symmetric positive semidefinite, the
    reduced model is passive.
    """
    if q < 1:
        raise ValueError("q must be at least 1")
    factor = lu_factor([[float(x) for x in row] for row in G])
    R = [lu_solve(factor, [float(x) for x in b]) for b in columns(B)]  # @line L1
    blocks = [orthonormalize(R, [])]  # @line L2
    basis = list(blocks[0])
    for _ in range(1, q):  # @line L3
        if not blocks[-1]:
            break  # the Krylov subspace is invariant: nothing new to add
        V = [lu_solve(factor, [-x for x in matvec(C, v)]) for v in blocks[-1]]  # @line L4
        scales = [math.sqrt(dot(v, v)) for v in V]
        for Xj in blocks:
            V = [project_out(v, Xj) for v in V]  # @line L5
        new = orthonormalize(V, basis, scales)  # @line L6
        blocks.append(new)
        basis.extend(new)
    X = basis  # @line L7
    GX = [matvec(G, x) for x in X]
    CX = [matvec(C, x) for x in X]
    Gr = [[dot(X[i], GX[j]) for j in range(len(X))] for i in range(len(X))]  # @line L8
    Cr = [[dot(X[i], CX[j]) for j in range(len(X))] for i in range(len(X))]
    Br = [[dot(x, b) for b in columns(B)] for x in X]
    Lr = [[dot(x, c) for c in columns(L)] for x in X]
    return ReducedModel(Gr, Cr, Br, Lr, X)  # @line L9


def transfer(G, C, B, L, s: complex) -> list:
    """H(s) = L^T (G + sC)^{-1} B, an r x p complex matrix."""
    n = len(G)
    factor = lu_factor([[G[i][j] + s * C[i][j] for j in range(n)] for i in range(n)])
    X = [lu_solve(factor, [complex(x) for x in b]) for b in columns(B)]
    return [[dot(l, x) for x in X] for l in columns(L)]


def block_moments(G, C, B, L, count: int) -> list:
    """M_k = L^T (-G^{-1} C)^k G^{-1} B for k = 0 .. count-1, in floating point."""
    factor = lu_factor([[float(x) for x in row] for row in G])
    X = [lu_solve(factor, [float(x) for x in b]) for b in columns(B)]
    out = []
    for _ in range(count):
        out.append([[dot(l, x) for x in X] for l in columns(L)])
        X = [lu_solve(factor, [-x for x in matvec(C, v)]) for v in X]
    return out


def polyval(c: Sequence, s):
    v = 0
    for x in reversed(c):
        v = v * s + x
    return v


def durand_kerner(c: Sequence, iterations: int = 4000) -> list:
    """All complex roots of the polynomial with coefficients c (c[k] of s^k)."""
    c = [complex(x) for x in c]
    while c and c[-1] == 0:
        c.pop()
    deg = len(c) - 1
    if deg < 1:
        return []
    monic = [x / c[-1] for x in c]
    radius = 1.0 + max(abs(x) for x in monic[:-1])
    z = [radius * (0.4 + 0.9j) ** k for k in range(deg)]
    for _ in range(iterations):
        change = 0.0
        for i in range(deg):
            den = 1.0
            for j in range(deg):
                if j != i:
                    den *= z[i] - z[j]
            step = polyval(monic, z[i]) / den
            z[i] -= step
            change = max(change, abs(step))
        if change <= 1e-15 * radius:
            break
    return z


def poles(Gr, Cr) -> list:
    """The finite poles of (Gr + s Cr)^{-1}: s = -1/mu for the non-zero eigenvalues mu of Gr^{-1} Cr.

    The characteristic polynomial comes from the Faddeev-LeVerrier recurrence
    and its roots from Durand-Kerner, so this is meant for small orders only.
    """
    k = len(Gr)
    factor = lu_factor(Gr)
    cols = [lu_solve(factor, c) for c in columns(Cr)]
    M = [[cols[j][i] for j in range(k)] for i in range(k)]
    coeffs = [0.0] * (k + 1)  # det(mu I - M) = sum coeffs[i] mu^i
    coeffs[k] = 1.0
    N = [[float(i == j) for j in range(k)] for i in range(k)]
    for m in range(1, k + 1):
        MN = [[dot(M[i], [N[r][j] for r in range(k)]) for j in range(k)] for i in range(k)]
        c = -sum(MN[i][i] for i in range(k)) / m
        coeffs[k - m] = c
        N = [[MN[i][j] + (c if i == j else 0.0) for j in range(k)] for i in range(k)]
    scale = max(abs(x) for x in coeffs)
    mus = durand_kerner(coeffs)
    out = []
    for mu in mus:
        if abs(mu) <= 1e-12 * scale:
            continue
        s = -1.0 / mu
        # Newton polishing on det(Gr + s Cr): d/ds log det = trace((Gr + s Cr)^{-1} Cr).
        for _ in range(3):
            try:
                f = lu_factor([[Gr[i][j] + s * Cr[i][j] for j in range(k)] for i in range(k)])
            except ValueError:
                break  # s is an exact pole
            t = sum(lu_solve(f, [complex(x) for x in c])[i] for i, c in enumerate(columns(Cr)))
            if t == 0:
                break
            s -= 1.0 / t
        out.append(s)
    return out
