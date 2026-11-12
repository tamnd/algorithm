# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autoencoder/. The authors are listed in prov/GR8CEC.jsonl.

"""A linear autoencoder trained by full-batch gradient descent, and the tools to compare it with PCA.

Model: code z = W1 x (k x d encoder), reconstruction x_hat = W2 z (d x k decoder), no biases,
on centered data. Loss: L = (1/n) sum_i |x_i - W2 W1 x_i|^2 = tr(S) - 2 tr(W2 W1 S) + tr(W2 W1 S W1^T W2^T),
with S = (1/n) sum_i x_i x_i^T. Gradients, with R = S - W2 W1 S:
    dL/dW1 = -2 W2^T R,    dL/dW2 = -2 R W1^T,
using that S is symmetric. Baldi and Hornik (1989): at the global minimum, the range of W2 is the
span of the top k eigenvectors of S, but W1 and W2 are fixed only up to an invertible k x k matrix.
"""

import math


def transpose(a):
    return [list(r) for r in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def center(data):
    n, d = len(data), len(data[0])
    mean = [sum(x[j] for x in data) / n for j in range(d)]
    return [[x[j] - mean[j] for j in range(d)] for x in data], mean


def second_moment(data):
    """S = (1/n) sum_i x_i x_i^T (the covariance when the data are centered)."""
    n, d = len(data), len(data[0])
    return [[sum(x[a] * x[b] for x in data) / n for b in range(d)] for a in range(d)]


def loss(s, w1, w2):
    """(1/n) sum |x - W2 W1 x|^2 written with S only."""
    p = matmul(w2, w1)
    ps = matmul(p, s)
    psp = matmul(ps, transpose(p))
    d = len(s)
    return sum(s[i][i] - 2.0 * ps[i][i] + psp[i][i] for i in range(d))


def gradients(s, w1, w2):
    """Return (dL/dW1, dL/dW2)."""
    p = matmul(w2, w1)
    ps = matmul(p, s)
    r = [[s[i][j] - ps[i][j] for j in range(len(s))] for i in range(len(s))]
    g1 = [[-2.0 * v for v in row] for row in matmul(transpose(w2), r)]
    g2 = [[-2.0 * v for v in row] for row in matmul(r, transpose(w1))]
    return g1, g2


def train_linear_autoencoder(data, k, rng, steps=4000, lr=0.02, enc_scale=0.1, dec_scale=0.1):
    """Gradient descent from a random start; data must be centered. Returns (W1, W2, loss history)."""
    d = len(data[0])
    s = second_moment(data)
    w1 = [[rng.gauss(0.0, enc_scale) for _ in range(d)] for _ in range(k)]
    w2 = [[rng.gauss(0.0, dec_scale) for _ in range(k)] for _ in range(d)]
    history = [loss(s, w1, w2)]
    for _ in range(steps):
        g1, g2 = gradients(s, w1, w2)
        w1 = [[w - lr * g for w, g in zip(rw, rg)] for rw, rg in zip(w1, g1)]
        w2 = [[w - lr * g for w, g in zip(rw, rg)] for rw, rg in zip(w2, g2)]
        history.append(loss(s, w1, w2))
    return w1, w2, history


def jacobi_eigen(s, sweeps=100):
    """Eigenvalues and eigenvectors (columns of V) of a symmetric matrix by cyclic Jacobi rotations."""
    n = len(s)
    a = [row[:] for row in s]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        if sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j) < 1e-26:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for m in (a, v):
                    for r in range(n):
                        x, y = m[r][p], m[r][q]
                        m[r][p], m[r][q] = c * x - sn * y, sn * x + c * y
                for r in range(n):
                    x, y = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * x - sn * y, sn * x + c * y
    return [a[i][i] for i in range(n)], v


def pca_basis(data, k):
    """The top k eigenvalues of S and their eigenvectors as the columns of a d x k matrix."""
    vals, vecs = jacobi_eigen(second_moment(data))
    order = sorted(range(len(vals)), key=lambda i: -vals[i])
    return [vals[i] for i in order], [[vecs[r][i] for i in order[:k]] for r in range(len(vals))]


def orthonormal_columns(a):
    """Gram-Schmidt (applied twice for accuracy) on the columns of a."""
    cols = transpose(a)
    out = []
    for c in cols:
        v = c[:]
        for _ in range(2):
            for q in out:
                dot = sum(x * y for x, y in zip(v, q))
                v = [x - dot * y for x, y in zip(v, q)]
        norm = math.sqrt(sum(x * x for x in v))
        out.append([x / norm for x in v])
    return transpose(out)


def principal_angles(a, b):
    """Principal angles (radians, ascending) between the column spaces of a and b (same size)."""
    qa, qb = orthonormal_columns(a), orthonormal_columns(b)
    m = matmul(transpose(qa), qb)
    vals, _ = jacobi_eigen(matmul(transpose(m), m))
    return sorted(math.acos(min(1.0, math.sqrt(max(0.0, v)))) for v in vals)
