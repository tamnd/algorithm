# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-accumulation/. The authors are listed in prov/H2P10E.jsonl.

"""Gradient accumulation: sum the gradients of m micro-batches, each weighted
by its share of the batch, and take one optimizer step.

For a loss that is a mean over examples this equals the gradient of the
whole batch exactly. With batch normalization it does not: each micro-batch
is normalized with its own mean and variance. All functions work with
Fractions, so equalities can be tested exactly.
"""

from fractions import Fraction
from math import isqrt


def mse_grad(w, batch):
    """Gradient of (1/|B|) sum (w . x - y)^2 for a linear model."""
    g = [0 * a for a in w]
    for x, y in batch:
        e = sum(a * b for a, b in zip(w, x)) - y
        g = [gi + 2 * e * xi for gi, xi in zip(g, x)]
    return [gi / len(batch) for gi in g]


def accumulated_grad(grad, w, micro_batches, weighting="size"):
    """Sum of micro-batch gradients. weighting="size" uses |B_j| / |B|,
    which is exact for any sizes; "equal" uses 1/m, exact only for equal sizes."""
    total = sum(len(b) for b in micro_batches)
    acc = [0 * a for a in w]
    for b in micro_batches:
        s = Fraction(len(b), total) if weighting == "size" else Fraction(1, len(micro_batches))
        acc = [a + s * g for a, g in zip(acc, grad(w, b))]
    return acc


def split(batch, sizes):
    out, i = [], 0
    for s in sizes:
        out.append(batch[i:i + s])
        i += s
    return out


def train_with_accumulation(grad, w, batches, sizes, lr):
    """SGD where each optimizer step uses one batch split into micro-batches
    of the given sizes. Returns the iterates."""
    path = [list(w)]
    for batch in batches:  # @line L1
        acc = [0 * a for a in w]  # @line L2
        total = len(batch)
        for micro in split(batch, sizes):  # @line L3
            g = grad(w, micro)  # @line L4
            acc = [a + gi * len(micro) / total for a, gi in zip(acc, g)]  # @line L5
        w = [a - lr * gi for a, gi in zip(w, acc)]  # @line L6
        path.append(w)
    return path  # @line L7


def batchnorm_loss_grad(w, batch):
    """Model out_i = (z_i - mean z) / std z with z_i = w . x_i (batch statistics,
    no epsilon, no affine), loss (1/n) sum (out_i - y_i)^2. Returns the loss and
    the gradient in w. With Fractions the result is exact when the batch
    variance is the square of a rational number."""
    n = len(batch)
    z = [sum(a * b for a, b in zip(w, x)) for x, _ in batch]
    mu = sum(z) / n
    var = sum((zi - mu) ** 2 for zi in z) / n
    sd = _sqrt(var)
    zh = [(zi - mu) / sd for zi in z]
    loss = sum((a - y) ** 2 for a, (_, y) in zip(zh, batch)) / n
    dzh = [2 * (a - y) / n for a, (_, y) in zip(zh, batch)]
    m1 = sum(dzh) / n
    m2 = sum(d * a for d, a in zip(dzh, zh)) / n
    dz = [(d - m1 - a * m2) / sd for d, a in zip(dzh, zh)]
    g = [sum(dz[i] * batch[i][0][k] for i in range(n)) for k in range(len(w))]
    return loss, g


def batchnorm_grad(w, batch):
    return batchnorm_loss_grad(w, batch)[1]


def _sqrt(v):
    """Square root; exact for a Fraction that is a perfect square."""
    if isinstance(v, Fraction):
        n, d = isqrt(v.numerator), isqrt(v.denominator)
        if n * n == v.numerator and d * d == v.denominator:
            return Fraction(n, d)
    return v ** 0.5
