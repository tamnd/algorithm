# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascades-framework/. The authors are listed in prov/SJBPXM.jsonl.
"""The task-based search of the Cascades framework on a small join model.

Cascades (Graefe, 1995) keeps equivalent logical expressions in groups of a
memo, like Volcano, but it does not explore all groups first. The search is a
stack of tasks. Optimizing a group for a required property explores the group
on demand, then tries the algorithms of each expression in the order of their
promise, and optimizes the input groups with an upper bound on their cost.
Results are stored as winners (or failures with the bound that caused them).

The model is the one of the Volcano page: relations R_0, ..., R_(n-1) share
one join attribute k, a group is a frozenset of relations, the rules are join
commutativity and associativity, and the physical property is the sort order
on k ("sorted" or "any").

Algorithms and their local costs (|A| is the estimated size of group A):
    TableScan(R)       |R|                gives no order
    IndexScan(R)       2 |R|              needs an index on R.k, gives sorted
    HashJoin(A, B)     |A| + 2 |B|        gives no order
    MergeJoin(A, B)    |A| + |B|          needs both inputs sorted, gives sorted
    NestedLoop(A, B)   |A| |B|            keeps the order of A
    Sort(A)            2 |A|              the enforcer of "sorted"

The size of a group is the product of its |R_i| divided by the product of its
distinct counts d_i without the smallest one.
"""

from fractions import Fraction
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

ANY = "any"
SORTED = "sorted"
INF = float("inf")
Group = FrozenSet[int]
RULES = ("commute", "associate")


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
        for d in sorted(self.distinct[i] for i in S)[1:]:
            p /= d
        return p


class Context:
    """The goal of one optimization: a group, a required property and an upper bound."""

    def __init__(self, S: Group, prop: str, limit) -> None:
        self.S, self.prop, self.limit, self.limit0 = S, prop, limit, limit
        self.best: Optional[Tuple[Fraction, str, list]] = None


class Cascades:
    def __init__(self, m: Model, prune: bool = True) -> None:
        self.m = m
        self.prune = prune
        self.exprs: Dict[Group, list] = {}
        self.seen: Dict[Group, set] = {}
        self.applied: set = set()
        self.explored: set = set()
        self.exploring: set = set()
        self.active: set = set()
        self.winner: Dict[Tuple[Group, str], Tuple[Fraction, str, list]] = {}
        self.failed: Dict[Tuple[Group, str], object] = {}
        self.stack: list = []
        self.tasks = 0

    # The memo.

    def add(self, S: Group, e) -> bool:
        if S not in self.exprs:
            self.exprs[S], self.seen[S] = [], set()
        if e in self.seen[S]:
            return False
        self.seen[S].add(e)
        self.exprs[S].append(e)
        return True

    def insert_query(self) -> Group:
        """The initial query: R_0 joined with R_1, then R_2, and so on."""
        for i in range(self.m.n):
            self.add(frozenset([i]), ("GET", i))
        S = frozenset([0])
        for i in range(1, self.m.n):
            T = S | {i}
            self.add(T, (S, frozenset([i])))
            S = T
        return S

    # The search.

    def optimize(self, prop: str = ANY) -> Tuple[Fraction, object]:
        if prop not in (ANY, SORTED):
            raise ValueError("the property is 'any' or 'sorted'")
        root = self.insert_query()
        self.stack.append(("O_GROUP", root, prop, INF))  # @line L1
        while self.stack:  # @line L2
            task = self.stack.pop()
            self.tasks += 1
            getattr(self, task[0])(*task[1:])
        return self.winner[(root, prop)][0], self.plan(root, prop)  # @line L3

    def O_GROUP(self, S: Group, prop: str, limit) -> None:
        key = (S, prop)
        if key in self.winner or (key in self.failed and self.failed[key] >= limit):  # @line L4
            return
        if S not in self.explored:  # @line L5
            self.stack.append(("O_GROUP", S, prop, limit))
            self.stack.append(("E_GROUP", S))
            return
        assert key not in self.active, "a goal must not depend on itself"
        self.active.add(key)
        ctx = Context(S, prop, limit if self.prune else INF)  # @line L6
        self.stack.append(("FINISH", ctx))
        for e in reversed(self.exprs[S]):
            self.stack.append(("O_EXPR", ctx, e))
        if prop == SORTED:
            local = 2 * self.m.size(S)
            self.stack.append(("O_INPUTS", ctx, (local, "Sort", [(S, ANY)]), 0, local))

    def E_GROUP(self, S: Group) -> None:
        if S in self.explored or S in self.exploring:  # @line L7
            return
        self.exploring.add(S)
        self.stack.append(("MARK_EXPLORED", S))
        for e in reversed(self.exprs[S]):
            self.stack.append(("E_EXPR", S, e))

    def E_EXPR(self, S: Group, e) -> None:
        if e[0] == "GET":
            return
        L, R = e
        for rule in reversed(RULES):  # @line L8
            if (S, e, rule) in self.applied:
                continue
            self.applied.add((S, e, rule))
            self.stack.append(("APPLY_RULE", S, e, rule))
            if rule == "associate" and len(L) > 1:
                self.stack.append(("E_GROUP", L))

    def APPLY_RULE(self, S: Group, e, rule: str) -> None:
        L, R = e
        new = []
        if rule == "commute":
            new.append((R, L))
        elif len(L) > 1:
            assert L in self.explored, "the pattern needs an explored input group"
            for A, B in list(self.exprs[L]):
                self.add(B | R, (B, R))
                new.append((A, B | R))
        for f in new:  # @line L9
            if self.add(S, f):
                self.stack.append(("E_EXPR", S, f))

    def MARK_EXPLORED(self, S: Group) -> None:
        self.exploring.discard(S)
        self.explored.add(S)  # @line L17

    def moves(self, S: Group, e, prop: str) -> List[Tuple[Fraction, str, list]]:
        m = self.m
        out = []
        if e[0] == "GET":
            i = e[1]
            if m.indexed[i]:
                out.append((2 * m.size(S), "IndexScan", []))
            if prop == ANY:
                out.append((m.size(S), "TableScan", []))
            return out
        L, R = e
        a, b = m.size(L), m.size(R)
        out.append((a + b, "MergeJoin", [(L, SORTED), (R, SORTED)]))
        if prop == ANY:
            out.append((a + 2 * b, "HashJoin", [(L, ANY), (R, ANY)]))
        out.append((a * b, "NestedLoop", [(L, prop), (R, ANY)]))
        return out

    def O_EXPR(self, ctx: Context, e) -> None:
        ms = sorted(self.moves(ctx.S, e, ctx.prop), key=lambda mv: mv[0])
        for mv in reversed(ms):  # @line L10
            self.stack.append(("O_INPUTS", ctx, mv, 0, mv[0]))

    def O_INPUTS(self, ctx: Context, mv, i: int, total) -> None:
        """Cost the inputs of one move from input i on; total is the cost so far."""
        _, label, inputs = mv
        while i < len(inputs):  # @line L11
            G, q = inputs[i]
            rest = ctx.limit - total
            if total >= ctx.limit or self.failed.get((G, q), -1) >= rest:  # @line L12
                return
            if (G, q) in self.winner:  # @line L13
                total += self.winner[(G, q)][0]
                i += 1
                continue
            self.stack.append(("O_INPUTS", ctx, mv, i, total))  # @line L14
            self.stack.append(("O_GROUP", G, q, rest if self.prune else INF))
            return
        if total < ctx.limit and (ctx.best is None or total < ctx.best[0]):  # @line L15
            ctx.best = (total, label, inputs)
            if self.prune:
                ctx.limit = total

    def FINISH(self, ctx: Context) -> None:
        key = (ctx.S, ctx.prop)
        self.active.discard(key)
        if ctx.best is not None:  # @line L16
            self.winner[key] = ctx.best
            self.failed.pop(key, None)
        else:
            self.failed[key] = ctx.limit0

    def plan(self, S: Group, prop: str):
        """The physical plan of the winner of (S, prop), read from the winners of its inputs."""
        _, label, inputs = self.winner[(S, prop)]
        if label in ("TableScan", "IndexScan"):
            (i,) = S
            return (label, i)
        return (label,) + tuple(self.plan(G, q) for G, q in inputs)


def cascades(m: Model, prop: str = ANY, prune: bool = True) -> Tuple[Fraction, object]:
    """The cheapest physical plan for the join of all relations of m that gives prop."""
    return Cascades(m, prune).optimize(prop)


def group_of(p) -> Group:
    if p[0] in ("TableScan", "IndexScan"):
        return frozenset([p[1]])
    out: set = set()
    for c in p[1:]:
        out |= group_of(c)
    return frozenset(out)


def delivered(p) -> str:
    """The sort order that a physical plan gives."""
    if p[0] in ("IndexScan", "Sort", "MergeJoin"):
        return SORTED
    if p[0] == "NestedLoop":
        return delivered(p[1])
    return ANY
