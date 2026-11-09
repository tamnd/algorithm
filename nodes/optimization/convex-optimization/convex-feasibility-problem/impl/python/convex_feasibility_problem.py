# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-feasibility-problem/. The authors are listed in prov/H1CESA.jsonl.

"""Cyclic projections (POCS) for the convex feasibility problem.

A set is one of
    ("halfspace", a, b)    {x : a . x <= b}, a != 0
    ("hyperplane", a, b)   {x : a . x == b}, a != 0
    ("ball", center, r)    {x : |x - center| <= r}
    ("box", lo, hi)        {x : lo[i] <= x[i] <= hi[i]}

The method projects onto the sets in turn. It stops when the current point
is within tol of every set, and returns None after max_cycles cycles.
Floating point; tol is an absolute distance.
"""

import math

Vec = list[float]


def dot(u: Vec, v: Vec) -> float:
    return sum(a * b for a, b in zip(u, v))


def project(s: tuple, x: Vec) -> Vec:
    kind = s[0]
    if kind in ("halfspace", "hyperplane"):
        a, b = s[1], s[2]
        excess = dot(a, x) - b
        if kind == "halfspace" and excess <= 0:
            return list(x)
        t = excess / dot(a, a)
        return [xi - t * ai for xi, ai in zip(x, a)]
    if kind == "ball":
        c, r = s[1], s[2]
        d = math.dist(x, c)
        if d <= r:
            return list(x)
        return [ci + (xi - ci) * r / d for xi, ci in zip(x, c)]
    if kind == "box":
        lo, hi = s[1], s[2]
        return [min(max(xi, l), h) for xi, l, h in zip(x, lo, hi)]
    raise ValueError(f"unknown set kind {kind!r}")


def distance(s: tuple, x: Vec) -> float:
    return math.dist(x, project(s, x))


def cyclic_projections(sets: list[tuple], x0: Vec, tol: float = 1e-9, max_cycles: int = 100000, trace: list | None = None) -> Vec | None:
    """Return a point within tol of every set, or None if none is found in max_cycles cycles."""
    x = [float(v) for v in x0]
    for _ in range(max_cycles + 1):
        if trace is not None:
            trace.append(list(x))
        if max(distance(s, x) for s in sets) <= tol:
            return x
        for s in sets:
            x = project(s, x)
    return None
