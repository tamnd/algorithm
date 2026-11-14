# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cam-profile-synthesis/. The authors are listed in prov/59Q72X.jsonl.

"""Cam profile synthesis for translating followers by the inversion (envelope) method.

The cam turns counterclockwise by the angle theta. In the fixed frame the follower
moves along the line x = eps, and its roller center is at (eps, d0 + s(theta)). In
the frame of the cam, a fixed point p appears at R(-theta) p, so the roller centers
trace the pitch curve C(theta) = R(-theta) (eps, d0 + s), and the cam profile is the
envelope of the roller circles. A flat-faced follower has its face on the line
y = Rb + s, and the profile is the envelope of those lines.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple

Vec = Tuple[float, float]
Law = Callable[[float], Tuple[float, float, float, float]]

TWO_PI = 2.0 * math.pi


def dwell(x):
    """The dwell: f = 0 and all derivatives zero. Cost O(1)."""
    z = x - x
    return z, z, z, z


def harmonic(x):
    """Simple harmonic rise f = (1 - cos(pi x)) / 2 and its first three derivatives. Cost O(1)."""
    c, s, p = math.cos(math.pi * x), math.sin(math.pi * x), math.pi
    return (1 - c) / 2, p / 2 * s, p * p / 2 * c, -p ** 3 / 2 * s


def cycloidal(x):
    """Cycloidal rise f = x - sin(2 pi x) / (2 pi) and its first three derivatives. Cost O(1)."""
    t = 2 * math.pi * x
    return x - math.sin(t) / (2 * math.pi), 1 - math.cos(t), 2 * math.pi * math.sin(t), 4 * math.pi ** 2 * math.cos(t)


def poly345(x):
    """The 3-4-5 polynomial f = 10x^3 - 15x^4 + 6x^5. Exact for Fraction input. Cost O(1)."""
    return (10 * x ** 3 - 15 * x ** 4 + 6 * x ** 5, 30 * x ** 2 * (1 - x) ** 2,
            60 * x * (1 - x) * (1 - 2 * x), 60 - 360 * x + 360 * x * x)


def poly4567(x):
    """The 4-5-6-7 polynomial f = 35x^4 - 84x^5 + 70x^6 - 20x^7. Exact for Fraction input. Cost O(1)."""
    return (35 * x ** 4 - 84 * x ** 5 + 70 * x ** 6 - 20 * x ** 7, 140 * x ** 3 * (1 - x) ** 3,
            420 * x ** 2 * (1 - x) ** 2 * (1 - 2 * x), 840 * x * (1 - x) * (1 - 5 * x + 5 * x * x))


LAWS = {"dwell": dwell, "harmonic": harmonic, "cycloidal": cycloidal, "poly345": poly345, "poly4567": poly4567}


@dataclass(frozen=True)
class Segment:
    """One segment of the cam program: a law, the cam angle beta > 0 and the lift (negative for a return)."""

    law: str
    beta: float
    lift: float


class CamProgram:
    """A full cycle of segments whose angles sum to 2 pi and whose lifts sum to 0.

    Construction costs O(m) for m segments; svaj costs O(log m).
    """

    def __init__(self, segments: Sequence[Segment], tol: float = 1e-9):
        if not segments or any(g.beta <= 0 or g.law not in LAWS for g in segments):
            raise ValueError("each segment needs a known law and a positive angle")
        if abs(sum(g.beta for g in segments) - TWO_PI) > tol:  # @line L1
            raise ValueError("the segment angles must sum to 2 pi")
        if abs(sum(g.lift for g in segments)) > tol * (1 + sum(abs(g.lift) for g in segments)):
            raise ValueError("the lifts must return the follower to its start")
        self.segments = list(segments)
        self.starts: List[float] = []
        self.heights: List[float] = []
        theta, h = 0.0, 0.0
        for g in segments:
            self.starts.append(theta)
            self.heights.append(h)
            theta += g.beta
            h += g.lift

    def segment_at(self, theta: float) -> int:
        """Index i of the segment with start_i <= theta < start_{i+1}, theta taken mod 2 pi."""
        return max(0, bisect.bisect_right(self.starts, theta % TWO_PI) - 1)

    def eval_segment(self, i: int, x: float) -> Tuple[float, float, float, float]:
        """s, ds/dtheta, d2s/dtheta2 and d3s/dtheta3 of segment i at the local parameter x in [0, 1]."""
        g = self.segments[i]
        f, f1, f2, f3 = LAWS[g.law](x)
        b = g.beta
        return self.heights[i] + g.lift * f, g.lift * f1 / b, g.lift * f2 / (b * b), g.lift * f3 / (b ** 3)  # @line L5

    def svaj(self, theta: float) -> Tuple[float, float, float, float]:
        """Displacement and its first three derivatives with respect to the cam angle."""
        t = theta % TWO_PI
        i = self.segment_at(t)  # @line L4
        return self.eval_segment(i, (t - self.starts[i]) / self.segments[i].beta)


def rot_minus(theta: float, p: Vec) -> Vec:
    """R(-theta) p: a point fixed in the ground, seen from the cam turned by theta."""
    c, s = math.cos(theta), math.sin(theta)
    return (c * p[0] + s * p[1], -s * p[0] + c * p[1])


@dataclass(frozen=True)
class RollerSample:
    theta: float
    s: float
    pitch: Vec
    contact: Vec
    pressure_angle: float
    rho: float
    undercut: bool


def roller_sample(prog: CamProgram, theta: float, rb: float, rf: float, eps: float) -> RollerSample:
    """Pitch point, cam point, pressure angle and pitch radius of curvature at one cam angle.

    Precondition: rb > 0, rf >= 0, |eps| < rb + rf. Cost O(log m).
    rho is the signed radius of curvature of the pitch curve (positive where it is convex);
    the sample is flagged as undercut when 0 < rho <= rf.
    """
    rp = rb + rf  # @line L2
    if not (rb > 0 and rf >= 0 and abs(eps) < rp):
        raise ValueError("bad cam size")
    d0 = math.sqrt(rp * rp - eps * eps)
    s, s1, s2, _ = prog.svaj(theta)
    u, w = d0 + s, s1 - eps  # @line L6
    d = math.hypot(u, w)
    pitch = rot_minus(theta, (eps, u))  # @line L7
    contact = rot_minus(theta, (eps + rf * w / d, u - rf * u / d))  # @line L8
    phi = math.atan2(w, u)  # @line L9
    den = u * u + w * (w + s1) - u * s2
    rho = d ** 3 / den if den != 0 else math.inf  # @line L10
    return RollerSample(theta, s, pitch, contact, phi, rho, 0 < rho <= rf)  # @line L11


def roller_profile(prog: CamProgram, rb: float, rf: float, eps: float, n: int) -> List[RollerSample]:
    """Cam profile for a translating roller follower with offset eps, at n equal cam angles.

    Precondition: rb > 0, rf >= 0, |eps| < rb + rf, n >= 1. Cost O(m + n log m).
    """
    if n < 1:
        raise ValueError("n must be positive")
    return [roller_sample(prog, TWO_PI * k / n, rb, rf, eps) for k in range(n)]  # @line L3


@dataclass(frozen=True)
class FlatSample:
    theta: float
    s: float
    contact: Vec
    rho: float
    face_offset: float


def flat_sample(prog: CamProgram, theta: float, rb: float) -> FlatSample:
    """Cam point, radius of curvature and face offset of a flat-faced follower at one cam angle.

    Precondition: rb > 0. Cost O(log m).
    """
    if not rb > 0:
        raise ValueError("bad cam size")
    s, s1, s2, _ = prog.svaj(theta)  # @line L13
    q = rot_minus(theta, (s1, rb + s))  # @line L14
    rho = rb + s + s2  # @line L15
    return FlatSample(theta, s, q, rho, s1)  # @line L16


def flat_faced_profile(prog: CamProgram, rb: float, n: int) -> List[FlatSample]:
    """Cam profile for a translating flat-faced follower with its face square to its axis.

    Precondition: rb > 0, n >= 1. Cost O(m + n log m). The profile is valid when every rho > 0.
    """
    if n < 1:
        raise ValueError("n must be positive")
    return [flat_sample(prog, TWO_PI * k / n, rb) for k in range(n)]  # @line L12
