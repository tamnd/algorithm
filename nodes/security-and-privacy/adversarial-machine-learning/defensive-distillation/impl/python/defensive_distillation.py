# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/defensive-distillation/. The authors are listed in prov/RHC19E.jsonl.

"""Defensive distillation of Papernot et al. (2016), with softmax regression models, on synthetic data only.

A teacher is trained at a temperature T on the hard labels, a student is trained at
the same T on the soft labels of the teacher, and the student is used at temperature 1.
The models here are linear (softmax regression), so that the tests can compare them
with closed forms. The data come from seeded Gaussian blobs of mlkit. Nothing here
reads real data or touches a real system.
"""

import math
from typing import Sequence

import mlkit as m

Vector = list[float]
Model = tuple[list[Vector], Vector]


def logits(model: Model, x: Sequence[float]) -> Vector:
    """The logits W x + b of a softmax regression model. Cost O(k d)."""
    w, b = model
    return [m.dot(r, x) + bi for r, bi in zip(w, b)]


def soft_labels(model: Model, x: Sequence[float], temperature: float) -> Vector:
    """softmax(z(x) / T), the soft label of x at temperature T. Cost O(k d)."""
    return m.softmax([a / temperature for a in logits(model, x)])


def tempered_loss(z: Sequence[float], q: Sequence[float], temperature: float) -> float:
    """Cross-entropy of the target distribution q against softmax(z / T). Cost O(k)."""
    s = [a / temperature for a in z]
    top = max(s)
    lse = top + math.log(math.fsum(math.exp(a - top) for a in s))
    return math.fsum(qi * (lse - si) for qi, si in zip(q, s))


def tempered_loss_gradient(z: Sequence[float], q: Sequence[float], temperature: float) -> Vector:
    """Gradient of tempered_loss in the logits: (softmax(z / T) - q) / T. Cost O(k)."""
    p = m.softmax([a / temperature for a in z])
    return [(pi - qi) / temperature for pi, qi in zip(p, q)]


def train_softmax(xs: Sequence[Sequence[float]], targets: Sequence[Sequence[float]], temperature: float,
                  steps: int, lr: float) -> Model:
    """Full-batch gradient descent on the mean tempered_loss, from zero weights.

    targets[i] is a probability vector over the k classes for xs[i]. Returns (W, b).
    Cost O(steps n k d).
    """
    n, d, k = len(xs), len(xs[0]), len(targets[0])
    w = [[0.0] * d for _ in range(k)]
    b = [0.0] * k
    for _ in range(steps):
        gw = [[0.0] * d for _ in range(k)]
        gb = [0.0] * k
        for x, q in zip(xs, targets):
            g = tempered_loss_gradient(logits((w, b), x), q, temperature)
            for c in range(k):
                gb[c] += g[c]
                for j in range(d):
                    gw[c][j] += g[c] * x[j]
        w = [[w[c][j] - lr * gw[c][j] / n for j in range(d)] for c in range(k)]
        b = [b[c] - lr * gb[c] / n for c in range(k)]
    return w, b


def defensive_distillation(data: m.Data, k: int, temperature: float, steps: int, lr: float) -> tuple[Model, Model]:
    """Train a teacher and a student at temperature T. Returns (teacher, student).

    The student is meant to be used at temperature 1, that is, with softmax(z(x)).
    Preconditions: labels in range(k), temperature > 0. Cost O(steps n k d).
    """
    xs = [x for x, _ in data]  # @line L1
    hard = [[1.0 if c == y else 0.0 for c in range(k)] for _, y in data]
    teacher = train_softmax(xs, hard, temperature, steps, lr)  # @line L2
    soft = [soft_labels(teacher, x, temperature) for x in xs]  # @line L3
    student = train_softmax(xs, soft, temperature, steps, lr)  # @line L4
    return teacher, student  # @line L5
