# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l-reduction/. The authors are listed in prov/VK0B3P.jsonl.

"""Brute-force checks of the two constants of an L-reduction.

An L-reduction (f, g, alpha, beta) from A to B must satisfy, for each instance x
of A and each feasible solution y of f(x):
  (L1) OPT_B(f(x)) <= alpha * OPT_A(x)
  (L2) |OPT_A(x) - c_A(g(y))| <= beta * |OPT_B(f(x)) - c_B(y)|
The helpers below enumerate all solutions, so they are for small instances only.
"""

from fractions import Fraction
from itertools import combinations, product
from typing import Iterable

Edge = frozenset[int]


def check_l_reduction(opt_a: int, opt_b: int, pairs: Iterable[tuple[int, int]]) -> tuple[Fraction, Fraction]:
    """Return the least alpha and beta that this one instance needs.

    pairs holds (c_B(y), c_A(g(y))) for every feasible y of f(x).
    """
    alpha = Fraction(opt_b, opt_a) if opt_a else (Fraction(0) if opt_b == 0 else Fraction(10**9))
    beta = Fraction(0)
    for cb, ca in pairs:
        gap_b, gap_a = abs(opt_b - cb), abs(opt_a - ca)
        if gap_b == 0:
            if gap_a:
                return alpha, Fraction(10**9)  # no beta works
        else:
            beta = max(beta, Fraction(gap_a, gap_b))
    return alpha, beta


# ---- MAX 3SAT to maximum independent set (alpha = beta = 1)

def clause_graph(clauses: list[tuple[int, ...]]) -> tuple[list[tuple[int, int]], set[Edge]]:
    labels = [(j, l) for j, c in enumerate(clauses) for l in c]
    edges = {frozenset((u, v)) for u, v in combinations(range(len(labels)), 2)
             if labels[u][0] == labels[v][0] or labels[u][1] == -labels[v][1]}
    return labels, edges


def satisfied(clauses: list[tuple[int, ...]], a: dict[int, bool]) -> int:
    return sum(1 for c in clauses if any(a[abs(l)] == (l > 0) for l in c))


def is_to_assignment(labels: list[tuple[int, int]], num_vars: int, s: Iterable[int]) -> dict[int, bool]:
    a = {v: False for v in range(1, num_vars + 1)}
    for v in s:
        a[abs(labels[v][1])] = labels[v][1] > 0
    return a


def independent_sets(n: int, edges: set[Edge]) -> list[tuple[int, ...]]:
    adj = [0] * n
    for e in edges:
        u, v = tuple(e)
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    out = []
    stack = [(0, 0, ())]
    while stack:
        i, banned, chosen = stack.pop()
        if i == n:
            out.append(chosen)
            continue
        stack.append((i + 1, banned, chosen))
        if not banned >> i & 1:
            stack.append((i + 1, banned | adj[i], chosen + (i,)))
    return out


def sat_to_mis_constants(clauses: list[tuple[int, ...]], num_vars: int) -> tuple[Fraction, Fraction]:
    opt_a = max(satisfied(clauses, {v + 1: b[v] for v in range(num_vars)})
                for b in product((False, True), repeat=num_vars))
    labels, edges = clause_graph(clauses)
    sets = independent_sets(len(labels), edges)
    opt_b = max(len(s) for s in sets)
    pairs = [(len(s), satisfied(clauses, is_to_assignment(labels, num_vars, s))) for s in sets]
    return check_l_reduction(opt_a, opt_b, pairs)


# ---- maximum independent set and minimum vertex cover in graphs of degree at most B

def vertex_covers(n: int, edges: set[Edge]) -> list[tuple[int, ...]]:
    return [s for k in range(n + 1) for s in combinations(range(n), k) if all(e & set(s) for e in edges)]


def mis_to_vc_constants(n: int, edges: set[Edge]) -> tuple[Fraction, Fraction]:
    """f is the identity and g(C) = V minus C. A is MIS-B, B is VC-B."""
    sets = independent_sets(n, edges)
    covers = vertex_covers(n, edges)
    opt_a = max(len(s) for s in sets)
    opt_b = min(len(c) for c in covers)
    return check_l_reduction(opt_a, opt_b, [(len(c), n - len(c)) for c in covers])


def vc_to_mis_constants(n: int, edges: set[Edge]) -> tuple[Fraction, Fraction]:
    """f is the identity and g(S) = V minus S. A is VC-B, B is MIS-B."""
    sets = independent_sets(n, edges)
    covers = vertex_covers(n, edges)
    opt_a = min(len(c) for c in covers)
    opt_b = max(len(s) for s in sets)
    return check_l_reduction(opt_a, opt_b, [(len(s), n - len(s)) for s in sets])


def max_degree(n: int, edges: set[Edge]) -> int:
    deg = [0] * n
    for e in edges:
        for v in e:
            deg[v] += 1
    return max(deg, default=0)


def random_bounded_degree_graph(rng, n: int, b: int, tries: int) -> set[Edge]:
    """Add random edges while both ends have degree below b."""
    deg = [0] * n
    edges: set[Edge] = set()
    for _ in range(tries):
        u, v = rng.sample(range(n), 2)
        e = frozenset((u, v))
        if e not in edges and deg[u] < b and deg[v] < b:
            edges.add(e)
            deg[u] += 1
            deg[v] += 1
    return edges
