# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iso-scallop-toolpath/. The authors are listed in prov/MQ38PN.jsonl.

"""Iso-scallop toolpath for a ball end mill on a translational surface.

The surface is z = f(x), the same for every y, and the passes run along y.
So the problem lives in the xz plane: the profile is p(t) = (t, f(t)), its
upward unit normal is n(t), and a ball of radius r that touches the profile at
p(t) has its center at c(t) = p(t) + r n(t). Between two passes the tool
leaves a ridge whose top, the cusp, is the meeting point of the two tool
circles on the side of the surface. The scallop height is the distance from
the cusp to the profile.

Each next pass is placed so that the scallop height to the last pass is the
target h: a bracket is found by doubling a trial step, and then 60 bisection
steps close it. The bisection always keeps the side with height at most h,
so every pair of neighbouring passes has a computed scallop height of at
most h.

This module uses floats. The answer is a numeric root, not a sign, and the
tests compare it with closed forms and a brute force within a tolerance.
"""

import math

GOLDEN = (math.sqrt(5) - 1) / 2


class Profile:
    """A profile z = f(x) on [a, b] with its derivative df."""

    def __init__(self, f, df, a, b):
        if not a < b:
            raise ValueError("the domain must have a < b")
        self.f, self.df, self.a, self.b = f, df, a, b

    def point(self, t):
        return (t, self.f(t))

    def normal(self, t):
        d = self.df(t)
        k = math.hypot(d, 1.0)
        return (-d / k, 1.0 / k)

    def center(self, t, r):
        (x, z), (nx, nz) = self.point(t), self.normal(t)
        return (x + r * nx, z + r * nz)


def cusp(profile, r, t0, t1):
    """The meeting point of the two tool circles on the side of the surface, or None."""
    c0, c1 = profile.center(t0, r), profile.center(t1, r)  # @line L7
    dx, dy = c1[0] - c0[0], c1[1] - c0[1]
    d = math.hypot(dx, dy)
    if d >= 2 * r:
        return None  # the circles do not meet: a strip between the passes is not cut
    if d == 0:
        return profile.point(t0)
    m = ((c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2)
    k = math.sqrt(r * r - d * d / 4)
    px, py = -dy / d, dx / d
    n0, n1 = profile.normal(t0), profile.normal(t1)
    down = (-(n0[0] + n1[0]), -(n0[1] + n1[1]))
    s = 1.0 if px * down[0] + py * down[1] >= 0 else -1.0
    return (m[0] + s * k * px, m[1] + s * k * py)  # @line L8


def scallop(profile, r, t0, t1, iters=80):
    """The distance from the cusp between the passes t0 < t1 to the profile on [t0, t1]."""
    q = cusp(profile, r, t0, t1)
    if q is None:
        return math.inf

    def g(x):
        p = profile.point(x)
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    lo, hi = t0, t1  # golden-section search for the nearest profile point
    x1, x2 = hi - GOLDEN * (hi - lo), lo + GOLDEN * (hi - lo)
    g1, g2 = g(x1), g(x2)
    for _ in range(iters):
        if g1 <= g2:
            hi, x2, g2 = x2, x1, g1
            x1 = hi - GOLDEN * (hi - lo)
            g1 = g(x1)
        else:
            lo, x1, g1 = x1, x2, g2
            x2 = lo + GOLDEN * (hi - lo)
            g2 = g(x2)
    return math.sqrt(min(g1, g2, g(t0), g(t1)))  # @line L9


def next_pass(profile, r, h, t):
    """The next contact t' > t with scallop height h to the pass at t; requires scallop(t, b) > h."""
    b = profile.b
    step = math.sqrt(8 * r * h) / 2
    lo, hi = t, min(t + step, b)
    while scallop(profile, r, t, hi) <= h:  # @line L3
        lo, step = hi, 2 * step
        hi = min(t + step, b)
    for _ in range(60):  # @line L4
        mid = (lo + hi) / 2
        if scallop(profile, r, t, mid) <= h:
            lo = mid
        else:
            hi = mid
    if lo <= t:
        raise ValueError("the target height is too small to advance")
    return lo


def iso_scallop(profile, r, h):
    """The contact parameters of the passes, from a to b."""
    if r <= 0 or h <= 0:
        raise ValueError("r and h must be positive")
    t = profile.a  # @line L1
    passes = [t]
    while scallop(profile, r, t, profile.b) > h:  # @line L2
        t = next_pass(profile, r, h, t)
        passes.append(t)  # @line L5
    passes.append(profile.b)  # @line L6
    return passes


def cylinder_step(R, r, h, convex=True):
    """The closed-form angle between neighbouring contacts on a cylinder of radius R."""
    big, rho = (R + r, R + h) if convex else (R - r, R - h)
    return 2 * math.acos((big * big + rho * rho - r * r) / (2 * big * rho))
