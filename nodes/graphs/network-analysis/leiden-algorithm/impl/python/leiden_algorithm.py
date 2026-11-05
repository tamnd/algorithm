# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leiden-algorithm/. The authors are listed in prov/K4ZNR0.jsonl.

from collections import deque
from fractions import Fraction


class _Graph:
    """A weighted graph on 0 .. k-1; members[x] is the set of original vertices that x stands for."""

    def __init__(self, adj: list[dict[int, Fraction]], loops: list[Fraction], members: list[list[int]]):
        self.k = len(adj)
        self.adj = adj
        self.loops = loops
        self.members = members
        self.degree = [loops[v] * 2 + sum(adj[v].values()) for v in range(self.k)]


def _gain(links: Fraction, tot: Fraction, deg: Fraction, total: Fraction) -> Fraction:
    """The modularity gain of putting a lone vertex into a community: k_{v,C}/W - tot(C) k_v / 2W^2."""
    return links / total - tot * deg / (2 * total * total)


def _best(h: _Graph, v: int, part: list[int], tot: list[Fraction], size: list[int], total: Fraction) -> int:
    """The community that line L11 picks for v; -1 stands for an empty community."""
    old = part[v]
    links: dict[int, Fraction] = {}
    for w, x in h.adj[v].items():
        links[part[w]] = links.get(part[w], Fraction(0)) + x
    best = old
    best_gain = _gain(links.get(old, Fraction(0)), tot[old] - h.degree[v], h.degree[v], total)
    for c in sorted(links):
        if c != old:
            g = _gain(links[c], tot[c], h.degree[v], total)
            if g > best_gain:
                best, best_gain = c, g
    if size[old] > 1 and best_gain < 0:
        return -1
    return best


def _move_nodes_fast(h: _Graph, part: list[int], total: Fraction) -> list[int]:
    """Queue-based local moving; part holds labels in 0 .. k-1 and is changed in place."""
    k = h.k
    tot = [Fraction(0)] * k
    size = [0] * k
    for v in range(k):
        tot[part[v]] += h.degree[v]
        size[part[v]] += 1
    queue = deque(range(k))  # @line L12
    queued = [True] * k
    while True:
        while queue:  # @line L13
            v = queue.popleft()  # @line L14
            queued[v] = False
            old = part[v]
            best = _best(h, v, part, tot, size, total)  # @line L15
            if best == -1:
                best = min(c for c in range(k) if size[c] == 0)
            tot[old] -= h.degree[v]  # @line L16
            size[old] -= 1
            part[v] = best
            tot[best] += h.degree[v]
            size[best] += 1
            if best != old:  # @line L17
                for w in sorted(h.adj[v]):
                    if part[w] != best and not queued[w]:
                        queue.append(w)
                        queued[w] = True
        pending = [v for v in range(k) if _best(h, v, part, tot, size, total) != part[v]]  # @line L18
        if not pending:
            return part  # @line L19
        for v in pending:
            queue.append(v)
            queued[v] = True


def _refine(h: _Graph, part: list[int], total: Fraction) -> list[int]:
    """The refined partition: merges of lone vertices inside each community, by labels in 0 .. k-1."""
    k = h.k
    label = list(range(k))  # @line L20
    rtot = h.degree[:]
    rsize = [1] * k
    eout = [sum((x for w, x in h.adj[v].items() if part[w] == part[v]), Fraction(0)) for v in range(k)]
    groups: dict[int, list[int]] = {}
    for v in range(k):
        groups.setdefault(part[v], []).append(v)
    for c in sorted(groups, key=lambda c: groups[c][0]):  # @line L21
        mem = groups[c]
        ctot = sum((h.degree[v] for v in mem), Fraction(0))
        good = [v for v in mem if eout[v] * 2 * total >= h.degree[v] * (ctot - h.degree[v])]  # @line L22
        for v in good:  # @line L23
            if rsize[label[v]] != 1:  # @line L24
                continue
            links: dict[int, Fraction] = {}
            for w, x in h.adj[v].items():
                if part[w] == c:
                    links[label[w]] = links.get(label[w], Fraction(0)) + x
            best, best_gain = -1, Fraction(0)
            for s in sorted(links):  # @line L25
                if eout[s] * 2 * total < rtot[s] * (ctot - rtot[s]):
                    continue
                g = _gain(links[s], rtot[s], h.degree[v], total)  # @line L26
                if best == -1 or g > best_gain:
                    best, best_gain = s, g
            if best != -1 and best_gain >= 0:  # @line L27
                eout[best] += eout[v] - 2 * links[best]
                rtot[best] += h.degree[v]
                rsize[best] += 1
                rsize[v] = 0
                label[v] = best
    return label  # @line L28


def _aggregate(h: _Graph, label: list[int], part: list[int]) -> tuple[_Graph, list[int]]:
    """One vertex per refined part; its community is the community of its members."""
    index: dict[int, int] = {}
    for v in range(h.k):
        if label[v] not in index:
            index[label[v]] = len(index)
    members: list[list[int]] = [[] for _ in index]
    adj: list[dict[int, Fraction]] = [{} for _ in index]
    loops = [Fraction(0)] * len(index)
    coarse: dict[int, int] = {}
    new_part = [0] * len(index)
    for v in range(h.k):
        a = index[label[v]]
        members[a] += h.members[v]
        loops[a] += h.loops[v]
        if part[v] not in coarse:
            coarse[part[v]] = len(coarse)
        new_part[a] = coarse[part[v]]
        for w, x in h.adj[v].items():
            b = index[label[w]]
            if a == b:
                if v < w:
                    loops[a] += x
            else:
                adj[a][b] = adj[a].get(b, Fraction(0)) + x
    return _Graph(adj, loops, members), new_part


def _flat(h: _Graph, part: list[int]) -> list[list[int]]:
    groups: dict[int, list[int]] = {}
    for v in range(h.k):
        groups.setdefault(part[v], []).extend(h.members[v])
    return sorted(sorted(g) for g in groups.values())


def leiden_algorithm(n: int, edges: list[tuple[int, int, int]]) -> list[list[int]]:
    """Return the communities that the Leiden algorithm finds by modularity, as sorted lists.

    edges holds triples (u, v, w) with integer weight w > 0 on the vertices
    0 .. n-1; a pair given twice adds its weights, and u == v is a self-loop.
    Deterministic: vertices in index order, a vertex keeps its community on
    ties, otherwise the smallest community id wins and an empty community comes
    last; the refinement merges a lone vertex greedily, which is the limit of
    the randomness parameter at 0. The passes repeat until a pass changes
    nothing. Arithmetic is exact. Every community returned is connected.
    """
    adj: list[dict[int, Fraction]] = [{} for _ in range(n)]
    loops = [Fraction(0)] * n
    total = Fraction(0)
    for u, v, w in edges:
        total += w
        if u == v:
            loops[u] += w
        else:
            adj[u][v] = adj[u].get(v, Fraction(0)) + w
            adj[v][u] = adj[v].get(u, Fraction(0)) + w
    g = _Graph(adj, loops, [[v] for v in range(n)])
    result = [[v] for v in range(n)]  # @line L1
    if total == 0:
        return result
    while True:  # @line L2
        previous = result  # @line L3
        h = g
        part = [0] * n
        for i, comm in enumerate(result):
            for v in comm:
                part[v] = i
        while True:  # @line L4
            part = _move_nodes_fast(h, part, total)  # @line L5
            if len(set(part)) == h.k:  # @line L6
                break
            label = _refine(h, part, total)  # @line L7
            h, part = _aggregate(h, label, part)  # @line L8, L9
        result = _flat(h, part)
        if result == previous:  # @line L10
            return result  # @line L11
