# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dropout/. The authors are listed in prov/8V15DT.jsonl.
"""Inverted dropout (Srivastava et al. 2014): at training time keep each unit with probability p and
divide the kept units by p; at test time use the layer unchanged. Also the exact expectations by
enumeration over all masks, and the equivalence with an adaptive L2 penalty for linear regression.
"""

import itertools
import random
from fractions import Fraction

Vec = list
Mat = list


def dropout_mask(n: int, p: float, rng: random.Random) -> list[int]:
    """A mask of n independent Bernoulli(p) entries: 1 keeps the unit, 0 drops it."""
    return [1 if rng.random() < p else 0 for _ in range(n)]


def dropout_forward(x: Vec, p, rng: random.Random, train: bool = True) -> tuple[Vec, list[int]]:
    """Inverted dropout. In training, y_i = m_i x_i / p. In evaluation, y = x and the mask is all ones."""
    if not train or p == 1:
        return list(x), [1] * len(x)
    m = dropout_mask(len(x), p, rng)
    return [mi * xi / p for mi, xi in zip(m, x)], m


def dropout_backward(grad_out: Vec, mask: list[int], p) -> Vec:
    """dL/dx_i = m_i dL/dy_i / p, with the mask saved by the forward pass."""
    return [mi * g / p for mi, g in zip(mask, grad_out)]


def all_masks(d: int, p: Fraction):
    """Every mask of length d with its probability under independent Bernoulli(p) entries."""
    for m in itertools.product((0, 1), repeat=d):
        k = sum(m)
        yield m, p ** k * (1 - p) ** (d - k)


def exact_moments(x: Vec, p: Fraction) -> tuple[Vec, Vec]:
    """The exact mean and variance of each output of inverted dropout, by enumeration over masks."""
    d = len(x)
    mean = [Fraction(0)] * d
    second = [Fraction(0)] * d
    for m, prob in all_masks(d, p):
        for i in range(d):
            y = m[i] * x[i] / p
            mean[i] += prob * y
            second[i] += prob * y * y
    return mean, [s - mu * mu for s, mu in zip(second, mean)]


def expected_dropout_loss(w: Vec, x: Vec, y, p: Fraction):
    """E over masks of (y - w . (m * x) / p)^2, by enumeration over all 2^d masks."""
    total = Fraction(0)
    for m, prob in all_masks(len(x), p):
        pred = sum(wj * mj * xj for wj, mj, xj in zip(w, m, x)) / p
        total += prob * (y - pred) ** 2
    return total


def dropout_penalty(w: Vec, x: Vec, p):
    """((1 - p) / p) sum_j w_j^2 x_j^2, the variance term of the expected loss."""
    return (1 - p) / p * sum(wj * wj * xj * xj for wj, xj in zip(w, x))


def solve(a: Mat, b: Vec) -> Vec:
    """Gaussian elimination with exact fractions."""
    n = len(b)
    m = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(a, b)]
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def dropout_regression_solution(xs: Mat, ys: Vec, p: Fraction) -> Vec:
    """The minimizer of sum_i E_m (y_i - w . (m * x_i) / p)^2, which is
    (X^T X + ((1 - p) / p) diag(X^T X))^{-1} X^T y."""
    d = len(xs[0])
    lam = (1 - p) / p
    a = [[sum(Fraction(x[i]) * x[j] for x in xs) for j in range(d)] for i in range(d)]
    for i in range(d):
        a[i][i] *= 1 + lam
    b = [sum(Fraction(x[i]) * y for x, y in zip(xs, ys)) for i in range(d)]
    return solve(a, b)


def train_linear_with_dropout(xs: Mat, ys: Vec, p: float, eta: float, epochs: int,
                              rng: random.Random) -> Vec:
    """Stochastic gradient descent on the squared loss of a linear model with inverted dropout on its
    inputs, one example per step. Returns the average of the iterates over the second half of training."""
    d = len(xs[0])
    w = [0.0] * d
    avg = [0.0] * d
    count = 0
    for epoch in range(epochs):
        for i in rng.sample(range(len(xs)), len(xs)):
            h, mask = dropout_forward(xs[i], p, rng)
            r = sum(wj * hj for wj, hj in zip(w, h)) - ys[i]
            w = [wj - eta * 2 * r * hj for wj, hj in zip(w, h)]
            if epoch >= epochs // 2:
                count += 1
                avg = [a + (wj - a) / count for a, wj in zip(avg, w)]
    return avg
