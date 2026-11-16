# SPDX-License-Identifier: MIT
# Shared helper of the pc1 complexity pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small undirected graphs for the tests of the vertex cover pages.

A graph is a list of edges (u, v) with u != v. Only the edges matter for a
vertex cover, so isolated vertices are not stored. The functions here are
test helpers: a brute-force vertex cover oracle and generators of all small
graphs, up to isomorphism where the full labeled count is too large.
"""

import itertools
import random
from collections.abc import Hashable, Iterator, Sequence

Edge = tuple[Hashable, Hashable]


def min_vertex_cover(edges: Sequence[Edge]) -> set[Hashable]:
    """Return a least vertex cover, by brute force over vertex sets.

    The vertices are those that appear in an edge, at most about 20 of them.
    A set is independent when it holds no edge; a least cover is the
    complement of a largest independent set. Time O(2^n) for n vertices.
    """
    names = sorted({x for e in edges for x in e}, key=repr)
    index = {x: i for i, x in enumerate(names)}
    n = len(names)
    adj = [0] * n
    for u, v in edges:
        a, b = index[u], index[v]
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    independent = bytearray(1 << n)
    independent[0] = 1
    best, best_mask = 0, 0
    for mask in range(1, 1 << n):
        low = (mask & -mask).bit_length() - 1
        rest = mask & (mask - 1)
        if independent[rest] and not adj[low] & rest:
            independent[mask] = 1
            size = mask.bit_count()
            if size > best:
                best, best_mask = size, mask
    return {names[i] for i in range(n) if not best_mask >> i & 1}


def min_vertex_cover_size(edges: Sequence[Edge]) -> int:
    """Return the least size of a vertex cover, by brute force."""
    return len(min_vertex_cover(edges))


def is_vertex_cover(edges: Sequence[Edge], cover: set[Hashable]) -> bool:
    """Return True if each edge has an endpoint in cover."""
    return all(u in cover or v in cover for u, v in edges)


def labeled_graphs(n: int) -> Iterator[list[tuple[int, int]]]:
    """Yield every graph on the vertices 0, ..., n-1, as an edge list (2^(n(n-1)/2) graphs)."""
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield [pairs[i] for i in range(len(pairs)) if mask >> i & 1]


def _canonical(n: int, adj: list[int]) -> int:
    """Return a code that is equal for two graphs exactly when they are isomorphic.

    The vertices are split into classes by their degree and the sorted degrees
    of their neighbors. The classes are put in a fixed order, and the code is
    the least edge code over the orders that permute each class.
    """
    deg = [a.bit_count() for a in adj]
    key = [(deg[v], tuple(sorted(deg[u] for u in range(n) if adj[v] >> u & 1))) for v in range(n)]
    classes: dict[tuple, list[int]] = {}
    for v in range(n):
        classes.setdefault(key[v], []).append(v)
    groups = [classes[c] for c in sorted(classes)]
    pair_bit = {}
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            pair_bit[i, j] = bit
            bit += 1
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if adj[u] >> v & 1]
    best = -1
    for choice in itertools.product(*(itertools.permutations(g) for g in groups)):
        pos = {}
        for block in choice:
            for v in block:
                pos[v] = len(pos)
        code = 0
        for u, v in edges:
            a, b = pos[u], pos[v]
            if a > b:
                a, b = b, a
            code |= 1 << pair_bit[a, b]
        if best < 0 or code < best:
            best = code
    return best


def graphs_up_to_isomorphism(n: int) -> list[list[tuple[int, int]]]:
    """Return one graph on the vertices 0, ..., n-1 from each isomorphism class.

    The classes are built by adding a vertex with every set of neighbors to
    each class on n - 1 vertices. The counts are 1, 2, 4, 11, 34, 156 and 1044
    for n = 1 to 7. Use n at most 7.
    """
    reps: list[list[int]] = [[]]  # one graph with 0 vertices, as adjacency masks
    for size in range(1, n + 1):
        seen: dict[int, list[int]] = {}
        for adj in reps:
            for nbrs in range(1 << (size - 1)):
                new = [a | ((nbrs >> v & 1) << (size - 1)) for v, a in enumerate(adj)] + [nbrs]
                code = _canonical(size, new)
                if code not in seen:
                    seen[code] = new
        reps = list(seen.values())
    return [[(u, v) for u in range(n) for v in range(u + 1, n) if adj[u] >> v & 1] for adj in reps]


def random_graph(n: int, p: float, rng: random.Random) -> list[tuple[int, int]]:
    """Return a random graph on 0, ..., n-1 where each edge appears with probability p."""
    return [(u, v) for u, v in itertools.combinations(range(n), 2) if rng.random() < p]
