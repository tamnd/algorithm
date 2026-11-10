# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-cover-inapproximability/. The authors are listed in prov/DAHD4S.jsonl.

"""The maps behind the constant-factor hardness of vertex cover.

A graph is (n, edges) with vertices 0 .. n - 1 and edges as frozensets of two
vertices. A formula is a list of clauses in the DIMACS style. The brute-force
helpers are exponential and are for small instances only.
"""

from itertools import combinations, product

Edge = frozenset[int]


def complement(n: int, edges: set[Edge]) -> set[Edge]:
    """The complement graph: u and v are joined exactly when they are not joined in the input."""
    return {frozenset((u, v)) for u, v in combinations(range(n), 2) if frozenset((u, v)) not in edges}


def clique_to_vertex_cover(n: int, clique: list[int]) -> list[int]:
    """A clique C of G gives the vertex cover V minus C of the complement of G."""
    inside = set(clique)
    return [v for v in range(n) if v not in inside]


def vertex_cover_to_clique(n: int, cover: list[int]) -> list[int]:
    """A vertex cover K of the complement of G gives the clique V minus K of G."""
    inside = set(cover)
    return [v for v in range(n) if v not in inside]


def is_clique(vertices: list[int], edges: set[Edge]) -> bool:
    return all(frozenset((u, v)) in edges for u, v in combinations(vertices, 2))


def is_vertex_cover(vertices: list[int], edges: set[Edge]) -> bool:
    inside = set(vertices)
    return all(e & inside for e in edges)


def min_vertex_cover_size(n: int, edges: set[Edge]) -> int:
    """tau(G) by branch and bound: some end of each edge is in the cover.

    The search keeps an explicit stack, so it does not recurse.
    """
    adj = [0] * n
    for e in edges:
        u, v = tuple(e)
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    best = n
    stack = [(0, 0)]  # (mask of chosen vertices, number chosen)
    while stack:
        chosen, size = stack.pop()
        if size >= best:
            continue
        u = next((x for x in range(n) if not chosen >> x & 1 and adj[x] & ~chosen), None)
        if u is None:
            best = size
            continue
        rest = adj[u] & ~chosen
        # Either u is in the cover, or all its uncovered neighbours are.
        stack.append((chosen | rest, size + bin(rest).count("1")))
        stack.append((chosen | 1 << u, size + 1))
    return best


def max_clique_size(n: int, edges: set[Edge]) -> int:
    """omega(G) by trying sets of shrinking size."""
    for k in range(n, 0, -1):
        for s in combinations(range(n), k):
            if is_clique(list(s), edges):
                return k
    return 0


def sat_to_vertex_cover(clauses: list[tuple[int, ...]]) -> tuple[int, set[Edge]]:
    """The composed map: the clause-literal graph of the formula, read as a vertex cover instance.

    One vertex for each literal of each clause; edges inside each clause and
    between complementary literals. Its maximum independent set is the largest
    number of clauses that one assignment satisfies, so its minimum vertex cover
    is the number of vertices minus that number.
    """
    labels = [(j, l) for j, c in enumerate(clauses) for l in c]
    edges = set()
    for u, v in combinations(range(len(labels)), 2):
        (ju, lu), (jv, lv) = labels[u], labels[v]
        if ju == jv or lu == -lv:
            edges.add(frozenset((u, v)))
    return len(labels), edges


def max_satisfied(clauses: list[tuple[int, ...]], num_vars: int) -> int:
    best = 0
    for bits in product((False, True), repeat=num_vars):
        count = sum(1 for c in clauses if any(bits[abs(l) - 1] == (l > 0) for l in c))
        best = max(best, count)
    return best
