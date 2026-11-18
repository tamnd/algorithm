# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volcano-optimizer-generator/. The authors are listed in prov/KJT4MR.jsonl.
"""The search of the Volcano optimizer generator on a small join model.

Volcano (Graefe and McKenna, 1993) generates an optimizer from rules. The
search has two phases. First it applies the transformation rules until no new
logical expression appears, and keeps the expressions in equivalence classes
(groups) of a memo. Then FIND-BEST-PLAN works top down: for a group and a
required physical property, it tries every algorithm that can give the
property and every enforcer of the property, asks for the best plans of the
inputs with their required properties, keeps the cheapest plan in a table,
and prunes with a cost limit (branch and bound).

The model of this file: relations R_0, ..., R_(n-1) that all share one join
attribute k, so every split of a set of relations is a valid join. A group is
a frozenset of relations. The logical operators are GET(R_i) and JOIN. The
transformation rules are join commutativity and associativity. The physical
property is the sort order on k: "sorted" or "any".

Algorithms and their local costs (sizes are estimates, |A| for a group A):
    TableScan(R)       |R|                gives no order
    IndexScan(R)       2 |R|              needs an index on R.k, gives sorted
    HashJoin(A, B)     |A| + 2 |B|        builds on B, gives no order
    MergeJoin(A, B)    |A| + |B|          needs both inputs sorted, gives sorted
    NestedLoop(A, B)   |A| |B|            keeps the order of A
    Sort(A)            2 |A|              the enforcer of "sorted"

The size of a group S is the product of |R_i| over S divided by the product
of the numbers of distinct keys d_i over S without the smallest d_i, which is
the usual estimate for an equijoin on one attribute.
"""

from fractions import Fraction
from typing import Dict, FrozenSet, Iterator, List, Optional, Sequence, Tuple

ANY = "any"
SORTED = "sorted"
INF = float("inf")
Group = FrozenSet[int]


class Model:
    def __init__(self, card: Sequence, distinct: Sequence, indexed: Sequence[bool]) -> None:
        if not (len(card) == len(distinct) == len(indexed)) or not card:
            raise ValueError("card, distinct and indexed need the same nonzero length")
        if any(d < 1 for d in distinct) or any(c < 0 for c in card):
            raise ValueError("sizes must be nonnegative and distinct counts positive")
        self.n = len(card)
        self.card = [Fraction(c) for c in card]
        self.distinct = [Fraction(d) for d in distinct]
        self.indexed = list(indexed)

    def size(self, S: Group) -> Fraction:
        p = Fraction(1)
        for i in S:
            p *= self.card[i]
        ds = sorted(self.distinct[i] for i in S)
        for d in ds[1:]:
            p /= d
        return p


def local_cost(m: Model, op: str, S: Group, inputs: Sequence[Group]) -> Fraction:
    if op == "TableScan":
        return m.size(S)
    if op == "IndexScan":
        return 2 * m.size(S)
    if op == "Sort":
        return 2 * m.size(S)
    a, b = (m.size(g) for g in inputs)
    if op == "HashJoin":
        return a + 2 * b
    if op == "MergeJoin":
        return a + b
    if op == "NestedLoop":
        return a * b
    raise ValueError("unknown operator %r" % (op,))


def moves(m: Model, exprs: Sequence, S: Group, prop: str) -> Iterator[Tuple[Fraction, object, list]]:
    """The algorithms and enforcers that give prop for group S, in order of promise.

    Each move is (local cost, label, [(input group, required property)]).
    """
    if len(S) == 1:
        (i,) = S
        if m.indexed[i]:
            yield local_cost(m, "IndexScan", S, []), ("IndexScan", i), []
        if prop == ANY:
            yield local_cost(m, "TableScan", S, []), ("TableScan", i), []
    else:
        for A, B in exprs:
            yield local_cost(m, "MergeJoin", S, [A, B]), "MergeJoin", [(A, SORTED), (B, SORTED)]
            if prop == ANY:
                yield local_cost(m, "HashJoin", S, [A, B]), "HashJoin", [(A, ANY), (B, ANY)]
            yield local_cost(m, "NestedLoop", S, [A, B]), "NestedLoop", [(A, prop), (B, ANY)]
    if prop == SORTED:
        yield local_cost(m, "Sort", S, [S]), "Sort", [(S, ANY)]


class Memo:
    """Groups of logical expressions. A join expression is a pair (left group, right group)."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.exprs: Dict[Group, List[Tuple[Group, Group]]] = {}
        self.seen: Dict[Group, set] = {}
        self.explored: set = set()

    def group(self, S: Group) -> Group:
        if S not in self.exprs:
            self.exprs[S], self.seen[S] = [], set()
        return S

    def add(self, S: Group, e: Tuple[Group, Group]) -> bool:
        self.group(S)
        if e in self.seen[S]:
            return False
        self.seen[S].add(e)
        self.exprs[S].append(e)
        return True

    def insert_left_deep(self) -> Group:
        """The initial query: R_0 joined with R_1, then R_2, and so on."""
        S = self.group(frozenset([0]))
        for i in range(1, self.n):
            R = self.group(frozenset([i]))
            T = S | R
            self.add(T, (S, R))
            S = T
        return S

    def explore(self, S: Group) -> None:
        """Apply commutativity and associativity to the group S until nothing new appears."""
        if S in self.explored or len(S) == 1:
            self.explored.add(S)
            return
        changed = True
        while changed:  # @line L3
            changed = False
            for L, R in list(self.exprs[S]):  # @line L4
                changed |= self.add(S, (R, L))  # @line L5
                if len(L) > 1:
                    self.explore(L)  # @line L6
                    for A, B in list(self.exprs[L]):
                        BR = B | R
                        self.add(BR, (B, R))
                        changed |= self.add(S, (A, BR))
        self.explored.add(S)  # @line L7

    def explore_all(self, root: Group) -> None:
        self.explore(root)
        while True:
            todo = [S for S in self.exprs if S not in self.explored]
            if not todo:
                return
            for S in todo:
                self.explore(S)


class Volcano:
    def __init__(self, m: Model, prune: bool = True) -> None:
        self.m = m
        self.prune = prune
        self.memo = Memo(m.n)
        self.table: Dict[Tuple[Group, str], tuple] = {}
        self.calls = 0

    def optimize(self, prop: str = ANY) -> Tuple[Fraction, object]:
        if prop not in (ANY, SORTED):
            raise ValueError("the property is 'any' or 'sorted'")
        root = self.memo.insert_left_deep()
        self.memo.explore_all(root)  # @line L1
        found = self.find_best_plan(root, prop, INF)  # @line L2
        assert found is not None
        return found

    def find_best_plan(self, S: Group, prop: str, limit) -> Optional[Tuple[Fraction, object]]:
        """The cheapest plan for S with property prop that costs less than limit, or None."""
        self.calls += 1
        key = (S, prop)
        if key in self.table:  # @line L8
            kind, a, plan = self.table[key]
            if kind == "plan":
                return (a, plan) if a < limit else None
            if limit <= a:
                return None
        limit0 = limit
        best = None  # @line L9
        for local, label, inputs in moves(self.m, self.memo.exprs[S], S, prop):  # @line L10
            total = local  # @line L11
            plans = []
            for g, p in inputs:  # @line L12
                if total >= limit:
                    break
                r = self.find_best_plan(g, p, limit - total if self.prune else INF)  # @line L13
                if r is None:  # @line L14
                    total = INF
                    break
                total += r[0]
                plans.append(r[1])
            if len(plans) == len(inputs) and total < limit and (best is None or total < best[0]):  # @line L15
                best = (total, label if not inputs else (label,) + tuple(plans))
                if self.prune:
                    limit = total
        if best is None:  # @line L16
            self.table[key] = ("fail", limit0, None)
        else:
            self.table[key] = ("plan", best[0], best[1])
        return best  # @line L17


def volcano(m: Model, prop: str = ANY, prune: bool = True) -> Tuple[Fraction, object]:
    """The cheapest physical plan for the join of all relations of m that gives prop."""
    return Volcano(m, prune).optimize(prop)


def group_of(p) -> Group:
    if isinstance(p[0], str) and p[0] in ("TableScan", "IndexScan"):
        return frozenset([p[1]])
    out: set = set()
    for c in p[1:]:
        out |= group_of(c)
    return frozenset(out)


def delivered(p) -> str:
    """The sort order that a physical plan gives."""
    op = p[0]
    if op in ("IndexScan", "Sort", "MergeJoin"):
        return SORTED
    if op == "NestedLoop":
        return delivered(p[1])
    return ANY


def plan_cost(m: Model, p) -> Fraction:
    """The cost of a physical plan; raises ValueError if an input lacks a required order."""
    op = p[0]
    if op in ("TableScan", "IndexScan"):
        if op == "IndexScan" and not m.indexed[p[1]]:
            raise ValueError("no index on R_%d" % p[1])
        return local_cost(m, op, group_of(p), [])
    kids = p[1:]
    if op == "MergeJoin" and any(delivered(c) != SORTED for c in kids):
        raise ValueError("a merge join needs sorted inputs")
    return local_cost(m, op, group_of(p), [group_of(c) for c in kids]) + sum(plan_cost(m, c) for c in kids)
