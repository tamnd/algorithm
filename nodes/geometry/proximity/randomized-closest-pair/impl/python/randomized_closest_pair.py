# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-closest-pair/. The authors are listed in prov/KQN34S.jsonl.

import math
import random
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
Result = tuple[Number, Point, Point]


def dist2(p: tuple[int, int], q: tuple[int, int]) -> int:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def _to_integers(points: list[Point]) -> tuple[list[tuple[int, int]], int]:
    """Scale by the lcm of the denominators; squared distances scale by its square."""
    scale = 1
    for x, y in points:
        for v in (x, y):
            if isinstance(v, Fraction):
                scale = scale * v.denominator // math.gcd(scale, v.denominator)
    ints = [(int(x * scale), int(y * scale)) for x, y in points]
    return ints, scale


def _shift(d2: int) -> int:
    """Exponent e with 4^e <= d2 < 4^(e+1), so the cell side s = 2^e has s <= delta < 2s."""
    return (d2.bit_length() - 1) // 2


def _build(pts: list[tuple[int, int]], idx: list[int], upto: int, e: int) -> dict[tuple[int, int], list[int]]:
    grid: dict[tuple[int, int], list[int]] = {}
    for t in range(upto):
        i = idx[t]
        grid.setdefault((pts[i][0] >> e, pts[i][1] >> e), []).append(i)
    return grid


def randomized_closest_pair(points: list[Point], rng: Optional[random.Random] = None,
                            stats: Optional[dict[str, int]] = None) -> Optional[Result]:
    """Return (squared distance, p, q) for a closest pair, or None if there are fewer than 2 points.

    Coordinates must be int or Fraction (Fractions are scaled to integers first), so every test is
    exact. Grid cells are found with arithmetic shifts (the floor function), and cells are kept in a
    dict (hashing). Cost: O(n) expected time over the random order, assuming O(1) dict operations;
    O(n) extra space. If stats is given, it receives the number of rebuilds and the rebuild work.
    """
    n = len(points)
    if n < 2:  # @line L1
        return None
    rng = rng or random.Random()
    pts, scale = _to_integers(points)
    idx = list(range(n))
    rng.shuffle(idx)  # @line L2
    a, b = idx[0], idx[1]
    d2 = dist2(pts[a], pts[b])  # @line L3
    rebuilds, work = 0, 0
    if d2 > 0:  # @line L4
        e = _shift(d2)  # @line L5
        grid = _build(pts, idx, 2, e)
        for k in range(2, n):  # @line L6
            i = idx[k]
            cx, cy = pts[i][0] >> e, pts[i][1] >> e  # @line L7
            best_here, arg = d2, -1
            for gx in range(cx - 2, cx + 3):  # @line L8
                for gy in range(cy - 2, cy + 3):
                    for j in grid.get((gx, gy), ()):
                        dd = dist2(pts[i], pts[j])
                        if dd < best_here:
                            best_here, arg = dd, j
            if best_here < d2:  # @line L9
                d2, a, b = best_here, arg, i  # @line L10
                if d2 == 0:
                    break
                e = _shift(d2)  # @line L11
                grid = _build(pts, idx, k + 1, e)
                rebuilds += 1
                work += k + 1
            else:
                grid.setdefault((cx, cy), []).append(i)  # @line L12
    if stats is not None:
        stats["rebuilds"] = rebuilds
        stats["work"] = work
    exact = Fraction(d2, scale * scale) if scale != 1 else d2
    return exact, points[a], points[b]  # @line L13
