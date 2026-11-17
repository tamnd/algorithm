# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-crf/. The authors are listed in prov/9CMFRH.jsonl.

"""Mean field inference in a fully connected CRF with Gaussian edge potentials.

Pixel i = v * w + u is (u, v) with the gray value img[v][u]. The energy of a
labeling x is

    E(x) = sum_i U[i][x_i] + sum_{i < j} [x_i != x_j] k(i, j),
    k(i, j) = w1 exp(-|p_i - p_j|^2 / (2 ta^2) - |I_i - I_j|^2 / (2 tb^2))
            + w2 exp(-|p_i - p_j|^2 / (2 tg^2)),

the Potts model with the two kernels of Kraehenbuehl and Koltun (2011). The
messages here are exact sums over all pixel pairs, O(n^2 L) per iteration,
for tiny images. gaussian_messages shows the filtering idea for the spatial
kernel: a separable Gaussian blur minus the self term.
"""

import itertools
import math


def kernel_matrix(img, w1, ta, tb, w2, tg):
    """Return the n x n matrix of k(i, j), with zero diagonal."""
    h, w = len(img), len(img[0])
    pix = [(u, v, img[v][u]) for v in range(h) for u in range(w)]
    n = len(pix)
    k = [[0.0] * n for _ in range(n)]
    for i in range(n):
        ui, vi, ci = pix[i]
        for j in range(i + 1, n):
            uj, vj, cj = pix[j]
            dp = (ui - uj) ** 2 + (vi - vj) ** 2
            dc = (ci - cj) ** 2
            val = w1 * math.exp(-dp / (2 * ta * ta) - dc / (2 * tb * tb)) + w2 * math.exp(-dp / (2 * tg * tg))
            k[i][j] = k[j][i] = val
    return k


def softmax_neg(e):
    """Return the distribution proportional to exp(-e)."""
    m = min(e)
    q = [math.exp(m - x) for x in e]
    s = sum(q)
    return [x / s for x in q]


def dense_crf(unary, kmat, iters, include_self=0.0):
    """Run iters parallel mean field updates and return Q (n lists of L probabilities).

    unary[i][l] is the unary energy and kmat the kernel matrix with zero diagonal.
    include_self adds include_self * Q_i(l) to the message of pixel i, which
    gives the convergent variant of Kraehenbuehl and Koltun (2013, Section 3.2)
    when include_self = k(i, i) = w1 + w2.
    """
    n, nl = len(unary), len(unary[0])
    q = [softmax_neg(unary[i]) for i in range(n)]  # @line L1
    for _ in range(iters):  # @line L2
        msg = [[include_self * q[i][l] for l in range(nl)] for i in range(n)]
        for i in range(n):  # @line L3
            row, mi = kmat[i], msg[i]
            for j in range(n):
                kij = row[j]
                if kij:
                    qj = q[j]
                    for l in range(nl):
                        mi[l] += kij * qj[l]
        new = []
        for i in range(n):
            total = sum(msg[i])
            pen = [total - msg[i][l] for l in range(nl)]  # @line L4
            e = [unary[i][l] + pen[l] for l in range(nl)]  # @line L5
            new.append(softmax_neg(e))  # @line L6
        q = new
    return q  # @line L7


def labels_of(q):
    """Return the label with the largest marginal for each pixel."""
    return [max(range(len(qi)), key=lambda l: qi[l]) for qi in q]


def mean_field_sequential(unary, kmat, sweeps, trace=None):
    """Update one pixel at a time, in index order. If trace is a list, append the free energy after each update."""
    n, nl = len(unary), len(unary[0])
    q = [softmax_neg(unary[i]) for i in range(n)]
    for _ in range(sweeps):
        for i in range(n):
            m = [0.0] * nl
            for j in range(n):
                if kmat[i][j]:
                    for l in range(nl):
                        m[l] += kmat[i][j] * q[j][l]
            total = sum(m)
            q[i] = softmax_neg([unary[i][l] + total - m[l] for l in range(nl)])
            if trace is not None:
                trace.append(free_energy(q, unary, kmat))
    return q


def free_energy(q, unary, kmat):
    """Return F(Q) = E_Q[E] - H(Q). F(Q) >= -log Z, with equality only for the true distribution."""
    n, nl = len(unary), len(unary[0])
    f = 0.0
    for i in range(n):
        for l in range(nl):
            if q[i][l] > 0:
                f += q[i][l] * (unary[i][l] + math.log(q[i][l]))
        for j in range(i + 1, n):
            if kmat[i][j]:
                f += kmat[i][j] * (1.0 - sum(q[i][l] * q[j][l] for l in range(nl)))
    return f


def concave_objective(q, unary, kmat, self_weight):
    """The approximate KL divergence (up to log Z) of Kraehenbuehl and Koltun (2013, eq. 9) for the Potts model.

    The Potts compatibility is written as -[l = l'], which differs from
    [l != l'] by a constant, and the kernel matrix gets the diagonal self_weight.
    """
    n, nl = len(unary), len(unary[0])
    f = 0.0
    for i in range(n):
        for l in range(nl):
            if q[i][l] > 0:
                f += q[i][l] * (unary[i][l] + math.log(q[i][l]))
        for j in range(n):
            kij = self_weight if i == j else kmat[i][j]
            if kij:
                f -= 0.5 * kij * sum(q[i][l] * q[j][l] for l in range(nl))
    return f


def energy(x, unary, kmat):
    n = len(x)
    e = sum(unary[i][x[i]] for i in range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if x[i] != x[j]:
                e += kmat[i][j]
    return e


def log_partition(unary, kmat):
    """Return log Z by summing over all labelings. Only for tiny problems."""
    n, nl = len(unary), len(unary[0])
    es = [-energy(x, unary, kmat) for x in itertools.product(range(nl), repeat=n)]
    m = max(es)
    return m + math.log(sum(math.exp(e - m) for e in es))


def gaussian_messages(q, w, h, theta):
    """Return sum_{j != i} exp(-|p_i - p_j|^2 / (2 theta^2)) Q_j(l) by a separable blur minus the self term.

    The spatial Gaussian factors into a Gaussian in u times a Gaussian in v, so
    a blur along the rows and then along the columns gives the full sum over j.
    The blur is exact here: it uses all pixels, with no truncation.
    """
    nl = len(q[0])
    g = [math.exp(-d * d / (2 * theta * theta)) for d in range(max(w, h))]
    rows = [[[0.0] * nl for _ in range(w)] for _ in range(h)]
    for v in range(h):
        for u in range(w):
            acc = rows[v][u]
            for x in range(w):
                c = g[abs(u - x)]
                qx = q[v * w + x]
                for l in range(nl):
                    acc[l] += c * qx[l]
    out = []
    for v in range(h):
        for u in range(w):
            acc = [0.0] * nl
            for y in range(h):
                c = g[abs(v - y)]
                ry = rows[y][u]
                for l in range(nl):
                    acc[l] += c * ry[l]
            qi = q[v * w + u]
            out.append([acc[l] - qi[l] for l in range(nl)])
    return out
