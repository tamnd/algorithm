# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/satplan/. The authors are listed in prov/WT1M0J.jsonl.

"""SATPLAN: planning as satisfiability (Kautz and Selman 1992, 1996).

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts, and
add and dele are disjoint. The function encode builds a CNF formula for a
horizon k: a variable for each fact at each time 0..k and for each action at
each step 1..k, with clauses for the initial state, the goal, preconditions,
effects, explanatory frame axioms and the exclusion of interfering actions.
Its models are exactly the parallel plans with k steps (a step may be empty).
The function satplan tries k = 0, 1, 2, ... and returns the first plan found,
as a list of steps where each step is a list of actions, or None when no plan
has at most max_steps steps. A small DPLL solver is included.
"""

from collections import namedtuple
from itertools import combinations
from typing import Dict, List, Optional

Action = namedtuple("Action", "name pre add dele")


def interfere(a: Action, b: Action) -> bool:
    """True when one action deletes a precondition or an add effect of the other."""
    return bool(a.dele & (b.pre | b.add) or b.dele & (a.pre | a.add))


class Encoding:
    """The CNF formula for horizon k, with clauses as lists of nonzero integers (DIMACS style)."""

    def __init__(self, actions, init, goal, k: int):
        self.actions, self.k = list(actions), k
        facts = set(init) | set(goal)
        for a in self.actions:
            facts |= a.pre | a.add | a.dele
        self.facts = sorted(facts, key=repr)
        self.var: Dict[tuple, int] = {}
        for t in range(k + 1):
            for f in self.facts:
                self.var[("fact", f, t)] = len(self.var) + 1
        for t in range(1, k + 1):
            for i in range(len(self.actions)):
                self.var[("action", i, t)] = len(self.var) + 1
        self.clauses: List[List[int]] = []
        self._build(set(init), set(goal))

    def fact(self, f, t):
        return self.var[("fact", f, t)]

    def action(self, i, t):
        return self.var[("action", i, t)]

    def _build(self, init, goal):
        cl, A, k = self.clauses, self.actions, self.k
        for f in self.facts:
            cl.append([self.fact(f, 0)] if f in init else [-self.fact(f, 0)])  # @line L6
        for g in goal:
            cl.append([self.fact(g, k)])  # @line L7
        pairs = [(i, j) for i, j in combinations(range(len(A)), 2) if interfere(A[i], A[j])]
        for t in range(1, k + 1):
            for i, a in enumerate(A):
                x = self.action(i, t)
                cl.extend([-x, self.fact(p, t - 1)] for p in sorted(a.pre, key=repr))  # @line L8
                cl.extend([-x, self.fact(f, t)] for f in sorted(a.add, key=repr))
                cl.extend([-x, -self.fact(f, t)] for f in sorted(a.dele, key=repr))
            for f in self.facts:
                before, after = self.fact(f, t - 1), self.fact(f, t)
                cl.append([-before, after] + [self.action(i, t) for i, a in enumerate(A) if f in a.dele])  # @line L9
                cl.append([before, -after] + [self.action(i, t) for i, a in enumerate(A) if f in a.add])
            cl.extend([-self.action(i, t), -self.action(j, t)] for i, j in pairs)  # @line L10

    def decode(self, model: Dict[int, bool]) -> List[List[Action]]:
        return [[a for i, a in enumerate(self.actions) if model[self.action(i, t)]] for t in range(1, self.k + 1)]


def _assign(clauses, lit):
    """Make lit true: drop the satisfied clauses and remove -lit from the others."""
    return [[x for x in c if x != -lit] for c in clauses if lit not in c]


def dpll(clauses: List[List[int]], n: int) -> Optional[Dict[int, bool]]:
    """A model of the clauses over the variables 1..n, or None. Unit propagation and branching."""

    def solve(cls, model):
        while True:
            if any(not c for c in cls):
                return None
            unit = next((c[0] for c in cls if len(c) == 1), None)
            if unit is None:
                break
            model[abs(unit)] = unit > 0
            cls = _assign(cls, unit)
        if not cls:
            return model
        lit = min(cls, key=len)[0]
        for choice in (lit, -lit):
            branch = dict(model)
            branch[abs(choice)] = choice > 0
            result = solve(_assign(cls, choice), branch)
            if result is not None:
                return result
        return None

    found = solve([list(c) for c in clauses], {})
    if found is None:
        return None
    return {v: found.get(v, False) for v in range(1, n + 1)}


def satplan(actions, init, goal, max_steps: Optional[int] = None) -> Optional[List[List[Action]]]:
    """A parallel plan with the fewest steps, or None when no plan has at most max_steps steps.

    The default bound is 2^n - 1 for n facts, the most steps that a plan without a repeated state can have.
    """
    if max_steps is None:
        facts = set(init) | set(goal)
        for a in actions:
            facts |= a.pre | a.add | a.dele
        max_steps = 2 ** len(facts) - 1
    for k in range(max_steps + 1):  # @line L1
        enc = Encoding(actions, init, goal, k)  # @line L2
        model = dpll(enc.clauses, len(enc.var))  # @line L3
        if model is not None:
            return enc.decode(model)  # @line L4
    return None  # @line L5
