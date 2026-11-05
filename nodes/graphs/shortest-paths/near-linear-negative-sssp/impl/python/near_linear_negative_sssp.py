# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/near-linear-negative-sssp/. The authors are listed in prov/KXQB8V.jsonl.

"""Negative-weight SSSP by scaling, low-diameter decomposition and ElimNeg.

This follows the structure of Bernstein, Nanongkai and Wulff-Nilsen (2022):
SPMAIN scales the weights, SCALEDOWN halves the most negative weight with a
potential, and ELIMNEG is the Dijkstra and Bellman-Ford hybrid. The low-diameter
decomposition here is a simple random ball carving. Correctness does not depend
on the decomposition; only the proven running time does.
"""

import heapq
import math
import random


class NegativeCycle(Exception):
    """Raised inside the recursion when a negative cycle is found."""


def _sccs(vs, arcs):
    """Strongly connected components of (vs, arcs), in topological order."""
    adj = {v: [] for v in vs}
    for u, v, _ in arcs:
        adj[u].append(v)
    index, low, on, stack, comps = {}, {}, set(), [], []
    counter = 0
    for root in vs:
        if root in index:
            continue
        work = [(root, iter(adj[root]))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            nxt = next(it, None)
            if nxt is not None:
                if nxt not in index:
                    index[nxt] = low[nxt] = counter
                    counter += 1
                    stack.append(nxt)
                    on.add(nxt)
                    work.append((nxt, iter(adj[nxt])))
                elif nxt in on:
                    low[v] = min(low[v], index[nxt])
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    x = stack.pop()
                    on.discard(x)
                    comp.append(x)
                    if x == v:
                        break
                comps.append(comp)
    comps.reverse()
    return comps


def _ldd(vs, arcs, diameter, rng):
    """Random ball carving on nonnegative weights. Returns the set of cut arcs."""
    out_adj = {v: [] for v in vs}
    in_adj = {v: [] for v in vs}
    for i, (u, v, w) in enumerate(arcs):
        out_adj[u].append((v, w, i))
        in_adj[v].append((u, w, i))
    left = set(vs)
    order = list(vs)
    rng.shuffle(order)
    p = min(1.0, 4 * math.log(len(vs) + 2) / max(diameter, 1))
    cut = set()
    for c in order:
        if c not in left:
            continue
        r = 0
        while r < diameter and rng.random() >= p:
            r += 1
        forward = rng.random() < 0.5
        adj = out_adj if forward else in_adj
        dist = {c: 0}
        heap = [(0, c)]
        ball = set()
        while heap:
            d, x = heapq.heappop(heap)
            if x in ball or d > dist[x]:
                continue
            ball.add(x)
            for y, w, _ in adj[x]:
                if y in left and d + w <= r and d + w < dist.get(y, math.inf):
                    dist[y] = d + w
                    heapq.heappush(heap, (d + w, y))
        for x in ball:
            for y, _, i in adj[x]:
                if y in left and y not in ball:
                    cut.add(i)
        left -= ball
    return cut


def _elim_neg(vs, arcs):
    """Distances from a virtual source with 0-arcs to every vertex (ELIMNEG)."""
    # @line L15
    pos = {v: [] for v in vs}
    neg = {v: [] for v in vs}
    for u, v, w in arcs:
        (neg if w < 0 else pos)[u].append((v, w))
    d = {v: 0 for v in vs}
    heap = [(0, v) for v in vs]
    heapq.heapify(heap)
    rounds = 0
    # @line L16
    while heap:
        # @line L17
        rounds += 1
        if rounds > len(vs):
            raise NegativeCycle
        # @line L18
        marked = set()
        while heap:
            dv, v = heapq.heappop(heap)
            if dv > d[v]:
                continue
            marked.add(v)
            for x, w in pos[v]:
                if dv + w < d[x]:
                    d[x] = dv + w
                    heapq.heappush(heap, (d[x], x))
        # @line L19
        for v in marked:
            for x, w in neg[v]:
                if d[v] + w < d[x]:
                    d[x] = d[v] + w
                    heapq.heappush(heap, (d[x], x))
    # @line L20
    return d


def _scale_down(vs, arcs, delta, b, rng):
    """Return phi with w(u, v) + phi(u) - phi(v) >= -b, given w >= -2b."""
    # @line L7
    arcs_b = [(u, v, w + b if w < 0 else w) for u, v, w in arcs]
    phi2 = {v: 0 for v in vs}
    # @line L8
    if delta > 2 and len(vs) > 1:
        # @line L9
        cut = _ldd(vs, [(u, v, max(0, w)) for u, v, w in arcs_b], delta * b // 4, rng)
        kept = [a for i, a in enumerate(arcs) if i not in cut]
        # @line L10
        comps = _sccs(vs, kept)
        where = {v: j for j, comp in enumerate(comps) for v in comp}
        # @line L11
        phi1 = {}
        for comp in comps:
            inner = set(comp)
            sub = [(u, v, w) for u, v, w in arcs if u in inner and v in inner]
            phi1.update(_scale_down(comp, sub, delta // 2, b, rng))
        # @line L12
        best = [0] * len(comps)
        for u, v, w in arcs_b:
            if where[u] < where[v]:
                best[where[v]] = min(best[where[v]], w + phi1[u] - phi1[v])
        level, acc = [0] * len(comps), 0
        for j in range(len(comps)):
            acc += best[j]
            level[j] = acc
        phi2 = {v: phi1[v] + level[where[v]] for v in vs}
    # @line L13
    reduced = [(u, v, w + phi2[u] - phi2[v]) for u, v, w in arcs_b]
    psi = _elim_neg(vs, reduced)
    # @line L14
    return {v: phi2[v] + psi[v] for v in vs}


def near_linear_negative_sssp(n: int, edges: list[tuple[int, int, int]], s: int, seed: int = 0) -> list[int | None] | None:
    """Single-source shortest paths with integer weights of any sign.

    Vertices are 0 .. n-1 and edges lists arcs (u, v, w) with integer w. Returns the
    list of distances from s, with None for vertices not reachable from s, or None
    when a negative cycle is reachable from s. The result does not depend on seed;
    only the work done does. Raises ValueError on a weight that is not an integer.
    """
    for _, _, w in edges:
        if not isinstance(w, int) or isinstance(w, bool):
            raise ValueError(f"weight {w!r} is not an integer")
    rng = random.Random(seed)
    # @line L1
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append(v)
    seen = [False] * n
    seen[s] = True
    stack = [s]
    while stack:
        u = stack.pop()
        for v in out[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    vs = [v for v in range(n) if seen[v]]
    arcs = [(u, v, w) for u, v, w in edges if seen[u] and seen[v]]
    k = len(vs)
    # @line L2
    worst = max([0] + [-w for _, _, w in arcs])
    bar = [(u, v, 2 * k * w) for u, v, w in arcs]
    big = 1
    while big < 2 * k * max(1, worst):
        big *= 2
    phi = {v: 0 for v in vs}
    try:
        # @line L3
        b = big
        while b > 1:
            b //= 2
            # @line L4
            reduced = [(u, v, w + phi[u] - phi[v]) for u, v, w in bar]
            psi = _scale_down(vs, reduced, k, b, rng)
            phi = {v: phi[v] + psi[v] for v in vs}
    except NegativeCycle:
        return None
    # @line L5
    star = [(u, v, w + phi[u] - phi[v] + 1, w0) for (u, v, w), (_, _, w0) in zip(bar, arcs)]
    if any(ws < 0 for _, _, ws, _ in star):
        return None
    # @line L6
    adj = [[] for _ in range(n)]
    for u, v, ws, w0 in star:
        adj[u].append((v, ws, w0))
    key = [math.inf] * n
    dist: list[int | None] = [None] * n
    key[s], dist[s] = 0, 0
    done = [False] * n
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, ws, w0 in adj[u]:
            if not done[v] and d + ws < key[v]:
                key[v] = d + ws
                dist[v] = dist[u] + w0
                heapq.heappush(heap, (key[v], v))
    return dist
