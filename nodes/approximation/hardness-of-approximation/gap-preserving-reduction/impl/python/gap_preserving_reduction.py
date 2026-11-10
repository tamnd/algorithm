# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gap-preserving-reduction/. The authors are listed in prov/YVSNYR.jsonl.

"""The gap-preserving reduction from MAX 3SAT to maximum independent set.

A formula is a list of clauses. A clause is a tuple of nonzero integers in the
DIMACS style: the literal v is the variable v, and -v is its negation.
Variables are 1 .. num_vars. The brute-force helpers are for small instances only.
"""

from itertools import product

Clause = tuple[int, ...]


def satisfied_count(clauses: list[Clause], assignment: dict[int, bool]) -> int:
    """The number of clauses that the assignment satisfies."""
    return sum(1 for c in clauses if any(assignment[abs(l)] == (l > 0) for l in c))


def max_satisfied(clauses: list[Clause], num_vars: int) -> int:
    """OPT of MAX SAT by trying all 2^num_vars assignments."""
    best = 0
    for bits in product((False, True), repeat=num_vars):
        a = {v + 1: bits[v] for v in range(num_vars)}
        best = max(best, satisfied_count(clauses, a))
    return best


def sat_to_independent_set(clauses: list[Clause]) -> tuple[list[tuple[int, int]], set[frozenset[int]]]:
    """The map f. One vertex (j, l) for each literal l of clause j.

    Two vertices are joined when they lie in the same clause, or when their
    literals are complementary. Returns the vertex labels and the edge set,
    with vertices numbered 0 .. len(labels) - 1.
    """
    labels = [(j, l) for j, c in enumerate(clauses) for l in c]
    edges: set[frozenset[int]] = set()
    for u in range(len(labels)):
        for v in range(u + 1, len(labels)):
            (ju, lu), (jv, lv) = labels[u], labels[v]
            if ju == jv or lu == -lv:
                edges.add(frozenset((u, v)))
    return labels, edges


def assignment_to_independent_set(clauses: list[Clause], assignment: dict[int, bool]) -> list[int]:
    """For each satisfied clause, take one vertex of a true literal of it."""
    labels, _ = sat_to_independent_set(clauses)
    chosen, done = [], set()
    for v, (j, l) in enumerate(labels):
        if j not in done and assignment[abs(l)] == (l > 0):
            chosen.append(v)
            done.add(j)
    return chosen


def independent_set_to_assignment(clauses: list[Clause], num_vars: int, independent: list[int]) -> dict[int, bool]:
    """The map g. Make each chosen literal true; set the other variables to False."""
    labels, _ = sat_to_independent_set(clauses)
    a = {v: False for v in range(1, num_vars + 1)}
    for v in independent:
        l = labels[v][1]
        a[abs(l)] = l > 0
    return a


def is_independent(vertices: list[int], edges: set[frozenset[int]]) -> bool:
    s = list(vertices)
    return all(frozenset((s[i], s[k])) not in edges for i in range(len(s)) for k in range(i + 1, len(s)))


def independent_sets(n: int, edges: set[frozenset[int]]) -> list[list[int]]:
    """All independent sets of a graph with n vertices, built one vertex at a time."""
    adj = [0] * n
    for e in edges:
        u, v = tuple(e)
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    out: list[list[int]] = []
    stack = [(0, 0, [])]  # next vertex to decide, mask of forbidden vertices, chosen vertices
    while stack:
        i, forbidden, chosen = stack.pop()
        if i == n:
            out.append(chosen)
            continue
        stack.append((i + 1, forbidden, chosen))
        if not forbidden >> i & 1:
            stack.append((i + 1, forbidden | adj[i], chosen + [i]))
    return out


def max_independent_set_size(n: int, edges: set[frozenset[int]]) -> int:
    return max(len(s) for s in independent_sets(n, edges))
