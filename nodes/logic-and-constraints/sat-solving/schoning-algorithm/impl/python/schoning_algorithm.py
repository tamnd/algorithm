# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schoning-algorithm/. The authors are listed in prov/JNC89S.jsonl.

"""Schoening's random walk for k-SAT, and Papadimitriou's walk for 2-SAT.

Clauses are DIMACS-style lists of nonzero ints over the variables 1 .. n.
The algorithm has one-sided error: it returns an assignment only when the
assignment satisfies every clause, and it returns None when no try found one,
which does not prove that the formula is unsatisfiable.
"""

import math
import random


class _Walk:
    """An assignment with the number of true literals in each clause."""

    def __init__(self, n: int, clauses: list[list[int]], x: list[bool]) -> None:
        self.clauses = clauses
        self.x = [False] + x  # x[v] for v = 1 .. n
        self.occ: list[list[int]] = [[] for _ in range(n + 1)]
        for j, cl in enumerate(clauses):
            for lit in cl:
                self.occ[abs(lit)].append(j)
        self.true_count = [sum(self.value(lit) for lit in cl) for cl in clauses]
        self.false_list: list[int] = []  # the clauses with no true literal
        self.where = [-1] * len(clauses)
        for j, c in enumerate(self.true_count):
            if c == 0:
                self._add(j)

    def value(self, lit: int) -> bool:
        return self.x[abs(lit)] == (lit > 0)

    def _add(self, j: int) -> None:
        self.where[j] = len(self.false_list)
        self.false_list.append(j)

    def _remove(self, j: int) -> None:
        i = self.where[j]
        last = self.false_list.pop()
        if last != j:
            self.false_list[i] = last
            self.where[last] = i
        self.where[j] = -1

    def flip(self, v: int) -> None:
        self.x[v] = not self.x[v]
        for j in self.occ[v]:
            # recount: a clause may contain v more than once
            before = self.true_count[j]
            after = sum(self.value(lit) for lit in self.clauses[j])
            self.true_count[j] = after
            if before == 0 and after > 0:
                self._remove(j)
            elif before > 0 and after == 0:
                self._add(j)


def schoning_try(n: int, clauses: list[list[int]], rng: random.Random, steps: int) -> list[bool] | None:
    """One try: a random start, then at most `steps` random flips."""
    x = [rng.random() < 0.5 for _ in range(n)]  # @line L2
    w = _Walk(n, clauses, x)
    for s in range(steps + 1):  # @line L3
        if not w.false_list:  # @line L4
            return w.x[1:]
        if s == steps:
            break
        j = w.false_list[rng.randrange(len(w.false_list))]  # @line L5
        lit = rng.choice(clauses[j])  # @line L6
        w.flip(abs(lit))  # @line L7
    return None


def success_lower_bound(n: int, k: int) -> float:
    """The proved lower bound on the success probability of one try."""
    k = max(k, 3)
    return ((k - 1) / k) ** (k - 3) / (3 * n + 1) * (k / (2 * (k - 1))) ** n


def tries_for(n: int, k: int, eps: float) -> int:
    """A number of tries after which a satisfiable formula is missed with probability at most eps."""
    return math.ceil(math.log(1 / eps) / success_lower_bound(n, k))


def schoning_algorithm(n: int, clauses: list[list[int]], tries: int | None = None, rng: random.Random | None = None) -> list[bool] | None:
    """Schoening's algorithm: random restarts of a walk of 3n flips.

    Returns a model as a list of n booleans (x[v - 1] is the value of v),
    or None when no try found one. With tries=None the number of tries is
    tries_for(n, k, 1e-6), so a satisfiable formula is missed with
    probability at most 1e-6.
    """
    rng = rng or random.Random()
    if any(len(cl) == 0 for cl in clauses):
        return None  # the empty clause is never satisfied
    k = max((len(cl) for cl in clauses), default=3)
    if tries is None:
        tries = tries_for(n, k, 1e-6)
    for _ in range(tries):  # @line L1
        x = schoning_try(n, clauses, rng, 3 * n)
        if x is not None:
            return x
    return None  # @line L8


def papadimitriou_2sat(n: int, clauses: list[list[int]], rng: random.Random | None = None, rounds: int = 30) -> list[bool] | None:
    """Papadimitriou's walk for 2-SAT: one walk of 2 n^2 flips per round.

    On a satisfiable 2-CNF formula each round succeeds with probability at
    least 1/2, so None is wrong with probability at most 2^(-rounds).
    """
    rng = rng or random.Random()
    if any(len(cl) == 0 for cl in clauses):
        return None
    for _ in range(rounds):
        x = schoning_try(n, clauses, rng, 2 * n * n)
        if x is not None:
            return x
    return None
