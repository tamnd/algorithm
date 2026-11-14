# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gear-generation-by-enveloping/. The authors are listed in prov/X68YYQ.jsonl.

"""Planar gear generation: the tooth profile as the envelope of a tool in relative motion.

A tool curve r_c(u) with unit normal n_c(u) is given in the tool frame. A generating
motion maps the tool frame into the gear frame by p_g = R(a(psi)) p_c + t(psi), where
psi is the turn of the gear. The equation of meshing

    f(u, psi) = (R(a) n_c(u)) . (a'(psi) J R(a) r_c(u) + t'(psi)) = 0

says that the tool point moves along the tool surface relative to the gear, so it is
a point of the envelope. For each u, its roots psi give the generated points.
"""

from __future__ import annotations

import math
from typing import Callable, List, Tuple

Vec = Tuple[float, float]


def rot(a: float, p: Vec) -> Vec:
    """R(a) p, the rotation by a counterclockwise."""
    c, s = math.cos(a), math.sin(a)
    return (c * p[0] - s * p[1], s * p[0] + c * p[1])


def perp(p: Vec) -> Vec:
    """J p, the rotation by +90 degrees."""
    return (-p[1], p[0])


def dot(p: Vec, q: Vec) -> float:
    return p[0] * q[0] + p[1] * q[1]


def inv(alpha: float) -> float:
    """The involute function tan(alpha) - alpha."""
    return math.tan(alpha) - alpha


def involute(rb: float, t: float) -> Vec:
    """The involute of the circle of radius rb about the origin, started at (rb, 0), at roll angle t."""
    c, s = math.cos(t), math.sin(t)
    return (rb * (c + t * s), rb * (s - t * c))


class Motion:
    """A planar generating motion: angle a(psi), translation t(psi) and their derivatives."""

    def __init__(self, a, da, t, dt):
        self.a, self.da, self.t, self.dt = a, da, t, dt

    def apply(self, psi: float, p: Vec) -> Vec:
        """Tool point p in the gear frame at the gear turn psi."""
        q, tr = rot(self.a(psi), p), self.t(psi)
        return (q[0] + tr[0], q[1] + tr[1])


def rack_motion(r: float) -> Motion:
    """A rack whose pitch line rolls on the pitch circle of radius r without slip.

    Fixed frame: gear center at the origin, rack pitch line y = r, pitch point (0, r).
    When the gear turns by psi counterclockwise, the rack moves by -r psi along x.
    """
    def t(psi):
        return rot(-psi, (-r * psi, r))

    def dt(psi):
        a, b = perp(t(psi)), rot(-psi, (-r, 0.0))
        return (-a[0] + b[0], -a[1] + b[1])

    return Motion(lambda psi: -psi, lambda psi: -1.0, t, dt)


def shaper_motion(r: float, rc: float) -> Motion:
    """A pinion cutter of pitch radius rc whose pitch circle rolls outside the gear pitch circle of radius r."""
    k = r / rc
    oc = (0.0, r + rc)

    def t(psi):
        return rot(-psi, oc)

    def dt(psi):
        a = perp(t(psi))
        return (-a[0], -a[1])

    return Motion(lambda psi: -(k + 1.0) * psi, lambda psi: -(k + 1.0), t, dt)


def rack_flank(phi: float):
    """The straight flank of a rack cutter through the pitch point, at the angle phi to the normal of the pitch line.

    Returns r_c(u) and the unit normal n_c(u) in the rack frame, whose origin is on the pitch line.
    """
    s, c = math.sin(phi), math.cos(phi)
    return (lambda u: (u * s, u * c)), (lambda u: (c, -s))


def shaper_flank(rc: float, phi: float):
    """An involute flank of a pinion cutter with pitch radius rc, through the pitch point (0, -rc) of its frame.

    It has the same normal there as rack_flank(phi), so both tools cut the same gear flank.
    """
    rb = rc * math.cos(phi)
    beta = -math.pi / 2 + inv(phi)

    def curve(t):
        x, y = involute(rb, t)
        return rot(beta, (x, -y))

    def normal(t):
        return rot(beta, (math.sin(t), math.cos(t)))

    return curve, normal


def meshing(curve, normal, motion: Motion, u: float, psi: float) -> float:
    """f(u, psi): the normal part of the velocity of the tool point relative to the gear. Cost O(1)."""
    a = motion.a(psi)
    n = rot(a, normal(u))
    v = perp(rot(a, curve(u)))
    dt = motion.dt(psi)
    return dot(n, (motion.da(psi) * v[0] + dt[0], motion.da(psi) * v[1] + dt[1]))


def _bisect(f, lo: float, hi: float, flo: float, tol: float) -> float:
    """A root of f in [lo, hi], given that f(lo) = flo and f(hi) have opposite signs."""
    while hi - lo > tol * (1 + abs(lo)):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0:
            return mid
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def envelope(curve: Callable[[float], Vec], normal: Callable[[float], Vec], motion: Motion,
             us: List[float], psi_lo: float, psi_hi: float, cells: int = 64,
             tol: float = 1e-14, keep=None) -> List[Tuple[float, float, Vec]]:
    """Points of the generated profile: for each u, every root psi of the equation of meshing in [psi_lo, psi_hi].

    keep(u, psi, p), if given, is the branch check: it returns False for a point that the tool removes
    at some other position. Precondition: psi_lo < psi_hi; two roots in the same cell of width
    (psi_hi - psi_lo)/cells are missed.
    Cost O(len(us) * (cells + log(1/tol))) evaluations of f, plus the calls to keep.
    Returns (u, psi, point in the gear frame).
    """
    out = []
    h = (psi_hi - psi_lo) / cells
    for u in us:  # @line L1
        def f(psi):
            return meshing(curve, normal, motion, u, psi)  # @line L2
        roots = []
        x0, f0 = psi_lo, f(psi_lo)
        for i in range(1, cells + 1):  # @line L3
            x1 = psi_hi if i == cells else psi_lo + i * h
            f1 = f(x1)
            if f0 == 0:
                roots.append(x0)
            elif f0 * f1 < 0:
                roots.append(_bisect(f, x0, x1, f0, tol))  # @line L4
            x0, f0 = x1, f1
        if f0 == 0:
            roots.append(x0)
        for psi in roots:
            p = motion.apply(psi, curve(u))  # @line L5
            if keep is None or keep(u, psi, p):  # @line L6
                out.append((u, psi, p))
    return out


def rack_clearance(phi: float, motion: Motion, p: Vec, psi_lo: float, psi_hi: float,
                   tip: float, samples: int = 400) -> float:
    """How far the gear point p stays outside one rack tooth over the sampled turns in [psi_lo, psi_hi].

    The tooth, in the rack frame, is the set of points q with n_c . q < 0 (behind the flank of
    rack_flank(phi)) and q_y > -tip (above the tip line, tip = addendum of the cutter).
    A negative result means that the tooth covers p at some sampled turn, so p is cut away.
    Cost O(samples).
    """
    _, normal = rack_flank(phi)
    n0 = normal(0.0)
    best = math.inf
    for i in range(samples + 1):
        psi = psi_lo + (psi_hi - psi_lo) * i / samples
        a, t = motion.a(psi), motion.t(psi)
        q = rot(-a, (p[0] - t[0], p[1] - t[1]))
        best = min(best, max(dot(n0, q), -tip - q[1]))
    return best
