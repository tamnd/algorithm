# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpccp/. The authors are listed in prov/0ECWZS.jsonl.
"""DPccp: dynamic programming over csg-cmp pairs (Moerkotte and Neumann, 2006).

It finds the cheapest bushy join tree without cross products for a connected
query graph. A csg is a connected set of relations; a csg-cmp pair is two
disjoint csgs S1 and S2 with an edge between them. Every join in a tree without
cross products combines such a pair, and DPccp enumerates each unordered pair
exactly once, in an order where the best plans of S1 and S2 are final when the
pair is used.

Sets of relations are bitmasks over the relations 0 .. n - 1. A plan is a
relation number (a leaf) or a pair (left, right) of plans. The cost of a plan
is the sum, over its joins, of join_cost(|left|, |right|, |result|), with sizes
under the independence assumption. All arithmetic is exact.
"""

from collections import deque
from fractions import Fraction
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple, Union

Plan = Union[int, tuple]
JoinCost = Callable[[Fraction, Fraction, Fraction], Fraction]


def c_out(left: Fraction, right: Fraction, out: Fraction) -> Fraction:
    """C_out: the size of each intermediate result."""
    return out


def hash_cost(left: Fraction, right: Fraction, out: Fraction) -> Fraction:
    """An asymmetric cost: the right input is the build side and costs more per tuple."""
    return out + left + 3 * right


class Query:
    """Relation sizes and a query graph with a selectivity per edge (i, j), i < j."""

    def __init__(self, card: Sequence, sel: Dict[Tuple[int, int], Fraction]) -> None:
        self.n = len(card)
        self.card = [Fraction(c) for c in card]
        self.sel = {(min(i, j), max(i, j)): Fraction(f) for (i, j), f in sel.items()}
        self.adj = [0] * self.n
        for (i, j) in self.sel:
            self.adj[i] |= 1 << j
            self.adj[j] |= 1 << i

    def size(self, S: int) -> Fraction:
        p = Fraction(1)
        for i in members(S):
            p *= self.card[i]
        for (i, j), f in self.sel.items():
            if S >> i & 1 and S >> j & 1:
                p *= f
        return p

    def neighborhood(self, S: int) -> int:
        """N(S): the relations outside S with an edge into S."""
        out = 0
        for i in members(S):
            out |= self.adj[i]
        return out & ~S

    def connected(self, S: int) -> bool:
        if S == 0:
            return False
        reach = S & -S
        while True:
            nxt = reach | (self.neighborhood(reach) & S)
            if nxt == reach:
                return reach == S
            reach = nxt

    def relabel(self, perm: Sequence[int]) -> "Query":
        """The same query with relation perm[k] renamed k."""
        pos = {v: k for k, v in enumerate(perm)}
        return Query([self.card[v] for v in perm], {(pos[i], pos[j]): f for (i, j), f in self.sel.items()})


def members(S: int) -> List[int]:
    out, i = [], 0
    while S:
        if S & 1:
            out.append(i)
        S >>= 1
        i += 1
    return out


def subsets(N: int) -> Iterator[int]:
    """The nonempty subsets of N, in increasing order as integers (so every subset comes before its supersets)."""
    s = (0 - N) & N
    while s:
        yield s
        s = (s - N) & N


def bfs_order(q: Query) -> List[int]:
    """The relations in breadth-first order from relation 0, neighbors by number."""
    seen, order, queue = {0}, [], deque([0])
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in members(q.adj[v]):
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return order


def enumerate_csg_rec(q: Query, S: int, X: int) -> Iterator[int]:
    N = q.neighborhood(S) & ~X  # @line L12
    for s in subsets(N):  # @line L13
        yield S | s
    for s in subsets(N):  # @line L14
        yield from enumerate_csg_rec(q, S | s, X | N)


def enumerate_csg(q: Query) -> Iterator[int]:
    """Every connected set exactly once, sets with a larger smallest member first."""
    for i in range(q.n - 1, -1, -1):  # @line L9
        yield 1 << i  # @line L10
        yield from enumerate_csg_rec(q, 1 << i, (1 << (i + 1)) - 1)  # @line L11


def enumerate_cmp(q: Query, S1: int) -> Iterator[int]:
    """Every csg S2 that is disjoint from S1, joined to it by an edge, and has a larger smallest member."""
    low = (S1 & -S1).bit_length() - 1
    X = ((1 << (low + 1)) - 1) | S1  # @line L15
    N = q.neighborhood(S1) & ~X  # @line L16
    for i in reversed(members(N)):  # @line L17
        yield 1 << i  # @line L18
        yield from enumerate_csg_rec(q, 1 << i, X | (N & ((1 << (i + 1)) - 1)))  # @line L19


def csg_cmp_pairs(q: Query) -> Iterator[Tuple[int, int]]:
    """The csg-cmp pairs (S1, S2) in the order DPccp uses them."""
    for S1 in enumerate_csg(q):  # @line L3
        for S2 in enumerate_cmp(q, S1):  # @line L4
            yield S1, S2


def plan_cost(q: Query, plan: Plan, join_cost: JoinCost = c_out) -> Fraction:
    def rec(p: Plan) -> Tuple[Fraction, int]:
        if isinstance(p, int):
            return Fraction(0), 1 << p
        cl, sl = rec(p[0])
        cr, sr = rec(p[1])
        return cl + cr + join_cost(q.size(sl), q.size(sr), q.size(sl | sr)), sl | sr
    return rec(plan)[0]


def map_plan(plan: Plan, perm: Sequence[int]) -> Plan:
    if isinstance(plan, int):
        return perm[plan]
    return (map_plan(plan[0], perm), map_plan(plan[1], perm))


def dpccp(q: Query, join_cost: JoinCost = c_out, bfs: bool = True,
          on_pair: Optional[Callable[[int, int], None]] = None) -> Tuple[Fraction, Plan]:
    """The cheapest bushy plan without cross products and its cost.

    The query graph must be connected. bfs=False keeps the given numbering.
    on_pair(S1, S2), if given, is called for each pair as it is used, with the
    sets as bitmasks over the original relation numbers."""
    if q.n == 0:
        raise ValueError("no relations")
    perm = bfs_order(q) if bfs else list(range(q.n))  # @line L1
    if len(perm) != q.n or not q.connected((1 << q.n) - 1):
        raise ValueError("DPccp needs a connected query graph")
    g = q.relabel(perm)
    back = lambda S: sum(1 << perm[i] for i in members(S))
    best: Dict[int, Tuple[Fraction, Plan]] = {1 << v: (Fraction(0), v) for v in range(g.n)}  # @line L2
    for S1, S2 in csg_cmp_pairs(g):
        if on_pair is not None:
            on_pair(back(S1), back(S2))
        S = S1 | S2  # @line L5
        size = (g.size(S1), g.size(S2), g.size(S))
        for (A, B, sa, sb) in ((S1, S2, size[0], size[1]), (S2, S1, size[1], size[0])):  # @line L6
            cost = best[A][0] + best[B][0] + join_cost(sa, sb, size[2])
            if S not in best or cost < best[S][0]:  # @line L7
                best[S] = (cost, (best[A][1], best[B][1]))
    cost, plan = best[(1 << g.n) - 1]  # @line L8
    return cost, map_plan(plan, perm)
