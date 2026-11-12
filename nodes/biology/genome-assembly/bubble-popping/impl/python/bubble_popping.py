# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bubble-popping/. The authors are listed in prov/ZPJBHM.jsonl.

"""Bubble popping in an edge-centric de Bruijn graph, in the style of SPAdes bulge removal.

The graph is a map from each k-mer (an edge from its prefix to its suffix) to
its count in the reads. The unitigs are taken in increasing order of mean
count. A unitig P from u to w is popped (its edges are deleted) when there is
another path Q from u to w in the graph of unitigs such that P and Q both
have at most max_len edges, their lengths differ by at most max_diff, and the
mean count of Q is at least the mean count of P. Q is a shortest such path,
and among the shortest ones it has the largest total count.
"""

import heapq
from fractions import Fraction


def _graph(edges: dict[str, int]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    out: dict[str, list[str]] = {}
    inn: dict[str, list[str]] = {}
    for x in sorted(edges):
        out.setdefault(x[:-1], []).append(x)
        inn.setdefault(x[:-1], [])
        inn.setdefault(x[1:], []).append(x)
        out.setdefault(x[1:], [])
    return out, inn


def unitigs(edges: dict[str, int]) -> list[list[str]]:
    """Return the unitigs that start at a non-simple vertex (isolated cycles are left out)."""
    out, inn = _graph(edges)

    def simple(v: str) -> bool:
        return len(inn[v]) == 1 and len(out[v]) == 1

    paths = []
    for u in sorted(out):
        if not simple(u):
            for e in out[u]:
                path = [e]
                while simple(path[-1][1:]):
                    path.append(out[path[-1][1:]][0])
                paths.append(path)
    return paths


def alternative(
    paths: list[list[str]], counts: dict[str, int], skip: int
) -> tuple[int, int, list[int]] | None:
    """Return (edges, total count, unitig indices) of the best path from the start to the end of paths[skip].

    The path uses unitigs other than paths[skip] and visits no vertex twice.
    Best means fewest edges, then largest total count. Return None if there is no path.
    """
    src, dst = paths[skip][0][:-1], paths[skip][-1][1:]
    adj: dict[str, list[int]] = {}
    for j, p in enumerate(paths):
        if j != skip:
            adj.setdefault(p[0][:-1], []).append(j)
    best: dict[str, tuple[int, int]] = {src: (0, 0)}
    back: dict[str, int] = {}
    heap = [(0, 0, src)]
    done: set[str] = set()
    while heap:  # @line L5
        length, neg, v = heapq.heappop(heap)
        if v in done:
            continue
        done.add(v)
        if v == dst and v != src:
            route = []
            while v != src:
                j = back[v]
                route.append(j)
                v = paths[j][0][:-1]
            return length, -neg, route[::-1]
        for j in adj.get(v, []):
            w = paths[j][-1][1:]
            key = (length + len(paths[j]), neg - sum(counts[x] for x in paths[j]))
            if w not in done and (w not in best or key < best[w]):
                best[w] = key
                back[w] = j
                heapq.heappush(heap, (key[0], key[1], w))
    return None


def find_bubble(counts: dict[str, int], max_len: int, max_diff: int) -> list[str] | None:
    """Return the first unitig, in increasing order of mean count, that can be popped."""
    paths = unitigs(counts)
    order = sorted(
        range(len(paths)),
        key=lambda j: (Fraction(sum(counts[x] for x in paths[j]), len(paths[j])), paths[j]),
    )
    for j in order:  # @line L3
        p = paths[j]
        if p[0][:-1] == p[-1][1:] or len(p) > max_len:  # @line L4
            continue
        alt = alternative(paths, counts, j)  # @line L5
        if alt is None:
            continue
        b, total, _ = alt
        cov_p = Fraction(sum(counts[x] for x in p), len(p))
        if b <= max_len and abs(b - len(p)) <= max_diff and Fraction(total, b) >= cov_p:  # @line L6
            return p  # @line L7
    return None


def bubble_popping(
    counts: dict[str, int], k: int, max_len: int | None = None, max_diff: int = 2
) -> dict[str, int]:
    """Return a copy of counts with bubbles popped. The default max_len is 2k edges."""
    if max_len is None:
        max_len = 2 * k
    g = dict(counts)
    while True:  # @line L1
        p = find_bubble(g, max_len, max_diff)  # @line L2
        if p is None:
            return g  # @line L9
        for x in p:  # @line L8
            del g[x]
