# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nn-descent/. The authors are listed in prov/264YR6.jsonl.

import math
import random
from typing import Callable, Sequence


def _update(lst: list[list], u: int, dist: float) -> int:
    """Insert (dist, u, new) into the k-list lst if u is absent and dist beats the worst; return 1 if inserted."""
    if any(e[1] == u for e in lst):
        return 0
    worst = max(range(len(lst)), key=lambda j: (lst[j][0], lst[j][1]))
    if (dist, u) >= (lst[worst][0], lst[worst][1]):
        return 0
    lst[worst] = [dist, u, True]
    return 1


def nn_descent(points: Sequence, k: int, d: Callable = math.dist, rho: float | None = None,
               delta: float = 0.0, seed: int = 0, init=None, stats: dict | None = None) -> list[list[tuple[float, int]]]:
    """Approximate k-nearest-neighbor lists by NN-Descent (Dong, Charikar and Li), with local join.

    Returns, for each point, its list of (distance, index) pairs sorted by distance. rho is the sampling
    rate (None means no sampling); the loop stops when fewer than delta * n * k updates happen in a round.
    init, if given, is the list of initial neighbor indices of each point.
    """
    n = len(points)
    if not 0 <= k < n and n > 0:
        raise ValueError("need 0 <= k < n")
    rng = random.Random(seed)
    evals = 0

    def dist(i: int, j: int) -> float:
        nonlocal evals
        evals += 1
        return d(points[i], points[j])

    lists: list[list[list]] = []
    for v in range(n):  # @line L1
        nbrs = init[v] if init is not None else rng.sample([u for u in range(n) if u != v], k)
        lists.append([[dist(v, u), u, True] for u in nbrs])
    size = None if rho is None else max(1, math.ceil(rho * k))
    rounds = 0
    while True:  # @line L2
        rounds += 1
        old = [[e[1] for e in lists[v] if not e[2]] for v in range(n)]  # @line L3
        new = []
        for v in range(n):
            flagged = [e for e in lists[v] if e[2]]
            if size is not None and len(flagged) > size:
                flagged = rng.sample(flagged, size)
            for e in flagged:
                e[2] = False  # @line L4
            new.append([e[1] for e in flagged])
        rold = [[] for _ in range(n)]  # @line L5
        rnew = [[] for _ in range(n)]
        for v in range(n):
            for u in old[v]:
                rold[u].append(v)
            for u in new[v]:
                rnew[u].append(v)
        c = 0
        for v in range(n):  # @line L6
            ro, rn = rold[v], rnew[v]
            if size is not None:
                ro = rng.sample(ro, min(size, len(ro)))
                rn = rng.sample(rn, min(size, len(rn)))
            o = list(dict.fromkeys(old[v] + ro))  # @line L7
            nw = list(dict.fromkeys(new[v] + rn))
            for a in range(len(nw)):  # @line L8
                u1 = nw[a]
                for u2 in nw[a + 1:] + [x for x in o if x not in nw]:
                    if u1 == u2:
                        continue
                    l = dist(u1, u2)  # @line L9
                    c += _update(lists[u1], u2, l) + _update(lists[u2], u1, l)  # @line L10
        if c <= delta * n * k:  # @line L11
            break
    if stats is not None:
        stats["evaluations"] = evals
        stats["rounds"] = rounds
    return [sorted((e[0], e[1]) for e in lists[v]) for v in range(n)]  # @line L12
