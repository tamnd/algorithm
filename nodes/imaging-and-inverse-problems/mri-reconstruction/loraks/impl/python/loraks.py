# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loraks/. The authors are listed in prov/HJ4N14.jsonl.

"""LORAKS: low-rank modeling of local k-space neighborhoods (Haldar 2014).

k-space convention: a grid kspace[a][b] of n1 rows and n2 columns of complex
samples, in centered order (row a holds the signed frequency a - n1 // 2, and
the same for the columns). A 1D line is a grid with n1 = 1. A neighborhood
is a list of integer offsets (da, db). The C matrix P(k) has one row for each
center (a, b) whose whole neighborhood lies inside the grid, and one column
for each offset: P(k)[row, j] = k[a + da_j][b + db_j]. P^H scatters a matrix
back onto the grid and adds the entries that fall on the same point, so
P^H P is the diagonal of the counts D (how many rows hold each point).

The method fits k-space so that P(k) is close to rank r and the samples
agree with the data. It minimizes, by majorize-minimize,

    J(k) = ||M k - d||^2 + lambda * sum_{j > r} sigma_j(P(k))^2,

with the 0/1 sampling mask M. With lambda = None the data are kept exactly
and J(k) is the tail sum alone.

Complex SVD: imgla.svd is for real matrices, so the best rank r
approximation C P_r uses the real symmetric embedding of the Gram matrix
C^H C and imgla.sym_eig (see low_rank_projector). This small piece of code
lives here and not in a helper.

Cost per iteration, for N rows and w offsets: O(N w^2) for the Gram matrix,
O(w^3) per Jacobi sweep of the 2w x 2w embedding, O(N w^2) for C P_r and
O(N w) for the scatter and the update.
"""

import math

from imgla import sym_eig


def line_offsets(radius):
    """The 1D neighborhood (0, -radius), ..., (0, radius)."""
    return [(0, d) for d in range(-radius, radius + 1)]


def disk_offsets(radius):
    """The 2D LORAKS neighborhood: all integer offsets with da^2 + db^2 <= radius^2."""
    top = int(math.floor(radius))
    return [
        (da, db)
        for da in range(-top, top + 1)
        for db in range(-top, top + 1)
        if da * da + db * db <= radius * radius
    ]


def centers(n1, n2, offsets):
    """The centers (a, b) whose whole neighborhood lies inside the n1 x n2 grid."""
    amin = min(da for da, _ in offsets)
    amax = max(da for da, _ in offsets)
    bmin = min(db for _, db in offsets)
    bmax = max(db for _, db in offsets)
    return [(a, b) for a in range(-amin, n1 - amax) for b in range(-bmin, n2 - bmax)]


def c_matrix(kspace, offsets):
    """P(k): one row per center, one column per offset."""
    n1, n2 = len(kspace), len(kspace[0])
    return [[kspace[a + da][b + db] for da, db in offsets] for a, b in centers(n1, n2, offsets)]


def c_adjoint(mat, n1, n2, offsets):
    """P^H(L): add each entry of L back onto its grid point."""
    out = [[0j] * n2 for _ in range(n1)]
    for (a, b), row in zip(centers(n1, n2, offsets), mat):
        for (da, db), v in zip(offsets, row):
            out[a + da][b + db] += v
    return out


def coverage(n1, n2, offsets):
    """D = P^H P as a grid: the number of rows of P(k) that hold each point."""
    out = [[0] * n2 for _ in range(n1)]
    for a, b in centers(n1, n2, offsets):
        for da, db in offsets:
            out[a + da][b + db] += 1
    return out


def gram(c):
    """G = C^H C."""
    w = len(c[0])
    g = [[0j] * w for _ in range(w)]
    for row in c:
        for i in range(w):
            ci = row[i].conjugate()
            if ci == 0:
                continue
            gi = g[i]
            for j in range(w):
                gi[j] += ci * row[j]
    return g


def low_rank_projector(c, r):
    """The orthogonal projector P_r onto the top r right singular vectors of C.

    Returns (P_r, s2) with s2 the squared singular values of C in descending
    order. The Hermitian Gram matrix G = C^H C is embedded as the real
    symmetric matrix [[Re G, -Im G], [Im G, Re G]]; each eigenvalue of G
    appears twice there, and the sum of q q^T over the top 2 r eigenvectors
    is the embedding of P_r.
    """
    g = gram(c)
    w = len(g)
    emb = [[0.0] * (2 * w) for _ in range(2 * w)]
    for i in range(w):
        for j in range(w):
            re, im = g[i][j].real, g[i][j].imag
            emb[i][j] = re
            emb[i + w][j + w] = re
            emb[i][j + w] = -im
            emb[i + w][j] = im
    vals, vecs = sym_eig(emb)
    top = list(range(2 * w - 1, 2 * w - 1 - 2 * r, -1))
    proj = [[0j] * w for _ in range(w)]
    for i in range(w):
        for j in range(w):
            re = sum(vecs[i][t] * vecs[j][t] for t in top)
            im = sum(vecs[i + w][t] * vecs[j][t] for t in top)
            proj[i][j] = complex(re, im)
    desc = sorted((max(v, 0.0) for v in vals), reverse=True)
    s2 = [desc[2 * t] for t in range(w)]
    return proj, s2


def rank_r_approx(c, r):
    """(L, tail): L = C P_r is the best rank r approximation of C in the
    Frobenius norm, and tail = ||C - L||_F^2 = sum_{j > r} sigma_j^2."""
    proj, s2 = low_rank_projector(c, r)
    w = len(proj)
    low = [[sum(row[k] * proj[k][j] for k in range(w)) for j in range(w)] for row in c]
    total = sum(abs(v) ** 2 for row in c for v in row)
    tail = max(total - sum(s2[:r]), 0.0)
    return low, tail


def objective(kspace, data, mask, offsets, r, lam=None):
    """J(k) = ||M k - d||^2 + lambda * tail, or the tail alone for lambda = None."""
    _, tail = rank_r_approx(c_matrix(kspace, offsets), r)
    if lam is None:
        return tail
    fit = sum(
        abs(kv - dv) ** 2
        for krow, drow, mrow in zip(kspace, data, mask)
        for kv, dv, mv in zip(krow, drow, mrow)
        if mv
    )
    return fit + lam * tail


def loraks(data, mask, offsets, r, lam=None, iters=100, history=None):
    """Recover a k-space grid from the samples data[a][b] where mask[a][b] is 1.

    lam = None keeps the samples exactly. Otherwise lam > 0 weighs the rank
    penalty against the data term. If history is a list, J of each iterate
    k_0, ..., k_{iters - 1} is appended to it.
    """
    n1, n2 = len(data), len(data[0])
    cnt = coverage(n1, n2, offsets)
    k = [[complex(data[a][b]) if mask[a][b] else 0j for b in range(n2)] for a in range(n1)]  # @line L1
    for _ in range(iters):  # @line L2
        c = c_matrix(k, offsets)  # @line L3
        low, tail = rank_r_approx(c, r)  # @line L4
        if history is not None:
            if lam is None:
                history.append(tail)
            else:
                fit = sum(
                    abs(k[a][b] - data[a][b]) ** 2
                    for a in range(n1)
                    for b in range(n2)
                    if mask[a][b]
                )
                history.append(fit + lam * tail)
        z = c_adjoint(low, n1, n2, offsets)  # @line L5
        for a in range(n1):  # @line L6
            for b in range(n2):
                if lam is None:  # @line L7
                    if mask[a][b]:
                        k[a][b] = complex(data[a][b])
                    elif cnt[a][b] > 0:
                        k[a][b] = z[a][b] / cnt[a][b]
                    else:
                        k[a][b] = 0j
                else:  # @line L8
                    num = (data[a][b] if mask[a][b] else 0.0) + lam * z[a][b]
                    den = (1.0 if mask[a][b] else 0.0) + lam * cnt[a][b]
                    k[a][b] = num / den if den > 0 else 0j
    return k  # @line L9
