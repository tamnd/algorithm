# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-random-field/. The authors are listed in prov/KQP2ZG.jsonl.

"""Discrete Markov random fields by brute force.

An MRF is an undirected graph with a nonnegative potential on each of a
list of cliques. p(x) = prod_C psi_C(x_C) / Z. The module computes Z and
the joint by enumeration, tests the pairwise, local and global Markov
properties of any joint distribution with respect to a graph, and
rebuilds clique potentials from a positive distribution by the Mobius
inversion of the Hammersley-Clifford theorem.
"""

from fractions import Fraction
from itertools import combinations, product
from typing import Callable, Dict, FrozenSet, List, Sequence, Set, Tuple

Assignment = Tuple[int, ...]
Joint = Dict[Assignment, Fraction]


class MarkovRandomField:
    def __init__(self, card: Sequence[int], potentials: Sequence[Tuple[Sequence[int], Dict[Assignment, Fraction]]]):
        """card[i]: number of values of variable i; potentials: (scope, table)
        pairs, the table mapping each value tuple of the scope to a value >= 0."""
        self.card = list(card)
        self.potentials = [(tuple(s), t) for s, t in potentials]
        n = len(card)
        self.adj: Dict[int, Set[int]] = {i: set() for i in range(n)}
        for scope, table in self.potentials:
            if any(v < 0 for v in table.values()):
                raise ValueError("potentials must be nonnegative")
            for u, v in combinations(scope, 2):
                self.adj[u].add(v)
                self.adj[v].add(u)

    def assignments(self):
        return product(*(range(c) for c in self.card))

    def unnormalized(self, x: Assignment) -> Fraction:
        v = Fraction(1)
        for scope, table in self.potentials:
            v *= table[tuple(x[i] for i in scope)]
        return v

    def partition_function(self) -> Fraction:
        return sum((self.unnormalized(x) for x in self.assignments()), Fraction(0))

    def joint(self) -> Joint:
        z = self.partition_function()
        return {x: self.unnormalized(x) / z for x in self.assignments()}


def _marg(p: Joint, keep: Sequence[int]) -> Dict[Assignment, Fraction]:
    out: Dict[Assignment, Fraction] = {}
    for x, v in p.items():
        k = tuple(x[i] for i in keep)
        out[k] = out.get(k, Fraction(0)) + v
    return out


def is_ci(p: Joint, a: Sequence[int], b: Sequence[int], s: Sequence[int]) -> bool:
    """X_a _||_ X_b | X_s, by p(a,b,s) p(s) = p(a,s) p(b,s) on every value."""
    a, b, s = list(a), list(b), list(s)
    pabs, pas, pbs, ps = _marg(p, a + b + s), _marg(p, a + s), _marg(p, b + s), _marg(p, s)
    keys_a = {k[:len(a)] for k in pabs}
    keys_b = {k[len(a):len(a) + len(b)] for k in pabs}
    for vs in ps:
        for va in keys_a:
            for vb in keys_b:
                lhs = pabs.get(va + vb + vs, 0) * ps[vs]
                rhs = pas.get(va + vs, 0) * pbs.get(vb + vs, 0)
                if lhs != rhs:
                    return False
    return True


def pairwise_markov(p: Joint, adj: Dict[int, Set[int]]) -> bool:
    n = len(adj)
    for u, v in combinations(range(n), 2):
        if v not in adj[u]:
            rest = [w for w in range(n) if w not in (u, v)]
            if not is_ci(p, [u], [v], rest):
                return False
    return True


def local_markov(p: Joint, adj: Dict[int, Set[int]]) -> bool:
    n = len(adj)
    for u in range(n):
        nb = sorted(adj[u])
        rest = [w for w in range(n) if w != u and w not in adj[u]]
        if rest and not is_ci(p, [u], rest, nb):
            return False
    return True


def separates(adj: Dict[int, Set[int]], a: Set[int], b: Set[int], s: Set[int]) -> bool:
    seen, stack = set(a), list(a)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v in b:
                return False
            if v not in seen and v not in s:
                seen.add(v)
                stack.append(v)
    return True


def global_markov(p: Joint, adj: Dict[int, Set[int]]) -> bool:
    """Check X_A _||_ X_B | X_S for every separating triple with A, B, S
    disjoint and A, B nonempty. Exponential; for small graphs only."""
    n = len(adj)
    nodes = range(n)
    for s_size in range(n - 1):
        for s in combinations(nodes, s_size):
            rest = [v for v in nodes if v not in s]
            for mask in range(1, 3 ** len(rest)):
                a, b, m = [], [], mask
                for v in rest:
                    m, r = divmod(m, 3)
                    if r == 1:
                        a.append(v)
                    elif r == 2:
                        b.append(v)
                if a and b and a[0] < b[0] and separates(adj, set(a), set(b), set(s)):
                    if not is_ci(p, a, b, list(s)):
                        return False
    return True


def is_clique(adj: Dict[int, Set[int]], nodes: Sequence[int]) -> bool:
    return all(v in adj[u] for u, v in combinations(nodes, 2))


def hammersley_clifford_potentials(p: Joint, n: int) -> Dict[FrozenSet[int], Callable[[Assignment], Fraction]]:
    """Mobius inversion for a positive distribution on n binary variables.

    Phi_A(x) = prod over B subset of A of p(x_B, 0 elsewhere) ^ ((-1)^|A - B|).
    Then p(x) = prod over A of Phi_A(x), and Phi_A depends only on x_A.
    When p is pairwise Markov for a graph, Phi_A = 1 unless A is a clique.
    """
    def restricted(x: Assignment, keep: Sequence[int]) -> Assignment:
        return tuple(x[i] if i in keep else 0 for i in range(n))

    out = {}
    for r in range(n + 1):
        for A in combinations(range(n), r):
            def phi(x: Assignment, A=A) -> Fraction:
                v = Fraction(1)
                for k in range(len(A) + 1):
                    for B in combinations(A, k):
                        q = p[restricted(x, B)]
                        v = v * q if (len(A) - k) % 2 == 0 else v / q
                return v
            out[frozenset(A)] = phi
    return out


def edge_support_closure_violations(p: Joint, edges: Sequence[Tuple[int, int]]) -> List[Assignment]:
    """Assignments with p = 0 whose value pair on every edge occurs in some
    assignment with p > 0. If any exist, p is not a product of edge
    potentials: every edge factor would be positive there."""
    seen = {e: {(x[e[0]], x[e[1]]) for x, v in p.items() if v > 0} for e in edges}
    return [x for x, v in p.items() if v == 0 and all((x[e[0]], x[e[1]]) in seen[e] for e in edges)]
