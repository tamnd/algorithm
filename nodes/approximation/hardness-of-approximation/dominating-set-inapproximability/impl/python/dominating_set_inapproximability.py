# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominating-set-inapproximability/. The authors are listed in prov/W53DKC.jsonl.
"""The two cost-preserving L-reductions between dominating set and set cover.

A graph is (n, edges) on vertices 0 .. n-1. A set system is (n, sets) on elements 0 .. n-1.
For small instances only: the exact solvers try every subset.
"""

from itertools import combinations


def closed_neighbourhoods(n: int, edges: list[tuple[int, int]]) -> list[frozenset[int]]:
    nbr = [{v} for v in range(n)]
    for u, v in edges:
        nbr[u].add(v)
        nbr[v].add(u)
    return [frozenset(s) for s in nbr]


def ds_to_sc(n: int, edges: list[tuple[int, int]]) -> tuple[int, list[frozenset[int]]]:
    """Dominating set to set cover: universe V, one set N[v] for each vertex v."""
    return n, closed_neighbourhoods(n, edges)


def cover_to_ds(cover: list[int]) -> list[int]:
    """A cover by the sets N[v], v in cover, is the dominating set `cover` itself."""
    return list(cover)


def sc_to_ds(n: int, sets: list[frozenset[int]]) -> tuple[int, list[tuple[int, int]]]:
    """Set cover to dominating set.

    Vertex j < m is the set S_j, and vertex m + e is the element e. The set vertices form a clique,
    and element e is joined to each set that holds it.
    """
    m = len(sets)
    edges = list(combinations(range(m), 2))
    edges += [(j, m + e) for j in range(m) for e in sorted(sets[j])]
    return m + n, edges


def ds_to_cover(n: int, sets: list[frozenset[int]], dom: list[int]) -> list[int]:
    """Map a dominating set of sc_to_ds(n, sets) back to a cover with at most as many sets."""
    m = len(sets)
    out = set()
    for v in dom:
        if v < m:
            out.add(v)
        else:
            e = v - m
            out.add(next(j for j in range(m) if e in sets[j]))
    return sorted(out)


def is_cover(n: int, sets: list[frozenset[int]], chosen: list[int]) -> bool:
    return set().union(*(sets[j] for j in chosen)) == set(range(n)) if chosen else n == 0


def is_dominating(n: int, edges: list[tuple[int, int]], dom: list[int]) -> bool:
    nb = closed_neighbourhoods(n, edges)
    return set().union(*(nb[v] for v in dom)) == set(range(n)) if dom else n == 0


def min_cover(n: int, sets: list[frozenset[int]]) -> int:
    for size in range(len(sets) + 1):
        for c in combinations(range(len(sets)), size):
            if is_cover(n, sets, list(c)):
                return size
    raise ValueError("some element is in no set")


def domination_number(n: int, edges: list[tuple[int, int]]) -> int:
    return min_cover(*ds_to_sc(n, edges))
