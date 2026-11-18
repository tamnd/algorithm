# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dphyp/. The authors are listed in prov/CD2W8Y.jsonl.
"""DPhyp: join enumeration over a query hypergraph (Moerkotte and Neumann, 2008).

A hyperedge {u, w} joins two disjoint nonempty sets of relations u and w: it
is a predicate that needs all relations of u on one side of the join and all
relations of w on the other, such as R0.a + R1.b = R2.c with u = {R0, R1} and
w = {R2}. A simple edge has |u| = |w| = 1.

A set S is connected if it is one relation, or it splits into two disjoint
connected sets S1 and S2 with a hyperedge {u, w}, u within S1 and w within S2.
A csg-cmp pair is such a split. DPhyp emits every csg-cmp pair exactly once,
in an order where the plans of both halves are final, and so finds the
cheapest bushy plan without cross products.

Sets of relations are bitmasks. A plan is a relation number or a pair
(left, right). The cost of a plan is the sum of join_cost(|left|, |right|,
|result|) over its joins. The size of a set is the product of the sizes of its
relations and of the selectivities of the hyperedges inside it.
"""

from fractions import Fraction
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple, Union

Plan = Union[int, tuple]
JoinCost = Callable[[Fraction, Fraction, Fraction], Fraction]
Hyperedge = Tuple[int, int]


def c_out(left: Fraction, right: Fraction, out: Fraction) -> Fraction:
    return out


def hash_cost(left: Fraction, right: Fraction, out: Fraction) -> Fraction:
    """An asymmetric cost: the right input is the build side."""
    return out + left + 3 * right


def lowest(S: int) -> int:
    """The singleton of the member of S with the smallest index."""
    return S & -S


def members(S: int) -> List[int]:
    return [i for i in range(S.bit_length()) if S >> i & 1]


def subsets(N: int) -> Iterator[int]:
    """The nonempty subsets of N in increasing order as integers."""
    s = (0 - N) & N
    while s:
        yield s
        s = (s - N) & N


class Hypergraph:
    """Relation sizes and hyperedges, each a pair of disjoint nonempty bitmasks with a selectivity."""

    def __init__(self, card: Sequence, edges: Sequence[Tuple[int, int, Fraction]]) -> None:
        self.n = len(card)
        self.card = [Fraction(c) for c in card]
        self.edges: List[Tuple[int, int, Fraction]] = []
        for u, w, f in edges:
            if not u or not w or u & w or (u | w) >> self.n:
                raise ValueError("a hyperedge needs two disjoint nonempty sets of relations")
            self.edges.append((u, w, Fraction(f)))
        self.directed = [(u, w) for u, w, _ in self.edges] + [(w, u) for u, w, _ in self.edges]

    def size(self, S: int) -> Fraction:
        p = Fraction(1)
        for i in members(S):
            p *= self.card[i]
        for u, w, f in self.edges:
            if (u | w) & ~S == 0:
                p *= f
        return p

    def joins(self, S1: int, S2: int) -> bool:
        """True if some hyperedge has one side within S1 and the other within S2."""
        return any(u & ~S1 == 0 and w & ~S2 == 0 for u, w in self.directed)

    def neighborhood(self, S: int, X: int) -> int:
        """N(S, X): the representative min(w) of each minimal w such that {u, w}
        is a hyperedge with u within S and w disjoint from S and X."""
        cands = {w for u, w in self.directed if u & ~S == 0 and w & (S | X) == 0}
        out = 0
        for w in cands:
            if not any(v != w and v & ~w == 0 for v in cands):
                out |= lowest(w)
        return out


class DPhyp:
    def __init__(self, h: Hypergraph, join_cost: JoinCost = c_out,
                 on_pair: Optional[Callable[[int, int], None]] = None) -> None:
        self.h, self.join_cost, self.on_pair = h, join_cost, on_pair
        self.best: Dict[int, Tuple[Fraction, Plan]] = {}

    def solve(self) -> Tuple[Fraction, Plan]:
        h = self.h
        for v in range(h.n):
            self.best[1 << v] = (Fraction(0), v)  # @line L1
        for v in range(h.n - 1, -1, -1):  # @line L2
            self.emit_csg(1 << v)  # @line L3
            self.enumerate_csg_rec(1 << v, (1 << (v + 1)) - 1)  # @line L4
        full = (1 << h.n) - 1
        if full not in self.best:
            raise ValueError("the hypergraph is not connected")
        return self.best[full]  # @line L5

    def enumerate_csg_rec(self, S1: int, X: int) -> None:
        N = self.h.neighborhood(S1, X)  # @line L6
        for s in subsets(N):  # @line L7
            if S1 | s in self.best:  # @line L8
                self.emit_csg(S1 | s)
        for s in subsets(N):  # @line L9
            self.enumerate_csg_rec(S1 | s, X | N)

    def emit_csg(self, S1: int) -> None:
        low = lowest(S1)
        X = S1 | (low | (low - 1))  # @line L10
        N = self.h.neighborhood(S1, X)  # @line L11
        for v in reversed(members(N)):  # @line L12
            S2 = 1 << v
            if self.h.joins(S1, S2):  # @line L13
                self.emit_csg_cmp(S1, S2)
            self.enumerate_cmp_rec(S1, S2, X | (N & ((S2 << 1) - 1)))  # @line L14

    def enumerate_cmp_rec(self, S1: int, S2: int, X: int) -> None:
        N = self.h.neighborhood(S2, X)  # @line L15
        for s in subsets(N):  # @line L16
            if S2 | s in self.best and self.h.joins(S1, S2 | s):  # @line L17
                self.emit_csg_cmp(S1, S2 | s)
        for s in subsets(N):  # @line L18
            self.enumerate_cmp_rec(S1, S2 | s, X | N)

    def emit_csg_cmp(self, S1: int, S2: int) -> None:
        if self.on_pair is not None:
            self.on_pair(S1, S2)
        h, S = self.h, S1 | S2
        out = h.size(S)  # @line L19
        for A, B in ((S1, S2), (S2, S1)):  # @line L20
            cost = self.best[A][0] + self.best[B][0] + self.join_cost(h.size(A), h.size(B), out)
            if S not in self.best or cost < self.best[S][0]:  # @line L21
                self.best[S] = (cost, (self.best[A][1], self.best[B][1]))


def dphyp(h: Hypergraph, join_cost: JoinCost = c_out,
          on_pair: Optional[Callable[[int, int], None]] = None) -> Tuple[Fraction, Plan]:
    """The cheapest plan without cross products for a connected hypergraph, and its cost."""
    return DPhyp(h, join_cost, on_pair).solve()


def plan_cost(h: Hypergraph, plan: Plan, join_cost: JoinCost = c_out) -> Fraction:
    def rec(p: Plan) -> Tuple[Fraction, int]:
        if isinstance(p, int):
            return Fraction(0), 1 << p
        cl, sl = rec(p[0])
        cr, sr = rec(p[1])
        if not h.joins(sl, sr) and not h.joins(sr, sl):
            raise ValueError("the plan has a cross product")
        return cl + cr + join_cost(h.size(sl), h.size(sr), h.size(sl | sr)), sl | sr
    return rec(plan)[0]
