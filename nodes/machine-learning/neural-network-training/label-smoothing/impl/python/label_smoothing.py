# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/label-smoothing/. The authors are listed in prov/6Q5BPV.jsonl.
"""Label smoothing (Szegedy et al. 2016): train with the target q' = (1 - eps) y + eps u, where y is the
one-hot label and u is uniform over the K classes. The loss H(q', p) is (1 - eps) H(y, p) + eps H(u, p),
its gradient in the logits is p - q', and its minimizer has a finite logit gap.
"""

import math
from fractions import Fraction


def softmax(z: list[float]) -> list[float]:
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def smooth_labels(label: int, k: int, eps):
    """q'_j = (1 - eps) [j == label] + eps / K."""
    return [(1 - eps) * (1 if j == label else 0) + eps / k for j in range(k)]


def cross_entropy(q: list, p: list) -> float:
    return -sum(qj * math.log(pj) for qj, pj in zip(q, p) if qj != 0)


def ls_loss(z: list[float], label: int, eps: float) -> float:
    """Cross-entropy of the softmax of the logits z against the smoothed target, computed stably."""
    m = max(z)
    lse = m + math.log(sum(math.exp(v - m) for v in z))
    return sum(qj * (lse - zj) for qj, zj in zip(smooth_labels(label, len(z), eps), z))


def ls_grad(z: list[float], label: int, eps: float) -> list[float]:
    """d loss / d z = softmax(z) - q'."""
    return [pj - qj for pj, qj in zip(softmax(z), smooth_labels(label, len(z), eps))]


def optimal_gap(k: int, eps: float) -> float:
    """The logit gap z_label - z_other at the minimizer, where softmax(z) = q'."""
    return math.log((1 - eps + eps / k) / (eps / k))


def bits(p: Fraction) -> int:
    """-log2 p for p = 2^-n, exactly."""
    n = p.denominator.bit_length() - 1
    if p.numerator != 1 or p.denominator != 1 << n:
        raise ValueError("not a power of two")
    return n


def cross_entropy_bits(q: list, p: list) -> Fraction:
    """H(q, p) in bits, exactly, when every p_j is a power of two."""
    return sum((Fraction(qj) * bits(Fraction(pj)) for qj, pj in zip(q, p)), Fraction(0))


def train_softmax_regression(xs: list[list[float]], labels: list[int], k: int, eps: float, eta: float,
                             steps: int) -> list[list[float]]:
    """Full-batch gradient descent on the mean label-smoothed cross-entropy of a linear softmax model
    with weights W (k rows) and no bias. Returns W."""
    d = len(xs[0])
    w = [[0.0] * d for _ in range(k)]
    n = len(xs)
    for _ in range(steps):
        g = [[0.0] * d for _ in range(k)]
        for x, y in zip(xs, labels):
            z = [sum(a * b for a, b in zip(row, x)) for row in w]
            dz = ls_grad(z, y, eps)
            for c in range(k):
                for j in range(d):
                    g[c][j] += dz[c] * x[j] / n
        w = [[a - eta * b for a, b in zip(row, grow)] for row, grow in zip(w, g)]
    return w
