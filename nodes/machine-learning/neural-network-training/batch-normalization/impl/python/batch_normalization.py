# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-normalization/. The authors are listed in prov/3YR4QN.jsonl.
"""Batch normalization of a mini-batch of m examples with d features: the training forward pass, its
backward pass, the running averages and the inference transform (Ioffe and Szegedy 2015, Algorithms 1, 2).

A batch is a list of m rows, each a list of d floats. The statistics are per feature (per column).
"""

import math

Vec = list[float]
Mat = list[list[float]]


def column_stats(x: Mat) -> tuple[Vec, Vec]:
    """The per feature mean and biased variance (divide by m) of the batch."""
    m, d = len(x), len(x[0])
    mean = [sum(row[j] for row in x) / m for j in range(d)]
    var = [sum((row[j] - mean[j]) ** 2 for row in x) / m for j in range(d)]
    return mean, var


def bn_forward(x: Mat, gamma: Vec, beta: Vec, eps: float = 1e-5) -> tuple[Mat, tuple[Mat, Vec]]:
    """Training mode: y = gamma * (x - mu_B) / sqrt(var_B + eps) + beta. Returns y and the cache
    (x_hat, inv_std) that the backward pass needs."""
    mean, var = column_stats(x)
    inv = [1 / math.sqrt(v + eps) for v in var]
    xhat = [[(row[j] - mean[j]) * inv[j] for j in range(len(row))] for row in x]
    y = [[gamma[j] * r[j] + beta[j] for j in range(len(r))] for r in xhat]
    return y, (xhat, inv)


def bn_backward(dy: Mat, cache: tuple[Mat, Vec], gamma: Vec) -> tuple[Mat, Vec, Vec]:
    """Given dL/dy, return dL/dx, dL/dgamma and dL/dbeta:
    dx_i = gamma * inv_std / m * (m dy_i - sum_k dy_k - x_hat_i sum_k dy_k x_hat_k)."""
    xhat, inv = cache
    m, d = len(dy), len(dy[0])
    dbeta = [sum(dy[i][j] for i in range(m)) for j in range(d)]
    dgamma = [sum(dy[i][j] * xhat[i][j] for i in range(m)) for j in range(d)]
    dx = [[gamma[j] * inv[j] / m * (m * dy[i][j] - dbeta[j] - xhat[i][j] * dgamma[j]) for j in range(d)]
          for i in range(m)]
    return dx, dgamma, dbeta


class BatchNorm:
    """A batch normalization layer with exponential running averages for inference.
    The running variance uses the unbiased batch variance m / (m - 1) * var_B."""

    def __init__(self, d: int, momentum: float = 0.1, eps: float = 1e-5) -> None:
        self.gamma = [1.0] * d
        self.beta = [0.0] * d
        self.running_mean = [0.0] * d
        self.running_var = [1.0] * d
        self.momentum = momentum
        self.eps = eps

    def train_step(self, x: Mat) -> Mat:
        m = len(x)
        mean, var = column_stats(x)
        a = self.momentum
        for j in range(len(mean)):
            self.running_mean[j] = (1 - a) * self.running_mean[j] + a * mean[j]
            self.running_var[j] = (1 - a) * self.running_var[j] + a * var[j] * m / (m - 1)
        y, _ = bn_forward(x, self.gamma, self.beta, self.eps)
        return y

    def infer(self, row: Vec) -> Vec:
        """Inference mode: a fixed affine map of one example, independent of the rest of the batch."""
        return [self.gamma[j] * (row[j] - self.running_mean[j]) / math.sqrt(self.running_var[j] + self.eps)
                + self.beta[j] for j in range(len(row))]


def population_statistics(batches: list[Mat]) -> tuple[Vec, Vec]:
    """Algorithm 2 of Ioffe and Szegedy: E[x] = mean of the batch means and
    Var[x] = m / (m - 1) times the mean of the batch variances, for batches of size m."""
    m = len(batches[0])
    stats = [column_stats(b) for b in batches]
    d = len(stats[0][0])
    mean = [sum(s[0][j] for s in stats) / len(stats) for j in range(d)]
    var = [m / (m - 1) * sum(s[1][j] for s in stats) / len(stats) for j in range(d)]
    return mean, var


def folded_affine(gamma: Vec, beta: Vec, mean: Vec, var: Vec, eps: float = 1e-5) -> tuple[Vec, Vec]:
    """The inference transform as y = a * x + c per feature, which can be folded into the previous layer."""
    a = [g / math.sqrt(v + eps) for g, v in zip(gamma, var)]
    c = [b - ai * mu for b, ai, mu in zip(beta, a, mean)]
    return a, c
