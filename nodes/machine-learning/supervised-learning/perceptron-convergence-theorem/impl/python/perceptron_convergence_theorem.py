# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perceptron-convergence-theorem/. The authors are listed in prov/8TYE96.jsonl.

"""Tools to check the Block-Novikoff bound (R / gamma)^2 on concrete streams."""

import math
from typing import Iterable, Sequence

Vector = Sequence[float]


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def online_perceptron(stream: Iterable[tuple[Vector, int]], d: int) -> tuple[list[float], int]:
    """Run the perceptron through the origin on a stream. Return (w, mistakes).

    A mistake is y * (w . x) <= 0; the update is w <- w + y x.
    """
    w = [0.0] * d
    mistakes = 0
    for x, y in stream:
        if y * dot(w, x) <= 0:
            for j in range(d):
                w[j] += y * x[j]
            mistakes += 1
    return w, mistakes


def margin(u: Vector, data: Iterable[tuple[Vector, int]]) -> float:
    """min y (u . x) / ||u||, the margin of the direction u on the data."""
    nu = math.sqrt(dot(u, u))
    return min(y * dot(u, x) for x, y in data) / nu


def radius(data: Iterable[tuple[Vector, int]]) -> float:
    return max(math.sqrt(dot(x, x)) for x, _ in data)


def novikoff_bound(r: float, gamma: float) -> float:
    return (r / gamma) ** 2


def bias_bound(r: float, b: float, gamma: float, c: float) -> float:
    """The bound after augmentation x -> (x, c), for a unit u and offset b.

    The augmented radius is sqrt(r^2 + c^2). The unit vector (u, b / c),
    normalized, has margin gamma / sqrt(1 + b^2 / c^2).
    """
    return (r * r + c * c) * (1 + b * b / (c * c)) / (gamma * gamma)


def adversarial_orthonormal(m: int) -> tuple[list[int], int]:
    """Feed e_1, ..., e_m and choose each label against the current prediction.

    Returns (labels, mistakes). The labels are separable by u = sum y_i e_i / sqrt(m)
    with margin 1 / sqrt(m) and radius 1, so (R / gamma)^2 = m.
    """
    w = [0.0] * m
    labels = []
    mistakes = 0
    for i in range(m):
        x = [0.0] * m
        x[i] = 1.0
        s = dot(w, x)
        y = -1 if s > 0 else 1  # the prediction is sign(s), with sign(0) taken as +1
        labels.append(y)
        if y * s <= 0:
            w[i] += y
            mistakes += 1
    return labels, mistakes
