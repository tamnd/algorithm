# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-dynamic-controllability/. The authors are listed in prov/KN0N0A.jsonl.

"""Morris's 2006 O(N^4) dynamic controllability check for STNUs.

An STNU has time points 0 .. n - 1. A requirement link (u, v, lo, hi)
asks lo <= t[v] - t[u] <= hi; lo may be None (no lower bound) and hi may
be None (no upper bound). A contingent link (a, c, x, y) says that
t[c] - t[a] is chosen by nature in [x, y], with 0 <= x <= y. The
contingent points must be distinct.

The semantics is the one of Morris (CP 2006): a decision may depend on
the contingent durations observed in the past or at the present instant.
"""

from typing import Dict, List, Optional, Tuple

Req = Tuple[int, int, Optional[int], Optional[int]]
Cont = Tuple[int, int, int, int]
# Edge key (source, target, label). label is None for an ordinary edge,
# or the index of a contingent link for an upper-case edge.
Key = Tuple[int, int, Optional[int]]


def _tighten(edges: Dict[Key, int], key: Key, w: int) -> bool:
    old = edges.get(key)
    if old is None or w < old:
        edges[key] = w
        return True
    return False


def _bellman_ford(n: int, edges: Dict[Key, int]) -> Optional[List[int]]:
    """Potential h with h[v] <= h[u] + w for every edge, or None on a negative cycle."""
    h = [0] * n
    arcs = [(u, v, w) for (u, v, _), w in edges.items()]
    for _ in range(n):
        changed = False
        for u, v, w in arcs:
            if h[u] + w < h[v]:
                h[v] = h[u] + w
                changed = True
        if not changed:
            return h
    return None


def _propagate(n: int, edges: Dict[Key, int], h: List[int], start: int,
               own: int) -> Dict[Key, int]:
    """Shortest allowed paths from start; return the moat ends.

    Allowed edges are ordinary edges and upper-case edges whose label is not
    own. A node is expanded only if its distance is non-negative. The result
    maps (node, label of last edge) to a negative distance.
    """
    out: Dict[int, List[Tuple[int, Optional[int], int]]] = {v: [] for v in range(n)}
    for (u, v, lab), w in edges.items():
        if lab != own:
            out[u].append((v, lab, w))
    inf = float("inf")
    red = [inf] * n  # distance in the reweighted graph
    red[start] = 0
    done = [False] * n
    moats: Dict[Key, int] = {}
    for _ in range(n):
        u = -1
        for v in range(n):
            if not done[v] and red[v] < inf and (u < 0 or red[v] < red[u]):
                u = v
        if u < 0:
            break
        done[u] = True
        du = red[u] + h[u] - h[start]  # true distance from start
        if du < 0:
            continue  # a moat end: the path stops here
        for v, lab, w in out[u]:
            dv = du + w
            if dv < 0:
                key = (start, v, lab)
                if key not in moats or dv < moats[key]:
                    moats[key] = dv
            r = red[u] + w + h[u] - h[v]
            if r < red[v]:
                red[v] = r
    return moats


def morris_dc(n: int, reqs: List[Req], conts: List[Cont]) -> bool:
    """Return True if the STNU is dynamically controllable.

    Precondition: integer bounds, 0 <= x <= y for each contingent link, and
    distinct contingent points. Cost: O(K * N^3) time with N = n + K nodes
    after the normal form, O(N^2 + K * N) space for the edges.
    """
    # @line L1 normal form: move each lower bound x > 0 onto a new executable point
    reqs = list(reqs)
    norm: List[Cont] = []
    for a, c, x, y in conts:
        if x > 0:
            a2 = n
            n += 1
            reqs.append((a, a2, x, x))
            norm.append((a2, c, 0, y - x))
        else:
            norm.append((a, c, 0, y))
    k = len(norm)
    # @line L2 labelled distance graph
    edges: Dict[Key, int] = {}
    for u, v, lo, hi in reqs:
        if hi is not None:
            _tighten(edges, (u, v, None), hi)
        if lo is not None:
            _tighten(edges, (v, u, None), -lo)
    lower: List[Tuple[int, int, int]] = []  # (a, c, index of the link)
    for i, (a, c, _, y) in enumerate(norm):
        _tighten(edges, (a, c, None), y)
        _tighten(edges, (c, a, None), 0)
        lower.append((a, c, i))
        _tighten(edges, (c, a, i), -y)
    # @line L3 rounds
    for rnd in range(k + 1):
        # @line L4 AllMax projection: ordinary and upper-case edges, labels dropped
        h = _bellman_ford(n, edges)
        # @line L5
        if h is None:
            return False
        # @line L6
        if rnd == k:
            return True
        found: Dict[Key, int] = {}
        # @line L7 each lower-case edge a --c:0--> c
        for a, c, i in lower:
            # @line L8 forward over breach-free, lower-case-free paths, stop at the first drop
            for (_, v, lab), d in _propagate(n, edges, h, c, i).items():
                # @line L9 the reduced edge from a, labelled as the moat edge
                _tighten(found, (a, v, lab), d)
        # @line L10 add the new edges after the round
        for key, w in found.items():
            if key[0] != key[1] or w < 0:
                _tighten(edges, key, w)
    return True
