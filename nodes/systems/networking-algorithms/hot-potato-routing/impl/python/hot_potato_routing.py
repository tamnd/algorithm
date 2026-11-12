# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hot-potato-routing/. The authors are listed in prov/P3PE21.jsonl.

"""Hot-potato routing: each router sends traffic for a destination to the
egress router with the least interior (IGP) cost, among the egresses whose
BGP routes tie before the interior-cost step of the decision process.

nearest_egress() is a multi-source Dijkstra from all egresses at once, with
labels (distance, egress id) compared in that order, so it also applies the
tie-break by the lowest router id. One run gives every router its egress,
its distance to it and its IGP next hop.
"""

import heapq


def nearest_egress(graph, egresses):
    """graph: dict router -> dict neighbour -> positive cost (symmetric).
    Returns label, nxt: label[v] = (distance, egress); nxt[v] = the
    neighbour toward that egress (None at an egress or if unreachable)."""
    inf = float("inf")
    label = {v: (inf, None) for v in graph}  # @line L1
    nxt = {v: None for v in graph}
    pq = []
    for e in egresses:
        label[e] = (0, e)  # @line L2
        heapq.heappush(pq, (0, e, e))
    done = set()
    while pq:  # @line L3
        d, e, u = heapq.heappop(pq)  # @line L4
        if u in done or (d, e) != label[u]:
            continue
        done.add(u)
        for v, w in graph[u].items():  # @line L5
            cand = (d + w, e)  # @line L6
            if v not in done and cand < label[v]:
                label[v] = cand  # @line L7
                nxt[v] = u
                heapq.heappush(pq, (cand[0], cand[1], v))
    return label, nxt  # @line L8


def choose_egresses(routes):
    """routes: dict egress -> the tuple of BGP attributes compared before the
    interior cost, as a key where smaller is better (for example
    (-local_pref, len(as_path), origin, med_rank, not_ebgp)). Returns the
    egresses whose key is least: the set that hot-potato routing picks from."""
    best = min(routes.values())
    return sorted(e for e, k in routes.items() if k == best)


def dijkstra(graph, s):
    dist, pq = {s: 0}, [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u].items():
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def nearest_egress_brute(graph, egresses):
    """One Dijkstra per egress, then the least (distance, id) per router."""
    dists = {e: dijkstra(graph, e) for e in egresses}
    out = {}
    for v in graph:
        opts = [(dists[e][v], e) for e in egresses if v in dists[e]]
        out[v] = min(opts) if opts else (float("inf"), None)
    return out
