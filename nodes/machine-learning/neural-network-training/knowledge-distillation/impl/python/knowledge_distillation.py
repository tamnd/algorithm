# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knowledge-distillation/. The authors are listed in prov/JV5DCP.jsonl.

"""Knowledge distillation with a temperature softmax (Hinton, Vinyals and Dean 2015).

z are the student logits and v the teacher logits for one example, with N
classes. The soft targets are q = softmax(v / T), the student's soft outputs
are p = softmax(z / T), and the soft loss is the cross entropy
C(z) = -sum_i q_i log p_i. Its gradient is dC/dz_i = (p_i - q_i) / T.
Multiplying the soft loss by T^2 keeps the gradient of order 1 when T grows;
as T -> infinity, T (p - q) tends to the gradient of
(1 / 2N) ||(z - mean z) - (v - mean v)||^2.
"""

import math
from typing import List, Sequence, Tuple

Vector = List[float]


def softmax(z: Sequence[float], t: float = 1.0) -> Vector:
    """softmax(z / t), with the maximum subtracted for stability."""
    m = max(z)
    e = [math.exp((a - m) / t) for a in z]
    s = sum(e)
    return [a / s for a in e]


def soft_loss(z: Sequence[float], v: Sequence[float], t: float) -> float:
    """Cross entropy of the student's softmax(z/T) against the teacher's softmax(v/T)."""
    q = softmax(v, t)
    m = max(a / t for a in z)
    log_norm = m + math.log(sum(math.exp(a / t - m) for a in z))
    return -sum(qi * (zi / t - log_norm) for qi, zi in zip(q, z))


def soft_grad(z: Sequence[float], v: Sequence[float], t: float) -> Vector:
    """dC/dz = (softmax(z/T) - softmax(v/T)) / T."""
    p, q = softmax(z, t), softmax(v, t)
    return [(a - b) / t for a, b in zip(p, q)]


def scaled_soft_grad(z: Sequence[float], v: Sequence[float], t: float) -> Vector:
    """The gradient of T^2 C(z): T (p - q)."""
    return [t * t * g for g in soft_grad(z, v, t)]


def high_temperature_limit_grad(z: Sequence[float], v: Sequence[float]) -> Vector:
    """The limit of T (p - q) as T -> infinity: ((z - mean z) - (v - mean v)) / N."""
    n = len(z)
    zm, vm = sum(z) / n, sum(v) / n
    return [((a - zm) - (b - vm)) / n for a, b in zip(z, v)]


def centered_squared_error(z: Sequence[float], v: Sequence[float]) -> float:
    """(1 / 2N) ||C z - C v||^2 with C the centering matrix; its gradient is the limit above."""
    n = len(z)
    zm, vm = sum(z) / n, sum(v) / n
    return sum(((a - zm) - (b - vm)) ** 2 for a, b in zip(z, v)) / (2 * n)


def distillation_grad(z: Sequence[float], v: Sequence[float], label: int, t: float, alpha: float) -> Vector:
    """Gradient of alpha T^2 C_soft + (1 - alpha) C_hard with respect to the student logits.

    C_hard is the usual cross entropy of softmax(z) (T = 1) against the true label.
    """
    s = scaled_soft_grad(z, v, t)
    p1 = softmax(z, 1.0)
    h = [pi - (1.0 if i == label else 0.0) for i, pi in enumerate(p1)]
    return [alpha * a + (1 - alpha) * b for a, b in zip(s, h)]


def logits(w: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    return [sum(a * b for a, b in zip(row, x)) for row in w]


def train_student(xs: Sequence[Sequence[float]], labels: Sequence[int], teacher_logits: Sequence[Sequence[float]],
                  classes: int, t: float, alpha: float, eta: float, epochs: int) -> List[Vector]:
    """Fit a linear softmax student W (classes x d) by full batch gradient descent on the distillation loss.

    alpha = 1 uses only the teacher's soft targets; alpha = 0 uses only the labels.
    """
    d = len(xs[0])
    w = [[0.0] * d for _ in range(classes)]
    n = len(xs)
    for _ in range(epochs):
        gw = [[0.0] * d for _ in range(classes)]
        for x, y, v in zip(xs, labels, teacher_logits):
            g = distillation_grad(logits(w, x), v, y, t, alpha)
            for k in range(classes):
                for j in range(d):
                    gw[k][j] += g[k] * x[j]
        w = [[a - eta * b / n for a, b in zip(rw, rg)] for rw, rg in zip(w, gw)]
    return w


def agreement(w: Sequence[Sequence[float]], w_teacher: Sequence[Sequence[float]], xs: Sequence[Sequence[float]]) -> Tuple[float, float]:
    """The fraction of inputs where student and teacher pick the same class, and the mean total variation distance."""
    same, tv = 0, 0.0
    for x in xs:
        p, q = softmax(logits(w, x)), softmax(logits(w_teacher, x))
        same += max(range(len(p)), key=p.__getitem__) == max(range(len(q)), key=q.__getitem__)
        tv += 0.5 * sum(abs(a - b) for a, b in zip(p, q))
    return same / len(xs), tv / len(xs)
