# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-hashing-max-load-bound/. The authors are listed in prov/E7P3Z6.jsonl.

"""The load bound of consistent hashing on a circle of length 1.

Model: n servers, each with v points placed independently and uniformly on
the circle [0, 1). A key goes to the first point clockwise from it, so each
point owns the arc from the point before it. The share of a server is the
total length of the arcs of its points, and the average share is 1/n.

The functions give the exact law of the largest arc for v = 1, the bounds of
the theorem, and a simulation of shares and key loads.
"""

import bisect
import math
import random
from fractions import Fraction
from typing import Sequence, Union

Num = Union[int, float, Fraction]


def ring_points(n: int, v: int, rng: random.Random) -> list[tuple[float, int]]:
    """The n * v points (position, server), sorted by position."""
    if n < 1 or v < 1:
        raise ValueError("n and v must be at least 1")
    return sorted((rng.random(), s) for s in range(n) for _ in range(v))


def shares_from_points(pts: Sequence[tuple[float, int]], n: int) -> list[float]:
    """Share of each server: point i owns the arc (pts[i - 1], pts[i]], with wrap-around."""
    shares = [0.0] * n
    for i, (p, s) in enumerate(pts):
        prev = pts[i - 1][0] - (1.0 if i == 0 else 0.0)
        shares[s] += p - prev
    return shares


def ring_shares(n: int, v: int, rng: random.Random) -> list[float]:
    return shares_from_points(ring_points(n, v, rng), n)


def owner(pts: Sequence[tuple[float, int]], positions: Sequence[float], x: float) -> int:
    """Server of the first point at or clockwise after x. positions[i] = pts[i][0]."""
    i = bisect.bisect_left(positions, x)
    return pts[i % len(pts)][1]


def key_loads(pts: Sequence[tuple[float, int]], n: int, keys: Sequence[float]) -> list[int]:
    """Number of keys (given by their positions on the circle) that each server holds."""
    positions = [p for p, _ in pts]
    loads = [0] * n
    for x in keys:
        loads[owner(pts, positions, x)] += 1
    return loads


def max_gap(n: int, rng: random.Random) -> float:
    """The largest arc between n uniform points on the circle: the largest share for v = 1."""
    return max(ring_shares(n, 1, rng))


def harmonic(n: int) -> Fraction:
    return sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0))


def prob_max_gap_exceeds(n: int, x: Num) -> Num:
    """Exact Pr[largest of the n arcs > x], by inclusion and exclusion:
    sum over k >= 1 of (-1)^(k+1) C(n, k) (1 - k x)_+^(n - 1). Exact for Fraction x."""
    total: Num = 0
    for k in range(1, n + 1):
        base = 1 - k * x
        if base <= 0:
            break
        total += (-1) ** (k + 1) * math.comb(n, k) * base ** (n - 1)
    return total


def expected_max_gap_exact(n: int) -> Fraction:
    """E[largest arc] = integral of the tail = sum (-1)^(k+1) C(n, k) / (k n), which is H_n / n."""
    return sum((Fraction((-1) ** (k + 1) * math.comb(n, k), k * n) for k in range(1, n + 1)), Fraction(0))


def prob_min_gap_exceeds(n: int, x: Num) -> Num:
    """Exact Pr[smallest of the n arcs > x] = (1 - n x)_+^(n - 1)."""
    base = 1 - n * x
    return base ** (n - 1) if base > 0 else 0


def upper_failure_bound(n: int, x: float) -> float:
    """Pr[largest arc > x] <= n (1 - x)^(n - 1), the union bound over the n arcs."""
    return min(1.0, n * max(0.0, 1 - x) ** (n - 1))


def lower_failure_bound(n: int, x: float) -> float:
    """Pr[largest arc <= x] <= 1 / (n (1 - x)^(n - 1)), the second moment bound on the
    number of arcs longer than x."""
    if x >= 1:
        return 1.0
    return min(1.0, 1 / (n * (1 - x) ** (n - 1)))


def upper_threshold(n: int, c: float) -> float:
    """(1 + c) ln n / (n - 1): the largest arc exceeds it with probability at most n^-c."""
    return (1 + c) * math.log(n) / (n - 1)


def lower_threshold(n: int, eps: float) -> float:
    """(1 - eps) ln n / n: the largest arc is at most this with probability at most e n^-eps."""
    return (1 - eps) * math.log(n) / n


def gamma_tail_bound(v: int, delta: float) -> float:
    """Chernoff bound on Pr[G outside [(1 - delta) v, (1 + delta) v]] for G a sum of v
    independent Exp(1) variables, 0 < delta < 1."""
    up = math.exp(-v * (delta - math.log1p(delta)))
    down = math.exp(-v * (-delta - math.log1p(-delta)))
    return up + down


def share_failure_bound(n: int, v: int, delta: float) -> float:
    """Pr[some share outside the window] <= 2 n exp(-v delta^2 / 4)."""
    return min(1.0, 2 * n * math.exp(-v * delta * delta / 4))


def vnodes_needed(n: int, delta: float, c: float = 1.0) -> int:
    """Least v with 2 n exp(-v delta^2 / 4) <= n^-c, that is v >= (4 / delta^2) ln(2 n^(c + 1))."""
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0, 1)")
    return math.ceil(4 / delta ** 2 * (math.log(2) + (c + 1) * math.log(n)))


def share_window(n: int, delta: float) -> tuple[float, float]:
    """Every share lies in this window when every server sum G_s is within (1 +- delta) v."""
    return (1 - delta) / ((1 + delta) * n), (1 + delta) / ((1 - delta) * n)
