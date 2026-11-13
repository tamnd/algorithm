# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lifting-scheme/. The authors are listed in prov/8YF7JV.jsonl.

"""The lifting scheme: a wavelet transform level as split, predict and update steps.

A step is a pair (kind, taps). kind is "P" (predict) or "U" (update), and taps
maps an offset k to a coefficient c. With the even samples s and the odd
samples d, of length h each, the steps are

    P:  d[i] <- d[i] + sum_k c_k s[(i + k) mod h]
    U:  s[i] <- s[i] + sum_k c_k d[(i + k) mod h]

Each step changes one half and reads only the other, so it works in place and
is undone by the same step with a minus sign. Indices wrap around (periodic
extension), as in the convolution form of the transform.
"""

import math
from fractions import Fraction
from typing import Any

Step = tuple[str, dict[int, Any]]


def _apply(s: list, d: list, kind: str, taps: dict, sign: int, rnd=None) -> None:
    h = len(s)
    src, dst = (s, d) if kind == "P" else (d, s)
    delta = []
    for i in range(h):  # @line L4
        acc = 0
        for k, c in taps.items():
            acc = acc + c * src[(i + k) % h]
        delta.append(acc if rnd is None else rnd(acc))  # @line L5
    for i in range(h):
        dst[i] = dst[i] + sign * delta[i]  # @line L6


def lift_forward(x: list, steps: list[Step], scale: tuple = (1, 1)) -> tuple[list, list]:
    """One level: split x into even and odd samples, run the steps, scale the halves."""
    if len(x) % 2:
        raise ValueError("the length must be even")
    s, d = list(x[0::2]), list(x[1::2])  # @line L1
    for kind, taps in steps:  # @line L2
        _apply(s, d, kind, taps, +1)  # @line L3
    ks, kd = scale
    return [ks * v for v in s], [kd * v for v in d]  # @line L7


def lift_inverse(s: list, d: list, steps: list[Step], inv_scale: tuple = (1, 1)) -> list:
    """Undo lift_forward. inv_scale holds the reciprocals of the scale factors."""
    ks, kd = inv_scale
    s, d = [ks * v for v in s], [kd * v for v in d]  # @line L8
    for kind, taps in reversed(steps):  # @line L9
        _apply(s, d, kind, taps, -1)  # @line L10
    out: list = [0] * (2 * len(s))
    out[0::2], out[1::2] = s, d  # @line L11
    return out


def _round_with(offset: Fraction):
    return lambda v: math.floor(Fraction(v) + offset)


def lift_forward_int(x: list[int], steps: list[Step], offsets: list[Fraction]) -> tuple[list[int], list[int]]:
    """Integer to integer transform: each step adds floor(sum + offset), with no final scaling."""
    if len(x) % 2:
        raise ValueError("the length must be even")
    s, d = list(x[0::2]), list(x[1::2])
    for (kind, taps), off in zip(steps, offsets):
        _apply(s, d, kind, taps, +1, _round_with(off))
    return s, d


def lift_inverse_int(s: list[int], d: list[int], steps: list[Step], offsets: list[Fraction]) -> list[int]:
    """Exact inverse of lift_forward_int: subtract the same rounded values in reverse order."""
    s, d = list(s), list(d)
    for (kind, taps), off in reversed(list(zip(steps, offsets))):
        _apply(s, d, kind, taps, -1, _round_with(off))
    out = [0] * (2 * len(s))
    out[0::2], out[1::2] = s, d
    return out


def multilevel(x: list, steps: list[Step], scale: tuple, levels: int) -> tuple[list, list[list]]:
    """Run lift_forward on the low-pass half `levels` times. Returns (a, details), finest first."""
    a, details = list(x), []
    for _ in range(levels):
        a, d = lift_forward(a, steps, scale)
        details.append(d)
    return a, details


# Haar: d = odd - even, s = even + d/2 = (even + odd)/2.
HAAR_STEPS: list[Step] = [("P", {0: -1}), ("U", {0: Fraction(1, 2)})]

# LeGall 5/3: d = odd - (even + next even)/2, s = even + (previous d + d)/4.
LEGALL_53_STEPS: list[Step] = [
    ("P", {0: Fraction(-1, 2), 1: Fraction(-1, 2)}),
    ("U", {-1: Fraction(1, 4), 0: Fraction(1, 4)}),
]
# Round half up in both steps. This gives the reversible 5/3 transform of JPEG 2000:
# d = odd - floor((even + next even)/2) and s = even + floor((previous d + d + 2)/4).
LEGALL_53_OFFSETS = [Fraction(1, 2), Fraction(1, 2)]


def daubechies4_steps() -> tuple[list[Step], tuple[float, float], tuple[float, float]]:
    """Lifting steps of the orthonormal Daubechies 4-tap wavelet (Daubechies and Sweldens 1998).

    Returns the steps, the scale factors and their reciprocals."""
    r3, r2 = math.sqrt(3), math.sqrt(2)
    steps: list[Step] = [
        ("U", {0: r3}),
        ("P", {0: -r3 / 4, -1: -(r3 - 2) / 4}),
        ("U", {1: -1.0}),
    ]
    ks, kd = (r3 - 1) / r2, (r3 + 1) / r2
    return steps, (ks, kd), (1 / ks, 1 / kd)
