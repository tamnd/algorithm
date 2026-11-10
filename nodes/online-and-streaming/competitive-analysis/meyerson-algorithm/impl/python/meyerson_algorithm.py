# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meyerson-algorithm/. The authors are listed in prov/DW570S.jsonl.

import random
from typing import Callable, Hashable, Iterable, List, Tuple

Point = Hashable


def meyerson(points: Iterable[Point], dist: Callable[[Point, Point], float], f: float,
             rng: random.Random) -> Tuple[float, List[Point], List[Point]]:
    """Meyerson's randomized algorithm for online facility location, uniform facility cost f.

    points: the demand points in the order of arrival. dist: a metric on the points.
    For each point p, let delta be the distance from p to the nearest open facility.
    With probability min(delta / f, 1) the algorithm opens a facility at p and pays f;
    otherwise it assigns p to the nearest facility and pays delta.
    Returns (total cost, open facilities in the order of opening, the facility of each point).
    Each point takes O(|F|) time, where F is the set of open facilities.
    """
    if f <= 0:
        raise ValueError("the facility cost must be positive")
    facilities: List[Point] = []  # @line L1
    cost = 0
    served: List[Point] = []
    for p in points:  # @line L2
        nearest, delta = None, None
        for q in facilities:  # @line L3
            dq = dist(p, q)
            if delta is None or dq < delta:
                nearest, delta = q, dq
        if delta is None or rng.random() * f < delta:  # @line L4
            facilities.append(p)  # @line L5
            cost += f
            served.append(p)
        else:  # @line L6
            cost += delta  # @line L7
            served.append(nearest)
    return cost, facilities, served  # @line L8
