# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slice-sampling/. The authors are listed in prov/97GJYT.jsonl.

import math
import random
from typing import Callable, Sequence

Point = tuple[float, ...]


def step_out(
    inside: Callable[[float], bool], x: float, w: float, m: int, u: float, v: float
) -> tuple[float, float]:
    """Stepping out from x with offset u and budget split v (both in [0, 1)).

    inside(z) tells whether z is in the slice. Returns the interval (L, R).
    """
    left = x - w * u  # @line L4
    right = left + w
    j = int(m * v)
    k = m - 1 - j
    while j > 0 and inside(left):  # @line L5
        left -= w
        j -= 1
    while k > 0 and inside(right):  # @line L6
        right += w
        k -= 1
    return left, right


def slice_update(
    log_f: Callable[[float], float], x: float, w: float, m: int, rng: random.Random
) -> float:
    """One slice-sampling update of a single real variable (stepping out and shrinkage)."""
    log_y = log_f(x) + math.log(1.0 - rng.random())  # @line L3
    inside = lambda z: log_f(z) > log_y
    left, right = step_out(inside, x, w, m, rng.random(), rng.random())
    while True:
        x1 = left + (right - left) * rng.random()  # @line L7
        if inside(x1):  # @line L8
            return x1
        if x1 < x:  # @line L9
            left = x1
        else:
            right = x1


def slice_sampling(
    log_f: Callable[[Point], float],
    x0: Sequence[float],
    w: float,
    m: int,
    n_steps: int,
    rng: random.Random,
) -> list[Point]:
    """Run coordinate-wise slice sampling and return X_1..X_T (one sweep per step).

    log_f is log of the unnormalized density, -inf outside the support.
    Precondition: log_f(x0) > -inf, w > 0 and m >= 1.
    """
    if w <= 0 or m < 1:
        raise ValueError("need w > 0 and m >= 1")
    x = [float(v) for v in x0]  # @line L1
    if log_f(tuple(x)) == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    chain: list[Point] = []
    for _ in range(n_steps):  # @line L2
        for i in range(len(x)):

            def log_fi(z: float, i: int = i) -> float:
                old = x[i]
                x[i] = z
                val = log_f(tuple(x))
                x[i] = old
                return val

            x[i] = slice_update(log_fi, x[i], w, m, rng)
        chain.append(tuple(x))  # @line L10
    return chain  # @line L11
