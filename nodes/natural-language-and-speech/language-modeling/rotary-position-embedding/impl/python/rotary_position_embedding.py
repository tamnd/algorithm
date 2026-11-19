# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rotary-position-embedding/. The authors are listed in prov/XBK70H.jsonl.

"""Rotary position embedding (RoPE) of Su et al. (RoFormer).

For an even size d and i = 0, ..., d/2 - 1, with theta_i = base^(-2i/d),
the pair (x[2i], x[2i + 1]) of a query or key at position pos is rotated by
the angle pos * theta_i:

    y[2i]     = cos(pos theta_i) x[2i] - sin(pos theta_i) x[2i + 1]
    y[2i + 1] = sin(pos theta_i) x[2i] + cos(pos theta_i) x[2i + 1]

So y = R_pos x with a block-diagonal rotation R_pos, and
rope(q, m) . rope(k, n) = q . R_(n - m) k depends on m and n only through n - m.

rope_half is the layout in halves used by many code bases: coordinate i is
paired with coordinate i + d/2 instead of i + 1.

Precondition: d is even and positive, base > 1.
Cost: Theta(d) operations per vector, Theta(n d) for n positions.
The code takes the query and key vectors as given. It does not train a network.
"""

import math
from typing import List, Sequence

Vector = List[float]


def _check(d: int, base: float) -> None:
    if d <= 0 or d % 2:
        raise ValueError("the size d must be even and positive")
    if not base > 1:
        raise ValueError("the base must be greater than 1")


def rope(x: Sequence[float], pos: float, base: float = 10000.0) -> Vector:
    """Rotate each pair (x[2i], x[2i + 1]) by pos * base^(-2i/d)."""
    d = len(x)
    _check(d, base)
    y = [0.0] * d
    for i in range(d // 2):  # @line L1
        theta = base ** (-2 * i / d)  # @line L2
        c, s = math.cos(pos * theta), math.sin(pos * theta)  # @line L3
        y[2 * i] = c * x[2 * i] - s * x[2 * i + 1]  # @line L4
        y[2 * i + 1] = s * x[2 * i] + c * x[2 * i + 1]  # @line L5
    return y  # @line L6


def rope_half(x: Sequence[float], pos: float, base: float = 10000.0) -> Vector:
    """The same rotations with coordinate i paired with coordinate i + d/2."""
    d = len(x)
    _check(d, base)
    h = d // 2
    y = [0.0] * d
    for i in range(h):
        theta = base ** (-2 * i / d)
        c, s = math.cos(pos * theta), math.sin(pos * theta)
        y[i] = c * x[i] - s * x[i + h]
        y[i + h] = s * x[i] + c * x[i + h]
    return y


def rope_score(q: Sequence[float], m: float, k: Sequence[float], n: float, base: float = 10000.0) -> float:
    """The attention score (before the 1/sqrt(d) scale) of a query at position m and a key at position n."""
    if len(q) != len(k):
        raise ValueError("q and k must have the same size")
    return math.fsum(a * b for a, b in zip(rope(q, m, base), rope(k, n, base)))
