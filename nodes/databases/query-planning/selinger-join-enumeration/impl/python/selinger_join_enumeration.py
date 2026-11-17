# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selinger-join-enumeration/. The authors are listed in prov/BKRT7Y.jsonl.
"""System R (Selinger) join enumeration: dynamic programming over subsets of
relations that finds the cheapest left-deep join plan, keeping one plan per
(subset, interesting order).

A query is a list of relations. Relation i has an estimated cardinality
card[i], a set cols[i] of join-column classes, and a set idx[i] (a subset of
cols[i]) of classes on which it has a sorted index. Two relations join on class k when both
have k (an equivalence class of columns, so the predicates are closed under
transitivity). Class k has the selectivity sel[k] per equality, so the size
of a join of a set S is the product of the cardinalities times
sel[k] ** (m_k - 1), where m_k is the number of relations of S with class k.

The fixed cost function (in abstract units, exact Fractions):
  scan R_j                  card_j,          no order
  index scan R_j on k       2 card_j,        order k
  nested loop  P x R_j      cost(P) + card_j + |P| card_j / 10, keeps the order of P
  hash join    P x R_j      cost(P) + 3 card_j + |P|,           no order
  merge join on k           cost(P) + sort(P) + right + |P| + card_j, order k
                            sort(P) = 2 |P| if P is not ordered on k, else 0
                            right = 2 card_j with an index on k, else 3 card_j
  index nested loop on k    cost(P) + 2 |P| + |P x R_j|, keeps the order of P
  final sort                2 |result| if the required order is not met
"""

from fractions import Fraction
from typing import Dict, FrozenSet, Iterator, List, Optional, Sequence, Tuple

Plan = tuple  # ("scan", j) | ("iscan", j, k) | (method, left_plan, j, k_or_None) | ("sort", plan, k)


class Query:
    def __init__(self, card: Sequence[int], cols: Sequence[FrozenSet[int]], idx: Sequence[FrozenSet[int]],
                 sel: Dict[int, Fraction], order_by: Optional[int] = None, cross: bool = False) -> None:
        self.n = len(card)
        self.card = [Fraction(c) for c in card]
        self.cols, self.idx, self.sel = list(cols), list(idx), dict(sel)
        self.order_by, self.cross = order_by, cross
        # An index sorts a relation on one of its own columns; ORDER BY names a
        # class (a column that no predicate joins is a class of one relation).
        assert all(self.idx[i] <= self.cols[i] for i in range(self.n))
        assert order_by is None or order_by in self.sel or any(order_by in c for c in self.cols)

    def size(self, S: FrozenSet[int]) -> Fraction:
        p = Fraction(1)
        for i in S:
            p *= self.card[i]
        for k, f in self.sel.items():
            m = sum(1 for i in S if k in self.cols[i])
            if m > 1:
                p *= f ** (m - 1)
        return p

    def shared(self, S: FrozenSet[int], j: int) -> List[int]:
        """Classes on which R_j joins some relation of S."""
        return sorted(k for k in self.cols[j] if any(k in self.cols[i] for i in S))

    def interesting(self, S: FrozenSet[int]) -> set:
        """Orders that can still help: a join class to a relation outside S, or ORDER BY."""
        out = {k for i in S for k in self.cols[i]
               if any(k in self.cols[x] for x in range(self.n) if x not in S)}
        if self.order_by is not None:
            out.add(self.order_by)
        return out


def access_paths(q: Query, j: int) -> Iterator[Tuple[Fraction, Optional[int], Plan]]:
    yield q.card[j], None, ("scan", j)
    for k in sorted(q.idx[j]):
        yield 2 * q.card[j], k, ("iscan", j, k)


def join_steps(q: Query, S: FrozenSet[int], order: Optional[int], j: int
               ) -> Iterator[Tuple[Fraction, Optional[int], str, Optional[int]]]:
    """(added cost, output order, method, class) for joining a plan of S that
    has the given order with the base relation R_j."""
    s, nj = q.size(S), q.card[j]
    keys = q.shared(S, j)
    yield nj + s * nj / 10, order, "nlj", None
    if not keys:
        return
    yield 3 * nj + s, None, "hash", None
    for k in keys:
        sort = 0 if order == k else 2 * s
        right = 2 * nj if k in q.idx[j] else 3 * nj
        yield sort + right + s + nj, k, "merge", k
        if k in q.idx[j]:
            yield 2 * s + q.size(S | {j}), order, "inl", k


def selinger(q: Query) -> Tuple[Optional[Fraction], Optional[Plan]]:
    """Cheapest left-deep plan, or (None, None) if none exists (a disconnected
    query graph with cross products off). Time O(n 2^n) subsets times the
    number of orders and methods."""
    n = q.n
    # best[S][order] = (cost, plan): the cheapest plan for the set S whose
    # output has the given interesting order (None: no useful order).
    best: Dict[FrozenSet[int], Dict[Optional[int], Tuple[Fraction, Plan]]] = {}

    def add(S: FrozenSet[int], order: Optional[int], cost: Fraction, plan: Plan) -> None:
        if order is not None and order not in q.interesting(S):  # @line A1
            order = None
        cell = best.setdefault(S, {})
        if order not in cell or cost < cell[order][0]:  # @line A2
            cell[order] = (cost, plan)

    for j in range(n):  # @line L1
        for cost, order, plan in access_paths(q, j):
            add(frozenset([j]), order, cost, plan)
    by_size: Dict[int, List[FrozenSet[int]]] = {}
    for mask in range(1, 1 << n):
        S = frozenset(i for i in range(n) if mask >> i & 1)
        by_size.setdefault(len(S), []).append(S)
    for size in range(2, n + 1):  # @line L2
        for S in by_size.get(size, []):  # @line L3
            for j in sorted(S):  # @line L4
                L = S - {j}  # @line L5
                if not q.shared(L, j) and not q.cross:  # @line L6
                    continue
                for order, (cost, plan) in best.get(L, {}).items():  # @line L7
                    for extra, out, method, k in join_steps(q, L, order, j):  # @line L8
                        add(S, out, cost + extra, (method, plan, j, k))  # @line L9
    full = frozenset(range(n))
    answer: Tuple[Optional[Fraction], Optional[Plan]] = (None, None)
    for order, (cost, plan) in best.get(full, {}).items():  # @line L10
        if q.order_by is not None and order != q.order_by:
            cost, plan = cost + 2 * q.size(full), ("sort", plan, q.order_by)
        if answer[0] is None or cost < answer[0]:
            answer = (cost, plan)
    return answer


def selinger_without_orders(q: Query) -> Tuple[Optional[Fraction], Optional[Plan]]:
    """The same DP but with one plan per subset (orders forgotten), to show
    why interesting orders are needed. It can miss the optimum."""
    n = q.n
    best: Dict[FrozenSet[int], Tuple[Fraction, Optional[int], Plan]] = {}
    for j in range(n):
        for cost, order, plan in access_paths(q, j):
            S = frozenset([j])
            if S not in best or cost < best[S][0]:
                best[S] = (cost, order, plan)
    for size in range(2, n + 1):
        for mask in range(1, 1 << n):
            S = frozenset(i for i in range(n) if mask >> i & 1)
            if len(S) != size:
                continue
            for j in sorted(S):
                L = S - {j}
                if L not in best or (not q.shared(L, j) and not q.cross):
                    continue
                cost, order, plan = best[L]
                for extra, out, method, k in join_steps(q, L, order, j):
                    if S not in best or cost + extra < best[S][0]:
                        best[S] = (cost + extra, out, (method, plan, j, k))
    full = frozenset(range(n))
    if full not in best:
        return None, None
    cost, order, plan = best[full]
    if q.order_by is not None and order != q.order_by:
        cost, plan = cost + 2 * q.size(full), ("sort", plan, q.order_by)
    return cost, plan


def plan_cost(q: Query, plan: Plan) -> Tuple[Fraction, Optional[int], FrozenSet[int]]:
    """Recompute (cost, order, relations) of a plan from scratch."""
    tag = plan[0]
    if tag == "scan":
        return q.card[plan[1]], None, frozenset([plan[1]])
    if tag == "iscan":
        assert plan[2] in q.idx[plan[1]]
        return 2 * q.card[plan[1]], plan[2], frozenset([plan[1]])
    if tag == "sort":
        cost, _, S = plan_cost(q, plan[1])
        return cost + 2 * q.size(S), plan[2], S
    method, left, j, k = plan
    cost, order, S = plan_cost(q, left)
    assert j not in S
    for extra, out, m, kk in join_steps(q, S, order, j):
        if m == method and kk == k:
            return cost + extra, out, S | {j}
    raise AssertionError("method not applicable")


def join_order(plan: Plan) -> List[int]:
    if plan[0] in ("scan", "iscan"):
        return [plan[1]]
    if plan[0] == "sort":
        return join_order(plan[1])
    return join_order(plan[1]) + [plan[2]]
