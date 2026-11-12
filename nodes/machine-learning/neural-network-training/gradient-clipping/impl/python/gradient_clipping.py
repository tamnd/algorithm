# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-clipping/. The authors are listed in prov/YBTGFW.jsonl.
"""Gradient clipping by global norm and by value.

A gradient is a list of tensors, each a flat list of floats.

clip_by_global_norm scales every tensor by min(1, c / nu), where nu is the
Euclidean norm of all entries together. The direction is kept and the new norm
is min(nu, c). clip_by_value clamps each entry to [-c, c]; this bounds every
entry but in general changes the direction.
"""

import math
from typing import Sequence

Tensor = list[float]


def global_norm(grads: Sequence[Tensor]) -> float:
    """The Euclidean norm of all entries, scaled to avoid overflow."""
    m = max((abs(x) for g in grads for x in g), default=0.0)
    if m == 0.0 or not math.isfinite(m):
        return m
    return m * math.sqrt(math.fsum((x / m) ** 2 for g in grads for x in g))


def clip_by_global_norm(grads: Sequence[Tensor], c: float):
    """Return (clipped, nu). If nu is not finite the step should be skipped:
    the input is returned unchanged with nu = inf or nan."""
    nu = global_norm(grads)  # @line L1
    if not math.isfinite(nu):
        return [list(g) for g in grads], nu
    if nu > c:  # @line L2
        scale = c / nu
        return [[x * scale for x in g] for g in grads], nu  # @line L3
    return [list(g) for g in grads], nu  # @line L4


def clip_by_value(grads: Sequence[Tensor], c: float) -> list[Tensor]:
    return [[max(-c, min(c, x)) for x in g] for g in grads]


def clip_each_tensor_by_norm(grads: Sequence[Tensor], c: float) -> list[Tensor]:
    """Per-tensor norm clipping: each tensor separately to norm at most c."""
    return [clip_by_global_norm([g], c)[0][0] for g in grads]


def sgd_step(theta: Sequence[float], grad: Sequence[float], eta: float, c: float | None = None):
    """One gradient step, with clipping by norm when c is given."""
    g = list(grad)
    if c is not None:
        g = clip_by_global_norm([g], c)[0][0]
    return [t - eta * x for t, x in zip(theta, g)]
