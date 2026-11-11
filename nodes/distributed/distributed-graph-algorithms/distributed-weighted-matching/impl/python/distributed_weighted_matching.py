# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-weighted-matching/. The authors are listed in prov/B1T5JR.jsonl.

"""Weighted matching in the synchronous LOCAL model, with rounds counted.

class_matching rounds every weight down to a power of 1 + eps and handles the
weight classes from the heaviest down. In each class, it computes a maximal
matching of the class edges whose ends are both still free, with random
priorities: an edge joins when its priority is the least among the live
class edges at both of its ends (Luby's MIS algorithm on the line graph).
locally_heaviest is the locally dominant rule, given here only to count its
rounds for comparison.

Precondition: adj is an undirected simple graph; w maps each edge (u, v) with
u < v to a positive weight; all nodes know the range of weight classes.
Cost: class_matching returns a maximal matching of weight at least
OPT / (2 (1 + eps)). It takes O(log m) phases of 3 rounds per class with high
probability, so O(log_(1+eps) W * log n) rounds, where W is the ratio of the
largest to the smallest weight. locally_heaviest returns a matching of
weight at least OPT / 2, but it can take n / 2 rounds.
"""

import math
import random

Edge = tuple[int, int]


def edges_of(adj: list[list[int]]) -> list[Edge]:
    """The edges (u, v) with u < v."""
    return [(u, v) for u in range(len(adj)) for v in adj[u] if u < v]


def is_maximal_matching(adj: list[list[int]], mate: list[int]) -> bool:
    """True if mate is a matching (mate[v] = -1 when v is unmatched) and no edge can be added."""
    for v, nbrs in enumerate(adj):
        if mate[v] >= 0 and (mate[v] not in nbrs or mate[mate[v]] != v):
            return False
        if mate[v] < 0 and any(mate[u] < 0 for u in nbrs):
            return False
    return True


def matching_weight(mate: list[int], w: dict[Edge, float]) -> float:
    return sum(w[(v, mate[v])] for v in range(len(mate)) if v < mate[v])


def class_matching(
    adj: list[list[int]], w: dict[Edge, float], eps: float, rng: random.Random
) -> tuple[list[int], int]:
    """Return (mate, rounds) for the weight-class algorithm."""
    n = len(adj)
    mate = [-1] * n
    rounds = 0
    cls = {e: math.floor(math.log(x) / math.log(1 + eps)) for e, x in w.items()}
    for c in sorted(set(cls.values()), reverse=True):
        while True:
            live = [e for e in edges_of(adj) if cls[e] == c and mate[e[0]] < 0 and mate[e[1]] < 0]
            if not live:
                break
            # round 1: the smaller end of each live class edge draws a priority and sends it
            prio = {e: (rng.random(), e) for e in live}
            # round 2: every node sends the least priority of its live class edges
            least: dict[int, tuple[float, Edge]] = {}
            for e, p in prio.items():
                for x in e:
                    if x not in least or p < least[x]:
                        least[x] = p
            # round 3: an edge that is least at both ends joins, and its ends announce it
            for (u, v), p in prio.items():
                if least[u] == p and least[v] == p:
                    mate[u], mate[v] = v, u
            rounds += 3
    return mate, rounds


def locally_heaviest(adj: list[list[int]], w: dict[Edge, float]) -> tuple[list[int], int]:
    """Return (mate, rounds): each round, every edge that is the heaviest live edge at both ends joins."""
    n = len(adj)
    mate = [-1] * n
    rounds = 0
    while True:
        live = [e for e in edges_of(adj) if mate[e[0]] < 0 and mate[e[1]] < 0]
        if not live:
            return mate, rounds
        best: dict[int, tuple[float, Edge]] = {}
        for e in live:
            key = (w[e], e)
            for x in e:
                if x not in best or key > best[x]:
                    best[x] = key
        for u, v in live:
            if best[u][1] == (u, v) and best[v][1] == (u, v):
                mate[u], mate[v] = v, u
        rounds += 1


def max_weight_matching_brute(adj: list[list[int]], w: dict[Edge, float]) -> float:
    """Exact maximum matching weight by exhaustive search; for small graphs only."""
    n = len(adj)

    def best(v: int, used: frozenset[int]) -> float:
        while v < n and v in used:
            v += 1
        if v == n:
            return 0.0
        result = best(v + 1, used | {v})
        for u in adj[v]:
            if u not in used:
                result = max(result, w[(min(u, v), max(u, v))] + best(v + 1, used | {u, v}))
        return result

    return best(0, frozenset())
