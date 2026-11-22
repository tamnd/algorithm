# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-packet-marking/. The authors are listed in prov/EZNZ9R.jsonl.

"""Edge sampling of Savage, Wetherall, Karlin and Anderson (SIGCOMM 2000, Section 4.3).

Routers are abstract names on a synthetic path or tree. A mark is a tuple
(start, end, distance). No packet is built and no network is touched.
"""

from fractions import Fraction
from itertools import combinations
from math import log
from typing import Hashable, Iterable

Router = Hashable
Mark = tuple[Router | None, Router | None, int]
Edge = tuple[Router, Router, int]

DIST_MAX = 31  # the 5-bit distance field of Section 5.2 saturates here


def mark(w: Mark, r: Router, p: float, u: float) -> Mark:
    """Router r forwards a packet with mark w; u is its uniform draw in [0, 1).

    Precondition: 0 < p < 1 and 0 <= u < 1. Cost: O(1).
    """
    start, end, distance = w
    # @line L1 (the caller draws u)
    if u < p:  # @line L2
        return (r, None, 0)  # @line L3
    if distance == 0:  # @line L4
        end = r  # @line L5
    return (start, end, min(distance + 1, DIST_MAX))  # @line L6


def send(path: list[Router], w0: Mark, p: float, us: Iterable[float]) -> Mark:
    """The mark that reaches the victim after the routers of path, in order.

    path[0] is the router next to the attacker and path[-1] the router next to
    the victim; w0 is the mark the attacker wrote. Cost: O(len(path)).
    """
    w = w0
    for r, u in zip(path, us):
        w = mark(w, r, p, u)
    return w


def reconstruct(marks: Iterable[Mark], v: Router) -> set[Edge]:
    """Keep the edges that chain to the victim v with consistent distances.

    An edge (x, y, k) is kept when y = v and k = 0, or when a kept edge
    (y, z, k - 1) exists. Cost: O(m + e log e) for m marks and e distinct edges.
    """
    edges: set[Edge] = set()  # @line L7
    for start, end, distance in marks:  # @line L8
        if start is None:
            continue
        if distance == 0:  # @line L9
            edges.add((start, v, 0))
        elif end is not None:  # @line L10
            edges.add((start, end, distance))
    kept: set[Edge] = set()  # @line L11
    level = {v}
    by_dist: dict[int, list[Edge]] = {}
    for e in edges:
        by_dist.setdefault(e[2], []).append(e)
    for k in range(0, max(by_dist, default=-1) + 1):
        nxt = set()
        for x, y, dist in by_dist.get(k, []):
            if y in level:
                kept.add((x, y, dist))
                nxt.add(x)
        level = nxt
        if not level:
            break
    return kept  # @line L12


def paths(kept: set[Edge], v: Router) -> set[tuple[Router, ...]]:
    """All maximal chains in the kept edges, each listed from far end to v."""
    into: dict[Router, list[Router]] = {}
    for x, y, _ in kept:
        into.setdefault(y, []).append(x)
    out: set[tuple[Router, ...]] = set()
    stack: list[tuple[Router, ...]] = [(v,)]
    while stack:
        chain = stack.pop()
        preds = into.get(chain[0], [])
        if not preds and len(chain) > 1:
            out.add(chain)
        for x in preds:
            if x not in chain:
                stack.append((x,) + chain)
    return out


def edge_probabilities(d: int, p: Fraction) -> list[Fraction]:
    """q[j] = p (1 - p)^j: the chance that the edge of the router j + 1 hops from the victim arrives."""
    return [p * (1 - p) ** j for j in range(d)]


def expected_packets(d: int, p: Fraction) -> Fraction:
    """Exact E[packets until all d edges have arrived], by inclusion and exclusion.

    E = sum over nonempty S of (-1)^(|S|+1) / sum_{j in S} q_j. Cost: O(2^d d).
    """
    q = edge_probabilities(d, p)
    total = Fraction(0)
    for size in range(1, d + 1):
        sign = 1 if size % 2 else -1
        for s in combinations(q, size):
            total += sign / sum(s)
    return total


def harmonic_bound(d: int, p: float) -> float:
    """H_d / (p (1 - p)^(d - 1)), an upper bound on expected_packets."""
    return sum(1 / i for i in range(1, d + 1)) / (p * (1 - p) ** (d - 1))


def savage_estimate(d: int, p: float) -> float:
    """ln(d) / (p (1 - p)^(d - 1)), the estimate printed by Savage et al."""
    return log(d) / (p * (1 - p) ** (d - 1))
