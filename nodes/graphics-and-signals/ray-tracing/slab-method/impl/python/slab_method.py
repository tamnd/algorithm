# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slab-method/. The authors are listed in prov/2SZ2M7.jsonl.

import math
from collections.abc import Sequence

Vec = Sequence[float]

# Unit roundoff of IEEE-754 binary64 and gamma(3) = 3u / (1 - 3u), as in PBRT, Section 3.9.
UNIT_ROUNDOFF = 2.0**-53
GAMMA3 = 3 * UNIT_ROUNDOFF / (1 - 3 * UNIT_ROUNDOFF)


def inverse_direction(d: Vec) -> tuple[float, float, float]:
    """Return 1/d per axis. A zero component (+0.0 or -0.0) gives an infinity of the same sign.

    Python raises on 1/0.0, so the IEEE-754 result is made with copysign.
    """
    return tuple(math.copysign(math.inf, x) if x == 0 else 1.0 / x for x in d)  # type: ignore[return-value]


def _max(x: float, y: float) -> float:
    """x if x > y else y. If x is NaN, the comparison is false and y is returned."""
    return x if x > y else y


def _min(x: float, y: float) -> float:
    """x if x < y else y. If x is NaN, the comparison is false and y is returned."""
    return x if x < y else y


def slab_test(
    lo: Vec,
    hi: Vec,
    o: Vec,
    inv: Vec,
    t0: float = 0.0,
    t1: float = math.inf,
    robust: bool = False,
) -> tuple[float, float] | None:
    """Intersect the ray o + t d, t in [t0, t1], with the closed box [lo, hi].

    inv is inverse_direction(d). Precondition: lo[a] <= hi[a] are finite, d is not the zero
    vector, and t0, t1 are not NaN. Return the parameter interval (t0', t1') of the part of
    the ray inside the box, or None if the ray misses it. With robust=True the far value of
    each slab is scaled by 1 + 2 gamma(3), so that rounding never turns a hit into a miss.
    Cost: O(1), at most 6 multiplications and 6 subtractions.
    """
    pad = 1.0 + 2.0 * GAMMA3 if robust else 1.0
    for a in range(3):  # @line L1
        if inv[a] >= 0:  # @line L2
            near, far = lo[a], hi[a]
        else:
            near, far = hi[a], lo[a]
        tn = (near - o[a]) * inv[a]  # @line L3
        tf = (far - o[a]) * inv[a] * pad  # @line L4
        t0 = _max(tn, t0)  # @line L5
        t1 = _min(tf, t1)  # @line L6
        if t0 > t1:  # @line L7
            return None
    return (t0, t1)  # @line L8
