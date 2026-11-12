# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graphical-model/. The authors are listed in prov/QJW75C.jsonl.

"""Graphical models on a few binary variables, by brute force.

A graphical model is a graph plus the distributions that factorize over
it. The module builds a joint distribution from directed (CPT) or
undirected (potential) factors, reads the conditional independences of a
distribution by enumeration, reads the independences that a graph
implies (separation for undirected graphs, d-separation for DAGs), and
enumerates all graphs on n nodes. With these, the tests check that a
v-structure has no undirected perfect map and a 4-cycle has no directed
perfect map.
"""

from fractions import Fraction
from itertools import combinations, product
from typing import Callable, Dict, FrozenSet, Iterable, List, Sequence, Set, Tuple

Assignment = Tuple[int, ...]
Statement = Tuple[int, int, FrozenSet[int]]


def joint_from_factors(n: int, factors: Iterable[Tuple[Sequence[int], Callable[..., Fraction]]]) -> Dict[Assignment, Fraction]:
    """Normalized product of factors over n binary variables.

    Each factor is (scope, f), where f takes the values of the scope
    variables. CPTs give a product that already sums to 1; potentials
    are divided by the partition function Z.
    """
    factors = list(factors)
    p = {}
    for x in product((0, 1), repeat=n):
        v = Fraction(1)
        for scope, f in factors:
            v *= f(*(x[i] for i in scope))
        p[x] = v
    z = sum(p.values())
    return {x: v / z for x, v in p.items()}


def marginal(p: Dict[Assignment, Fraction], keep: Sequence[int]) -> Dict[Assignment, Fraction]:
    out: Dict[Assignment, Fraction] = {}
    for x, v in p.items():
        k = tuple(x[i] for i in keep)
        out[k] = out.get(k, Fraction(0)) + v
    return out


def is_ci(p: Dict[Assignment, Fraction], a: int, b: int, z: Iterable[int]) -> bool:
    """a independent of b given z: p(a,b,z) p(z) = p(a,z) p(b,z) for all values."""
    z = sorted(z)
    pabz = marginal(p, [a, b] + z)
    paz = marginal(p, [a] + z)
    pbz = marginal(p, [b] + z)
    pz = marginal(p, z)
    for va, vb in product((0, 1), repeat=2):
        for vz in product((0, 1), repeat=len(z)):
            lhs = pabz.get((va, vb) + vz, 0) * pz.get(vz, 0)
            rhs = paz.get((va,) + vz, 0) * pbz.get((vb,) + vz, 0)
            if lhs != rhs:
                return False
    return True


def all_statements(n: int) -> List[Statement]:
    """All a _||_ b | Z with a < b single variables and Z a subset of the rest."""
    out = []
    for a, b in combinations(range(n), 2):
        rest = [i for i in range(n) if i not in (a, b)]
        for r in range(len(rest) + 1):
            for z in combinations(rest, r):
                out.append((a, b, frozenset(z)))
    return out


def independences(p: Dict[Assignment, Fraction], n: int) -> Set[Statement]:
    return {s for s in all_statements(n) if is_ci(p, s[0], s[1], s[2])}


def separated(adj: Dict[int, Set[int]], a: int, b: int, z: FrozenSet[int]) -> bool:
    """True if every path from a to b in the undirected graph meets z."""
    seen, stack = {a}, [a]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v == b:
                return False
            if v not in seen and v not in z:
                seen.add(v)
                stack.append(v)
    return True


def d_separated(parents: Dict[int, Set[int]], a: int, b: int, z: FrozenSet[int]) -> bool:
    """d-separation by the moralized ancestral graph criterion."""
    anc, stack = set(), [a, b, *z]
    while stack:
        u = stack.pop()
        if u not in anc:
            anc.add(u)
            stack.extend(parents[u])
    adj: Dict[int, Set[int]] = {u: set() for u in anc}
    for u in anc:
        ps = list(parents[u])
        for p in ps:
            adj[u].add(p)
            adj[p].add(u)
        for p, q in combinations(ps, 2):
            adj[p].add(q)
            adj[q].add(p)
    return separated(adj, a, b, z)


def undirected_independences(adj: Dict[int, Set[int]], n: int) -> Set[Statement]:
    return {s for s in all_statements(n) if separated(adj, s[0], s[1], s[2])}


def dag_independences(parents: Dict[int, Set[int]], n: int) -> Set[Statement]:
    return {s for s in all_statements(n) if d_separated(parents, s[0], s[1], s[2])}


def all_undirected_graphs(n: int) -> List[Dict[int, Set[int]]]:
    pairs = list(combinations(range(n), 2))
    graphs = []
    for mask in range(1 << len(pairs)):
        adj: Dict[int, Set[int]] = {i: set() for i in range(n)}
        for k, (u, v) in enumerate(pairs):
            if mask >> k & 1:
                adj[u].add(v)
                adj[v].add(u)
        graphs.append(adj)
    return graphs


def _acyclic(parents: Dict[int, Set[int]]) -> bool:
    indeg = {u: len(ps) for u, ps in parents.items()}
    children: Dict[int, List[int]] = {u: [] for u in parents}
    for u, ps in parents.items():
        for p in ps:
            children[p].append(u)
    queue = [u for u, d in indeg.items() if d == 0]
    seen = 0
    while queue:
        u = queue.pop()
        seen += 1
        for c in children[u]:
            indeg[c] -= 1
            if indeg[c] == 0:
                queue.append(c)
    return seen == len(parents)


def all_dags(n: int) -> List[Dict[int, Set[int]]]:
    """Every DAG on n labeled nodes: each pair is absent, u -> v, or v -> u."""
    pairs = list(combinations(range(n), 2))
    dags = []
    for choice in product(range(3), repeat=len(pairs)):
        parents: Dict[int, Set[int]] = {i: set() for i in range(n)}
        for c, (u, v) in zip(choice, pairs):
            if c == 1:
                parents[v].add(u)
            elif c == 2:
                parents[u].add(v)
        if _acyclic(parents):
            dags.append(parents)
    return dags
