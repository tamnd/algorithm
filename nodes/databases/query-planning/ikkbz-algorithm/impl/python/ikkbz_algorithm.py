# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ikkbz-algorithm/. The authors are listed in prov/ZKFGDY.jsonl.
"""The IKKBZ algorithm: the cheapest left-deep join order without cross
products for an acyclic (tree) query graph, under a cost function with the
adjacent sequence interchange (ASI) property.

A query has n relations 0 .. n - 1 with cardinalities card[i] and a tree of
join predicates: sel maps a pair (i, j) with i < j to the selectivity of the
predicate between R_i and R_j. Under the independence assumption the size of
the join of a set S of relations is the product of card[i] for i in S times
the product of the selectivities of the edges inside S.

The cost function is C_out of a left-deep order: the sum of the sizes of the
results of the n - 1 joins. With the root r first, a relation v that joins
its parent p(v) multiplies the size of the result by T(v) = sel(v, p(v)) *
card[v]. The cost of a sequence s of non-root relations is
    C(empty) = 0,  C(v) = T(v),  C(s1 s2) = C(s1) + T(s1) C(s2),
with T(s) the product of T(v) over s, and C_out(r s) = card[r] * C(s).
The rank of a nonempty sequence is (T(s) - 1) / C(s).
All arithmetic is exact (Fractions).
"""

from fractions import Fraction
from itertools import permutations
from typing import Dict, List, Sequence, Tuple

Edges = Dict[Tuple[int, int], Fraction]


class Module:
    """A sequence of relations that the algorithm keeps together, with T and C."""

    __slots__ = ("seq", "T", "C")

    def __init__(self, seq: Tuple[int, ...], T: Fraction, C: Fraction) -> None:
        self.seq, self.T, self.C = seq, T, C

    def rank(self) -> Fraction:
        return (self.T - 1) / self.C

    def then(self, other: "Module") -> "Module":
        """The concatenation of self and other."""
        return Module(self.seq + other.seq, self.T * other.T, self.C + self.T * other.C)


def edge_sel(sel: Edges, i: int, j: int) -> Fraction:
    return sel[(min(i, j), max(i, j))]


def neighbors(n: int, sel: Edges) -> List[List[int]]:
    adj: List[List[int]] = [[] for _ in range(n)]
    for (i, j) in sel:
        adj[i].append(j)
        adj[j].append(i)
    return [sorted(a) for a in adj]


def is_tree(n: int, sel: Edges) -> bool:
    if len(sel) != n - 1:
        return False
    adj = neighbors(n, sel)
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def join_size(card: Sequence, sel: Edges, S) -> Fraction:
    """The estimated size of the join of the set S, under independence."""
    p = Fraction(1)
    for i in S:
        p *= card[i]
    for (i, j), f in sel.items():
        if i in S and j in S:
            p *= f
    return p


def cout(card: Sequence, sel: Edges, order: Sequence[int]) -> Fraction:
    """C_out of a left-deep order: the sum of the sizes of the n - 1 join results."""
    return sum((join_size(card, sel, set(order[:k])) for k in range(2, len(order) + 1)), Fraction(0))


def is_connected_order(n: int, sel: Edges, order: Sequence[int]) -> bool:
    """True if each relation after the first joins some earlier relation (no cross product)."""
    adj = neighbors(n, sel)
    seen = {order[0]}
    for v in order[1:]:
        if not any(w in seen for w in adj[v]):
            return False
        seen.add(v)
    return True


def rooted_tree(n: int, sel: Edges, root: int) -> Tuple[Dict[int, int], Dict[int, List[int]]]:
    """Parent and children lists of the query tree rooted at root (the precedence tree)."""
    adj = neighbors(n, sel)
    parent, children = {root: -1}, {v: [] for v in range(n)}
    stack = [root]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in parent:
                parent[w] = v
                children[v].append(w)
                stack.append(w)
    for v in children:
        children[v].sort()
    return parent, children


def linearize(v: int, root: int, children: Dict[int, List[int]], T: Dict[int, Fraction]) -> List[Module]:
    """The modules of the subtree of v, in the order of an optimal sequence.

    For v other than the root, the first module starts with v, and the ranks of
    the modules are nondecreasing. For the root, the list holds only the modules
    of its children (the root itself comes first in every sequence)."""
    chains = [linearize(c, root, children, T) for c in children[v]]
    tagged = [(m.rank(), ci, pos, m) for ci, ch in enumerate(chains) for pos, m in enumerate(ch)]
    tagged.sort(key=lambda x: (x[0], x[1], x[2]))
    merged = [m for _, _, _, m in tagged]  # @line L9
    if v == root:  # @line L10
        return merged
    head = Module((v,), T[v], T[v])  # @line L11
    while merged and head.rank() > merged[0].rank():  # @line L12
        head = head.then(merged.pop(0))  # @line L13
    return [head] + merged  # @line L14


def ikkbz_for_root(n: int, card: Sequence, sel: Edges, root: int) -> Tuple[Fraction, Tuple[int, ...]]:
    """The cheapest order that starts with root, and its C_out."""
    parent, children = rooted_tree(n, sel, root)  # @line L3
    T = {v: edge_sel(sel, v, parent[v]) * card[v] for v in range(n) if v != root}  # @line L4
    mods = linearize(root, root, children, T)  # @line L5
    order = (root,) + tuple(x for m in mods for x in m.seq)
    rest = Module((), Fraction(1), Fraction(0))
    for m in mods:
        rest = rest.then(m)
    cost = Fraction(card[root]) * rest.C  # @line L6
    return cost, order


def ikkbz(card: Sequence, sel: Edges) -> Tuple[Fraction, Tuple[int, ...]]:
    """The cheapest left-deep order without cross products, and its C_out.

    sel must form a tree on the relations 0 .. n - 1. Ties go to the smaller root."""
    n = len(card)
    if n == 1:
        return Fraction(0), (0,)
    if not is_tree(n, sel):
        raise ValueError("IKKBZ needs an acyclic, connected query graph")
    best = None  # @line L1
    for r in range(n):  # @line L2
        cost, order = ikkbz_for_root(n, card, sel, r)
        if best is None or cost < best[0]:  # @line L7
            best = (cost, order)
    return best  # @line L8


def brute_force(card: Sequence, sel: Edges) -> Tuple[Fraction, Tuple[int, ...]]:
    """Try every left-deep order without cross products."""
    n = len(card)
    best = None
    for order in permutations(range(n)):
        if is_connected_order(n, sel, order):
            c = cout(card, sel, order)
            if best is None or c < best[0]:
                best = (c, order)
    return best
