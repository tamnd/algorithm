# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-discriminant-analysis/. The authors are listed in prov/SMRZT0.jsonl.

"""Fisher's linear discriminant analysis and the Gaussian LDA classifier.

FISHER-LDA computes the within-class scatter S_W and the between-class
scatter S_B, solves the symmetric-definite generalized eigenproblem
S_B w = lambda S_W w through a Cholesky factor of S_W and a Jacobi
eigensolver, and returns the top directions, scaled so that W^T S_W W = I.
The Gaussian LDA classifier uses the pooled maximum likelihood covariance
S_W / n and the linear discriminant functions
delta_c(x) = x^T Sigma^-1 mu_c - mu_c^T Sigma^-1 mu_c / 2 + log pi_c.
"""

import math

Vector = list[float]
Matrix = list[list[float]]


def zeros(r: int, c: int) -> Matrix:
    return [[0.0] * c for _ in range(r)]


def mat_vec(a: Matrix, x: Vector) -> Vector:
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def quad(x: Vector, a: Matrix, y: Vector) -> float:
    return sum(xi * v for xi, v in zip(x, mat_vec(a, y)))


def cholesky(a: Matrix) -> Matrix:
    """Lower triangular L with L L^T = a. Raises ValueError if a is not positive definite."""
    d = len(a)
    low = zeros(d, d)
    for i in range(d):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("the within-class scatter is not positive definite")
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def forward_solve(low: Matrix, b: Vector) -> Vector:
    z: Vector = []
    for i in range(len(b)):
        z.append((b[i] - sum(low[i][t] * z[t] for t in range(i))) / low[i][i])
    return z


def back_solve_transpose(low: Matrix, b: Vector) -> Vector:
    """Solve L^T x = b."""
    d = len(b)
    x = [0.0] * d
    for i in range(d - 1, -1, -1):
        x[i] = (b[i] - sum(low[t][i] * x[t] for t in range(i + 1, d))) / low[i][i]
    return x


def jacobi_eigh(a: Matrix, tol: float = 1e-13, max_sweeps: int = 100) -> tuple[Vector, Matrix]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a symmetric matrix."""
    d = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        scale = sum(m[i][i] ** 2 for i in range(d)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p], m[k][q] = c * mkp - s * mkq, s * mkp + c * mkq
                for k in range(d):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k], m[q][k] = c * mpk - s * mqk, s * mpk + c * mqk
                for k in range(d):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(d), key=lambda i: -m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for i in order] for r in range(d)]


def scatter_matrices(xs: list[Vector], ys: list) -> tuple[list, dict, Vector, Matrix, Matrix]:
    """Return (classes, class means, overall mean, S_W, S_B)."""
    n, d = len(xs), len(xs[0])
    classes = sorted(set(ys), key=repr)
    mu = [sum(x[j] for x in xs) / n for j in range(d)]
    means, s_w, s_b = {}, zeros(d, d), zeros(d, d)
    for c in classes:
        pts = [x for x, y in zip(xs, ys) if y == c]
        mc = [sum(p[j] for p in pts) / len(pts) for j in range(d)]
        means[c] = mc
        for p in pts:
            for i in range(d):
                for j in range(d):
                    s_w[i][j] += (p[i] - mc[i]) * (p[j] - mc[j])  # @line L2
        for i in range(d):
            for j in range(d):
                s_b[i][j] += len(pts) * (mc[i] - mu[i]) * (mc[j] - mu[j])  # @line L3
    return classes, means, mu, s_w, s_b


def fisher_lda(xs: list[Vector], ys: list, r: int | None = None) -> tuple[Vector, list[Vector]]:
    """Return the top r generalized eigenvalues of (S_B, S_W) and the directions w_1..w_r.

    The directions satisfy w_i^T S_W w_j = [i == j]. By default r = min(k - 1, d).
    """
    classes, _, _, s_w, s_b = scatter_matrices(xs, ys)  # @line L1
    d = len(xs[0])
    if r is None:
        r = min(len(classes) - 1, d)
    low = cholesky(s_w)  # @line L4
    # M = L^-1 S_B L^-T, built column by column.
    tmp = [forward_solve(low, [s_b[i][j] for i in range(d)]) for j in range(d)]  # columns of L^-1 S_B
    m_rows = [forward_solve(low, [tmp[j][i] for j in range(d)]) for i in range(d)]  # @line L5
    m = [[0.5 * (m_rows[i][j] + m_rows[j][i]) for j in range(d)] for i in range(d)]
    lam, vecs = jacobi_eigh(m)  # @line L6
    dirs = [back_solve_transpose(low, [vecs[i][t] for i in range(d)]) for t in range(r)]  # @line L7
    return lam[:r], dirs  # @line L8


def fisher_two_class(xs: list[Vector], ys: list) -> Vector:
    """The two-class Fisher direction S_W^-1 (mu_1 - mu_0), with the classes in sorted order."""
    classes, means, _, s_w, _ = scatter_matrices(xs, ys)
    if len(classes) != 2:
        raise ValueError("needs exactly two classes")
    low = cholesky(s_w)
    diff = [b - a for a, b in zip(means[classes[0]], means[classes[1]])]
    return back_solve_transpose(low, forward_solve(low, diff))


def rayleigh(w: Vector, s_b: Matrix, s_w: Matrix) -> float:
    """Fisher's criterion J(w) = w^T S_B w / w^T S_W w."""
    return quad(w, s_b, w) / quad(w, s_w, w)


def project(xs: list[Vector], dirs: list[Vector]) -> list[Vector]:
    return [[sum(wi * xi for wi, xi in zip(w, x)) for w in dirs] for x in xs]


class GaussianLDA:
    """The Bayes rule for Gaussian classes with one shared covariance, fitted by maximum likelihood."""

    def __init__(self, xs: list[Vector], ys: list) -> None:
        classes, means, _, s_w, _ = scatter_matrices(xs, ys)
        n = len(xs)
        self.classes = classes
        self.means = means
        self.priors = {c: sum(1 for y in ys if y == c) / n for c in classes}
        self.low = cholesky([[v / n for v in row] for row in s_w])
        self.coef = {}
        self.const = {}
        for c in classes:
            a = back_solve_transpose(self.low, forward_solve(self.low, means[c]))  # Sigma^-1 mu_c
            self.coef[c] = a
            self.const[c] = -0.5 * sum(ai * mi for ai, mi in zip(a, means[c])) + math.log(self.priors[c])

    def scores(self, x: Vector) -> dict:
        return {c: sum(a * xi for a, xi in zip(self.coef[c], x)) + self.const[c] for c in self.classes}

    def predict(self, x: Vector):
        s = self.scores(x)
        return max(self.classes, key=lambda c: s[c])


def predict_in_fisher_space(xs: list[Vector], ys: list, x: Vector):
    """Classify x by the nearest projected class mean with the prior term, using r = k - 1 directions.

    With W^T S_W W = I and Sigma = S_W / n, the score is -n ||W^T (x - mu_c)||^2 / 2 + log pi_c.
    For r = k - 1 (and S_B of rank k - 1) this equals the Gaussian LDA rule.
    """
    classes, means, _, _, _ = scatter_matrices(xs, ys)
    n = len(xs)
    _, dirs = fisher_lda(xs, ys)
    z = project([x], dirs)[0]
    best, best_score = None, -math.inf
    for c in classes:
        zc = project([means[c]], dirs)[0]
        prior = sum(1 for y in ys if y == c) / n
        score = -0.5 * n * sum((a - b) ** 2 for a, b in zip(z, zc)) + math.log(prior)
        if score > best_score:
            best, best_score = c, score
    return best
