# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locally-dominant-matching/. The authors are listed in prov/EHBHSK.jsonl.

"""Locally dominant matching, simulated round by round.

Each unmatched vertex points to its heaviest edge to an unmatched neighbour.
An edge pointed to by both its ends is locally dominant and joins the
matching. Ties in weight are broken by the edge index, so the keys
(w, index) are distinct. The result is the greedy matching in decreasing
key order, a 1/2-approximation of the maximum weight matching.

Precondition: edges is a list of triples (u, v, w) with 0 <= u, v < n and
w a number. Self-loops are ignored. Parallel edges are allowed.
Cost: each adjacency list is sorted once by decreasing key, O(m log m) work.
After that, each vertex moves a pointer forward along its sorted list, and
each matched vertex tells its neighbours once, so the rounds cost O(n + m)
work in total. A round has O(log n) span.
"""

import math


class Cost:
    """Counters for work, span and rounds."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0


def locally_dominant_matching(
    n: int, edges: list[tuple[int, int, float]], cost: Cost | None = None
) -> list[int]:
    """Return the indices of the matched edges, sorted."""
    c = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 2)))
    adj: list[list[tuple[float, int, int]]] = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        if u != v:
            adj[u].append((w, i, v))
            adj[v].append((w, i, u))
    for a in adj:
        a.sort(reverse=True)  # @line L1 (each list by decreasing key (w, index))
    c.work += n + sum(len(a) * max(1, math.ceil(math.log2(len(a) + 1))) for a in adj)
    c.span += lg * lg
    mate = [-1] * n
    ptr = [0] * n
    cand = [-1] * n  # the index of the edge v points to, or -1
    matched: list[int] = []
    check = [v for v in range(n) if adj[v]]  # @line L2 (the vertices whose pointer must be set)
    while check:  # @line L3 (a last pass may find that no edge is left; it is not counted as a round)
        for v in check:  # @line L4 (in parallel)
            a = adj[v]
            while ptr[v] < len(a) and mate[a[ptr[v]][2]] != -1:
                ptr[v] += 1
                c.work += 1
            cand[v] = a[ptr[v]][1] if ptr[v] < len(a) else -1  # @line L5 (the heaviest live edge)
        in_check = set(check)
        new = []
        for v in check:  # @line L6 (an edge pointed to by both ends is locally dominant)
            i = cand[v]
            if i != -1:
                u, x, _ = edges[i]
                other = x if u == v else u
                if cand[other] == i and (other not in in_check or v < other):
                    new.append((v, other, i))
        c.rounds += 1 if new else 0
        for v, u, i in new:  # @line L7
            mate[v], mate[u] = u, v
            matched.append(i)
        nxt = set()
        for v, u, _ in new:  # @line L8 (tell the neighbours that pointed to a matched vertex)
            for x in (v, u):
                for _, i, y in adj[x]:
                    if mate[y] == -1 and cand[y] == i:
                        nxt.add(y)
                c.work += len(adj[x])
        c.work += 3 * len(check) + 2 * len(new)
        c.span += 3 * lg
        check = sorted(nxt)  # @line L9
    return sorted(matched)  # @line L10
