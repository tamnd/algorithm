# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/periodic-boundary-conditions/. The authors are listed in prov/VY641R.jsonl.

import math
from typing import Callable

Point = list[float]


def wrap(r: Point, box: float) -> Point:
    """Put r back into the box [0, box)^d by adding a whole number of box lengths on each axis."""
    out = []
    for x in r:
        y = x - box * math.floor(x / box)  # @line L1
        out.append(0.0 if y >= box else y)
    return out


def minimum_image(ri: Point, rj: Point, box: float) -> Point:
    """The vector from the nearest periodic image of rj to ri, in a cubic box of side box."""
    d = [a - b for a, b in zip(ri, rj)]  # @line L2
    return [x - box * round(x / box) for x in d]  # @line L3


def distance(ri: Point, rj: Point, box: float) -> float:
    return math.sqrt(sum(x * x for x in minimum_image(ri, rj, box)))  # @line L4


def pair_energy(positions: list[Point], box: float, rc: float, phi: Callable[[float], float]) -> float:
    """The sum of phi over all pairs closer than rc, each through its nearest image.

    The cutoff must be at most half the box, so that each pair has at most one
    image within the cutoff.
    """
    if rc > box / 2:  # @line L5
        raise ValueError("the cutoff must be at most half the box")
    u = 0.0  # @line L6
    n = len(positions)
    for i in range(n):  # @line L6
        for j in range(i + 1, n):  # @line L6
            r = distance(positions[i], positions[j], box)  # @line L7
            if r < rc:  # @line L7
                u += phi(r)  # @line L7
    return u  # @line L8


def fcc_lattice(cells: int, a: float) -> list[Point]:
    """The 4 cells^3 sites of a face-centered cubic lattice with cubic cell side a, in a box of side cells * a."""
    basis = [(0.0, 0.0, 0.0), (0.5, 0.5, 0.0), (0.5, 0.0, 0.5), (0.0, 0.5, 0.5)]
    out = []
    for i in range(cells):
        for j in range(cells):
            for k in range(cells):
                for b in basis:
                    out.append([(i + b[0]) * a, (j + b[1]) * a, (k + b[2]) * a])
    return out
