# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wander-join/. The authors are listed in prov/SRQFRM.jsonl.
"""Wander join (Li, Wu, Yi and Zhao, SIGMOD 2016): online aggregation over joins by random walks.

A query is a natural join of relations, each a list of rows (dicts), with
optional selection predicates and an expression v over the joined row. The
aggregate is SUM(v); COUNT is SUM(1). A walk plan is an order of the
relations in which each relation after the first shares attributes with an
earlier one, its parent, and has an index on those attributes.

One walk picks a row of the first relation uniformly, then, for each next
relation, a uniform row among those that join with the row of its parent.
If the walk reaches a row with no match, or a row that fails a selection or
a join condition with a relation other than its parent (a cycle edge), the
walk fails and its estimate is 0. Otherwise the estimate is v / p, where p
is the probability of the walk. By the Horvitz-Thompson argument every
walk is an unbiased estimate of SUM(v), and so is the mean of many walks.
"""

import math
from fractions import Fraction
from random import Random
from typing import Callable, Dict, List, Optional, Sequence, Tuple

Row = Dict[str, object]
Pred = Callable[[Row], bool]


class WalkPlan:
    """A walk order with an index on the join attributes of each step."""

    def __init__(self, relations: Dict[str, List[Row]], order: Sequence[str],
                 predicates: Optional[Dict[str, Pred]] = None):
        self.relations = relations
        self.order = list(order)
        self.predicates = predicates or {}
        if sorted(self.order) != sorted(relations):
            raise ValueError("the order must name each relation once")
        attrs = {name: set(rows[0]) if rows else set() for name, rows in relations.items()}
        self.parent: Dict[str, str] = {}
        self.key: Dict[str, Tuple[str, ...]] = {}
        self.checks: Dict[str, List[Tuple[str, Tuple[str, ...]]]] = {}
        self.index: Dict[str, Dict[tuple, List[Row]]] = {}
        for i, name in enumerate(self.order[1:], start=1):
            earlier = self.order[:i]
            linked = [e for e in earlier if attrs[e] & attrs[name]]
            if not linked:
                raise ValueError("relation %s shares no attribute with an earlier one" % name)
            par = linked[0]
            self.parent[name] = par
            self.key[name] = tuple(sorted(attrs[par] & attrs[name]))
            # attributes shared with earlier relations other than the parent are checked after the step
            self.checks[name] = [(e, tuple(sorted(attrs[e] & attrs[name]))) for e in linked[1:]]
            idx: Dict[tuple, List[Row]] = {}
            for row in relations[name]:
                idx.setdefault(tuple(row[a] for a in self.key[name]), []).append(row)
            self.index[name] = idx

    def _ok(self, name: str, row: Row) -> bool:
        pred = self.predicates.get(name)
        return pred is None or bool(pred(row))

    def walk(self, rng: Random, value: Callable[[Row], float]) -> Tuple[float, int]:
        """One random walk. Returns (the estimate, the number of index lookups)."""
        first = self.relations[self.order[0]]
        if not first:
            return 0.0, 0
        t = {self.order[0]: first[rng.randrange(len(first))]}  # @line L2
        p_inv = len(first)
        if not self._ok(self.order[0], t[self.order[0]]):
            return 0.0, 0
        lookups = 0
        for name in self.order[1:]:  # @line L3
            par = t[self.parent[name]]
            matches = self.index[name].get(tuple(par[a] for a in self.key[name]), [])  # @line L4
            lookups += 1
            if not matches:  # @line L5
                return 0.0, lookups
            row = matches[rng.randrange(len(matches))]  # @line L6
            p_inv *= len(matches)
            if not self._ok(name, row):
                return 0.0, lookups
            for other, attrs in self.checks[name]:  # @line L7
                if any(t[other][a] != row[a] for a in attrs):
                    return 0.0, lookups
            t[name] = row
        joined: Row = {}
        for row in t.values():
            joined.update(row)
        return value(joined) * p_inv, lookups

    def exact_expectation(self, value: Callable[[Row], object]) -> Fraction:
        """The expected value of one walk: the sum, over every outcome of the
        random choices, of its probability times the estimate of `walk`.
        Failed walks have estimate 0 and are left out of the sum."""
        first = self.relations[self.order[0]]
        total = Fraction(0)

        def rec(i: int, t: Dict[str, Row], prob: Fraction, p_inv: int) -> Fraction:
            if i == len(self.order):
                joined: Row = {}
                for row in t.values():
                    joined.update(row)
                return prob * Fraction(value(joined)) * p_inv
            name = self.order[i]
            par = t[self.parent[name]]
            matches = self.index[name].get(tuple(par[a] for a in self.key[name]), [])
            s = Fraction(0)
            for row in matches:
                if not self._ok(name, row):
                    continue
                if any(t[o][a] != row[a] for o, attrs in self.checks[name] for a in attrs):
                    continue
                t2 = dict(t)
                t2[name] = row
                s += rec(i + 1, t2, prob / len(matches), p_inv * len(matches))
            return s

        for row in first:
            if self._ok(self.order[0], row):
                total += rec(1, {self.order[0]: row}, Fraction(1, len(first)), len(first))
        return total


def wander_join(plan: WalkPlan, value: Callable[[Row], float], walks: int, rng: Random,
                z: float = 1.96) -> Tuple[float, float]:
    """Run `walks` random walks. Returns (the estimate of SUM(value), the half-width of a z interval)."""
    xs = [plan.walk(rng, value)[0] for _ in range(walks)]  # @line L1
    mean = sum(xs) / walks  # @line L8
    if walks < 2:
        return mean, math.inf
    var = sum((x - mean) ** 2 for x in xs) / (walks - 1)
    return mean, z * math.sqrt(var / walks)


def choose_plan(plans: Sequence[WalkPlan], value: Callable[[Row], float], rng: Random,
                tau: int = 100, max_rounds: int = 100000) -> int:
    """Pick a walk plan by trial walks, as in Section 4 of the paper.

    Walk the plans round robin until one has tau successful walks. Among the
    plans with at least tau / 2 successes, return the index of the one with
    the smallest (sample variance of one walk) * (mean number of lookups).
    """
    xs: List[List[float]] = [[] for _ in plans]
    cost: List[int] = [0 for _ in plans]
    ok = [0 for _ in plans]
    for _ in range(max_rounds):
        for i, plan in enumerate(plans):
            x, c = plan.walk(rng, value)
            xs[i].append(x)
            cost[i] += c + 1
            ok[i] += x != 0
        if max(ok) >= tau:
            break
    best, best_score = -1, math.inf
    for i in range(len(plans)):
        if ok[i] < tau / 2:
            continue
        m = sum(xs[i]) / len(xs[i])
        var = sum((x - m) ** 2 for x in xs[i]) / max(1, len(xs[i]) - 1)
        score = var * cost[i] / len(xs[i])
        if score < best_score:
            best, best_score = i, score
    return best
