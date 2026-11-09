# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saga/. The authors are listed in prov/GYY34P.jsonl.

"""SAGA for F(x) + psi(x) with F(x) = (1/n) sum_i f_i(x).

The method keeps a table of the last gradient seen for each component and its average.
A step uses v = grad f_j(x) - table[j] + average, which is unbiased for grad F(x), then
replaces table[j] by grad f_j(x) and applies the proximal map of psi (the identity if psi = 0).
"""

import random
from collections.abc import Callable

Vector = list[float]
Observer = Callable[[int, int, Vector, list[Vector], Vector], None]


def saga(
    grad: Callable[[int, Vector], Vector],
    n: int,
    x0: Vector,
    step: float,
    iters: int,
    rng: random.Random,
    prox: Callable[[Vector, float], Vector] | None = None,
    indices: list[int] | None = None,
    observer: Observer | None = None,
) -> list[Vector]:
    """Return [x_0, ..., x_iters].

    prox(z, t) must return argmin_y psi(y) + |y - z|^2 / (2 t). indices fixes the sampled
    components, for traces. observer(k, j, x_k, table, average) is called after each table update.
    """
    x = list(x0)  # @line L1
    table = [grad(i, x) for i in range(n)]
    avg = [sum(g[c] for g in table) / n for c in range(len(x))]
    xs = [x]
    picks = iter(indices) if indices is not None else None
    for k in range(iters):  # @line L2
        j = next(picks) if picks is not None else rng.randrange(n)  # @line L3
        u = grad(j, x)  # @line L4
        v = [a - b + c for a, b, c in zip(u, table[j], avg)]  # @line L5
        avg = [a + (b - c) / n for a, b, c in zip(avg, u, table[j])]  # @line L6
        table[j] = u
        if observer is not None:
            observer(k, j, x, table, avg)
        z = [a - step * b for a, b in zip(x, v)]
        x = prox(z, step) if prox is not None else z  # @line L7
        xs.append(x)
    return xs  # @line L8


def soft_threshold(lam: float) -> Callable[[Vector, float], Vector]:
    """The proximal map of lam |x|_1."""

    def prox(z: Vector, t: float) -> Vector:
        return [(abs(a) - lam * t) * (1.0 if a > 0 else -1.0) if abs(a) > lam * t else 0.0 for a in z]

    return prox
