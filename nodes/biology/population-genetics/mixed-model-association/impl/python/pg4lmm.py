# SPDX-License-Identifier: MIT
# Group module of the pg4 pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Dense linear algebra and genotype simulation for the mixed model pages.

This module holds no method of a page. It has the matrix routines that the
pages mixed-model-association and snp-heritability-estimation both use
(Cholesky factor, solves, a symmetric eigendecomposition), the genomic
relationship matrix of GCTA, and a simulator of genotypes from two
populations. Matrices are lists of rows of floats.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

Matrix = List[List[float]]


# Small helpers

def dot(a: Sequence[float], b: Sequence[float]) -> float:
    s = 0.0
    for x, y in zip(a, b):
        s += x * y
    return s


def matvec(A: Matrix, x: Sequence[float]) -> List[float]:
    return [dot(row, x) for row in A]


def tmatvec(A: Matrix, x: Sequence[float]) -> List[float]:
    """A^T x."""
    out = [0.0] * len(A[0])
    for row, xi in zip(A, x):
        if xi != 0.0:
            for j, a in enumerate(row):
                out[j] += a * xi
    return out


def transpose(A: Matrix) -> Matrix:
    return [list(col) for col in zip(*A)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    Bt = transpose(B)
    return [[dot(row, col) for col in Bt] for row in A]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


# Cholesky factor and solves

def cholesky(A: Matrix) -> Matrix:
    """Lower triangular L with L L^T = A, for a symmetric positive definite A."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        Li = L[i]
        for j in range(i + 1):
            Lj = L[j]
            s = A[i][j]
            for k in range(j):
                s -= Li[k] * Lj[k]
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                Li[i] = math.sqrt(s)
            else:
                Li[j] = s / Lj[j]
    return L


def chol_solve(L: Matrix, b: Sequence[float]) -> List[float]:
    """Solve (L L^T) x = b."""
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        s = b[i]
        Li = L[i]
        for k in range(i):
            s -= Li[k] * y[k]
        y[i] = s / Li[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for k in range(i + 1, n):
            s -= L[k][i] * x[k]
        x[i] = s / L[i][i]
    return x


def chol_logdet(L: Matrix) -> float:
    return 2.0 * sum(math.log(L[i][i]) for i in range(len(L)))


def chol_inverse(L: Matrix) -> Matrix:
    """(L L^T)^-1, column by column."""
    n = len(L)
    cols = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        cols.append(chol_solve(L, e))
    return transpose(cols)


def solve_small(A: Matrix, b: Sequence[float]) -> List[float]:
    """Solve A x = b by Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0.0:
            raise ValueError("singular matrix")
        M[c], M[piv] = M[piv], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f != 0.0:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = M[r][n]
        for k in range(r + 1, n):
            s -= M[r][k] * x[k]
        x[r] = s / M[r][r]
    return x


def inverse_small(A: Matrix) -> Matrix:
    n = len(A)
    cols = [solve_small(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return transpose(cols)


# Symmetric eigendecomposition: Householder tridiagonalization, then the
# implicit QL method (the tred2 and tql2 routines of EISPACK, as in JAMA).

def eigh(A: Matrix) -> Tuple[List[float], Matrix]:
    """Eigenvalues (ascending) and eigenvectors of a symmetric matrix.

    Returns (d, V): column k of V is a unit eigenvector for d[k], so
    A = V diag(d) V^T.
    """
    n = len(A)
    V = [list(map(float, row)) for row in A]
    d = [0.0] * n
    e = [0.0] * n
    if n == 1:
        return [V[0][0]], [[1.0]]
    # tred2
    for j in range(n):
        d[j] = V[n - 1][j]
    for i in range(n - 1, 0, -1):
        scale = 0.0
        h = 0.0
        for k in range(i):
            scale += abs(d[k])
        if scale == 0.0:
            e[i] = d[i - 1]
            for j in range(i):
                d[j] = V[i - 1][j]
                V[i][j] = 0.0
                V[j][i] = 0.0
        else:
            for k in range(i):
                d[k] /= scale
                h += d[k] * d[k]
            f = d[i - 1]
            g = math.sqrt(h)
            if f > 0:
                g = -g
            e[i] = scale * g
            h -= f * g
            d[i - 1] = f - g
            for j in range(i):
                e[j] = 0.0
            for j in range(i):
                f = d[j]
                V[j][i] = f
                g = e[j] + V[j][j] * f
                for k in range(j + 1, i):
                    g += V[k][j] * d[k]
                    e[k] += V[k][j] * f
                e[j] = g
            f = 0.0
            for j in range(i):
                e[j] /= h
                f += e[j] * d[j]
            hh = f / (h + h)
            for j in range(i):
                e[j] -= hh * d[j]
            for j in range(i):
                f = d[j]
                g = e[j]
                for k in range(j, i):
                    V[k][j] -= f * e[k] + g * d[k]
                d[j] = V[i - 1][j]
                V[i][j] = 0.0
        d[i] = h
    for i in range(n - 1):
        V[n - 1][i] = V[i][i]
        V[i][i] = 1.0
        h = d[i + 1]
        if h != 0.0:
            for k in range(i + 1):
                d[k] = V[k][i + 1] / h
            for j in range(i + 1):
                g = 0.0
                for k in range(i + 1):
                    g += V[k][i + 1] * V[k][j]
                for k in range(i + 1):
                    V[k][j] -= g * d[k]
        for k in range(i + 1):
            V[k][i + 1] = 0.0
    for j in range(n):
        d[j] = V[n - 1][j]
        V[n - 1][j] = 0.0
    V[n - 1][n - 1] = 1.0
    e[0] = 0.0
    # tql2
    for i in range(1, n):
        e[i - 1] = e[i]
    e[n - 1] = 0.0
    f = 0.0
    tst1 = 0.0
    eps = 2.0 ** -52
    for l in range(n):
        tst1 = max(tst1, abs(d[l]) + abs(e[l]))
        m = l
        while m < n:
            if abs(e[m]) <= eps * tst1:
                break
            m += 1
        if m == n:
            m = n - 1
        if m > l:
            for _ in range(200):
                g = d[l]
                p = (d[l + 1] - g) / (2.0 * e[l])
                r = math.hypot(p, 1.0)
                if p < 0:
                    r = -r
                d[l] = e[l] / (p + r)
                d[l + 1] = e[l] * (p + r)
                dl1 = d[l + 1]
                h = g - d[l]
                for i in range(l + 2, n):
                    d[i] -= h
                f += h
                p = d[m]
                c = c2 = c3 = 1.0
                el1 = e[l + 1]
                s = s2 = 0.0
                for i in range(m - 1, l - 1, -1):
                    c3 = c2
                    c2 = c
                    s2 = s
                    g = c * e[i]
                    h = c * p
                    r = math.hypot(p, e[i])
                    e[i + 1] = s * r
                    s = e[i] / r
                    c = p / r
                    p = c * d[i] - s * g
                    d[i + 1] = h + s * (c * g + s * d[i])
                    for k in range(n):
                        Vk = V[k]
                        h = Vk[i + 1]
                        Vk[i + 1] = s * Vk[i] + c * h
                        Vk[i] = c * Vk[i] - s * h
                p = -s * s2 * c3 * el1 * e[l] / dl1
                e[l] = s * p
                d[l] = c * p
                if abs(e[l]) <= eps * tst1:
                    break
            else:
                raise ArithmeticError("eigenvalue iteration did not converge")
        d[l] += f
        e[l] = 0.0
    order = sorted(range(n), key=lambda k: d[k])
    d_sorted = [d[k] for k in order]
    V_sorted = [[V[i][k] for k in order] for i in range(n)]
    return d_sorted, V_sorted


# Genotypes

def allele_freqs(G: Sequence[Sequence[int]]) -> List[float]:
    """Sample frequency of the counted allele at each SNP; G is n people by m SNPs."""
    n = len(G)
    m = len(G[0])
    return [sum(G[i][j] for i in range(n)) / (2.0 * n) for j in range(m)]


def standardize(G: Sequence[Sequence[int]], freqs=None) -> Matrix:
    """W[i][j] = (x_ij - 2 p_j) / sqrt(2 p_j (1 - p_j)); monomorphic SNPs give 0."""
    p = freqs or allele_freqs(G)
    sd = [math.sqrt(2.0 * q * (1.0 - q)) for q in p]
    return [[(row[j] - 2.0 * p[j]) / sd[j] if sd[j] > 0 else 0.0 for j in range(len(p))]
            for row in G]


def grm(G: Sequence[Sequence[int]]) -> Matrix:
    """The genomic relationship matrix of GCTA (Yang et al. 2011).

    Off the diagonal, A_jk = (1/m) sum_i (x_ji - 2p_i)(x_ki - 2p_i) / (2p_i(1-p_i)).
    On the diagonal, A_jj = 1 + (1/m) sum_i (x_ji^2 - (1 + 2p_i) x_ji + 2p_i^2) / (2p_i(1-p_i)).
    Here j and k are people and i runs over the m polymorphic SNPs.
    """
    p = allele_freqs(G)
    keep = [i for i, q in enumerate(p) if 0.0 < q < 1.0]
    m = len(keep)
    n = len(G)
    W = [[(G[a][i] - 2.0 * p[i]) / math.sqrt(2.0 * p[i] * (1.0 - p[i])) for i in keep] for a in range(n)]
    A = [[0.0] * n for _ in range(n)]
    for a in range(n):
        Wa = W[a]
        for b in range(a + 1, n):
            v = dot(Wa, W[b]) / m
            A[a][b] = v
            A[b][a] = v
        s = 0.0
        for i in keep:
            x = G[a][i]
            q = p[i]
            s += (x * x - (1.0 + 2.0 * q) * x + 2.0 * q * q) / (2.0 * q * (1.0 - q))
        A[a][a] = 1.0 + s / m
    return A


def simulate_two_populations(rng, n_a: int, n_b: int, m: int, fst: float,
                             pmin: float = 0.1, pmax: float = 0.9):
    """Genotypes of n_a + n_b people from two populations, m unlinked SNPs.

    For each SNP, in order: an ancestral frequency p ~ Uniform(pmin, pmax),
    then a frequency for population A and one for B, each from the
    Balding-Nichols beta law with mean p and variance fst p (1 - p). Then the
    genotypes, person by person, as Binomial(2, frequency) by two
    rng.random() draws each. Returns (G, pop), G as n by m, pop[i] in {0, 1}.
    """
    pops = [0] * n_a + [1] * n_b
    freqs = []
    c = (1.0 - fst) / fst
    for _ in range(m):
        p = pmin + (pmax - pmin) * rng.random()
        fa = rng.betavariate(c * p, c * (1.0 - p))
        fb = rng.betavariate(c * p, c * (1.0 - p))
        freqs.append((fa, fb))
    G = []
    for k in pops:
        row = []
        for j in range(m):
            f = freqs[j][k]
            row.append((rng.random() < f) + (rng.random() < f))
        G.append(row)
    return G, pops
