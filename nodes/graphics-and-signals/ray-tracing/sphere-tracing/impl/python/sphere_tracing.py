# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sphere-tracing/. The authors are listed in prov/W0Z18J.jsonl.
"""Sphere tracing (Hart 1996): step along a ray by the value of a signed distance bound.

The field f must satisfy |f(x)| <= dist(x, surface) and be positive outside. Then the open ball
of radius f(x) around x contains no surface point, so a step of length f(x) along a unit
direction never passes the first hit. Works with float or Fraction coordinates.
"""


def sphere_trace(f, o, d, t_max, eps, max_steps: int = 1000, record=None):
    """Return the parameter t of the first point with f(o + t d) < eps, or None.

    d must be a unit vector. None means that t passed t_max or that max_steps steps ran out.
    If record is a list, each visited t is appended to it.
    """
    t = t_max * 0  # @line L1
    for _ in range(max_steps):  # @line L2
        if t > t_max:  # @line L3
            return None
        p = (o[0] + t * d[0], o[1] + t * d[1], o[2] + t * d[2])
        dist = f(p)  # @line L4
        if record is not None:
            record.append(t)
        if dist < eps:  # @line L5
            return t
        t = t + dist  # @line L6
    return None  # @line L7


def lipschitz_scaled(f, lam):
    """Turn a function with Lipschitz bound lam into a signed distance bound (Hart, Theorem 1)."""
    return lambda p: f(p) / lam
