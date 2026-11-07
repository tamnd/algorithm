# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-wiedemann-algorithm/. The authors are listed in prov/0EQBTW.jsonl.

import random
from typing import Sequence

SparseRows = Sequence[Sequence[tuple[int, int]]]  # row i is a list of (column, value)
Block = list[list[int]]  # n x s, stored by rows


def apply_block(rows: SparseRows, v: Block, p: int) -> Block:
    """A V modulo p for a sparse A and a dense n x s block V: s * nnz(A) multiplications."""
    s = len(v[0]) if v else 0
    return [[sum(a * v[j][c] for j, a in r) % p for c in range(s)] for r in rows]


def apply_vector(rows: SparseRows, u: Sequence[int], p: int) -> list[int]:
    """A u modulo p."""
    return [sum(a * u[j] for j, a in r) % p for r in rows]


def minimal_generator(seq: Sequence[Block], s: int, p: int) -> list[tuple[int, list[list[int]]]]:
    """Right generators of a sequence of s x s matrices S_0, ..., S_{L-1} over F_p.

    Returns pairs (d, f) with f = [f_0, ..., f_d], vectors of length s, such that
    sum_j S_{i+j} f_j = 0 for 0 <= i < L - d, sorted by d. Computed as an order-L
    approximant basis of the 2s x s matrix [S(x)^T; -I] by the iterative M-Basis method,
    with the degree shift (0, ..., 0, 1, ..., 1): O(s^3 L^2) operations modulo p.
    """
    big_l = len(seq)
    m = 2 * s
    g = []
    for k in range(big_l):
        top = [[seq[k][c][i] % p for c in range(s)] for i in range(s)]
        bot = [[(p - 1) if (i == c and k == 0) else 0 for c in range(s)] for i in range(s)]
        g.append(top + bot)
    poly = [[[int(i == j)] for j in range(m)] for i in range(m)]  # poly[i][j]: coefficients of P_ij
    delta = [0] * s + [1] * s
    for k in range(big_l):
        disc = []  # coefficient of x^k in P G
        for i in range(m):
            acc = [0] * s
            for j in range(m):
                for t, cf in enumerate(poly[i][j]):
                    if cf and t <= k:
                        gr = g[k - t][j]
                        for c in range(s):
                            acc[c] += cf * gr[c]
            disc.append([x % p for x in acc])
        pivots: list[tuple[int, int]] = []
        for i in sorted(range(m), key=lambda r: delta[r]):
            for j, c in pivots:
                if disc[i][c]:
                    f = disc[i][c] * pow(disc[j][c], -1, p) % p
                    disc[i] = [(x - f * y) % p for x, y in zip(disc[i], disc[j])]
                    for q in range(m):
                        a, b = poly[i][q], poly[j][q]
                        a = a + [0] * (len(b) - len(a))
                        poly[i][q] = [(a[t] - f * (b[t] if t < len(b) else 0)) % p for t in range(len(a))]
            c = next((c for c in range(s) if disc[i][c]), None)
            if c is not None:
                pivots.append((i, c))
        for i, _ in pivots:
            poly[i] = [[0] + pol for pol in poly[i]]
            delta[i] += 1
    out = []
    for i in sorted(range(m), key=lambda r: delta[r]):
        a = poly[i][:s]
        if not any(any(pol) for pol in a):
            continue
        d = delta[i]
        f = [[a[c][d - j] if d - j < len(a[c]) else 0 for c in range(s)] for j in range(d + 1)]
        out.append((d, f))
    return out


def block_wiedemann_kernel(rows: SparseRows, n: int, p: int, s: int = 4,
                           seed: int = 0, tries: int = 10) -> list[int] | None:
    """A nonzero u with A u = 0 over F_p for a sparse n x n matrix A, or None.

    Las Vegas: a returned vector is always checked, and None means that no kernel vector
    was found in the given number of tries (always the case for a nonsingular A).
    Cost per try: about 3n/s products of A with an n x s block, 2 n^2 s operations for the
    projections, and O(s n^2) for the generator, all modulo p.
    """
    rng = random.Random(seed)
    for _ in range(tries):
        if n == 0:
            return None
        x = [[rng.randrange(p) for _ in range(s)] for _ in range(n)]  # @line L1
        z = [[rng.randrange(p) for _ in range(s)] for _ in range(n)]
        v = apply_block(rows, z, p)
        big_l = 2 * (-(-n // s)) + 4  # @line L2
        seq = []
        for _ in range(big_l):  # @line L3
            seq.append([[sum(x[r][a] * v[r][c] for r in range(n)) % p for c in range(s)] for a in range(s)])  # @line L4
            v = apply_block(rows, v, p)
        gens = minimal_generator(seq, s, p)  # @line L5
        for d, f in gens:  # @line L6
            if d > big_l - (-(-n // s)):
                break
            e = next(j for j in range(d + 1) if any(f[j]))  # @line L7
            u = [0] * n
            w = z
            for j in range(e, d + 1):
                for r in range(n):
                    u[r] = (u[r] + sum(w[r][c] * f[j][c] for c in range(s))) % p
                if j < d:
                    w = apply_block(rows, w, p)
            for _ in range(e + 2):  # @line L8
                if not any(u):
                    break
                au = apply_vector(rows, u, p)
                if not any(au):  # @line L9
                    return u
                u = au  # @line L10
    return None  # @line L11
