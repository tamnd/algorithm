# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-pca/. The authors are listed in prov/V5B4MS.jsonl.

"""Kernel PCA (Schölkopf, Smola and Müller 1998).

fit(x, kernel, k) centers the Gram matrix in feature space, K' = K - 1K - K1 + 1K1 with
1 = (1/n) J, finds its top eigenpairs, and scales each coefficient vector so that
lam ||alpha||^2 = 1, which makes the feature-space component a unit vector.
transform projects new points, and preimage_rbf finds an approximate pre-image of a
projection for the Gaussian kernel by the fixed-point iteration of Mika et al. (1999).
"""

import math


def linear_kernel(a, b):
    return sum(s * t for s, t in zip(a, b))


def rbf_kernel(gamma):
    def k(a, b):
        return math.exp(-gamma * sum((s - t) ** 2 for s, t in zip(a, b)))
    return k


def polynomial_kernel(degree, c=1.0):
    def k(a, b):
        return (linear_kernel(a, b) + c) ** degree
    return k


def jacobi_eigen(a, tol=1e-14, max_sweeps=100):
    """Eigenvalues and eigenvectors (columns of v) of a symmetric matrix, cyclic Jacobi."""
    n = len(a)
    a = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = math.sqrt(sum(x * x for row in a for x in row)) or 1.0
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for r in range(n):
                    arp, arq = a[r][p], a[r][q]
                    a[r][p], a[r][q] = c * arp - s * arq, s * arp + c * arq
                for r in range(n):
                    apr, aqr = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * apr - s * aqr, s * apr + c * aqr
                for r in range(n):
                    vrp, vrq = v[r][p], v[r][q]
                    v[r][p], v[r][q] = c * vrp - s * vrq, s * vrp + c * vrq
    return [a[i][i] for i in range(n)], v


def gram(x, y, kernel):
    return [[kernel(a, b) for b in y] for a in x]


def center_gram(k):
    """K' = K - 1K - K1 + 1K1, with 1 the n x n matrix of entries 1/n."""
    n = len(k)
    row = [sum(r) / n for r in k]
    total = sum(row) / n
    return [[k[i][j] - row[i] - row[j] + total for j in range(n)] for i in range(n)]


class KernelPCA:
    def __init__(self, x, kernel, k):
        self.x, self.kernel = [list(p) for p in x], kernel
        n = len(x)
        kmat = gram(self.x, self.x, kernel)  # @line L1
        self.col_mean = [sum(r) / n for r in kmat]  # mean of each column (K is symmetric)
        self.total_mean = sum(self.col_mean) / n
        kc = center_gram(kmat)  # @line L2
        vals, vecs = jacobi_eigen(kc)  # @line L3
        order = sorted(range(n), key=lambda j: -vals[j])[:k]
        self.eigenvalues, self.alphas = [], []
        for j in order:  # @line L4
            lam = vals[j]
            if lam <= 1e-12 * max(1.0, abs(vals[order[0]])):
                break  # a zero eigenvalue has no normalizable component
            v = [vecs[i][j] for i in range(n)]
            big = max(range(n), key=lambda i: abs(v[i]))
            sign = -1.0 if v[big] < 0 else 1.0
            self.alphas.append([sign * t / math.sqrt(lam) for t in v])  # @line L5
            self.eigenvalues.append(lam)
        self.kc = kc

    def feature_variances(self):
        """Eigenvalues of the feature-space covariance (divisor n): lam / n."""
        return [lam / len(self.x) for lam in self.eigenvalues]

    def transform(self, points):
        n = len(self.x)
        out = []
        for t in points:
            kt = [self.kernel(xi, t) for xi in self.x]  # @line L6
            mt = sum(kt) / n
            ktc = [kt[i] - mt - self.col_mean[i] + self.total_mean for i in range(n)]  # @line L7
            out.append([sum(a * b for a, b in zip(alpha, ktc)) for alpha in self.alphas])  # @line L8
        return out

    def training_scores(self):
        """Score of x_j on component k is (K' alpha^k)_j = lam_k alpha^k_j."""
        return [[lam * alpha[j] for lam, alpha in zip(self.eigenvalues, self.alphas)] for j in range(len(self.x))]

    def preimage_rbf(self, beta, gamma, z0, iters=200, tol=1e-12):
        """Approximate pre-image of P = sum_k beta_k V^k + mean, for k(a,b) = exp(-gamma ||a-b||^2).
        P = sum_i g_i phi(x_i) with g_i = sum_k beta_k alpha^k_i + (1 - sum_j sum_k beta_k alpha^k_j) / n.
        Fixed point of Mika et al.: z <- sum_i g_i k(z, x_i) x_i / sum_i g_i k(z, x_i)."""
        n = len(self.x)
        g = [sum(b * alpha[i] for b, alpha in zip(beta, self.alphas)) for i in range(n)]
        shift = (1.0 - sum(g)) / n
        g = [gi + shift for gi in g]
        z = list(z0)
        for _ in range(iters):
            w = [gi * math.exp(-gamma * sum((s - t) ** 2 for s, t in zip(z, xi))) for gi, xi in zip(g, self.x)]
            den = sum(w)
            if den == 0.0:
                break
            nz = [sum(wi * xi[d] for wi, xi in zip(w, self.x)) / den for d in range(len(z))]
            done = math.sqrt(sum((s - t) ** 2 for s, t in zip(nz, z))) < tol
            z = nz
            if done:
                break
        return z
