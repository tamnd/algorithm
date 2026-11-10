# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lin-kernighan-helsgaun/. The authors are listed in prov/44V9MX.jsonl.
"""The candidate part of LKH: the 1-tree bound, subgradient ascent, alpha-nearness and alpha lists.

The search part is the Lin-Kernighan step of the lin-kernighan page (one 2-opt step at a time).
LKH itself uses sequential 5-opt basic steps; this file does not implement them.
"""

from typing import Sequence

EPS = 1e-12


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    n = len(tour)
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n)) if n > 1 else 0.0


def transformed(cost: Sequence[Sequence[float]], pi: Sequence[float]) -> list[list[float]]:
    n = len(cost)
    return [[cost[i][j] + pi[i] + pi[j] if i != j else 0.0 for j in range(n)] for i in range(n)]


def one_tree(d: Sequence[Sequence[float]], special: int = 0) -> tuple[float, list[tuple[int, int]]]:
    """A minimum 1-tree: a minimum spanning tree on the other cities (Prim) plus the two cheapest edges at special."""
    n = len(d)
    rest = [v for v in range(n) if v != special]
    root = rest[0]
    key = {v: d[root][v] for v in rest}
    link = {v: root for v in rest}
    inside = {root}
    edges = []
    while len(inside) < len(rest):
        v = min((u for u in rest if u not in inside), key=lambda u: (key[u], u))
        inside.add(v)
        edges.append((link[v], v))
        for u in rest:
            if u not in inside and d[v][u] < key[u]:
                key[u], link[u] = d[v][u], v
    first, second = sorted(rest, key=lambda u: (d[special][u], u))[:2]
    edges += [(special, first), (special, second)]
    return sum(d[u][v] for u, v in edges), edges


def degrees(n: int, edges: Sequence[tuple[int, int]]) -> list[int]:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return deg


def ascent(cost: Sequence[Sequence[float]], rounds: int = 100) -> tuple[float, list[float]]:
    """Subgradient ascent on w(pi) = L(T_pi) - 2 sum(pi), the Held-Karp 1-tree bound. Return (best w, its pi)."""
    n = len(cost)
    pi = [0.0] * n
    best_w, best_pi = float("-inf"), pi[:]
    length, _ = one_tree(cost)
    step = length / (10 * n) if n else 0.0
    for _ in range(rounds):
        length, edges = one_tree(transformed(cost, pi))
        w = length - 2 * sum(pi)
        if w > best_w + EPS:
            best_w, best_pi = w, pi[:]
        deg = degrees(n, edges)
        if all(x == 2 for x in deg):  # the 1-tree is a tour, so w is OPT
            break
        pi = [p + step * (x - 2) for p, x in zip(pi, deg)]
        step *= 0.95
    return best_w, best_pi


def alpha_values(d: Sequence[Sequence[float]], special: int = 0) -> list[list[float]]:
    """alpha(i, j) = L(minimum 1-tree that holds {i, j}) - L(minimum 1-tree)."""
    n = len(d)
    _, edges = one_tree(d, special)
    tree = {frozenset(e) for e in edges}
    adj: dict[int, list[int]] = {v: [] for v in range(n)}
    for u, v in edges:
        if special not in (u, v):
            adj[u].append(v)
            adj[v].append(u)
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        if i == special:
            continue
        beta = {i: float("-inf")}  # the largest edge on the tree path from i
        stack = [i]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in beta:
                    beta[v] = max(beta[u], d[u][v])
                    stack.append(v)
        for j in range(n):
            if j != i and j != special and frozenset((i, j)) not in tree:
                a[i][j] = d[i][j] - beta[j]
    second = max(d[special][u] for e in edges if special in e for u in e if u != special)
    for j in range(n):
        if j != special and frozenset((special, j)) not in tree:
            a[special][j] = a[j][special] = d[special][j] - second
    return a


def alpha_lists(cost: Sequence[Sequence[float]], k: int = 5, rounds: int = 100) -> list[list[int]]:
    """The k alpha-nearest cities of each city under the pi of the ascent; ties go to the smaller cost."""
    n = len(cost)
    _, pi = ascent(cost, rounds)  # @line L1
    d = transformed(cost, pi)
    a = alpha_values(d)  # @line L2
    return [sorted((j for j in range(n) if j != i), key=lambda j: (a[i][j], d[i][j], j))[:k] for i in range(n)]  # @line L3


def lk_search(cost, path, candidates, breadth=(5, 3)):
    """The Lin-Kernighan search of the lin-kernighan page, without the trace."""
    t1 = path[0]
    removed, added, best = {frozenset((path[0], path[-1]))}, set(), None

    def step(p, gain, depth):
        nonlocal best
        y, where, options = p[-1], {c: i for i, c in enumerate(p)}, []
        for z in candidates[y]:
            i = where[z]
            if i >= len(p) - 2:
                continue
            w, g = p[i + 1], gain - cost[y][z]
            if g > EPS and frozenset((y, z)) not in removed and frozenset((z, w)) not in added:
                options.append((cost[z][w] - cost[y][z], i, z, w, g))
        options.sort(reverse=True)
        for _, i, z, w, g in options[: breadth[depth] if depth < len(breadth) else 1]:
            new_path, new_gain = p[: i + 1] + p[i + 1 :][::-1], g + cost[z][w]
            close = new_gain - cost[w][t1]
            if close > EPS and (best is None or close > best[0] + EPS):
                best = (close, new_path)
            added.add(frozenset((y, z)))
            removed.add(frozenset((z, w)))
            if depth + 1 < len(p) and (best is None or new_gain > best[0] + EPS):
                step(new_path, new_gain, depth + 1)
            added.discard(frozenset((y, z)))
            removed.discard(frozenset((z, w)))
            if best is not None:
                return

    step(path, cost[path[0]][path[-1]], 0)
    return best


def lkh(cost: Sequence[Sequence[float]], tour: Sequence[int], k: int = 5) -> tuple[list[int], int]:
    """LK searches with the k alpha-nearest candidate lists until no search gains."""
    t, n = list(tour), len(tour)
    if n < 4:
        return t, 0
    candidates = alpha_lists(cost, min(k, n - 1))
    improvements = 0
    while True:  # @line L4
        found = None
        for start in range(n):
            ring = t[t.index(start) :] + t[: t.index(start)]
            for path in (ring[:1] + ring[1:][::-1], ring):  # @line L5
                found = lk_search(cost, path, candidates)
                if found is not None:
                    break
            if found is not None:
                break
        if found is None:
            return t, improvements  # @line L7
        t = found[1]  # @line L6
        improvements += 1
