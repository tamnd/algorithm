# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/girvan-newman-algorithm/. The authors are listed in prov/G0RYGC.jsonl.

from collections import deque
from fractions import Fraction


def _components(n: int, adj: list[set[int]]) -> list[list[int]]:
    seen = [False] * n
    comps = []
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        comp = [s]
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for w in adj[u]:
                if not seen[w]:
                    seen[w] = True
                    comp.append(w)
                    queue.append(w)
        comps.append(sorted(comp))
    return comps


def _modularity(n: int, edges: list[tuple[int, int]], part: list[list[int]]) -> Fraction:
    m = len(edges)
    if m == 0:
        return Fraction(0)
    label = [0] * n
    for i, comp in enumerate(part):
        for v in comp:
            label[v] = i
    inside = [0] * len(part)
    degsum = [0] * len(part)
    for u, v in edges:
        degsum[label[u]] += 1
        degsum[label[v]] += 1
        if label[u] == label[v]:
            inside[label[u]] += 1
    return sum(
        (Fraction(inside[i], m) - Fraction(degsum[i], 2 * m) ** 2 for i in range(len(part))),
        Fraction(0),
    )


def edge_betweenness(n: int, adj: list[set[int]]) -> dict[tuple[int, int], Fraction]:
    """Exact edge betweenness over unordered pairs, keyed by (u, v) with u < v."""
    b = {(u, v): Fraction(0) for u in range(n) for v in adj[u] if u < v}  # @line L10
    for s in range(n):  # @line L11
        dist = [-1] * n  # @line L12
        sigma = [0] * n
        dist[s] = 0
        sigma[s] = 1
        order = []
        queue = deque([s])
        while queue:
            u = queue.popleft()
            order.append(u)
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    queue.append(w)
                if dist[w] == dist[u] + 1:
                    sigma[w] += sigma[u]
        delta = [Fraction(0)] * n  # @line L13
        for w in reversed(order):  # @line L14
            for v in adj[w]:  # @line L15
                if dist[v] == dist[w] - 1:
                    c = Fraction(sigma[v], sigma[w]) * (1 + delta[w])  # @line L16
                    b[(min(v, w), max(v, w))] += c
                    delta[v] += c
    for e in b:  # @line L17
        b[e] /= 2
    return b  # @line L18


def girvan_newman_algorithm(
    n: int, edges: list[tuple[int, int]]
) -> tuple[list[list[int]], list[list[list[int]]]]:
    """Return (best, levels) for an undirected simple graph on 0 .. n-1.

    levels lists the partitions into connected components seen while edges of
    largest betweenness are removed one by one, ties broken by the smallest
    (u, v) with u < v; best is the first level of largest modularity in the
    original graph. Each partition is a sorted list of sorted lists.
    Time O(m n (n + m)), extra space O(n + m) besides the levels.
    """
    edges = sorted({(min(u, v), max(u, v)) for u, v in edges if u != v})
    adj = [set() for _ in range(n)]  # @line L1
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    part = _components(n, adj)
    levels = [part]
    best, best_q = part, _modularity(n, edges, part)
    remaining = len(edges)
    while remaining > 0:  # @line L2
        b = edge_betweenness(n, adj)  # @line L3
        top = max(b.values())  # @line L4
        u, v = min(e for e, x in b.items() if x == top)
        adj[u].discard(v)  # @line L5
        adj[v].discard(u)
        remaining -= 1
        comps = _components(n, adj)
        if len(comps) > len(part):  # @line L6
            part = comps  # @line L7
            levels.append(part)
            q = _modularity(n, edges, part)  # @line L8
            if q > best_q:
                best, best_q = part, q
    return best, levels  # @line L9
